"""
Verbose Diffusion Text Architecture
==================================

This module provides *VerboseDiffusionNarrator* – a light-weight generator that
converts internal Kimera SWM state (geoids, scars, contradiction events) into a
rich textual narrative.  It is **diffusion-style** in that it starts from a
high-level synopsis and iteratively expands details, echoing the way
probabilistic text-diffusion models refine outputs across steps.

Key Features
------------
• Multi-pass narrative expansion (sketch → elaboration → flourish).
• Adjustable verbosity levels (0 = terse, 3 = highly verbose).
• Optional inclusion of scar topology and contradiction chains.
• No external ML dependency – relies on deterministic templates, making it a
  safe, auditable component that can later be swapped with LLM/decoder models.

This is **not** a generative language model; rather, it organises and verbalises
existing structured data in the SWM substrate for operator consumption,
debugging, or archival export.
"""

from __future__ import annotations

import textwrap
from datetime import datetime
from typing import List, Optional

from .geoid import Geoid, GeoidSubstrate
from .scar_vault import ScarVault
from .contradiction import ContradictionEvent


class VerboseDiffusionNarrator:
    """Generate verbose, multi-stage textual narratives for a set of geoids."""

    def __init__(
        self,
        substrate: GeoidSubstrate,
        scar_vault: Optional[ScarVault] = None,
        default_verbosity: int = 2,
    ) -> None:
        self.substrate = substrate
        self.scar_vault = scar_vault
        self.default_verbosity = max(0, min(default_verbosity, 3))

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def diffuse(
        self,
        geoid_ids: List[str],
        verbosity: Optional[int] = None,
        include_scars: bool = True,
    ) -> str:
        """Return a multi-pass, human-readable narrative describing the geoids."""
        verbosity = self._clamp_verbosity(verbosity)

        # Validate geoids
        geoids = [self._require_geoid(gid) for gid in geoid_ids]

        # Pass 1 – skeleton summary
        lines: List[str] = [
            f"Narrative generated: {datetime.utcnow().isoformat()}Z",
            f"Participants: {len(geoids)} geoids",
        ]

        # High-level synopsis
        for g in geoids:
            lines.append(self._synopsis_line(g))

        if verbosity == 0:
            return "\n".join(lines)

        # Pass 2 – detail expansion
        for g in geoids:
            lines.extend(self._detail_block(g, verbosity))

        # Optional: scars / contradictions
        if include_scars and self.scar_vault is not None and verbosity >= 2:
            lines.append("\nScars & Contradictions")
            lines.append("-----------------------")
            for g in geoids:
                lines.extend(self._scar_section(g))

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clamp_verbosity(self, level: Optional[int]) -> int:
        if level is None:
            level = self.default_verbosity
        return max(0, min(level, 3))

    def _require_geoid(self, gid: str) -> Geoid:
        g = self.substrate.geoids.get(gid)
        if g is None:
            raise ValueError(f"Geoid '{gid}' not found in substrate")
        return g

    @staticmethod
    def _synopsis_line(g: Geoid) -> str:
        return (
            f"• {g.id[:8]} | modality={g.core.modality} | symbols={list(g.shell.symbols)[:3]} | "
            f"mutations={g.mutation_count} | scars={len(g.scar_index)}"
        )

    def _detail_block(self, g: Geoid, verbosity: int) -> List[str]:
        header = f"\nGeoid {g.id} – Detailed View"
        underline = "-" * len(header)
        block = [header, underline]

        block.append(f"Created: {g.created_at.isoformat()}")
        block.append(f"Modality: {g.core.modality}")
        block.append(f"Symbol count: {len(g.shell.symbols)}")
        block.append(f"Mutation count: {g.mutation_count}")

        if verbosity >= 2:
            block.append("Resonance Links:")
            for target, strength in sorted(g.resonance_links.items(), key=lambda x: -x[1])[:10]:
                block.append(f"  -> {target[:8]} : {strength:.3f}")

            block.append("Contradiction Links:")
            for target, intensity in sorted(g.contradiction_links.items(), key=lambda x: -x[1])[:10]:
                block.append(f"  x  {target[:8]} : {intensity:.3f}")

        # Verbosity 3 – include essence snippet
        if verbosity >= 3:
            snippet = textwrap.shorten(" ".join(map(lambda x: f"{x:.3f}", g.core.essence[:20])), width=120)
            block.append(f"Essence vector (partial): {snippet} ...")

        return block

    def _scar_section(self, g: Geoid) -> List[str]:
        lines: List[str] = [f"\nScars for Geoid {g.id[:8]}:"]
        if not g.scar_index:
            lines.append("  (none)")
            return lines

        for scar_id in g.scar_index[:20]:
            scar = self.scar_vault.scars.get(scar_id) if self.scar_vault else None
            if scar is None:
                lines.append(f"  • {scar_id[:8]} – (not in vault)")
                continue

            age = (datetime.utcnow() - scar.created_at).total_seconds() / 3600.0  # hours
            lines.append(
                f"  • {scar.id[:8]} | age={age:.1f}h | geoids={len(scar.participant_ids)} | intensity={scar.max_intensity:.3f}"
            )
        return lines
