# A Street Corner for a Dime

Where did Don Rosa's ten-year-old Scrooge McDuck earn his first coin, and how often would a match that good turn up by chance? The paper (`paper/main.pdf`, version 1.5, DOI [10.5281/zenodo.24205196](https://doi.org/10.5281/zenodo.24205196)) tests the shoeshine scene of *The Last of the Clan McDuck* and *Of Ducks, Dimes and Destinies* against the Ordnance Survey 1:500 plans of Glasgow (1857–58, 1892–94) and sampled Post Office directories (1860–1906). Every corner of a declared window is censused (30 corners; 46 orientations tested, 14 untestable, every orientation read in the directory), every point of the facing frontage being a possible watching point. The drawn relations (no lane as either street; the clothier's shop fronting the side street) leave 8 corners with the handedness of the inked corner view and 14 without it. In the 1877–78 directory, 1 of them (2 without the handedness convention) has a clothier whose shop fronts the side street and licensed premises facing it across that street: Jamaica Street × Howard Street NE (and Jamaica Street × Argyle Street SW). The pair occurs at 3 of the 30 corners of the window, one of them the later Paisley's corner, which fails the drawn geometry; at least one survivor would show it 62% of the time by chance, and the evidence raises the odds that Rosa drew a real corner of this window by a factor of 1.2–1.5 (at most 1.7 in any variant). A first coding, which let a lane count as a street and the clothier front either street, also returned Argyle Street × Adam's Court Lane SE (82% by chance); the two requirements were added after it, and both codings are reported. Restricted to the openings recorded in 1857, the census returns version 1.4's corners and its single match.

## Reproduce

```bash
brew install tectonic          # macOS; on other systems install Tectonic from https://tectonic-typesetting.github.io/
make setup                     # Python venv from pinned requirements
make all                       # tables -> figures -> paper/main.pdf
make test                      # checks the counts and chance figures, and that every generated file matches the code byte for byte
make anon                      # anonymised PDF for double-anonymous review (paper/anon.pdf)
```

Python 3 with `venv` is required (checked with Python 3.15.0 and Tectonic 0.17.0, which downloads its TeX bundle on first use). `requirements.txt` pins the direct dependencies; `requirements-lock.txt` records every package version used for the release build (`.venv/bin/pip install -r requirements-lock.txt`). Without Tectonic, build the paper with a TeX distribution after `make tables figures`: `cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main`.

Hand-entered inputs: street widths (`WIDTH` in `src/census.py`, read with the NLS measuring tool, ±0.7 m), corner coordinates (hard-coded in `src/geo.py` and `src/census.py`, documented in `data/corners_reference_OS1857.csv`), the frontages (`FACADES` in `src/geo.py`), 46 orientations of 30 corners (`src/census.py`), the 62 openings (`data/openings_OS1857_Jamaica.csv`) and the directory evidence for every orientation (`data/trades_1877.csv`; column `checked` says whether a row was checked on the page image or read in the OCR only). Coordinates are projected with pyproj (local azimuthal equidistant projection on WGS84); frontage points are sampled with shapely. The pipeline regenerates the census, the chance analysis and its full grid of variants (`data/chance_multiverse.csv`), the tables, Figures 1–3 and `paper/tables/*.tex`.

**Directory coding.** *Corner premises*: the entries tied to the corner building by an address on both streets, or by adjacency to an "X street intersects" or "here" marker or to the end of the street. *Clothier*: `yes` if a corner-premises trade contains clothier, clothes or outfitter; `no` if the corner premises are identified and given to another named trade; `unknown` otherwise (silence in the OCR is never evidence of absence). *Clothier on X* (`clothier_on_x`): `yes` if the clothier's own entry (general or street section) gives an address on X, where the shop must front (H4); `no` if its only address is on Y; `unknown` if not checked; `n/a` when the corner premises are not a clothier's. *Facing block*: the frontage across X that looks at the stand. *Licensed*: `yes` for a spirit dealer, spirit merchant, wine and spirit merchant, restaurateur or publican within a few premises of the corner of the facing block; `partial` for one further along the block, a grocer and wine merchant, a wholesaler or a hotel whose licence is not stated; `no` when the facing block is read and none is licensed, or when it is a river quay (`facing_quay`); temperance hotels are never licensed; `unknown` otherwise. *Other columns*: `corner_premises` and `facing_premises` (addresses), `corner_trade` and `facing_trade` (the directory text, abridged), `checked` (`image` or `ocr`), `in_v14` (`yes` if the orientation was in version 1.4; it defines the version-1.4 population), `source`.

