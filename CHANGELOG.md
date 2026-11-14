# Changelog

## Version 1.5 (13 November 2026; DOI 10.5281/zenodo.24205196)

- Census of every corner of a declared window (30 corners), every point of the facing frontage a possible watching point; the openings recorded in 1857 kept as a sensitivity. Every orientation of every corner is read in the 1877–78 directory, tested or not.
- New chance analysis (`src/chance.py`, SciPy): hypergeometric null over the corners of the window and a Bayes factor for "the scene shows a real corner"; full grid of variants in `data/chance_multiverse.csv`.
- Drawn relations applied in full: no lane as either street, and the clothier's shop must front the side street. Both were added after a first coding returned Argyle Street × Adam's Court Lane SE; the first coding is reported throughout.
- The width-ratio filter (from one exploratory language-model reading) and the five model readings of the panels are no longer used as evidence.
- Local projection with pyproj and frontage sampling with shapely; distances change by about 0.1 m (JW6: 27.9 m, 17.1 m).
- Result revised: Jamaica Street × Howard Street NE is the only corner with both trades under the handedness convention, but such a match would arise by chance more often than not, and the later Paisley's corner carries the same pair of trades; version 1.4's "probable topographic basis" is withdrawn.
- The hiding views are re-read: they draw a roadway between the watchers and the boy and agree with the corner view; the view from the bar confirms the handedness.
- The paper's AI use statement describes how generative AI was used for this version.
- `make test` checks that every generated file is byte-identical to what the code writes; `make anon` builds an anonymised PDF.

## Version 1.4 (13 November 2026; DOI 10.5281/zenodo.24195132)

First public version; earlier drafts were withdrawn. The method, data, code and their limits are described in the paper and the README.
