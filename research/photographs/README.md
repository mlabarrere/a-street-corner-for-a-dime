# Photographs of the foot of Jamaica Street, c. 1870–1915

A working catalogue of documented photographs of the paper's window (Argyle Street to the Clyde, Oswald Street to St Enoch Square, with Glasgow Bridge and the Broomielaw at the foot of Jamaica Street). The aim is to find the photographs Don Rosa drew from in 1991–92. The PAISLEY'S sign he drew is real; in 1991–92 his source would have been printed, not a website.

Compiled 15 November 2026 in two passes, and closed the same day: the findings are written up in the paper, version 1.6, section "What the photographs tell us". The catalogue changes nothing in `data/`, `src/` or `evidence/`, and the census and chance figures do not use it. No image is stored in this repository: links and metadata only.

**Status: closed.** Rosa's own photograph was not identified. The open questions below are what a library visit, not a further web search, would settle.

## Files

- `catalogue.csv`: 38 documented images, one row per image (P01–P38). Each has a holding institution or a named publisher, a reference and a stated date or photographer.
- `leads.csv`: 10 rows (L02–L11).
  - Images without a traceable publisher or holding reference, or known only from a defunct enthusiast site.
  - One row (L06) listing documented records that still could not be opened.
  - L01 was identified in the second pass and is now P28.

Main columns:

- `stated_date` is quoted as the source gives it.
- `own_dating` and `own_dating_reasoning` hold our own dating, mostly from signs checked against the Post Office directory.
- `paisleys`, `jamaica_st_plate` and `peachys` record whether those signs are legible.
- `visual_check` says whether we looked at the image ourselves, and at what resolution.

## What the panels give (from `paper/main.tex`, Table 1)

What to look for in each photograph:

- **H2:** a JAMAICA ST. plate above a PAISLEY'S sign on a flat frontage, with no corner in view.
- **H4:** PEACHY'S, a clothes shop on a corner, and a bar across the side street.
- **H4–H6:** cobbled roadways, kerbed footways, a horse and cart, and watchers against a brick wall beside a quoined corner.

## Method

1. **TheGlasgowStory** (Glasgow Museums, Mitchell Library, Glasgow City Archives, Glasgow University images).
   - Every quick-search result for Jamaica Street, Broomielaw, Glasgow Bridge, Paisley's, St Enoch (Square), Oswald Street, Howard Street, Clyde Street, Union Street, Dixon Street, Midland Street and Anchor Line was harvested: 275 records.
   - These were filtered by place, period and medium.
   - Drawings, engravings, etchings and paintings were set aside (see "Non-photographic images" below).
2. **Wikimedia Commons**, through its API: category sweeps (Jamaica Street, Glasgow Bridge, Broomielaw, St Enoch Square, Union Street, Clyde Street, Glasgow in the 1880s/1890s/1900s, photochrom prints) and searches for LoC items. Commons copies were used only where they carry the holding institution's reference (LoC LCCN, Rijksmuseum object number, Aberdeen accession number) or a named publisher.
3. **Second pass (15 Nov 2026).**
   - TuckDB (Tuck postcard database): Jamaica Street and Glasgow Bridge cards, fronts and backs.
   - University of St Andrews Valentine collection, Te Papa, Rijksmuseum (data API and IIIF), Francis Frith.
   - glasgowhistory.com is now a parked domain (`?p=209` redirects to a parking page). Its Jamaica Street page was read from the Wayback Machine captures of 2019-09-05 and 2022-08-13.
   - Books: archive.org metadata, archive.org full-text search snippets, and the archive.org book reader's own search-inside. The reader gives the printed page or leaf for each hit, with no loan and no login. The OCR files of lending-library books cannot be downloaded.
4. **Sites that refuse automated fetches.** Library of Congress, National Galleries of Scotland, trove.scot/Canmore and Getty were not fetched.
   - Their metadata comes from web-search snippets, or from Commons copies of the same object (the LoC photochroms).
   - No attempt was made to get round the blocks.
   - Capital Collections now shows an interactive bot check, which was not passed.
