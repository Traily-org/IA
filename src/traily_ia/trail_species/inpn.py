"""INPN / TaxRef legal-protection filter (ADR 0002).

Built from two files published by PatriNat (INPN's own hosts were down after a
cyberattack at MNHN; temporary downloads live on assets.patrinat.fr):

* BDC  — "Base de connaissances: statuts", one row per (taxon, status);
* TAXREF — every scientific name with the `CD_REF` of its accepted taxon, used
  so that a protected taxon is also recognised under its synonyms.

A compact JSON index is derived from them once (`build_protected_index`), with
the provenance of both inputs recorded in it, so every species list can say
which version of the law-derived data it was filtered with.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Literal, NamedTuple, cast

from traily_ia.trail_species.location import REGION_ISO_CODES, Location

Scope = Literal["national", "anywhere", "local"]

# Protection statuses in BDC (REGROUPEMENT_TYPE == "Protection"); reglementation
# (invasives, picking rules) is deliberately not treated as protection.
PROTECTION_TYPES = {"PN", "PR", "PD", "POM"}
# Overseas territories: a protection there says nothing about metropolitan trails.
OVERSEAS = {
    "Guyane",
    "Guadeloupe",
    "Martinique",
    "Mayotte",
    "Réunion",
    "Province Nord",
    "Province Sud",
    "Polynésie française",
}
SPECIES_RANK = "ES"
STALE_AFTER_DAYS = 365

csv.field_size_limit(10_000_000)


def _binomial(name: str) -> str:
    return " ".join(name.split()[:2])


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _member(zf: zipfile.ZipFile, *, prefix: str, suffix: str) -> zipfile.ZipInfo:
    """The single archive member whose base name matches (BDC_18/ has several CSVs)."""
    (info,) = (
        i
        for i in zf.infolist()
        if Path(i.filename).name.startswith(prefix) and i.filename.endswith(suffix)
    )
    return info


def _provenance(
    zip_path: Path, member: zipfile.ZipInfo, version: str
) -> dict[str, str]:
    return {
        "zip": zip_path.name,
        "zip_sha256": _sha256(zip_path),
        "member": member.filename,
        "content_date": date(*member.date_time[:3]).isoformat(),
        "version": version,
        "downloaded": datetime.fromtimestamp(zip_path.stat().st_mtime, UTC)
        .date()
        .isoformat(),
    }


class IndexSummary(NamedTuple):
    taxa: int
    names: int
    provenance: dict[str, object]


_DEPARTEMENT_ISO = re.compile(r"FR-(0[1-9]|[1-8]\d|9[0-5]|2[AB])")


def unmapped_zones(taxa: dict[str, dict[str, object]]) -> set[tuple[str, str, str]]:
    """Metropolitan PR/PD protections whose zone code cannot be placed.

    Such a protection would silently never apply to any trail, so the index build
    refuses to continue when there is one (e.g. a new territory in a later BDC).
    """
    known_regions = set().union(*REGION_ISO_CODES.values())
    bad: set[tuple[str, str, str]] = set()
    for taxon in taxa.values():
        for p in cast(list[dict[str, object]], taxon["protections"]):
            if p["type"] in {"PR", "PD"} and p["metropolitan"]:
                iso = str(p["iso"])
                if iso not in known_regions and not _DEPARTEMENT_ISO.fullmatch(iso):
                    bad.add((str(p["type"]), str(p["territory"]), iso))
    return bad


def build_protected_index(
    bdc_zip: Path, taxref_zip: Path, out_path: Path, *, source_url: str
) -> IndexSummary:
    """Distil the two PatriNat archives into the small JSON index the filter reads."""
    taxa: dict[str, dict[str, object]] = {}
    with zipfile.ZipFile(bdc_zip) as zf:
        bdc_member = _member(zf, prefix="bdc_", suffix=".csv")
        with zf.open(bdc_member) as raw:
            for row in csv.DictReader(
                io.TextIOWrapper(raw, encoding="utf-8", newline="")
            ):
                if (
                    row["REGNE"] != "Plantae"
                    or row["CD_TYPE_STATUT"] not in PROTECTION_TYPES
                ):
                    continue
                taxon = taxa.setdefault(
                    row["CD_REF"], {"name": row["LB_NOM"], "protections": []}
                )
                cast(list[dict[str, object]], taxon["protections"]).append(
                    {
                        "type": row["CD_TYPE_STATUT"],
                        "territory": row["LB_ADM_TR"],
                        "metropolitan": row["LB_ADM_TR"] not in OVERSEAS,
                        "status": row["CODE_STATUT"],
                        "iso": row["CD_ISO3166_2"],
                    }
                )

    if bad := unmapped_zones(taxa):
        raise ValueError(
            "protections with a zone code that maps to no région/département: "
            f"{sorted(bad)}"
        )

    aliases: dict[str, set[str]] = defaultdict(set)
    with zipfile.ZipFile(taxref_zip) as zf:
        taxref_member = _member(zf, prefix="TAXREFv", suffix=".txt")
        with zf.open(taxref_member) as raw:
            reader = csv.DictReader(
                io.TextIOWrapper(raw, encoding="utf-8", newline=""), delimiter="\t"
            )
            for row in reader:
                if row["CD_REF"] not in taxa:
                    continue
                aliases[row["LB_NOM"]].add(row["CD_REF"])
                # A protected *accepted* subspecies/variety makes its parent species
                # unsafe to list. Never done for synonyms: "Bellis perennis subsp.
                # sylvestris" is a synonym of the protected Bellis sylvestris, and
                # collapsing it would wrongly flag the common daisy.
                if row["RANG"] != SPECIES_RANK and row["CD_NOM"] == row["CD_REF"]:
                    aliases[_binomial(row["LB_NOM"])].add(row["CD_REF"])

    bdc_prov = _provenance(bdc_zip, bdc_member, "18")
    taxref_prov = _provenance(taxref_zip, taxref_member, "18")

    index: dict[str, object] = {
        "provenance": {
            "bdc": bdc_prov,
            "taxref": taxref_prov,
            "source_url": source_url,
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        },
        "taxa": taxa,
        "aliases": {name: sorted(refs) for name, refs in sorted(aliases.items())},
    }
    out_path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return IndexSummary(
        len(taxa), len(aliases), cast(dict[str, object], index["provenance"])
    )


@dataclass(frozen=True)
class InpnProtectionFilter:
    """Matches GBIF canonical names against the protected-plant index."""

    _taxa: dict[str, dict[str, object]]
    _aliases: dict[str, list[str]]
    _scope: Scope
    _provenance: dict[str, object]
    _index_id: str
    _zone: frozenset[str] | None = None

    @classmethod
    def from_index(
        cls, path: Path, *, scope: Scope = "anywhere"
    ) -> InpnProtectionFilter:
        """Load a built index.

        scope="anywhere": protected by national law *or* in any metropolitan region
        or département — over-excludes (fewer species listed) but never
        under-excludes, whatever the trail's location.
        scope="national": national protection (PN) only.
        scope="local": national protection plus the régional and départemental
        protections of the trail's own zone — call `for_location` before use.
        """
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found — run scripts/build_inpn_index.py. Refusing to "
                "fall back to an unfiltered list."
            )
        text = path.read_text(encoding="utf-8")
        raw = json.loads(text)
        # Hash of the index itself: rebuilding it with different matching rules
        # must invalidate cached lists even if the input files are unchanged.
        index_id = hashlib.sha256(text.encode()).hexdigest()[:8]
        return cls(raw["taxa"], raw["aliases"], scope, raw["provenance"], index_id)

    def for_location(self, location: Location) -> InpnProtectionFilter:
        """A filter for one trail: national + that trail's régional/départemental."""
        return replace(self, _scope="local", _zone=location.iso_codes)

    @property
    def source(self) -> str:
        bdc = cast(dict[str, str], self._provenance["bdc"])
        taxref = cast(dict[str, str], self._provenance["taxref"])
        return (
            f"inpn-bdc{bdc['version']}-{bdc['content_date']}"
            f"+taxref{taxref['version']}-{taxref['content_date']}"
            f"#{self._index_id}:{self._scope}"
            + (f"[{','.join(sorted(self._zone))}]" if self._zone is not None else "")
        )

    @property
    def data_date(self) -> date:
        """Date of the oldest input file's content."""
        bdc = cast(dict[str, str], self._provenance["bdc"])
        taxref = cast(dict[str, str], self._provenance["taxref"])
        return min(
            date.fromisoformat(bdc["content_date"]),
            date.fromisoformat(taxref["content_date"]),
        )

    def age_days(self, today: date | None = None) -> int:
        return ((today or date.today()) - self.data_date).days

    def is_stale(self, today: date | None = None) -> bool:
        return self.age_days(today) > STALE_AFTER_DAYS

    def is_protected(self, scientific_name: str) -> bool:
        if self._scope == "local" and self._zone is None:
            raise ValueError(
                "scope 'local' needs a location: call for_location() first"
            )
        for cd_ref in self._aliases.get(scientific_name, ()):
            for p in cast(list[dict[str, object]], self._taxa[cd_ref]["protections"]):
                if p["type"] == "PN":
                    return True
                if self._scope == "anywhere" and p["metropolitan"]:
                    return True
                if self._scope == "local" and p["iso"] in cast(
                    frozenset[str], self._zone
                ):
                    return True
        return False
