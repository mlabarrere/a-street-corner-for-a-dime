# A Street Corner for a Dime

Where did Don Rosa's ten-year-old Scrooge McDuck earn his first coin? The paper (`paper/main.pdf`, preprint version 1.4, 13 November 2026; concept DOI [10.5281/zenodo.24170392](https://doi.org/10.5281/zenodo.24170392)) tests the shoeshine scene of *The Last of the Clan McDuck* and *Of Ducks, Dimes and Destinies* against the Ordnance Survey 1:500 plans of Glasgow (1857–58, 1892–94) and sampled Post Office directories (1860–1906). On twelve selected facades, 187 corner-and-opening configurations are censused. Under the author's contested width-ratio filter, 17 configurations on five corners pass the geometric model; Jamaica Street and Howard Street NE is the only one of those five with affirmative 1877–78 evidence for both required trades. No principal survivor meets the model-read 17 m distance, one configuration (Howard Street and Adam's Court Lane NW, opening HS3) meets the 20.4 m threshold of the author's earlier working dossier, and the range of the model-read central width ratios leaves two configurations at one corner whose corner premises the 1877–78 directory gives to a non-clothier, although the envelope of those readings keeps the candidate. Measuring the viewing angles on the plan instead of treating the streets as perpendicular keeps the same five corners. Those non-metric proportions are weaker evidence than the conjunction of named street, geometry and trades: Jamaica and Howard NE is the strongest candidate and the probable topographic basis of the scene, although literal single-source copying is not established.

## Reproduce

```bash
brew install tectonic          # macOS; on other systems install Tectonic from https://tectonic-typesetting.github.io/
make setup                     # Python venv from pinned requirements
make all                       # tables -> figures -> paper/main.pdf
make test                      # asserts 187 -> 45 -> 23 -> 20 -> 17; five filtered corners; sensitivities and documentary result
```

Python 3 with `venv` is required (checked with Python 3.15.0 and Tectonic 0.17.0, which downloads its TeX bundle on first use). `requirements.txt` pins the direct dependencies; `requirements-lock.txt` records every package version used for the release build (`.venv/bin/pip install -r requirements-lock.txt`). Without Tectonic, build the paper with a TeX distribution after `make tables figures`: `cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main`.

Hand-entered inputs: street widths (`WIDTH` in `src/census.py`, read with the NLS measuring tool, ±0.7 m), corner coordinates (hard-coded in `src/geo.py` and `src/census.py`, documented in `data/corners_reference_OS1857.csv`), 32 selected orientations of 24 physical corners, the 62 openings (`data/openings_OS1857_Jamaica.csv`) and the directory evidence for the five filtered corners and for the two corners that enter only under sensitivity settings (`data/trades_1877.csv`). The pipeline regenerates the census, filter counts, distances and angles from those inputs, Tables 2–3, Figures 1–3 and `paper/tables/*.tex`. Narrative distances not used by the model are identified as approximate in the paper.

## Layout

| Path | Content |
|---|---|
| `paper/` | `main.tex` (version 1.4), `refs.bib`, `main.pdf`, generated `tables/` and `figures/` |
| `data/` | `openings_OS1857_Jamaica.csv` (62 openings), `corners_reference_OS1857.csv` (26 corners: the 24 used and two Wood Lane corners), `trades_1877.csv` (directory trades of seven corners), `directory_lines.md` (all directory lines relied on, 1860–1906), `configurations_phase1.csv` (187 configurations, generated) |
| `src/` | `geo.py` (local frame, facades, blocks), `census.py` (configurations, filters, documentary selection, sensitivity, LaTeX tables), `figures.py` (the three deterministic figures) |
| `evidence/` | `model_reading_sensitivity.md` (aggregate protocol and numerical results, without prompts or conversations), NLS viewer screenshots (with the layer's "Re-use: CC-BY (NLS)" header), `map_openings_OS1857.png` (hand-annotated extract of the NLS layer keying the opening codes), `PROVENANCE.md` |
| `tests/` | `test_pipeline.py` |

## Status and publication

Version 1.4 applies the corrections of an audit of version 1.3; version 1.3 answered an external review of version 1.0 and a consistency review of an earlier draft. `CHANGELOG.md` lists what changed and why. Page and panel references count from the first page of each story, with a correspondence to the book pages of the French and English editions; references not yet checked against the printed pages are marked as provisional in the paper. An independent human reading of the pages is still wanted. The repository is archived on Zenodo (concept DOI 10.5281/zenodo.24170392, all versions).

The citable release archive contains the scientific inputs, code, aggregate sensitivity record and paper; it does not contain raw AI prompts, conversations or editorial working reports. Earlier working files, including those, remain in the public Git history (tags v7 to v1.0).

| Version | Date | Zenodo DOI |
|---|---|---|
| 1.4 (tag `v1.4`) | 13 November 2026 | given on the Zenodo record; concept DOI [10.5281/zenodo.24170392](https://doi.org/10.5281/zenodo.24170392) |
| 1.3 (tag `v1.3`) | 13 November 2026 | [10.5281/zenodo.24192371](https://doi.org/10.5281/zenodo.24192371) |
| 1.2 (tag `v1.2`) | 12 November 2026 | [10.5281/zenodo.24173283](https://doi.org/10.5281/zenodo.24173283) |
| drafts 7 and 7.1, versions 1.0 and 1.1 (tags `v7`, `v7.1`, `v1.0`, `v1.1`) | 12 November 2026 | no current Zenodo record; cite version 1.2 or later |

Maps: Ordnance Survey 1:500 town plans of Glasgow, surveyed 1857–58 and 1892–94, redrawn from the georeferenced layers of the National Library of Scotland (layer re-use statement CC-BY (NLS), consulted 9 November 2026). No comic panel is reproduced: the author's photographs of the comic pages and of the directory pages are not distributed.

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24170392.svg)](https://doi.org/10.5281/zenodo.24170392)

Labarrère, M. (2026). *A Street Corner for a Dime: Placing Don Rosa's 1877 Glasgow Shoeshine Scene* (preprint, version 1.4). Zenodo. https://doi.org/10.5281/zenodo.24170392

```bibtex
@misc{labarrere2026streetcorner,
  author    = {Labarr{\`e}re, Micka{\"e}l},
  title     = {A Street Corner for a Dime: Placing Don Rosa's 1877 Glasgow Shoeshine Scene},
  year      = {2026},
  publisher = {Zenodo},
  note      = {Preprint, version 1.4},
  doi       = {10.5281/zenodo.24170392},
  url       = {https://doi.org/10.5281/zenodo.24170392}
}
```

The DOI above is the concept DOI: it covers all versions and resolves to the latest published version, here 1.4; the DOI of each version is given on its Zenodo record and in the table above. Author ORCID: [0009-0006-0822-3649](https://orcid.org/0009-0006-0822-3649).

## Licences

Original text, data files (`data/`, Markdown files in `evidence/`), tables and diagrams: CC BY 4.0 (`LICENSE-CC-BY-4.0.md`). Source code (`src/`, `tests/`, `Makefile`): MIT (`LICENSE`). Directory lines are transcribed from the National Library of Scotland digitisation on the Internet Archive (CC BY-NC-SA 2.5 Scotland). Third-party maps keep their stated rights (OS plans redrawn from the National Library of Scotland georeferenced layers, CC-BY (NLS)). No comic panel is reproduced.