5. **Visual check.** Every reachable image was opened and zoomed (crops at 2–7×) to read signs.
   - Viewing copies were kept outside the repository and are not committed.
   - The resolution used is recorded per row.
   - Most web copies are about 1000 px wide, so small street plates may be invisible at that size even where they exist.
6. **Dating by signs.** The OCR (`_djvu.txt`) of the Post Office Glasgow directory volumes from 1870–71 to 1911–12 (archive.org `postofficeannual<yyyy><yy>gla`) was downloaded to a scratch folder outside the repository.
   - It was searched only by pattern (grep-style), for each legible name.
   - The OCR is uneven; the ranges below are first and last volumes with a hit and were not checked on the page images.

### Directory windows used for dating

| Sign | Directory evidence (OCR) | Window |
|---|---|---|
| PAISLEY'S | Peter Paisley, clothier and outfitter, 72 Jamaica St (1880–81 to 1882–83); 80 to 96 Jamaica St (1883–84 to 1889–90), "and Broomielaw corner" (1884–85 to 1886–87); 82 to 96 Jamaica St and 2–12 Broomielaw (1890–91 on); P. Paisley & Son (1902–03 on); 76–96 Jamaica St (1911–12) | PAISLEY'S at the corner block: 1883–84 or later; on the Broomielaw front: 1890–91 or later |
| URIE / ARTIST / PHOTOGRAPHER | John Urie, photographer (and portrait painter), 83 Jamaica St, 1870–71 to 1887–88; at another address from 1891–92 | up to c. 1888 |
| THE ST MUNGO VINTNERS' CO. | St Mungo Vintners' Co., spirit merchants (100 Gt Clyde St and other premises), 1881–82 to 1895–96 | c. 1881–1896 |
| The SCOTTISH WHOLESALE STORES | Scottish Wholesale Drapery Stores, 14 Broomielaw (1884–85), 4–16 Broomielaw (1885–86); not found later | c. 1884–86 (OCR only) |
| The GRAND COLOSSEUM WAREHOUSE Co. | that style from 1894–95 (Walter Wilson & Co.'s Colosseum, Jamaica St, from 1878; "Grand Colosseum Warehouse" first seen 1890–91) | 1890s or later |
| G. KEPPIE & Co | Keppie, photographers, 56 Jamaica St, from 1895–96 | 1895–96 or later |
| [RAMSA]Y, PHOTOGRAPHER / [M']WATTERS, watchmaker | Colin Ramsay, 6 Union St, 1876–77 to 1883–84; John M'Watters, 6 Union St, to 1882–83 | c. 1882–83 |
| HOWELL'S TOBACCOS | Alfred Howell, cigar importer, 178 Argyle St, every volume 1870–71 to 1911–12 | not discriminating |
| [D]ROOKO | Royal Drooko Stores, 219 Argyle St (1899–1909), 6 Jamaica St (from 1909–10) | 1899 or later |

**Correction to the parent notes.** Paisley's reached the corner block (80–96 Jamaica St) in 1883–84, not 1885–86. The 1885–86 volume was simply the first one sampled.

## Results

- 38 documented images catalogued; 31 checked by eye here (P38 only in a limited book preview).
- 4 have metadata only (Canmore, through search snippets).
- 2 were seen only by the parent session (NGS, Getty).
- 1 could not be opened (Aberdeen; the download failed).
- PAISLEY'S is legible on 10 documented images (P01–P04, P28–P33). It is also in the OCR of the Scribner plate (P38), but was not found by eye in the preview.
- **No JAMAICA ST. street plate is legible on any image.** P32 (Tuck "Town & City" 2150) is the only image with street-name plates on the Paisley's corner pier, and they are unreadable at 1490 px.
- **PEACHY'S appears nowhere**, neither on an image nor in the OCR of any book searched.

### Findings that change earlier notes

- **L01 is Raphael Tuck & Sons' "Sepia" Postcard No. 2015, now P28** (TuckDB 97807, card 9/12 of the set "GLASGOW,").
  - The back reads "Glasgow. Raphael Tuck & Sons' 'Sepia' Postcard. No. 2015. Art Publishers to Their Majesties the King & Queen", with "Copyright London" and "Printed in England". Read by eye.
  - TuckDB gives a first use of 03/10/1902. Dating: c. 1902–05.
  - Tuck also issued the same negative as "Glosso" No. 1092 (P29).
  - The Never Was copy is this card with the right edge, and the Tuck trade mark, cropped off.
- **Valentine "Jamaica Street, Glasgow. 2522 J.V." exists as two negatives.**
  - St Andrews records the number as "Registered 1882". Its negative (P34) shows electric car 749 under span wires, G. KEPPIE & Co at 56 and the Colosseum's ANNUAL JULY SALE, so it dates from July 1901 or 1902. It is a replacement issued under the old number and caption.
  - The two HES dates are therefore both plausible: PA 46/7, c. 1882, with horse trams (P22), is probably the original; B 55723, c. 1900 (P23), the replacement.
  - The camera stands at about no. 70 looking north, so Paisley's (72–96) is behind it. On the 1882 original, Paisley's at 72 would be just behind the camera or at the left edge; that original has not been seen.
- **Valentine "The Broomielaw Bridge, Glasgow. 287. J.V." (Te Papa, P30) is c. 1884–87**, not "circa 1890".
  - At 6786 px it shows PAISLEY'S / CLOTHIERS / PAISLEY'S, 96, BROOMIELAW CORNER, URIE / ARTIST / PHOTOGRAPHER and THE ST MUNGO VINTNERS COMPANY. Read by eye.
  - It was taken from the same spot as TGSE00176 (P01) at about the same time, but it is a different exposure (different traffic; a landing stage with a kiosk where P01 has a Clutha ferry).
- **P01 and P02 were taken from the west of Glasgow Bridge, not the east.** In both, the 1878 railway bridge is in the left foreground and the camera looks north across the bridge.
- **Four more Paisley's views with a named publisher:** Tuck Photochrome 1414 (P31), Tuck "Town & City" 2150 (P32), James M. Davis "Jamaica Bridge, Glasgow" (Rijksmuseum, P33), and the E. A. Schwerdtfeger card 02332 (lead L08, 1911–14).
- **The earliest dated photograph with legible shop names in the window** is Valentine "Argyle Street, Glasgow. 2568 J.V." (Rijksmuseum, P35), c. 1882–83, looking east along Argyle Street from the Jamaica Street crossing.

## Candidates for Rosa's source, ranked

The ranking weighs two things:

- How closely the image matches H2: PAISLEY'S on a flat frontage, no corner, street level.
- How plausibly Rosa, in Kentucky in 1991–92, could have seen it in print.

1. **P28, Tuck "Sepia" 2015, "Jamaica Street. N. Glasgow."** (c. 1902–05; same negative as P29).
   - Still the best match to H2: street level, large fascia letters "96 PAISLEY'S 82" on a flat frontage, no corner in frame.
   - Its publisher and number are now known. No book reproduction before 1992 has been found; a postcard from a dealer or a collection remains possible.
2. **P38, Quennell, *The Day Before Yesterday* (New York: Scribner, 1978), plate 133, "Jamaica Street, Glasgow, c.1896".**
   - The only Jamaica Street photograph found in a book published in the US before 1992. The archive.org copy came from a US public library.
   - Street level, with horse trams; the Colosseum front at left.
   - PAISLEY'S is in the plate's OCR but was not seen in the low-resolution preview; the photographer and the plate's credit were not found.
   - A copy of the book, opened at plate 133, would settle both.
3. **Jack House, *Glasgow Old and New* (1974 and Drew editions), "Corner of Broomielaw and Jamaica Street – 1914"**, and **Morton, *Old Glasgow* (1988), p. 61, "1914 view of Jamaica Street, looking north to Paisley's Corner"**.
   - British books, but in print in the 1970s–80s, with the Paisley's corner in their captions.
   - Both 1914 views may come from the Glasgow Corporation Tramways traffic photographs of April 1914 (cf. P09, dated 15.4.14). That is inferred and not checked.
   - The corner is in view, which H2 does not draw.
4. **P30, Valentine 287 J.V., and P01, TGSE00176** (c. 1884–88).
   - The PAISLEY'S / CLOTHIERS / PAISLEY'S frontage is on a flat white wall, and the date is the closest to the 1877 setting. However, they are seen from across the river.
   - Valentine sold the print in albums. No book printing before 1992 has been found for either.
5. **P02, LoC photochrom 13174** (c. 1890–94).
   - US-held and sold in the US, in colour.
   - No book reprint before 1992 was found.
6. **P03, Mitchell Library postcard "Jamaica Street looking north"**, and **P32, Tuck "Town & City" 2150** (c. 1901–05). Street level, but the corner is in view.

For the clothes shop on a corner (H4), P08 (Argyle Street at Jamaica Street, c. 1900–12) shows a corner shop with garments under a canopy; its fascia is not legible. P35 shows "[..] & SON CLOTHIERS." near the same crossing, c. 1882–83.

## Photo books published before 1992

All verified with the archive.org book reader's search-inside unless stated otherwise. Captions are quoted from the OCR, so OCR errors are kept. Plates are uncredited unless a credit is given.

- **Peter Quennell, *The Day Before Yesterday: a photographic album of daily life in Victorian and Edwardian Britain*, New York: Scribner, 1978, ISBN 0684160668.** archive.org `daybeforeyesterd00quen`; "photographs by Francis Frith and others".
  - Plate 133 (leaves n125–n126): "133. Jamaica Street, Glasgow, c.1896. Activity in Glasgow city streets was as great as in any of the English cities like London and Manchester." See P38.
- **Jack House, *Glasgow Old and New*, Wakefield: EP Publishing, 1974, ISBN 0715810782.** archive.org `bwb_KS-192-719`.
  - p. 45: "Corner of Broomielaw and Jamaica Street - 1914 / Paisley's Corner has been famous in Glasgow for well over 100 years. A single motor car moves grimly through the horse traffic and a tram-car in Jamaica Street waits for a chance to cross. On the left is the railway into Central Station …" p. 46 is the 1974 pair.
  - General credit: House's own collection, the Mitchell Library and other city libraries, *The Glasgow Herald* and *Evening Times*, and "numerous other sources".
- **Jack House, *Glasgow Old and New*, Glasgow: Richard Drew** (preface dated 1983; catalogued as 1988). archive.org `glasgowoldnew0000jack`.
  - p. 48: the same 1914 photograph, "Corner of Broomielaw and Jamaica Street 1914". p. 49 is the 1983 pair. The index gives "Paisley's Corner 48, 49".
- **Henry Brougham Morton, *Old Glasgow*, Glasgow: Richard Drew, 1988, ISBN 0862672384.** archive.org `oldglasgow0000mort`.
  - p. 61: "No motor vehicles are visible in this 1914 view of Jamaica Street, looking north to Paisley's Corner. Two 'shawlie' women pass the ornate lamp standard (foreground right), positioned in the middle of the road to carry tramway wires across Jamaica Bridge". The caption was joined from three OCR fragments.
  - Credit (p. 4): "All the photographs in this book have been reproduced by permission of Strathclyde Regional Archive unless otherwise indicated."
  - p. 79: "Traffic on Jamaica Bridge, 1936" (outside the period).
- **Ian G. McM. Stewart, *Glasgow Tramscapes*, Dianswell, 1984, ISBN 0950976709.** archive.org `glasgowtramscape0000stew`. Section "Jamaica Bridge Scenes":
  - p. 6: "Glasgow Bridge in the 1880's was a bustling place. … Note the advertisements for Gaiety Theatre attractions in the foreground." Credit: R. B. Napier collection.
  - p. 6: a Clutha at Jamaica Bridge Pier. Credit: J. Leggett collection.
  - p. 7: "By 1903 the same bridge seems more orderly with open-topped electric tramcars then in evidence. …" Credit: T. & R. Annan. It could be the Annan view of 1905 (P04); not seen.
  - p. 7: "Paisley's corner at Broomielaw was timeless, changing hardly at all in eighty years. A policeman stands patiently watching heavy horse-drawn traffic …" Credit: R. B. Napier collection.
- **Ronald W. Brash, *Glasgow in the Tramway Age*, London: Longman, 1971, ISBN 0582204887.** archive.org `glasgowintramway0000bras`.
  - p. 11: "The trams rule the road in Jamaica Street around 1912". Credit: Museum of Transport, Glasgow.
  - p. 28: "Glasgow's Jamaica Bridge in the 1880s, showing the original privately-owned horse cars". Credit: T. & R. Annan.
  - p. 66: "Steamers leaving the Broomielaw about the turn of the ce[ntury]". Credit: T. & R. Annan.
- **C. S. Minto, *Victorian and Edwardian Scotland from Old Photographs*, London: Batsford, 1970; New York: Viking, 1971.** archive.org `victorianedwardi0000unse_t8e8` (the US printing). This is the Batsford "from old photographs" series title for Scotland; no Glasgow-only title in the series could be confirmed.
  - Plate 33: "Glasgow Bridge c.1867. On the far bank to the left is the Broomielaw quay …" Credit: The Science Museum, London. This is before Paisley's.
  - Plate 38: "Argyle Street … c.1885". Credit: Edinburgh Public Library. Edinburgh's libraries hold Valentine prints, so this could be a view like P35 (not seen).
  - Plate 42: "At the Broomielaw, c.1890. The 'Balmoral' sails for Greenock."
- **Jack House, *The Heart of Glasgow*, London: Hutchinson, 1978 edition, ISBN 0091334500.** archive.org `heartofglasgow0000hous_g1m2`.
  - Plate 9b (between pp. 144 and 145): "The Broomielaw Bridge in 1870, known also as Jamaica Bridge and Glasgow Bridge." This is before Paisley's.
- **John Butt, *Industrial History in Pictures: Scotland*, Newton Abbot: David & Charles, 1968, ISBN 0715342711.** archive.org `industrialhistor0000butt`.
  - p. 103: "Traffic on Jamaica Bridge, Glasgow, c1914 …". Credit: Richard Dell, Glasgow City Archivist (reassembled from two-column OCR).
- **C. A. Oakley, *Our Illustrious Forebears*, Glasgow: Blackie, 1980, ISBN 0216909996.** archive.org `ourillustriousfo0000oakl`.
  - p. 174: "Jamaica Street in 1888. Most of the buildings seen here remained almost unaltered until after the second word war." No credit found. Worth seeing: 1888 is within Paisley's corner-block period.
- **C. A. Oakley, *The Second City*, Glasgow: Blackie, 1975, ISBN 0216893887.** archive.org `thesecondcity0000oakl`.
  - p. 234: "Congestion at Jamaica Street Bridge, period 1920." p. 90 is a Muirhead Bone drawing; pp. 70–71 a panorama drawing of 1858.
- **C. A. Oakley, *Dear Old Glasgow Town*, London: Blackie, 1975, ISBN 0216898986.** archive.org `dearoldglasgowto0000oakl`.
  - p. 65: "Argyle Street and the Union Street-Jamaica Street crossing, once unquestionably the city centre. …" No date or credit.
- ***Glasgow's Glasgow: people within a city* (souvenir guide), 1990.** archive.org `glasgowsglasgowp0000unse`. Full-text snippet only, no page: "Corner of Broomielaw & Jamaica Street".

**Searched, no relevant plate:** Daiches, *Glasgow* (1977); Worsdall, *A Glasgow Keek Show* (1981); *Glasgow and the Clyde 100 Years Ago* (1978, engravings). Lindsay (1972, 1989), Barr (1980, 1981), Blair (1985), Checkland (1976) and *The Clyde* (1946) were screened by full-text search only. "Peachy", "photochrom" and "Valentine" (as photographer) occur in none of the books.

**Exist or proposed, but not searchable:** A. Finlay, *Trams of Scotland in Old Picture Postcards* (Zaltbommel: European Library, 1984), with no scan. No European Library *Glasgow in Old Picture Postcards*, Annan *Glasgow at the Turn of the Century* or Glasgow-only Batsford title could be confirmed. Stenlake's pre-1992 titles on archive.org cover other towns. The only pre-1992 US Detroit Publishing compilation found, *Main Street, U.S.A.* (Dover, 1988), covers US views only.

## Sources consulted

| Source | Access | Result |
|---|---|---|
| TheGlasgowStory | direct fetch works | 275 records harvested; 16 catalogued (P01, P03–P16) |
| Wikimedia Commons | API works | LoC photochroms (P02, P17), Rijksmuseum (P18), Aberdeen (P19), postcards (P20, P21), leads |
| TuckDB | direct fetch works | P28, P29, P31, P32; two painted cards set aside |
| University of St Andrews collections | works in a browser; bot check refuses scripts | P34; L06, L10 have no image online |
| Te Papa | direct fetch works | P30 |
| Rijksmuseum | data API and IIIF work | P33, P35, P36 |
| Francis Frith | works in a browser; refuses scripts | P37 |
| archive.org | metadata, full-text search and the book reader's search-inside work; OCR of lending books cannot be downloaded | directory OCR; the book plates above; P38 |
| glasgowhistory.com | parked domain; read from Wayback captures | L07–L09, L11 |
| Library of Congress (loc.gov) | refuses automated fetches (403) | metadata from Commons copies of the LoC files |
| National Galleries of Scotland | refuses automated fetches (403) | P24 from the parent session only |
| trove.scot / Canmore | refuses automated fetches (403); Canmore was switched off in June 2025 and replaced by trove.scot, so old URLs may not resolve | P22, P23, P25, P26 from search snippets; not viewed |
| Getty Images / photos.com | refuses automated fetches | P27 from the parent session and a search snippet |
| Capital Collections | interactive bot check, not passed | L06 from search snippets |
| Aberdeen emuseum | no response | P19 metadata from Commons only |
| eBay, HipPostcard, Delcampe | refuse automated fetches or no usable results | search snippets only; nothing catalogued |
| SCRAN, Glasgow City Archives, Virtual Mitchell, NLS, Historic England | not reached | not searched |

Not a photograph, but noted:

- **Mitchell & Kenyon film** *Jamaica Street Glasgow* (1901; BFI). The collection was rediscovered in 1994, so it could not have been a source in 1991–92.
- **Non-photographic images**, set aside:
  - TheGlasgowStory TGSA00159 (Broomielaw Bridge, engraving, c. 1890), TGSA00161 (River Clyde, drawing, 1880s), TGSB00083 and TGSB00088 (Edwin Law etchings, c. 1900).
  - Tuck Oilette No. 791, "Glasgow Bridge", painted by D. Small (TuckDB 97762; first use 1902). It shows PAISLEY'S on the pediment and fascia, seen from the south end of the rebuilt bridge.
  - Tuck Oilette No. 7978, "Jamaica Bridge, Glasgow", painted by C. E. Flower (TuckDB 97896; first use 1926). It shows "[PA]ISLEY'S STORE".
  - Muirhead Bone, building Jamaica Street Bridge, 1895 (in Oakley, *The Second City*, p. 90).

## Open questions

1. Who took plate 133 of *The Day Before Yesterday* (Scribner, 1978), and where is PAISLEY'S on it? The plate's credit and a legible copy need a physical copy or a loan. It may be the Hulton "Street in Glasgow" (P27, circa 1895) or the 1882 Valentine 2522 (P22).
2. Was the Tuck "Sepia" 2015 card (P28) reproduced in any book before 1992? None found so far.
3. What do the 1914 Paisley's corner views in House (p. 45 / p. 48) and Morton (p. 61) show, and are they the Glasgow Corporation Tramways photographs of April 1914? Neither page image was seen.
4. What does Oakley's "Jamaica Street in 1888" (*Our Illustrious Forebears*, 1980, p. 174) show? It falls within Paisley's corner-block period.
5. Does any image, at full resolution, show a JAMAICA ST. plate? The best chance is the corner pier on P32 (Tuck 2150, plates unreadable at 1490 px).
6. The HES image of the 1882 Valentine 2522 (PA 46/7, P22) needs a person to view it on trove.scot. It would show whether Paisley's at 72 Jamaica St is at the left edge.
7. Still not opened (L06): St Andrews RNWS-26-75 and RNWS-39-302 (no image online), Capital Collections 24422 (bot check), Canmore C 47388.
8. The directory windows above come from OCR only and have not been checked on the page images.
