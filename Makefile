PY ?= .venv/bin/python
TECTONIC ?= tectonic
# Release builds use a fixed timestamp (2026-11-13 00:00:00 UTC) so the PDF
# and the complete generated artifact set are byte-for-byte reproducible.
export SOURCE_DATE_EPOCH ?= 1794528000

.PHONY: all setup tables figures paper test clean

all: tables figures paper

setup:
	python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt

tables:
	$(PY) src/census.py

figures:
	$(PY) src/figures.py

paper: tables figures
	cd paper && $(TECTONIC) --keep-logs --keep-intermediates main.tex

test: tables
	$(PY) tests/test_pipeline.py

clean:
	rm -f paper/main.pdf paper/main.log paper/main.aux paper/main.out paper/main.blg paper/tables/*.tex paper/figures/*.pdf
