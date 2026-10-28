# Technical Amendment — 2026-10-06
Made before inspecting any ON/OFF results (outcome-blind).

1. **Distance metric**: freeze text says "shortest path distance on the planar graph of
   facility points and small-area centroids". Under an uncapacitated nearest-supply rule
   this is the geodesic distance to the nearest facility; implemented as WGS84 geodesic
   (pyproj Geod.inv). The pre-specified travel-time sensitivity covers the
   speed-assumption leg (40 km/h road proxy, 4 km/h walk).
2. **F2 demand weights**: age-restricted (school-age) small-area populations are not
   published at r2ka level; alternative weight uses SETAI (households). Documented, not
   improvised post hoc.
3. **Capacitated sensitivity**: not run. Neither P04 nor P29 supplies a capacity
   attribute (P04_008..010 are administrative flags). No capacity was invented;
   capacity-neutrality stands as the declared limitation.
4. **F1 tiers**: P04_001 = 1 hospital / 2 general clinic / 3 dental. "Primary care vs
   hospital" is implemented as clinic tier vs hospital tier; dental facilities are
   excluded (not primary-care substitutes).
