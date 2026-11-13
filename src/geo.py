"""Local geometry of the Jamaica Street / Howard Street quarter, Glasgow, from the OS 1857 survey (NLS).
All coordinates in metres; origin = north-east corner of Jamaica/Howard (55.85717, -4.25709), x east, y north."""
import math, csv

LAT0, LON0 = 55.85717, -4.25709
R = 6371000.0
def enu(lat, lon):
    x = (lon - LON0) * math.pi / 180 * R * math.cos(LAT0 * math.pi / 180)
    y = (lat - LAT0) * math.pi / 180 * R
    return (x, y)

# ---- reference points read by the author on the NLS 1857 layer (corners listed in data/corners_reference_OS1857.csv; the remaining points were read for the figures only)
P = {
 'JH_NE': enu(55.85717,-4.25709), 'JH_SE': enu(55.85706,-4.25712),
 'JA_NW': enu(55.85747,-4.25734), 'JA_SW': enu(55.85737,-4.25738),
 'JAr_SE': enu(55.85826,-4.25669), 'JAr_SW': enu(55.85827,-4.25705),
 'JB_NW': enu(55.85650,-4.25769), 'JGC_NE': enu(55.85647,-4.25734),
 'HD_SW': enu(55.85677,-4.25566), 'HD_SE': enu(55.85673,-4.25541),
 'HACL_NW': enu(55.85701,-4.25630), 'HACL_NE': enu(55.85700,-4.25624),
 'HStE_NW': enu(55.85693,-4.25585), 'HStE_NE': enu(55.85676,-4.25502),
 'AO_NE': enu(55.85761,-4.25959), 'AO_SE': enu(55.85751,-4.25959),
 'OB_NE': enu(55.85666,-4.25958), 'OB_NW': enu(55.85667,-4.25989),
 'OAr_SE': enu(55.85850,-4.25960), 'OAr_SW': enu(55.85853,-4.25988),
 'DF_NE': enu(55.85641,-4.25562), 'DF_SE': enu(55.85634,-4.25568),
 'DGC_NE': enu(55.85607,-4.25586), 'DGC_NW': enu(55.85614,-4.25608),
 'BW_NE': enu(55.85663,-4.25856), 'BW_NW': enu(55.85669,-4.25871),
 'ACL_Ar_W': enu(55.85817,-4.25587),   # NE corner of the block west of Adam's Court Lane, on Argyle
 'ACL_Ar_E': enu(55.85817,-4.25580),   # approx. (lane width 4.4 m)
 'UM_SE': enu(55.85833,-4.25588),      # Union-Mitchell block, SE corner
 'Union_E': enu(55.85840,-4.25665),    # corner of Union St on Argyle (east side)
 'Alston_W': enu(55.85851,-4.25781), 'Alston_E': enu(55.85850,-4.25766),
 'PAISLEY': enu(55.85651,-4.25770),
 'JW6_N': enu(55.857059,-4.257493), 'JW6_S': enu(55.857033,-4.257503),
 'PH1893': enu(55.85696,-4.25687),
 'JE5_N': enu(55.85734,-4.25703), 'JE5_S': enu(55.85731,-4.25704),
 'HS1_W': enu(55.85697,-4.25663), 'HS1_E': enu(55.85696,-4.25658),
 'LP_JW6': enu(55.857033,-4.257503),
}

