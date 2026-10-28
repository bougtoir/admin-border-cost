# Healthcare access — ON/OFF results (MLIT P04-20)

Demand: 11,978 small-area units, pop 3,991,697 (2020 Census). Supply: hospitals n=221
(Shiga 57 / Kyoto 164), general clinics n=3,584 (1,079 / 2,505), dental excluded.
Assignment: uncapacitated nearest facility, WGS84 geodesic km; ON = same prefecture
only, OFF = unrestricted.

| metric | hospital ON | hospital OFF | ON−OFF |
|---|---|---|---|
| mean (pop-weighted, km) | 1.6306 | 1.6260 | +0.0046 |
| median km | 1.0056 | 1.0036 | +0.0020 |
| p90 km | 3.5982 | 3.5982 | 0.0000 |
| p95 km | 5.3887 | 5.3887 | +0.0000 |
| max km | 22.112 | 22.002 | +0.110 |
| share >10 km | (see metrics csv) | | +3e-6 (>5km col) |
| OFF cross-boundary pop share | — | 0.1729% | |
| mean km, border munis | 1.4640 | 1.4497 | +0.0143 |
| worst-decile border−interior gap (km) | 0.662 | 0.457 | −0.205 |

Clinic tier: mean 0.4527 → 0.4521 km (+0.0005 km); OFF cross-boundary share 0.1055%;
worst-decile border−interior gap 0.217 → 0.174 km.

**Reading**: the prefectural boundary imposes a mean access cost of ~5 m (hospital) /
~0.5 m (clinic) — essentially zero; under OFF only ~0.1–0.2% of population would be twice-served
across the line. Costs concentrate in 11 border municipalities. Status: measured, not
optimised (closed-form argmin — no solver gap possible).
