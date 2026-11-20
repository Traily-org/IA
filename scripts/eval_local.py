#!/usr/bin/env python
"""Evaluate the pipeline on labelled photos and write a dated report.

    python scripts/eval_local.py data/test_images \
        --species-file data/species_lists/catalog.txt --annotate data/out/eval

Labels come from `<folder>/labels.csv` (columns: file,species[,organ]) when it
exists, otherwise from the file names ("Genus species.JPEG", "Genus species(1).JPEG").

Two candidate-list settings are measured, because they answer different questions:
  catalog        the list as given — the true species may be missing from it, which
                 shows how the pipeline behaves on a plant it does not know;
  catalog+truth  the list plus every labelled species — how well it separates
                 species when the answer is on the list.
Each is run on the detector's crop, on the whole photo, and on "hybrid>=T" variants
(crop only when the detector box covers at least T % of the photo, else whole photo).

Reports go to docs/eval/YYYY-MM-DD[-n].md (+ .json), never overwriting an earlier one.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import torch

from traily_ia import DEFAULT_CONFIDENCE_THRESHOLD, SpeciesScore
from traily_ia.annotate import annotate_image
from traily_ia.pipeline import build_default_pipeline, load_image
from traily_ia.result import IdentificationResult
from traily_ia.species import load_species_file

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
# Label typos found in the file names, fixed here instead of renaming user files.
NAME_CORRECTIONS = {"Euonymys japonicus": "Euonymus japonicus"}
CONFIDENT = 0.9
HYBRID_THRESHOLDS = (2, 5, 10, 20, 40)
# BioCLIP was evaluated in Nov 2023 (iNat21 snapshot + EOL + BIOSCAN), so a photo
# uploaded to iNaturalist from 2024 on cannot be in its training data.
TRAINING_CUTOFF = "2024-06-01"
BINS = [(0.0, 0.5), (0.5, 0.8), (0.8, 0.95), (0.95, 1.01)]


def read_created(folder: Path) -> dict[str, str]:
    """file name -> upload date (YYYY-MM-DD) when labels.csv has `photo_created`."""
    csv_path = folder / "labels.csv"
    if not csv_path.exists():
        return {}
    with csv_path.open(encoding="utf-8", newline="") as f:
        return {
            row["file"]: row["photo_created"]
            for row in csv.DictReader(f)
            if row.get("photo_created")
        }


def read_labels(folder: Path) -> dict[Path, tuple[str, str]]:
    """image path -> (species, organ or '')."""
    labels: dict[Path, tuple[str, str]] = {}
    csv_path = folder / "labels.csv"
    if csv_path.exists():
        with csv_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                labels[folder / row["file"]] = (
                    NAME_CORRECTIONS.get(row["species"], row["species"]),
                    row.get("organ", "") or "",
                )
        return labels
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES:
            name = re.sub(r"\(\d+\)$", "", p.stem).strip()
            labels[p] = (NAME_CORRECTIONS.get(name, name), "")
    return labels


def classify_full(pipeline, image, candidates) -> list[SpeciesScore]:
    return pipeline.classifier.classify(image, candidates)


def evaluate(
    pipeline, labels, candidates, annotate_dir: Path | None, created=None
) -> dict:
    """Run both variants on every photo for one candidate list."""
    rows = []
    for path, (truth, organ) in labels.items():
        image = load_image(path)
        crop_result: IdentificationResult = pipeline.identify(image, candidates)
        full_scores = classify_full(pipeline, image, candidates)
        if annotate_dir is not None:
            annotate_dir.mkdir(parents=True, exist_ok=True)
            annotate_image(image, crop_result, truth=truth).save(
                annotate_dir / f"{path.stem}.jpg"
            )
        crop_scores = list(crop_result.alternatives)
        box = crop_result.bbox
        rows.append(
            {
                "file": path.name,
                "truth": truth,
                "organ": organ,
                "created": (created or {}).get(path.name, ""),
                "reachable": truth in candidates,
                "box_area_pct": (
                    round(
                        100 * box.width * box.height / (image.width * image.height), 1
                    )
                    if box
                    else 0.0
                ),
                "crop": [(s.species, round(s.score, 3)) for s in crop_scores[:3]],
                "full": [(s.species, round(s.score, 3)) for s in full_scores[:3]],
            }
        )
    # "hybrid>=T": use the detector crop only when its box covers at least T % of
    # the photo, otherwise classify the whole photo. Derived from the two runs above.
    for r in rows:
        for t in HYBRID_THRESHOLDS:
            r[f"hybrid>={t}"] = r["crop"] if r["box_area_pct"] >= t else r["full"]
    variants = ("crop", "full", *(f"hybrid>={t}" for t in HYBRID_THRESHOLDS))
    return {"rows": rows, "metrics": {v: metrics(rows, v) for v in variants}}


def genus(name: str) -> str:
    return name.split()[0]


def metrics(rows: list[dict], variant: str) -> dict:
    top1 = top3 = genus1 = 0
    conf_ok, conf_bad, answered, answered_ok = [], [], 0, 0
    confident_wrong = 0
    bins = [[0, 0] for _ in BINS]
    wrong_pairs: Counter = Counter()
    for r in rows:
        preds = r[variant]
        if not preds:
            continue
        best, conf = preds[0]
        ok = best == r["truth"]
        top1 += ok
        top3 += r["truth"] in [p[0] for p in preds]
        genus1 += genus(best) == genus(r["truth"])
        (conf_ok if ok else conf_bad).append(conf)
        confident_wrong += (not ok) and conf >= CONFIDENT
        if conf >= DEFAULT_CONFIDENCE_THRESHOLD:
            answered += 1
            answered_ok += ok
        for i, (lo, hi) in enumerate(BINS):
            if lo <= conf < hi:
                bins[i][0] += 1
                bins[i][1] += ok
        if not ok:
            wrong_pairs[(r["truth"], best)] += 1
    n = len(rows)
    mean = lambda xs: round(sum(xs) / len(xs), 3) if xs else None  # noqa: E731
    return {
        "n": n,
        "top1": top1,
        "top3": top3,
        "genus1": genus1,
        "mean_conf_correct": mean(conf_ok),
        "mean_conf_wrong": mean(conf_bad),
        "confident_wrong": confident_wrong,
        "answered_at_threshold": answered,
        "correct_when_answered": answered_ok,
        "calibration": [
            {"range": f"{lo:.2f}-{min(hi, 1):.2f}", "n": b[0], "correct": b[1]}
            for (lo, hi), b in zip(BINS, bins, strict=True)
        ],
        "wrong_pairs": [[t, p, c] for (t, p), c in wrong_pairs.most_common(8)],
    }


def pct(a: int, b: int) -> str:
    return f"{a}/{b}" + (f" ({100 * a / b:.0f}%)" if b else "")


def render(report: dict, previous: dict | None) -> str:
    out = [f"# Eval report — {report['date']} — {report['name']}", ""]
    out.append(f"- Photos: {report['n_photos']} (labels from {report['label_source']})")
    out.append(
        f"- Candidate list: `{report['species_file']}` ({report['n_candidates']} species)"
    )
    out.append(
        f"- Confidence threshold for abstaining: {DEFAULT_CONFIDENCE_THRESHOLD} (placeholder)"
    )
    out.append(f"- Device: {report['device']}")
    out.append(
        "- Labels are PlantNet suggestions given by the team, not expert-verified: "
        "treat the second word of each name as uncertain (genus-level is more reliable)."
    )
    out.append("")
    for setting, data in report["settings"].items():
        out.append(f"## Setting: {setting}")
        rows = data["rows"]
        reachable = sum(r["reachable"] for r in rows)
        out.append(
            f"True species on the candidate list for {pct(reachable, len(rows))} of the photos."
        )
        out.append("")
        out.append(
            "| variant | top-1 | top-3 | genus top-1 | mean conf. correct / wrong | wrong at ≥0.9 | correct when answered (≥ threshold) |"
        )
        out.append("|---|---|---|---|---|---|---|")
        for v, m in data["metrics"].items():
            out.append(
                f"| {v} | {pct(m['top1'], m['n'])} | {pct(m['top3'], m['n'])} | "
                f"{pct(m['genus1'], m['n'])} | {m['mean_conf_correct']} / {m['mean_conf_wrong']} | "
                f"{m['confident_wrong']} | {pct(m['correct_when_answered'], m['answered_at_threshold'])} |"
            )
        out.append("")
        out.append(
            "Calibration (detector crop): of the answers in each confidence range, how many were right"
        )
        out.append("")
        out.append("| confidence | answers | correct |")
        out.append("|---|---|---|")
        for b in data["metrics"]["crop"]["calibration"]:
            out.append(f"| {b['range']} | {b['n']} | {b['correct']} |")
        out.append("")
        dated = [r for r in rows if r.get("created")]
        if dated:
            out.append(
                f"Could BioCLIP have seen these photos? Split by iNaturalist upload date "
                f"(cutoff {TRAINING_CUTOFF}: BioCLIP 2 training data ends with a GBIF snapshot of 2024-05-01):"
            )
            out.append("")
            out.append(
                "| subset | photos | full top-1 | full top-3 | crop top-1 | crop top-3 |"
            )
            out.append("|---|---|---|---|---|---|")
            for label, subset in (
                (
                    f"uploaded on/after {TRAINING_CUTOFF} (cannot be in training data)",
                    [r for r in dated if r["created"] >= TRAINING_CUTOFF],
                ),
                (
                    "uploaded earlier (may be in training data)",
                    [r for r in dated if r["created"] < TRAINING_CUTOFF],
                ),
            ):
                if not subset:
                    continue
                full, crop = metrics(subset, "full"), metrics(subset, "crop")
                out.append(
                    f"| {label} | {len(subset)} | {pct(full['top1'], full['n'])} | "
                    f"{pct(full['top3'], full['n'])} | {pct(crop['top1'], crop['n'])} | "
                    f"{pct(crop['top3'], crop['n'])} |"
                )
            out.append("")
        out.append(
            "Most frequent confusions (truth → predicted, count), detector crop / full photo:"
        )
        for v in ("crop", "full"):
            pairs = ", ".join(
                f"{t} → {p} ×{c}" for t, p, c in data["metrics"][v]["wrong_pairs"]
            )
            out.append(f"- {v}: {pairs or 'none'}")
        out.append("")
        out.append("| photo | truth | organ | box % | crop: top-1 | full: top-1 |")
        out.append("|---|---|---|---|---|---|")
        for r in rows:

            def cell(preds, truth=r["truth"]):
                if not preds:
                    return "-"
                s, c = preds[0]
                return f"{'OK' if s == truth else 'X'} {s} {c:.2f}"

            out.append(
                f"| {r['file']} | {r['truth']}{'' if r['reachable'] else ' (not on list)'} | "
                f"{r['organ']} | {r['box_area_pct']} | {cell(r['crop'])} | {cell(r['full'])} |"
            )
        out.append("")
    if previous:
        out.append(
            f"## Compared with the previous report ({previous['date']}, {previous['name']})"
        )
        if previous.get("n_candidates") != report["n_candidates"]:
            out.append(
                f"**The candidate list changed ({previous.get('n_candidates')} -> "
                f"{report['n_candidates']} species): a drop can come from new look-alike "
                "species on the list rather than from the model. Compare with care.**"
            )
        for setting, data in report["settings"].items():
            old = previous.get("settings", {}).get(setting)
            if not old:
                continue
            for v in ("crop", "full"):
                new_m, old_m = data["metrics"][v], old["metrics"][v]
                delta = new_m["top1"] / new_m["n"] - old_m["top1"] / old_m["n"]
                flag = "  **REGRESSION**" if delta < -1e-9 else ""
                out.append(
                    f"- {setting} / {v}: top-1 {old_m['top1']}/{old_m['n']} → {new_m['top1']}/{new_m['n']}{flag}"
                )
        out.append("")
    else:
        out.append("No previous report to compare with.")
        out.append("")
    return "\n".join(out)


def next_paths(out_dir: Path, name: str) -> tuple[Path, Path]:
    stamp = date.today().isoformat()
    base = out_dir / f"{stamp}-{name}"
    n = 1
    while base.with_suffix(".md").exists():
        n += 1
        base = out_dir / f"{stamp}-{name}-{n}"
    return base.with_suffix(".md"), base.with_suffix(".json")


def latest_report(out_dir: Path, dataset: str) -> dict | None:
    """Most recent earlier report on the same photo folder (never another set)."""
    files = sorted(out_dir.glob("*.json")) if out_dir.exists() else []
    reports = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    # Reports written before the field existed all used data/test_images.
    same = [
        r
        for r in reports
        if isinstance(r, dict) and r.get("dataset", "data/test_images") == dataset
    ]
    return same[-1] if same else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("folder", type=Path)
    parser.add_argument("--species-file", type=Path, required=True)
    parser.add_argument("--name", default="local-photos", help="short report name")
    parser.add_argument("--device", default=None)
    parser.add_argument("--annotate", type=Path, help="write annotated photos here")
    parser.add_argument("--out", type=Path, default=Path("docs/eval"))
    args = parser.parse_args()

    labels = read_labels(args.folder)
    if not labels:
        parser.error(f"no labelled images in {args.folder}")
    catalog = load_species_file(args.species_file)
    truth_species = sorted({sp for sp, _ in labels.values()})
    settings = {
        "catalog": catalog,
        "catalog+truth": catalog + [s for s in truth_species if s not in catalog],
    }

    print(f"Loading models (device={args.device or 'auto'})...", file=sys.stderr)
    # 0.0 = pipeline.identify classifies the detector's crop: that is the "crop"
    # variant below. (The pipeline default is the whole photo, measured separately.)
    pipeline = build_default_pipeline(
        device=args.device,
        confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD,
        crop_min_area_fraction=0.0,
    )
    previous = latest_report(args.out, str(args.folder))
    report = {
        "date": date.today().isoformat(),
        "name": args.name,
        "dataset": str(args.folder),
        "n_photos": len(labels),
        "label_source": (
            "labels.csv" if (args.folder / "labels.csv").exists() else "file names"
        ),
        "species_file": str(args.species_file),
        "n_candidates": len(catalog),
        "device": args.device or ("cuda" if torch.cuda.is_available() else "cpu"),
        "settings": {},
    }
    for setting, candidates in settings.items():
        sub = args.annotate / setting.replace("+", "_plus_") if args.annotate else None
        report["settings"][setting] = evaluate(
            pipeline, labels, candidates, sub, read_created(args.folder)
        )

    args.out.mkdir(parents=True, exist_ok=True)
    md_path, json_path = next_paths(args.out, args.name)
    md_path.write_text(render(report, previous), encoding="utf-8")
    json_path.write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print(md_path.read_text(encoding="utf-8"))
    print(f"\nReport: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