# ---- frontages (polylines): lists of points
FACADES = {
 'Jamaica W (south of Ann)': [P['JA_SW'], P['JB_NW']],
 'Jamaica W (north of Ann)': [P['JA_NW'], P['JAr_SW']],
 'Jamaica E (north of Howard)': [P['JH_NE'], P['JAr_SE']],
 'Jamaica E (south of Howard)': [P['JH_SE'], P['JGC_NE']],
 'Howard N (west of ACL)': [P['JH_NE'], P['HACL_NW']],
 'Howard N (east of ACL)': [P['HACL_NE'], P['HStE_NW']],
 'Howard S': [P['JH_SE'], P['HD_SW']],
 'Howard S (east of Dixon)': [P['HD_SE'], enu(55.85660,-4.25470)],
 'Ann N': [P['JA_NW'], P['AO_NE']], 'Ann S': [P['JA_SW'], P['AO_SE']],
 'Broomielaw N (east of Wood)': [P['JB_NW'], P['BW_NE']], 'Broomielaw N (west of Wood)': [P['BW_NW'], P['OB_NE']],
 'Great Clyde N': [P['JGC_NE'], P['DGC_NW']],
 'Dixon W': [P['HD_SW'], P['DGC_NW']], 'Dixon E (north of Fox)': [P['HD_SE'], P['DF_NE']], 'Dixon E (south of Fox)': [P['DF_SE'], P['DGC_NE']],
 'Oswald E (south of Ann)': [P['OB_NE'], P['AO_SE']], 'Oswald E (north of Ann)': [P['AO_NE'], P['OAr_SE']],
 'Oswald W': [P['OB_NW'], P['OAr_SW']],
 'Argyle S (west of Jamaica)': [P['JAr_SW'], P['OAr_SE']],
 'Argyle S (east of Jamaica)': [P['JAr_SE'], P['ACL_Ar_W']],
 'Argyle N': [P['Alston_E'], P['Union_E']],
 'Argyle N (Union-Mitchell)': [enu(55.85841,-4.25648), P['UM_SE']],
 'ACL W': [P['HACL_NW'], P['ACL_Ar_W']], 'ACL E': [P['HACL_NE'], P['ACL_Ar_E']],
 'Square W': [P['HStE_NW'], enu(55.85812,-4.25545)], 'Square E': [P['HStE_NE'], enu(55.85795,-4.25500)],
}

# ---- blocks (approximate polygons, for filling)
BLOCKS = {
 'A (51-53 Jamaica / 1-9 Howard)': [P['JH_NE'], P['JAr_SE'], P['ACL_Ar_W'], P['HACL_NW']],
 'B (Custom House)': [P['JH_SE'], P['HD_SW'], P['DGC_NW'], P['JGC_NE']],
 'W-S (Ann - Broomielaw)': [P['JA_SW'], P['JB_NW'], P['BW_NE'], P['BW_NW'], P['OB_NE'], P['AO_SE']],
 'W-N (Ann - Argyle)': [P['JA_NW'], P['JAr_SW'], P['OAr_SE'], P['AO_NE']],
 'E-ACL-Square': [P['HACL_NE'], P['ACL_Ar_E'], enu(55.85812,-4.25545), P['HStE_NW']],
 'E-Dixon': [P['HD_SE'], P['DF_NE'], enu(55.85628,-4.25470), enu(55.85660,-4.25465)],
 'SE-Fox': [P['DF_SE'], P['DGC_NE'], enu(55.85600,-4.25475), enu(55.85622,-4.25470)],
 'NE-Square': [P['HStE_NE'], enu(55.85660,-4.25465), enu(55.85800,-4.25440), enu(55.85795,-4.25500)],
}

def load_openings(path='data/openings_OS1857_Jamaica.csv'):
    out = []
    with open(path, encoding='utf-8') as f:
        rd = csv.DictReader(f, delimiter=';')
        for r in rd:
            a = tuple(map(float, r['N or W wall (lat, lon)'].split(',')))
            b = tuple(map(float, r['S or E wall (lat, lon)'].split(',')))
            out.append(dict(id=r['id'], street=r['street'], side=r['side'], type=r['type'],
                            w=float(r['width (m)']), p1=enu(*a), p2=enu(*b)))
    return out

# axes
def unit(p, q):
    dx, dy = q[0]-p[0], q[1]-p[1]; n = math.hypot(dx, dy); return (dx/n, dy/n)
U_JAM = unit(P['JH_NE'], P['JAr_SE'])     # northwards along Jamaica
U_HOW = unit(P['JH_NE'], P['HStE_NW'])    # eastwards along Howard
W_JAM = 22.9; W_HOW = 11.5
