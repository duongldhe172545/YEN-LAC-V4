# D2Com Pilot Yên Lạc — SSOT Repo (V5.0.2)

## Run OK Computer (demo)
```bash
python -m pip install -r requirements.txt
streamlit run code/ok_computer/app.py
```

## Validate registries (CI local)
```bash
python code/scripts/validate_registry.py --repo_root .
pytest -q
```

## Where things live
- SSOT registries: `registry/`
- Patch ledger: `patch_ledger/`
- Appendix overlays (human-readable): `docs/appendix_overlays/`
- Audit logs (append-only): `audit/*.jsonl`

## Quick run (local)

```bash
pip install -r requirements.txt
python code/scripts/validate_registry.py --repo_root .
pytest -q
streamlit run code/ok_computer/app.py
```

## War-room drills
Xem `docs/war_room_rehearsal/` (Run of Show + Tier2/Tier3 + Rollback + AAR template).


## Templates

- Template registry: `registry/template_registry.yaml`
- CSV templates: `templates/` (hard + soft)
- Guide: `docs/templates/template_matrix_v5_0_2.md`


## Run demo data pipeline (GD1)

```bash
pip install -r requirements.txt
make demo_prep
make run
```

- `make demo_prep` sẽ: validate registry → preflight A7 → ingest events_demo → tạo KPI pulse → chạy scenario demo.
- Input demo nằm ở `demo_inputs/`.