**Book-page concordance.** Story page n of chapter 0 is book page n+8 in *The Don Rosa Library* vol. 4 and in Glénat vol. 2 (pp. 9–23); story page n of chapter 1 is book page n+24 in *The Don Rosa Library* vol. 4 (pp. 25–39) and n+10 in Glénat vol. 1 (pp. 11–25).

## Layout

| Path | Content |
|---|---|
| `paper/` | `main.tex` (version 1.5), `anon.tex` (anonymised build), `refs.bib`, `main.pdf`, generated `tables/` and `figures/` |
| `data/` | `openings_OS1857_Jamaica.csv` (62 openings), `corners_reference_OS1857.csv` (the 30 corners; the four added in version 1.5 are approximate), `trades_1877.csv` (directory trades at every orientation of the 30 corners: 46 tested, 14 untestable), `directory_lines.md` (all directory lines relied on, 1860–1906), `configurations_phase1.csv` (the 187 opening configurations of version 1.4, generated), `chance_multiverse.csv` (36 variants of the chance analysis, generated) |
| `src/` | `geo.py` (local frame, facades, blocks), `census.py` (configurations, filters, documentary selection, sensitivity, LaTeX tables), `chance.py` (chance rates and Bayes factors, with SciPy), `figures.py` (the three deterministic figures) |
| `evidence/` | `model_reading_sensitivity.md` (aggregate record of the model readings used up to version 1.4, no longer used as evidence), NLS viewer screenshots (with the layer's "Re-use: CC-BY (NLS)" header), `map_openings_OS1857.png` (hand-annotated extract of the NLS layer keying the opening codes), `PROVENANCE.md` |
| `tests/` | `test_pipeline.py` |

## Status and publication

Version 1.5 (13 November 2026) revises version 1.4, whose conclusion that Jamaica and Howard NE was the probable topographic basis of the scene is withdrawn; earlier drafts were withdrawn. Still to check: the rows of `data/trades_1877.csv` read in the OCR only (page images), the references marked provisional in the paper (printed pages), the coordinates of the four corners added in version 1.5 (to re-digitise on the NLS 1857 layer), and the 1877–78 valuation roll. The repository is archived on Zenodo; the concept DOI [10.5281/zenodo.24170392](https://doi.org/10.5281/zenodo.24170392) resolves to the latest version.

The citable release archive contains the scientific inputs, code, aggregate sensitivity record and paper; raw AI prompts, conversations and editorial working reports are not distributed.

Maps: Ordnance Survey 1:500 town plans of Glasgow, surveyed 1857–58 and 1892–94, redrawn from the georeferenced layers of the National Library of Scotland (layer re-use statement CC-BY (NLS), consulted 9 November 2026). No comic panel is reproduced: the author's photographs of the comic pages and of the directory pages are not distributed.

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24170392.svg)](https://doi.org/10.5281/zenodo.24170392)

Labarrère, M. (2026). *A Street Corner for a Dime: Don Rosa's Glasgow and the Chance of a Match* (preprint, version 1.5). Zenodo. https://doi.org/10.5281/zenodo.24205196

```bibtex
@misc{labarrere2026streetcorner,
  author    = {Labarr{\`e}re, Micka{\"e}l},
  title     = {A Street Corner for a Dime: Don Rosa's Glasgow and the Chance of a Match},
  year      = {2026},
  publisher = {Zenodo},
  note      = {Preprint, version 1.5},
  doi       = {10.5281/zenodo.24205196},
  url       = {https://doi.org/10.5281/zenodo.24205196}
}
```

The badge's concept DOI resolves to the latest published version; the citation above is version 1.5 ([10.5281/zenodo.24205196](https://doi.org/10.5281/zenodo.24205196)); version 1.4 is [10.5281/zenodo.24195132](https://doi.org/10.5281/zenodo.24195132). Author ORCID: [0009-0006-0822-3649](https://orcid.org/0009-0006-0822-3649).

## Licences

Original text, data files (`data/`, Markdown files in `evidence/`), tables and diagrams: CC BY 4.0 (`LICENSE-CC-BY-4.0.md`), except the directory transcriptions (`data/directory_lines.md` and the quoted directory text in `data/trades_1877.csv`), which follow the source's CC BY-NC-SA 2.5 Scotland terms. Source code (`src/`, `tests/`, `Makefile`): MIT (`LICENSE`). The directory digitisation is the National Library of Scotland's, on the Internet Archive (CC BY-NC-SA 2.5 Scotland). Third-party maps keep their stated rights (OS plans redrawn from the National Library of Scotland georeferenced layers, CC-BY (NLS)). No comic panel is reproduced.
