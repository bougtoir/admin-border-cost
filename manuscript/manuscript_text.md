# The cost of inherited borders: quantifying the administrative-boundary constraint in electoral-district spatial optimization across Kyoto and Shiga, Japan

## Highlights

- We quantify, for the first time in a Japanese two-prefecture setting, the marginal cost of an administrative-border constraint in electoral-district optimization.
- Exact CP-SAT formulation (municipality level) and heuristic simulated annealing (census small-area level) models are matched on identical objectives and constraints.
- The Kyoto–Shiga border's constraint cost is bounded to at most ~30% of the incumbent objective scale at municipality resolution and a best-found difference of zero at census small-area resolution; the line crosses fewer commuting trips than all 200 matched placebo borders, a pattern consistent with the border's broad alignment with the Lake Biwa watershed.
- In 200 matched placebo borders, 61% admit no feasible constrained map at the same tolerance (no-incumbent outcomes; none recovered at 10× budget), and the real border's cost is at the 10th percentile — the inherited line is unusually benign, not generic.
- All results regenerate end-to-end from raw official data (e-Stat statistical GIS, Census Table 6-1, IPSS projections, e-Gov statute XML).

## Abstract

Electoral districts are drawn inside inherited administrative territories, yet the populations organizing daily life flow across those borders. We measure the cost of this mismatch for the statutory rule that Japan's House of Representatives districts not straddle prefectural boundaries, using the Kyoto–Shiga border, which bisects a commuting field of {{n_cross}} cross-prefecture trips (2020 census). We pose a nonpartisan districting problem (population deviation ≤ 20%, contiguity, compactness, municipal coherence, flow retention) and solve it twice under identical objectives and solver settings, once with the border as a hard constraint (ON) and once without (OFF), giving Cost_border = L*(ON) − L*(OFF). At municipality scale the true optimum is not tightly identified — the defensible interval is {{cost_border_A_lo}} to {{cost_border_A_hi}} objective units (up to ~30% of incumbent scale) — while at census small-area scale the constrained and unconstrained best-found maps coincide (best-found difference {{cost_border_B}}). Functionally the border is unusually well placed: it crosses only {{cross_od_real}} trips, fewer than all 200 matched placebo borders (median {{cross_od_placebo_median}}), consistent with the Lake Biwa watershed; {{placebo_infeasible_share}}% of placebo borders admit no feasible map at the same tolerance, and among feasible borders the real border's cost sits at the {{placebo_pct}}th percentile. Projections to 2050 degrade ON and OFF maps alike. Inherited borders should be priced, not assumed — and this one is cheap, in an unusually benign location.

**Keywords:** electoral geography; redistricting; administrative boundaries; modifiable areal unit problem; functional connectivity; combinatorial optimization; Japan

## 1. Introduction

Political representation in single-member systems is delivered through space (Balinski & Young, 1982). The maps that allocate voters to districts are not drawn on a blank field: they are assembled inside pre-existing administrative territories — prefectures, municipalities, wards — whose boundaries were fixed for purposes quite unrelated to representation. In Japan the constraint is statutory: since the 1994 introduction of single-member districts for the House of Representatives, districts have been allocated and delimited within each prefecture, so that no district contains territory of two prefectures (Public Offices Election Act, 1950, as amended 2022).

This paper asks a simple geographic question that the redistricting literature — dominated by compactness metrics (Polsby & Popper, 1991), optimization formulations (Mehrotra et al., 1998; Ricca et al., 2013), and ensemble benchmarking (Tam Cho & Liu, 2016; DeFord et al., 2021; Herschlag et al., 2020) — has rarely isolated: *what does the administrative border cost?* By cost we mean the measurable deterioration in a districting plan's nonpartisan quality — population balance, compactness, municipal coherence, and retention of functional connectivity — that is attributable solely to forbidding districts to cross the prefectural line. Answering it requires a controlled comparison that statutory redistricting processes cannot provide: two maps produced by the same optimizer, the same constraints, and the same data, differing only in whether the border constraint is applied.

The Kyoto–Shiga prefectural boundary in Japan's Kinki region is an ideal case. The two prefectures share a roughly 118&nbsp;km border that is also the watershed of the Lake Biwa basin. The southern segment bisects a continuous urban fabric: Ōtsu (Shiga) adjoins Kyoto City, and the 2020 census records {{n_cross}} commuting and schooling trips crossing the border. The border is thus simultaneously a hard statutory line and a geographic fiction relative to the daily mobility field.

