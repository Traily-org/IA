"""Legal-protection filtering (ADR 0002).

GBIF has no legal-protection field, so the authoritative French source (INPN /
TaxRef "Espèces protégées et réglementées") has to be cross-referenced. That
source is not wired in yet — see DELTA_LOG.md — so only the contract and an
explicitly-named stand-in exist here.
"""

from __future__ import annotations

from typing import Protocol


class ProtectionFilter(Protocol):
    @property
    def source(self) -> str:
        """Identifier recorded in the cache, e.g. 'inpn-bdc-statuts-v18'."""
        ...

    def is_protected(self, scientific_name: str) -> bool: ...


class NoProtectionFilter:
    """Filters nothing. Lists built with it are marked UNFILTERED in the cache.

    For development only: such a list may contain legally protected species and
    must never reach `identify` in production.
    """

    source = "none-UNFILTERED"

    def is_protected(self, scientific_name: str) -> bool:
        return False
