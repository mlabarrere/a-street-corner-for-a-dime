# Aggregate model-reading sensitivity

Date: 10 November 2026. Five Claude model instances read either 10 or 14 supplied comic-page images. All received the same narrative context and imposed definitions of the corner and streets X and Y; the 14-image set added three inked-page captures and the SOU'S/PEACHY'S page. No map, directory, candidate location or web search was available. These are exploratory model readings, not independent human observations or archival evidence.

Adult height H is converted at 1.7 m. Page and panel labels used in the readings were the working labels of the time; the paper's references were re-established against the printed pages, and the table at the end maps the old labels to them.

Readers are listed in the same order (A to E) in every row. The version 1.0 summary swapped the width and ratio values of readers A and B; the values here follow the verbatim record.

| Quantity | Individual central readings | Aggregate used in sensitivity analysis |
|---|---|---|
| Family-to-corner distance | 4, 5, 4, 3.5, 5 H | 4--5 H; full envelope 2.5--10 H (4--17 m) |
| Side of street X | right, right, right, right, right | right, unanimous; one pencil draft is mirrored |
| Width of street Y | 5, 6.5, 4, 3, 4.5 H | 3--6.5 H |
| Width of street X | 6.5, 4, 6.5, 7.5, 6 H | 4--7.5 H |
| Ratio Y/X | 0.8, 1.6, 0.6, 0.4, 0.75 (individual intervals 0.4--1.8, 0.6--4, 0.25--1.9, 0.2--0.9, 0.2--3) | range of central values 0.4--1.6; envelope 0.2--4; neither street is securely wider |
| Licensed premises | four place it across X or nearly so; one indeterminate | across X retained as the majority reading |

## Application to the census

- Principal model (author's ratio 1.5--3, angle at least 15 degrees): 17 configurations on 5 corners.
- Distance D at most 17 m, the full model-reading envelope: 0 configurations.
- Distance D at most 20.4 m, the threshold fixed in the author's earlier working dossier (not deposited): 1 configuration, Howard × Adam's Court Lane NW (opening HS3, 20.0 m); Jamaica/Howard is not among them.
- Model-read width ratio 0.4--1.6: 2 configurations on 1 corner, Howard × Dixon SE, whose corner premises the 1877-78 directory gives to a non-clothier; Jamaica/Howard (ratio 2.0) is removed.
- Model-read width-ratio envelope 0.2--4 (treated like the distance envelope): 20 configurations on 7 corners; Jamaica/Howard is kept.
- No width-ratio constraint: 20 configurations on 7 corners.
- No handedness constraint: 34 configurations on 9 corners.

The drawings are non-metric: no panel shows both street widths cleanly, perspective and focal length are unknown, and the distance intervals are broad. The readings are therefore reported as sensitivity tests rather than as archival facts or a substitute for human iconographic assessment.

## Working labels in the earlier verbatim record

The verbatim record of these readings (`blind_readings_v3*`, `src/blind_reading/`) and the working reports (`expertise/`) are kept unchanged in the version 1.0 archive and in the Git history. Their page and panel labels mix story pages, book pages and pencil numbering. The paper counts pages from the first page of each story and panels from left to right, then top to bottom; chapter 0 story page n is book page n + 8 in *The Don Rosa Library* vol. 4 and in Glénat vol. 2; chapter 1 story page n is book page n + 24 in the former and n + 10 in Glénat vol. 1. References marked provisional in the paper have not yet been checked against the printed page.

| Label in the earlier files | What it denotes | Reference in the paper |
|---|---|---|
| `ch0-p15c1` (image file names) | chapter 0, story page 15, panel 1 | ch. 0 p. 15 panel 1 (provisional) |
| `ch1-p7c6` (image file names) | described in the working reports as the corner view with the watchers' heads cut by the frame | ch. 1 p. 7 panel 4; panel 6 is a hiding view |
| `C0_EN22`, "ch. 0 p. 22" | book page 22 of *The Don Rosa Library* vol. 4 | ch. 0 p. 14 |
| "ch. 1 p. 6 panel 8" (called inked in the summary) | the printed page 6 has six panels, so this is the pencil numbering | pencil p. 6 panel 8 (provisional); the printed hiding view is ch. 1 p. 6 panel 6 |
| "ch. 1 p. 7 panel 4" (version 1.0) and "panel 6" (version 1.2) for the corner view | two different panels | corner view ch. 1 p. 7 panel 4; hiding view ch. 1 p. 7 panel 6 |
| "pencil draft: 5; paper: 6" (version 1.0 quality check) | index of the corner panel | pencil p. 7 panel 5 (provisional); printed corner view ch. 1 p. 7 panel 4 |
| "ch. 0 p. 11" for the PAISLEY'S panel (version 1.2) | book page 11 | ch. 0 p. 3, lower-left panel |
| "p. 15 panel 1" for the PAISLEY'S panel (earlier working dossier, cited in version 1.0 reports) | another label for the sign panel | ch. 0 p. 3, lower-left panel |
| "p. 7 panel 6" said to be absent from the 10-image set (version 1.0 summary), although an image of that set is named `ch1-p7c6` | one label used for two different things | not used in the paper |
