PY = .venv/bin/python

.PHONY: all data geography flows projections primary levelA levelB placebo sensitivity figures tables manuscript qc clean

all: data primary placebo figures tables manuscript qc

data: geography flows projections

geography:
	$(PY) src/geography/build_geography.py

flows:
	$(PY) src/flows/build_flows.py

projections:
	$(PY) src/projections/build_projections.py

levelA:
	$(PY) -m src.run_levelA_batch

levelB:
	$(PY) -m src.run_levelB_batch

primary: levelA levelB

placebo_borders:
	$(PY) -m src.placebo.gen_placebo

placebo: placebo_borders
	$(PY) -m src.placebo.run_placebo

aggregate:
	$(PY) -m src.report.aggregate_results

figures: aggregate
	$(PY) -m src.visualization.make_figures

tables: aggregate
	$(PY) -m src.report.make_tables

manuscript: figures tables
	$(PY) -m src.report.build_manuscript

sensitivity: primary
	@echo "tau sensitivity included in levelA/levelB batches"

qc: aggregate
	$(PY) -m src.report.qc_report

clean:
	rm -rf outputs/models outputs/figures outputs/tables outputs/placebo
