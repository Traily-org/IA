#!/usr/bin/env python
"""Test the "none of these" case: can the pipeline tell when the species is not listed?

    python scripts/eval_open_set.py data/web_test_images \
        --species-file data/species_lists/catalog.txt --also data/test_images

Every labelled photo is classified twice (whole photo, no detector):
  IN      candidates = the full list, true species included;
  ABSENT  candidates = the list without the true species (the right answer is
          "none of these"; a species of the same genus may well remain on it).
Four acceptance scores are compared (see traily_ia/openset.py): softmax probability
(what the pipeline does today), raw cosine similarity, top-1/top-2 margin, and an
explicit "other" class. For each, a threshold keeps a chosen share of the correct IN
answers, and count how many ABSENT photos still get a (necessarily wrong) answer.

--also: a second, naturally mixed folder (e.g. the team's own photos, most of whose
species are not on the list); the thresholds found on the first folder are applied.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from eval_local import NAME_CORRECTIONS, next_paths, read_labels
from traily_ia.bioclip_classifier import PROMPT_TEMPLATE, BioClipClassifier
from traily_ia.openset import (
    OTHER_PROMPTS,
    Scores,
    accept_rate,
    auroc,
    score_photo,
    threshold_for_recall,
)
from traily_ia.pipeline import DEFAULT_CONFIDENCE_THRESHOLD, load_image
from traily_ia.species import load_species_file

METHODS = {
    "prob": "softmax probability (today's rule)",
    "cosine": "raw cosine similarity",
    "margin": "margin top-1 minus top-2",
    "other": "explicit 'other' classes",
}
RECALLS = (0.95, 0.90, 0.80)


def genus(name: str) -> str:
    return name.split()[0]


def value(s: Scores, method: str) -> float:
    return float(getattr(s, method))


def run_photos(
    clf, labels, catalog, species_feats, other_feats
) -> list[dict[str, Any]]:
    """Scores for every photo, in both conditions."""
    index = {name: i for i, name in enumerate(catalog)}
    samples = []
    for path, (truth, _organ) in labels.items():
        feat = clf.embed_image(load_image(path))
        in_list = truth in index
        full = score_photo(feat, species_feats, other_feats, clf.logit_scale)
        samples.append(
            {
                "file": path.name,
                "truth": truth,
                "condition": "IN" if in_list else "NOT-ON-LIST",
                "scores": full,
                "species": catalog[full.top],
                "correct": in_list and catalog[full.top] == truth,
                "congener_present": any(
                    genus(c) == genus(truth) for c in catalog if c != truth
                ),
            }
        )
        if in_list:  # simulate the species being missing from the list
            keep = [i for i, c in enumerate(catalog) if c != truth]
            absent = score_photo(
                feat, species_feats[keep], other_feats, clf.logit_scale
            )
            remaining = [catalog[i] for i in keep]
            samples.append(
                {
                    "file": path.name,
                    "truth": truth,
                    "condition": "ABSENT",
                    "scores": absent,
                    "species": remaining[absent.top],
                    "correct": False,
                    "congener_present": any(
                        genus(c) == genus(truth) for c in remaining
                    ),
                }
            )
    return samples


def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def analyse(samples: list[dict[str, Any]]) -> dict[str, Any]:
    in_correct = [s for s in samples if s["condition"] == "IN" and s["correct"]]
    in_wrong = [s for s in samples if s["condition"] == "IN" and not s["correct"]]
    absent = [s for s in samples if s["condition"] == "ABSENT"]
    absent_cong = [s for s in absent if s["congener_present"]]
    absent_alone = [s for s in absent if not s["congener_present"]]
    result: dict[str, Any] = {
        "counts": {
            "in_correct": len(in_correct),
            "in_wrong": len(in_wrong),
            "absent": len(absent),
            "absent_with_congener_on_list": len(absent_cong),
        },
        "methods": {},
    }
    both = in_correct + in_wrong + absent
    for method in METHODS:
        scores = [value(s["scores"], method) for s in both]
        correct = [s["correct"] for s in both]
        rows = {}
        for recall in RECALLS:
            t = threshold_for_recall(
                [value(s["scores"], method) for s in in_correct], recall
            )
            rows[str(recall)] = {
                "threshold": t,
                "in_correct_kept": accept_rate(
                    [value(s["scores"], method) for s in in_correct], t
                ),
                "in_wrong_accepted": accept_rate(
                    [value(s["scores"], method) for s in in_wrong], t
                ),
                "absent_accepted": accept_rate(
                    [value(s["scores"], method) for s in absent], t
                ),
                "absent_with_congener_accepted": accept_rate(
                    [value(s["scores"], method) for s in absent_cong], t
                ),
                "absent_without_congener_accepted": accept_rate(
                    [value(s["scores"], method) for s in absent_alone], t
                ),
            }
        result["methods"][method] = {
            "auroc": auroc(scores, correct),
            "operating_points": rows,
        }
    # today's behaviour: softmax probability >= the pipeline's default threshold
    t = DEFAULT_CONFIDENCE_THRESHOLD
    result["today"] = {
        "threshold": t,
        "in_correct_kept": accept_rate(
            [value(s["scores"], "prob") for s in in_correct], t
        ),
        "in_wrong_accepted": accept_rate(
            [value(s["scores"], "prob") for s in in_wrong], t
        ),
        "absent_accepted": accept_rate([value(s["scores"], "prob") for s in absent], t),
    }
    return result


def apply_to_natural(samples, analysis, recall: str) -> dict[str, Any]:
    """Thresholds learned on the calibration folder, applied to a mixed folder."""
    out = {}
    for method in METHODS:
        t = analysis["methods"][method]["operating_points"][recall]["threshold"]
        rows = {"threshold": t, "photos": []}
        for s in samples:
            accepted = value(s["scores"], method) >= t
            rows["photos"].append(
                {
                    "file": s["file"],
                    "truth": s["truth"],
                    "on_list": s["condition"] == "IN",
                    "answer": s["species"] if accepted else None,
                    "correct": bool(accepted and s["correct"]),
                }
            )
        out[method] = rows
    return out


def render(report: dict[str, Any]) -> str:
    a = report["analysis"]
    c = a["counts"]
    out = [f"# Open-set report — {report['date']} — 'none of these'", ""]
    out += [
        f"- Calibration photos: {report['n_photos']} from `{report['folder']}` "
        f"(true species always on the {report['n_candidates']}-species list)",
        "- Whole-photo classification only (no detector crop); confidence from BioCLIP zero-shot.",
        f"- IN: {c['in_correct']} correct + {c['in_wrong']} wrong answers. ABSENT: {c['absent']} cases "
        f"with the true species removed, of which {c['absent_with_congener_on_list']} still have a "
        "species of the same genus on the list (hard: a look-alike is available).",
        "- Labels: iNaturalist research-grade (community-validated).",
        "",
        "## Today's rule (softmax probability ≥ 0.5)",
        f"Keeps {pct(a['today']['in_correct_kept'])} of the correct IN answers, but still answers "
        f"{pct(a['today']['absent_accepted'])} of the ABSENT cases (wrongly) and "
        f"{pct(a['today']['in_wrong_accepted'])} of the wrong IN answers.",
        "",
        "## Separating a correct answer from a wrong or unknown one (AUROC, 0.5 = useless, 1 = perfect)",
        "",
        "| score | AUROC |",
        "|---|---|",
    ]
    for m, label in METHODS.items():
        out.append(f"| {label} | {a['methods'][m]['auroc']:.3f} |")
    for recall in RECALLS:
        out += [
            "",
            f"## Threshold that keeps {pct(recall)} of the correct IN answers",
            "",
            "| score | threshold | wrong IN answers still accepted | ABSENT answered | ABSENT answered (look-alike on list) | ABSENT answered (no look-alike) |",
            "|---|---|---|---|---|---|",
        ]
        for m, label in METHODS.items():
            p = a["methods"][m]["operating_points"][str(recall)]
            out.append(
                f"| {label} | {p['threshold']:.3f} | {pct(p['in_wrong_accepted'])} | "
                f"{pct(p['absent_accepted'])} | {pct(p['absent_with_congener_accepted'])} | "
                f"{pct(p['absent_without_congener_accepted'])} |"
            )
    if "natural" in report:
        nat = report["natural"]
        out += [
            "",
            f"## Applied to a naturally mixed folder: `{nat['folder']}` ({nat['n_photos']} photos, "
            f"{nat['n_not_on_list']} whose species is not on the list)",
            "Thresholds from the 90% setting above. 'Wrongly answered' = a species was given for a "
            "photo whose species is not on the list; 'right' = correct species given for a listed one.",
            "",
            "| score | wrongly answered (not on list) | right (on list) | on-list photos wrongly rejected or wrong |",
            "|---|---|---|---|",
        ]
        for m, label in METHODS.items():
            photos = nat["results"][m]["photos"]
            off = [p for p in photos if not p["on_list"]]
            on = [p for p in photos if p["on_list"]]
            out.append(
                f"| {label} | {sum(p['answer'] is not None for p in off)}/{len(off)} | "
                f"{sum(p['correct'] for p in on)}/{len(on)} | {sum(not p['correct'] for p in on)}/{len(on)} |"
            )
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "folder", type=Path, help="labelled photos, species on the list"
    )
    parser.add_argument("--species-file", type=Path, required=True)
    parser.add_argument(
        "--also", type=Path, help="naturally mixed folder to apply thresholds to"
    )
    parser.add_argument("--name", default="open-set")
    parser.add_argument("--device", default=None)
    parser.add_argument("--out", type=Path, default=Path("docs/eval"))
    args = parser.parse_args()

    catalog = load_species_file(args.species_file)
    clf = BioClipClassifier(device=args.device)
    species_feats = clf.embed_species(catalog)
    other_feats = clf.embed_texts(OTHER_PROMPTS)

    labels = read_labels(args.folder)
    samples = run_photos(clf, labels, catalog, species_feats, other_feats)
    analysis = analyse(samples)
    report: dict[str, Any] = {
        "date": date.today().isoformat(),
        "name": args.name,
        "folder": str(args.folder),
        "n_photos": len(labels),
        "n_candidates": len(catalog),
        "other_prompts": list(OTHER_PROMPTS),
        "prompt_template": PROMPT_TEMPLATE,
        "analysis": analysis,
    }
    if args.also:
        mixed = read_labels(args.also)
        nat_samples = [
            s
            for s in run_photos(clf, mixed, catalog, species_feats, other_feats)
            if s["condition"] != "ABSENT"
        ]
        report["natural"] = {
            "folder": str(args.also),
            "n_photos": len(mixed),
            "n_not_on_list": sum(s["condition"] == "NOT-ON-LIST" for s in nat_samples),
            "results": apply_to_natural(nat_samples, analysis, "0.9"),
        }

    args.out.mkdir(parents=True, exist_ok=True)
    md_path, json_path = next_paths(args.out, args.name)
    md_path.write_text(render(report), encoding="utf-8")
    json_path.write_text(
        json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print(md_path.read_text(encoding="utf-8"))
    print(f"Report: {md_path}")
    return 0


if __name__ == "__main__":
    _ = NAME_CORRECTIONS  # label typo fixes are shared with eval_local
    raise SystemExit(main())
