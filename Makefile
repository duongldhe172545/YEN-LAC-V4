.PHONY: lint test run demo_prep demo_kpi demo_scenario clean_data

# --- Quality gates ---
lint:
	python code/scripts/validate_registry.py --repo_root .

test:
	pytest -q

# --- Streamlit ---
run:
	streamlit run code/ok_computer/app.py

# --- Demo pipeline (GD1) ---
# validate registry -> preflight A7 -> ingest events -> kpi pulse -> scenario

demo_prep: lint clean_data
	python code/scripts/preflight_templates.py --repo_root . --template_code A7_events_evt_star --input_csv demo_inputs/events/events_demo.csv
	python code/scripts/ingest_events.py --repo_root . --input_csv demo_inputs/events/events_demo.csv --source_batch_id DEMO_BATCH_001
	$(MAKE) demo_kpi
	$(MAKE) demo_scenario

demo_kpi:
	python code/scripts/demo_kpi_pulse.py --repo_root . --event_log data/event_store/event_log.jsonl --out data/kpi_pulse/kpi_pulse.json

demo_scenario:
	python code/scripts/demo_scenario.py --repo_root . --input_json demo_inputs/scenario/scenarios_demo.json --out data/scenario/scenario_results.json

clean_data:
	rm -rf data/preflight data/event_store data/quarantine data/kpi_pulse data/scenario
	mkdir -p data