Our contributions are fourfold. First, we formalize the administrative-border constraint cost as a paired-optimization estimand and compute it at two spatial resolutions, bracketing the modifiable areal unit problem (MAUP; Openshaw & Taylor, 1979). Second, we couple the districting model to the commuting/schooling flow network, measuring how much functional connectivity each institutional map retains. Third, we embed the real border in a distribution of 200 matched placebo borders to test whether the constraint's cost is specific to this geography. Fourth, we evaluate temporal robustness under official municipal population projections to 2050. All data, code, and provenance are public and the pipeline regenerates every number end-to-end.

We emphasize scope. This is a measurement paper about a constraint, not a proposal to abolish prefectures or to redraw any particular statutory map, and it is deliberately nonpartisan: no variable related to party, candidate, incumbent, or vote share enters the model, the data, or the evaluation.

## 2. Study area, data, and methods

### 2.1 Study area

The combined Kyoto-fu/Shiga-ken region contains {{n_muni}} municipal units (36 in Kyoto including Kyoto City's 11 wards; 19 in Shiga) partitioned into {{n_small}} census small areas (totals may differ after merging 420 multi-part fragments of the same small area). The 2020 census population is {{region_pop}} — Shiga {{pop_shiga}}, Kyoto {{pop_kyoto}}. Statutory representation allocates 6 single-member districts to Kyoto and 3 to Shiga (K = 9).

### 2.2 Data and provenance

All inputs are official public sources, archived locally with SHA-256 manifests (Table T1): (i) e-Stat statistical GIS small-area boundaries (r2ka, JGD2011) with 2020 census population and household counts; (ii) 2020 Census Table 6-1 municipality×municipality commuting/schooling origin–destination (OD) matrices, at ward resolution for Kyoto City; (iii) IPSS 2023 municipal population projections to 2050; (iv) the statutory district definition from the Public Offices Election Act (e-Gov law API) and the Ministry of Internal Affairs district map. Adjacency is Queen-contiguity on small-area geometry; disconnected island/peninsula components and detached fragments of one census unit are handled by recorded bridging rules (docs/METHODS_DECISIONS.md). Because the two prefectures' r2ka boundaries do not coincide exactly, shared-boundary lengths are measured with a 30 m tolerance, and municipality-level edge weights aggregate small-area weights.

### 2.3 Optimization models

Units are assigned to K = 9 districts. Hard constraints: population per district within ±τ of the district mean (τ = 20%; sensitivity 10/15/30%), contiguity of every district, and — in Boundary-ON runs only — no district may contain both Kyoto (25) and Shiga (26) units. Objectives are a declared weighted sum of population deviation, boundary cut length (compactness), municipal splits (Level B only), severed OD flow, and — for M4 — projected deviation; full weights and seeds are in config/config.yaml.

- **M0** evaluates the current statutory map.
- **M1** minimizes population deviation + contiguity only.
- **M2** (Boundary ON) is the full objective under the prefectural constraint.
- **M3** (Boundary OFF) is identical without the constraint.
- **M4** adds projected-population deviation (S1 proportional downscaling; S2 ±10% centroid-drift sensitivity).
- **M5** minimizes reassigned population from the current map subject to feasibility — the minimal-intervention benchmark.

Level A is formulated exactly as a mixed-integer program and solved by CP-SAT (OR-Tools; Perron & Furnon, 2022) to the reported solver status and bounds on 55 municipal/ward units with rooted single-commodity-flow contiguity, 300–600 s limits, solution hints from M1, and recorded optimality gaps — we report bounds and never claim global optimality when the gap is open. Level B runs seeded simulated annealing with donor-connectivity checks and an incremental municipal-share closed form for severed flow on 11,978 small-area units, warm-started from the Level A solution. The same metrics module evaluates every assignment at both levels.

The core estimand is **Cost_border = L*(Boundary ON) − L*(Boundary OFF)**, the difference in achieved objective under otherwise identical settings, computed within level, τ, and seed.

### 2.4 Placebo borders

Two hundred internal placebo borders partition the municipality-level adjacency graph via random spanning-tree cuts, matched to the real border on two-sided population share (±10%), interface boundary length (±50%), and two-sided contiguity. Each border is re-optimized ON and OFF at Level A (60 s limits); the distribution of placebo costs benchmarks whether the real border's cost is generic.

## 3. Results

### 3.1 The current map

The statutory map (Figure F2) is contiguous but, reconstructed on 2020 census small-area populations, carries max |dev| = {{B_current_max_rel_dev}} and max/min ratio {{B_current_max_min_ratio}} — Kyoto-5 (279k) is at 0.63 of the district mean. This exceeds the experimental ±20% tolerance used throughout this study (real statutory max/min ≈ 2.0; ours {{A_current_max_min_ratio}} at Level A). Note this is a reconstruction property, not a legal judgment: the statutory map was drawn on the apportionment population basis and vintage in force at its delimitation, which differs from the 2020 census counts used here.

### 3.2 Constraint cost

At Level A, CP-SAT returns FEASIBLE (not OPTIMAL) incumbents within 300 s: M2-ON objective {{A_on_objective}} (best bound {{A_on_bound}}) against M3-OFF incumbent {{A_off_objective}}. The raw incumbent difference ({{cost_border_A}}) has the wrong sign for a nested minimization problem — every ON-feasible map is OFF-feasible, so L*_OFF ≤ L*_ON — which identifies it as a search artifact, not a cost. Because the validated ON assignment is itself an OFF-feasible solution of identical objective (invariant check I8), the OFF optimum is bounded above by the ON incumbent; the defensible interval for the true cost is therefore **[{{cost_border_A_lo}}, {{cost_border_A_hi}}] objective units** — at most {{cost_border_A_hi_frac}} of the incumbent objective scale — and its lower end is consistent with zero. A longer hinted OFF solve (900 s, warm-started from the ON incumbent) still returned no incumbent, so tighter identification is not claimed.

At Level B the corrected accounting is sharper: recorded annealing bests referred to pre-repair intermediate solutions; evaluated on the *final contiguous assignments*, the ON best-found map scores {{B_on_objective}} and the OFF run warm-started from that map retains exactly the same best ({{B_off_objective}}): **a best-found ON–OFF difference of {{cost_border_B}}** — removing the border constraint produces no improvement in the best-found small-area solution. The substantive explanation is visible in the maps (Figure F3) and in the flow network: the real border crosses only {{cross_od_real}} commuting/schooling trips, below *every* one of the 200 matched placebo borders (median {{cross_od_placebo_median}}, IQR {{cross_od_placebo_iqr}}; real border at the {{cross_od_real_pct}}th percentile). The administrative boundary broadly aligns with the Lake Biwa watershed, a geographic pattern consistent with the relatively weak functional connectivity observed across it: the observed cross-border flow indicates an unusually weak functional interface relative to the matched placebo borders. Compactness (mean PP {{B_on_polsby_popper_mean}} ON vs {{B_off_polsby_popper_mean}} OFF), municipal splits ({{B_on_n_split_munis}} vs {{B_off_n_split_munis}}), and severed intra-region flow ({{B_on_severed_flow_total}} vs {{B_off_severed_flow_total}} trips) differ only marginally.

### 3.3 Placebo benchmark

Across 200 matched placebo borders, {{placebo_infeasible_share}}% ({{placebo_n_feasible}} feasible of 200) yielded no feasible constrained map under the shared ±20% population tolerance — these are *no-incumbent-found* outcomes, not proven infeasibility; diagnostic reruns at up to 10× the iteration budget on a 12-border sample recovered none — persistent non-recovery under extended search, consistent with severe feasibility/search difficulty rather than a time-limit artifact, but not a proof of mathematical infeasibility (Table T5). Among the feasible borders the median constraint cost is {{placebo_cost_median}} (IQR {{placebo_cost_iqr}}; the lower tail extends slightly below zero, again an incumbent-time artifact on a nested minimization, not a negative cost), and the real border — priced by the identical heuristic solver — sits at the {{placebo_pct}}th percentile (Figure F6). The real border is therefore not merely inexpensive: it is in the cheapest decile of feasible alternatives *and* among the minority of lines that permit any feasible map.

### 3.4 Future robustness and minimal intervention

Under IPSS S1 projections the ON best-found map's max deviation reaches {{B_on_fut_S1_2050_maxdev}} by 2050 and first breaches τ in {{B_on_durability_S1}}; the OFF map breaches in {{B_off_durability_S1}}. M4 explicitly robust maps and the M5 minimum-intervention repair ({{M5_reassigned_pop}} people, {{M5_reassigned_pop_frac}} of the region, {{M5_reassigned_units}} small areas) are tabulated in T6.

### 3.5 Sensitivity and scale

The τ sweep (Table T4), seed replicates, and the Level A↔B scale comparison bound MAUP effects on the estimand; severed-flow results are robust to OD symmetrization/normalization choices (supplement).

## 4. Discussion

The prefectural border turns out to be cheap — and that is itself the finding, with an honest precision caveat. At municipality scale the true cost is only bounded: the interval [0, {{cost_border_A_hi}}] objective units is wide relative to incumbent scale because the OFF optimum resisted identification even at 900 s of hinted search, and we do not claim tighter. At census small-area scale the constrained and unconstrained best-found maps coincide exactly. The flow metrics are consistent with the low measured cost: the real border crosses only {{cross_od_real}} daily trips — fewer than all 200 matched placebo borders — and the border's broad alignment with the Lake Biwa watershed is consistent with this relatively weak functional connectivity, so the functional-geography cuts a border-respecting optimizer must make are almost the same ones an unconstrained optimizer chooses anyway. The placebo benchmark sharpens this: most matched alternative borders either admit no feasible constrained incumbent or are more expensive, so the actual line is unusually well-placed, not merely unobtrusive. For applied electoral geography the lesson is that border constraints are measurable design parameters to be priced, reported, and weighed — and that a constraint's headline legality can coexist with near-zero practical cost when the line broadly aligns with the underlying functional geography. The Ōtsu–Kyoto corridor is the exception the rule proves: it is the one place the border bisects a commuting field, and it is small enough to be accommodated.

Limitations are stated in docs/LIMITATIONS.md: municipal-share severed-flow is a closed-form approximation at Level B; SA results are heuristic without optimality bounds; Level A gaps remain open at time limits; placebo matching is statistical, not parametric-identification; and all analyses are nonpartisan by design — no electoral outcome is modeled.

## 5. Conclusion

We quantified the administrative-boundary constraint cost in electoral-district optimization for Kyoto–Shiga. The constraint is binding but cheap: the true cost is bounded within [0, {{cost_border_A_hi}}] objective units at municipality scale and is zero among best-found small-area maps, and the real border is functionally unusually benign — it crosses less commuting flow than every matched placebo border and permits a feasible map where most placebo lines yield no feasible incumbent. Projections show the constraint does not drive future imbalance, which arrives by 2040 for ON and OFF maps alike. District-evaluation practice — in Japan and wherever districts are built inside inherited jurisdictions — should report the border's price explicitly, because, as here, the answer may be near zero.

## References (APA 7th; verified; see manuscript/references.bib)

Balinski, M. L., & Young, H. P. (1982). *Fair representation: Meeting the ideal of one man, one vote*. Yale University Press.

DeFord, D., Duchin, M., & Solomon, J. (2021). Recombination: A family of Markov chains for redistricting. *Harvard Data Science Review, 3*(1). https://doi.org/10.1162/99608f92.eb30390f

Herschlag, G., Kang, H. S., Luo, J., Graves, C. V., Bangia, S., Ravier, R., & Mattingly, J. C. (2020). Quantifying gerrymandering in North Carolina. *Statistics and Public Policy, 7*(1), 30–38. https://doi.org/10.1080/2330443X.2020.1796400

Mehrotra, A., Johnson, E. L., & Nemhauser, G. L. (1998). An optimization-based heuristic for political districting. *Management Science, 44*(8), 1100–1114. https://doi.org/10.1287/mnsc.44.8.1100

Ministry of Internal Affairs and Communications (Japan). (2020). *2020 population census, Table 6-1: Commuting and schooling origin–destination by municipality* [Data set]. e-Stat.

Ministry of Internal Affairs and Communications (Japan). (2020). *Statistical GIS boundary data (r2ka small areas, JGD2011)* [Data set]. e-Stat.

National Institute of Population and Social Security Research. (2023). *Municipal population projections, 2020–2050* [Data set].

Openshaw, S., & Taylor, P. J. (1979). A million or so correlation coefficients: Three experiments on the modifiable areal unit problem. In N. Wrigley (Ed.), *Statistical applications in the spatial sciences* (pp. 127–144). Pion.

Perron, L., & Furnon, V. (2022). *OR-Tools CP-SAT solver* [Computer software]. Google.

Polsby, D. D., & Popper, R. D. (1991). The third criterion: Compactness as a procedural safeguard against partisan gerrymandering. *Yale Law & Policy Review, 9*, 301–353.

Public Offices Election Act, Law No. 100 of 1950, as amended through 2022; Annex 1 (single-member districts) (Japan). e-Gov law database.

Ricca, F., Scozzari, A., & Simeone, B. (2013). Political districting: From classical models to recent approaches. *Annals of Operations Research, 204*, 271–299. https://doi.org/10.1007/s10479-012-1267-2

Tam Cho, W. K., & Liu, Y. Y. (2016). Toward a talismanic redistricting tool: A computational method for identifying extreme redistricting plans. *Election Law Journal, 15*(4), 351–366. https://doi.org/10.1089/elj.2016.0384

## Figures (separate files)

- F1 study area; F2 current statutory districts; F3 best-found ON vs OFF maps; F4 cross-prefecture OD network; F5 metric comparison; F6 placebo cost distribution; F7 future robustness.

## Tables (separate files)

- T1 data sources; T2 current-map metrics; T3 model comparison ON/OFF; T4 τ sensitivity; T5 placebo summary; T6 future robustness and minimal intervention.
