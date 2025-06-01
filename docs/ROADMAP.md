# Kimera SWM – Roadmap & "Pathway Playbook"

*flexible by design, but opinionated where it must be*

## 1 · 90-Day Roadmap  (rolling, update every sprint)

| 🔢     | Theme / Outcome                      | Concrete deliverables                                                                                                                     | "Done" signals (tests / metrics)                                       | Owner(s)           |
| ------ | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------ |
| **P0** | **Stabilise CI & red tests**         | • Fix 19 failing tests (storage teardown, pickling, `geoid.id` bug).<br>• Green GitHub Actions on Linux/Windows.<br>• Tag **v0.7.6-rc1**. | `pytest -q` passes on Win+Linux.<br>CI badge back to green.            | current tiger team |
| **P1** | **Full Unified Identity write-path** | • `geoid_to_identity` patch (uses `gid`).<br>• CLS lattice reads/writes `Identity`.<br>• Storage dual-write flag live on **staging**.     | `tests/test_cls_integration.py` green *with* `KIMERA_ID_DUAL_WRITE=1`. | Identity sub-squad |
| **P2** | **Entropy instrumentation**          | • Histogram of entropy buckets in Prometheus.<br>• Exponential decay verified by integration test.<br>• Grafana dashboard v1.             | Dashboard shows non-zero entropy traffic for 24 h.                     | Observability      |
| **P3** | **Migration & Roll-back tooling**    | • `migrate_identity.py` idempotent.<br>• `kimera db backup/restore` CLI.<br>• Runbook in `docs/ops/`.                                     | Dry-run on staging copies data with zero checksum drift.               | DevOps             |
| **P4** | **Search & Query API**               | • `find_identities_by_entropy()` exposed via FastAPI.<br>• Vector index PoC (DuckDB ext).                                                 | `curl /search?q=…` < 50 ms for 1 M rows.                               | Search team        |

> **Update cadence:** Keep only the next 3 sprints locked; anything beyond sits in the "Backlog Futures" list and can be re-cut every PI planning.

---

## 2 · Critical Pathways  (check-lists you clone per feature)

### 2.1 Identity ⇄ CLS Pathway

1. **API shim**

   ```py
   def lattice_resolve(a,b,*_, **kw):
       a = geoid_to_identity(a) if isinstance(a, Geoid) else a
       …
   ```
2. **Storage dual-write** – env `KIMERA_ID_DUAL_WRITE=1`.
3. **Metric hook** – `cls_resolve_seconds`.
4. **Test** – two geoids → resolve → `identities` table has 2 rows.

### 2.2 Entropy Logging Pathway

| Step                       | Metric                           | Log line                          |
| -------------------------- | -------------------------------- | --------------------------------- |
| After `Identity.entropy()` | `identity_entropy_total{type=…}` | `{"evt":"entropy","val":E}`       |
| After storage write        | `storage_write_seconds`          | `{"evt":"store_identity","id":…}` |

### 2.3 Windows-Safe Storage Tests

```py
db_path = fresh_duckdb_path()
storage = None
try:
    storage = get_storage(db_path)
    …
finally:
    if storage:
        storage.close()
    if os.path.exists(db_path):
        os.remove(db_path)
```

### 2.4 Multiprocessing Guard

```py
from multiprocessing import freeze_support
if __name__ == "__main__":
    freeze_support()
    main()
```

---

## 3 · Canonical Snippets (copy/paste)

```py
# adaptive τ – single source
DEFAULT_TAU_S = 14*24*3600
ENTROPY_SCALE = 0.10
def adaptive_tau(entropy: float, base: float = DEFAULT_TAU_S) -> float:
    return base * (1 + ENTROPY_SCALE * entropy)
```

```py
# safe_print – emoji on Windows
def safe_print(msg: str):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii","backslashreplace").decode())
```

```py
# fresh DuckDB path
def fresh_duckdb_path() -> str:
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)        # close handle
    os.unlink(path)     # remove file so DuckDB can create it
    return path
```

---

## 4 · Definition of Done (per PR)

* [ ] Unit & integration tests pass (`pytest -q`).
* [ ] If touching storage: migration script or dual-write flag included.
* [ ] Observability: metric OR log line added.
* [ ] Docs: README or ADR updated.
* [ ] Windows runner passes (GitHub CI).

---

## 5 · How to Propose Changes

1. **Open an ADR draft** (`docs/adr/NNN-title.md`) if the public API or schema changes.
2. **Slack #architecture** summary (< 10 lines).
3. **PR**: title starts with `[ADR-NNN]`.

---

## 6 · Backlog Futures (keep light)

* Cross-form resonance engine (ADR-004 draft).
* Plugin SDK (external embeddings, custom entropy funcs).
* WASM build for edge inference.

---

## 7 · Quick Links

| Resource         | Path                          |
| ---------------- | ----------------------------- |
| ADR index        | `docs/adr/README.md`          |
| Migration script | `scripts/migrate_identity.py` |
| Test dashboard   | `tests/README.md`             |
| CI config        | `.github/workflows/ci.yml`    |

---

**Remember:** *ship thin vertical slices, measure entropy, keep docs breathing.*
Happy hacking — Kimera SWM is yours to evolve.