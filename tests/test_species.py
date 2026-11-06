from __future__ import annotations

from pathlib import Path

from traily_ia.species import load_species_file


def test_skips_blanks_comments_and_duplicates(tmp_path: Path) -> None:
    path = tmp_path / "species.txt"
    path.write_text(
        "# header comment\n"
        "Bellis perennis\n"
        "\n"
        "  Urtica dioica  # inline comment\n"
        "Bellis perennis\n",
        encoding="utf-8",
    )

    assert load_species_file(path) == ["Bellis perennis", "Urtica dioica"]


def test_sample_file_is_loadable() -> None:
    sample = Path(__file__).parents[1] / "examples" / "species_sample.txt"

    names = load_species_file(sample)

    assert len(names) == len(set(names)) >= 5
