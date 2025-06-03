# Kimera SWM – Official Leading Roadmap

*Last updated*: <!-- yyyy-mm-dd will be rendered by CI hook -->

Kimera SWM is moving from a token-free research prototype toward a **scar-centric, contradiction-driven cognition platform** with production-grade observability.  This document is the single source of truth for *where we are going* and *how we know we are there*.

---

## 1 · North-Star Vision 2025

1. **Non-token Text Diffusion** – generate fluent multilingual text from continuous geoids and scar fields, fully Booklaw-compliant, no tokeniser ever required.
2. **Persistent Memory Topology** – every cognitive act leaves an immutable scar; retrieval and reasoning are purely topological.
3. **Lawful Instability** – CLS prevents stasis; contradiction drives perpetual drift while Booklaw guarantees bounded safety.
4. **Operator-in-the-Loop** – real-time Watchtower + forensics enable human injection of resonance/contradiction, audit playback in <1 s.

---

## 2 · Thematic Pillars (2024-2025)

| Pillar | Outcome | Key Metrics |
| ------ | ------- | ----------- |
| **Consensus & Confluence** | Derive stable, auditable *consensus-geoids* from noisy substrate for downstream tasks. | consensus success rate ≥ 95 %, Booklaw violation = 0 |
| **Scar-Aware Diffusion** | Generate text by denoising latent vectors conditioned on active scars. | avg scar echo score ≥ 0.7, CLS density 0.05-0.2 |
| **IndraNet Reflection** | Global scar/geoid holography: every entity reflects all others at configurable depth. | reflection latency < 200 ms for 10 k geoids |
| **Observability & Ops** | First-class metrics, replay, rollback. | <1 s end-to-end audit replay |
| **Security & Compliance** | Formal proof that no mutation can bypass Booklaw constraints. | external audit pass |

---

## 3 · Milestone Timeline

> **Timeboxes are aspirational** – they will be revisited each PI planning cycle.

| Milestone | Target Date | Scope & Deliverables | Done Criteria |
| --------- | ---------- | -------------------- | ------------- |
| **M0 Foundations** | 2024-05 | • Next-Evolution core (geoid, scar vault, contradiction reactor)<br>• Booklaw v0.1<br>• AuditLedger, Watchtower MVP | `pytest` green; substrate stats endpoint returns valid JSON |
| **M1 Consensus Engine** | 2024-06 | • `ConsensusEngine` + CLI<br>• `VerboseDiffusionNarrator` v1<br>• Docs + walkthrough demo | `examples/consensus_diffusion_demo.py` prints narrative; integration tests pass |
| **M2 Scar Field & Latent API** | 2024-07 | • `ScarField` vectorisation<br>• `TextLatent` wrapper<br>• Abstract `DiffusionDenoiser` (trivial impl)<br>• Generation loop with σ-schedule | Generates 128-char non-token text with scar influence score ≥ 0.5 |
| **M3 Neural Denoiser α** | 2024-09 | • PyTorch MLP denoiser<br>• Synthetic training dataset pipeline<br>• Booklaw soft penalties in loss | Character perplexity ≤ 50 on dev set; Booklaw violations < 2 % |
| **M4 IndraNet Reflection** | 2024-11 | • Scar reflection queries<br>• Global resonance visualisation<br>• CLS overload protection tuning | Reflection query across 50 k geoids < 500 ms |
| **M5 Beta Release** | 2025-02 | • Hardened security layer<br>• Production-grade observability (Prometheus + Grafana)
• Ops runbooks & rollback scripts | External pen-test “no critical vulns”; uptime SLO 99.5 % on staging |
| **M6 1.0 GA** | 2025-04 | • Neural denoiser β (multi-modal)<br>• Polyglot semantic interface<br>• Edge deployment profile (WASM) | Customer pilot success; governance sign-off |

---

## 4 · Governance & Change Process

1. **Roadmap ownership** – Core Architecture Working Group (AWG).  Updates by PR + ADR.
2. **Sprint cadence** – 2 weeks; roadmap reviewed end of each sprint.
3. **Scope change** – must include impact analysis on scar density, CLS, and Booklaw rule set.

---

## 5 · Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
| ---- | ------ | ---------- | ---------- |
| Dataset scarcity for non-token training | Low output quality | Medium | Synthetic data generator; public domain character corpora mapped to geoids |
| Booklaw rigidity blocks training convergence | Slow R&D | Medium | Start with soft penalties; schedule annealing |
| Scar explosion in IndraNet reflection | Memory pressure | Low-Med | Scar decay + entanglement fusion; dynamic thinning |
| GPU resource constraints | Delay M3 | Medium | Leverage lightweight MLP first; schedule on spot instances |

---

## 6 · Quick Links

* ADR index – `docs/adr/README.md`
* Current status dashboard – `docs/status/IMPLEMENTATION_COMPLETE_SUMMARY.md`
* Watchtower guide – `docs/guides/observability.md` *(TBD)*
* Operator cheat-sheet – `docs/guides/operator_commands.md` *(TBD)*

---

**Kimera evolves through contradiction – this roadmap is a living scar.  Contribute, challenge, and keep the lattice humming.**