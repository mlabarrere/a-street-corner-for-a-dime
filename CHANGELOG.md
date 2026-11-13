# Changelog

## Version 1.4 (13 November 2026)

Corrections from an audit of version 1.3: three independent reviews and a contradictor, whose findings were checked against the files. The census and its principal result (187 → 45 → 23 → 20 → 17 configurations on five corners, one complete documentary match) are unchanged.

### Method
- **What.** Step 4 of the procedure and the census docstring define *d* as the census computes it: the offset of the nearer wall of the opening along the axis of Y, from the line through A perpendicular to Y. JW6 is 17.0 m south of the corner, measured along Jamaica Street.
- **Why.** The paper measured *d* "from the far building line of X" and placed JW6 "south of the Howard Street building line"; neither matched the code or the plan. The code applies the right condition for seeing face X; only the description was wrong.
- **What.** The model treats the two streets of each corner as perpendicular, and the paper now says so. A new sensitivity row measures visibility and the viewing angle against the recorded face X (`geo.FACADES`): 18 configurations on the same five corners. JW6 is seen at 46° rather than 37° (the candidate's faces meet at about 98°), two configurations lie within 20.4 m and none within 17 m. Figure 3 gives both angles.
- **Why.** The approximation was undeclared and changes one sensitivity row; it does not change the five corners.

### Readings and views
- **What.** H8 is "read; not met", and the paper no longer says that the author's readings do not conflict with the candidate: every distance reading, the author's included, is shorter than any admissible opening. H7 is "adopted; contested", with the central values (0.4–1.6) and envelope (0.2–4.0) of the model ratios. The model-reading protocol is described as it was: narrative context, imposed definitions, two image sets including pencil drafts.
- **What.** H6 fixes the kind of watching point (an opening), not the street layout. JW6 is called a possible watching point, not a hiding place, in Table 4 and Figures 2–3, and Figure 3 shows three watchers instead of four.
- **What.** In our count, Rosa's "panel 6 of page 7" is a hiding view, not the corner view (panel 4); the paper says so and keeps his designations provisional.

### Sources and directory evidence
- **What.**
  - Ottens's tram objection concerns the visitor's arrival street. The Wikipedia summary of the 1872 line names the Jamaica Bridge, not Jamaica Street.
  - The "96 PAISLEY'S" fascia is the author's reading of Ottens's photograph; Ottens notes that the real storefront looked different.
  - Rosa recreated panels from the 1963 and 1964 stories, which bears on the composite alternative.
  - The title variant *Of Ducks and Dimes and Destinies* is given, and Rosa's phrases are marked as our translation.
- **What.** The even side of Oswald Street is in the 1877–78 OCR (p. 600), contrary to "not relocated"; Ann x Oswald NE now records it, and its trades stay unknown because the OCR does not mark where Ann Street crosses. The 1870–71 Morrison entry fills the 1870–71 gap at 53 Jamaica Street. The Jamaica Street section confirms Dryburgh at the Ann Street corner.
- **What.** The bibliography note and the AI statement say that only lines marked † were checked on the page images. The NLS digitisation licence (CC BY-NC-SA 2.5 Scotland) is credited.

### Smaller corrections
- Four rivals, not three, offer a nearer opening or a wider angle; all rival evidence is OCR-only.
- The mirror alternative has four openings, and it also fails handedness.
- 26 reference points; fourteen other volumes.
- The 1885–86 and later Paisley's entries; number 68 "appears stable".
- The width check holds at the candidate corner only; 36 Jamaica Street lies north of Ann Street.
- Simpson and Paxton no longer appear among the rivals.
- The last sentence of the paper is scoped to the declared window and filters.
- B is placed at the recorded "P.H." in the figures.
- `PROVENANCE.md` and the model-reading record are updated.
- `make test` now covers the plan angles, the mirror orientation, the later Paisley's corner, the candidate's four openings, the nearest opening and the 83 m distance.
- `requirements-lock.txt` records every package version used for the build, and the README gives the Tectonic version.

### Not changed
- The conclusion ("probable identification") is unchanged.
- Provisional panel references remain to be checked in the albums.

## Metadata changes after version 1.3 (13 November 2026, on `main`, no new release)

Metadata only; the paper, data and code of version 1.3 are unchanged.
- `LICENSE` holds the standard MIT text, so that GitHub and other tools recognise it; its scope (`src/`, `tests/`, `Makefile`) is stated in the README and in `LICENSE-CC-BY-4.0.md`.
- The CC BY 4.0 notice now names the data files, as the paper already did, and credits the National Library of Scotland digitisation of the directories (CC BY-NC-SA 2.5 Scotland).
- The README and `CITATION.cff` cite the version DOI of 1.3 (10.5281/zenodo.24192371), now assigned, with the concept DOI alongside; the README gives a table of versions and DOIs and states that earlier working files remain in the public Git history.
- Keywords are aligned across `CITATION.cff`, `.zenodo.json`, Zenodo and GitHub; the `CITATION.cff` abstract follows the version 1.3 results.

## Version 1.3 (13 November 2026)

Corrections after an external review of version 1.0 and a consistency review of version 7.1, checked against version 1.2. The census and its principal result (187 → 45 → 23 → 20 → 17 configurations on five corners, one complete documentary match) are unchanged.

### Drawn distance and width ratio (review point 1)
- **What.** The abstract, Section 4 and the conclusion state the Table 3 results exactly. No principal survivor lies within 17 m. One configuration, HS3 at Howard Street and Adam's Court Lane NW, lies within 20.4 m. The model-read ratio removes Jamaica and Howard. "Fits no corner" and "no candidate reproduces the drawn distance" are gone.
- **What.** The 20.4 m value has one label throughout: the threshold fixed in the author's earlier, undeposited working dossier.
- **Why.** Version 1.0 said the readings "fit no corner" while its own sensitivity table kept one configuration at 20.4 m and two under the model-read ratio. Version 1.2 called the same threshold both "the author's first reading" and "an early working threshold". In fact it was a decision threshold, not a reading of the panels.
- **What.** Numbers that the census computes and the text quotes are generated macros.

### The two views of the watchers (review point 2)
- **What.** A new paragraph in Section 4 states that the inked pages stage the watchers twice. In ch. 1 p. 7 panel 4 they are across a roadway. In p. 6 panel 6 and p. 7 panel 6 they stand against a wall beside a quoined edge, with no street drawn before the boy; the pencil draft agrees with the latter. The geometry follows p. 7 panel 4, the only view showing both faces of the corner and the street between; the hiding views are not used as constraints. H5, H6, the Figure 1 caption, Table 4, the composite alternative and the conclusion follow.
- **Why.** The Figure 1 caption sent readers to a discussion that Section 4 did not contain. Version 1.2 had treated the difference as inked versus pencil, but it lies within the inked pages.

### Page and panel references (review point 3)
- **What.** Pages count from the first page of each story and panels from left to right, then top to bottom. A note gives the book pages in *The Don Rosa Library* vol. 4 and the Glénat volumes (from the Inducks issue index).
- **What.** Corrected against the printed pages: the PAISLEY'S panel is ch. 0 p. 3 (version 1.2 had given book page 11 as a story page), and the corner view is ch. 1 p. 7 panel 4 (version 1.2 had panel 6). References not yet checked are marked with an asterisk as provisional.
- **What.** `evidence/model_reading_sensitivity.md` maps the working labels of the earlier verbatim files, which stay unchanged in the version 1.0 archive, to the paper's references. The Glénat entries take their published titles, and volume 2 its 2013 date.
- **Why.** The same panel carried several numbers across the repository, mixing story pages, book pages and pencil numbering.

### Open items of the version 7.1 consistency review
- **C3(b).** The distance test used the envelope of the model readings and the ratio test the range of their central values. Table 3 now also applies the envelope to the ratio (0.2–4.0: 20 configurations on 7 corners, Jamaica and Howard kept), and the test checks it.
- **C10.** H7 and the AI use statement say that the 1.5–3 band was adopted from a single earlier exploratory ChatGPT reading.
- **M10.** The appendix ties "6 W. Howard st." to the Howard Street section.
- **M14.** The README states the Python requirement and a pdflatex route.

### New evidence and reader questions
- **What.** The 1877–78 directory, read in its OCR text, gives the corner premises of the two corners that enter only under sensitivity settings to non-clothiers: a restaurant at Howard Street and Dixon Street SE, and a fruiterer at Howard Street and St Enoch's Square NW. Licensed premises facing the stand are recorded as unknown.
- **Why.** Version 1.2 said these corners were "not checked".
- **What.** The point from which the survey window and the 83 m distance are measured is Paisley's corner from 1885–86, at the Broomielaw, not the 1880–82 address at 72 Jamaica Street. Figure 2 and the text now say so.
- **What.** The abstract defines a configuration; the introduction says where the JAMAICA ST. plate appears and why the sign alone does not answer the question.
- **What.** The paper engages with Ottens's reviews:
  - his tram objection, which, read literally, counts against the Jamaica Street corners;
  - Jamaica Street as a drapery street, which makes a clothier there weak evidence on its own;
  - his early twentieth-century view of the street;
  - the earlier shoeshine stories by Lockman (1963) and Fallberg (1964).

### Not changed in this version
- The conclusion ("probable identification") is unchanged.
- The citation files and the README cite the concept DOI, since the version DOI is assigned by Zenodo when the release is archived.
