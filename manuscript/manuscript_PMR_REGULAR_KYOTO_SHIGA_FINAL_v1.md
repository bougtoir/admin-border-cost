# One administrative territory, multiple functional geographies: pricing territorial congruence in Kyoto–Shiga


## Abstract

Governments organize many public functions inside inherited territorial containers, yet the cost of requiring those functions to respect the same boundary is rarely measured. This paper defines the alignment opportunity cost of a boundary for a public function and prices it across electoral representation, healthcare access, and education access on the Kyoto–Shiga prefectural boundary in Japan. Aggregate boundary costs are small in every domain — bounded at [0, 532,293] objective units for representation and under +0.006 km mean population-weighted cost for every access function — but the residual burden concentrates in 11 border municipalities, whose worst-decile access gap narrows under an unconstrained counterfactual. Territorial congruence should therefore be evaluated at both aggregate and local scales. Where average opportunity cost is low but local penalties are concentrated, selective territorial permeability may be a more relevant place-based design question than wholesale territorial redesign.

**Keywords:** place-based strategy; territorial congruence; administrative boundaries; selective permeability; public value

## 1. Introduction

Governments organize many functions inside inherited territorial containers. Schools, clinics, electoral districts, and administrative routines are all run within boundaries drawn for institutional histories long past. Under demographic and fiscal pressure, reform debates often ask whether those containers should be retained, consolidated, or replaced. A prior question is rarely measured: what does requiring each function to respect the same boundary actually cost?

This question matters for place-based strategy because the answer is not obvious in either direction. Inside-out strategy reasons from the container outward — the prefecture or municipality is the unit of planning, and services are configured to fit it. Outside-in strategy reasons from functions inward — the geography of demand and provision should determine where administrative lines matter. Both stances can go wrong. Insisting on congruence where it is cheap buys legibility at little price; insisting on it where it is expensive destroys value silently; and relaxing boundaries where measured cost is already low yields nothing. Harmonization is not self-justifying in either direction. What is missing from most territorial debates is a price — a measured opportunity cost of requiring congruence, computed function by function.

This paper supplies that measurement logic and demonstrates it on a single unusually informative boundary. For each public function s with plan space F and objective L, we define the alignment opportunity cost of boundary B for function s as the difference between the best achievable objective under Boundary ON and Boundary OFF, where Boundary ON confines the function's design to plans that respect an inherited boundary set B and Boundary OFF removes that restriction with all else held constant. The estimand prices congruence for one function at a time, in that function's own units, without presuming that different functions should have different territories.

We apply this protocol to the boundary between Kyoto-fu and Shiga-ken, Japan — a pair chosen because the two prefectures are unusually close institutionally and functionally. Their government offices are the nearest such pair in Japan (approximately 10.5 km by geodesic distance, rank 1 of 1,081 prefectural pairs). The border bisects a dense field of daily cross-prefecture movement: 79,466 commuting and schooling trips cross it in the 2020 census, and Kyoto is the largest external destination for 18 of 19 Shiga municipalities. The same boundary is a hard statutory constraint for one function — single-member electoral districts may not straddle prefectural lines — and an invisible but potentially binding default for everyday service access.

Three domains are measured. For electoral representation we solve matched districting problems at two resolutions (55 municipal/ward units; 11,978 census small areas) with and without the no-straddle constraint, benchmarked against 200 statistically matched placebo borders. For healthcare and education access we use official national facility registers — MLIT P04-20 medical institutions and P29-21 schools — and assign every census small-area demand unit to its nearest supply point by geodesic distance, once with assignments confined to the same prefecture and once unconstrained, holding everything else constant. Hospital and general-clinic tiers and elementary and junior-high levels are analysed separately, because pooling tiers or levels would not measure a real choice.

The completed results overturn the most convenient story in both directions. The aggregate price of congruence is small for every measured function: the electoral boundary cost is bounded at [0, 532,293] objective units at municipality scale with solver status FEASIBLE (not OPTIMAL) and a best-found cost of exactly zero at small-area scale; the mean population-weighted access opportunity cost of the boundary is +0.0046 km for hospitals, +0.0005 km for general clinics, +0.0060 km for elementary schools, and +0.0042 km for junior-high schools. Under Boundary OFF, only 0.11–0.20% of the population would be assigned across the prefecture line. Yet the cost is not uniformly trivial. The measured burden is spatially concentrated: in the 11 border municipalities, the worst-decile access gap over interior areas narrows under Boundary OFF — from 0.75 km to 0.28 km for elementary schools — and individual border small areas gain up to roughly 14–17 km of avoided detour at junior-high and elementary level.

The paper makes four contributions. First, a measurement contribution: territorial congruence is operationalized as a function-by-function opportunity cost with declared estimands and declared solver status — measurable, not asserted. Second, a scale-and-distribution contribution: a near-zero average boundary cost does not imply zero territorial consequence; the distribution of cost, not only its mean, is the object of measurement. Third, a place-based strategy contribution: the design problem is not simply retain versus redraw the boundary; where aggregate cost is low but marginal burdens are concentrated, the live option is selective territorial permeability — retaining the administrative container while permitting targeted cross-boundary use for specific functions and locations. We present permeability as a design implication to evaluate, not a tested intervention. Fourth, a public-value contribution: aggregate efficiency and local distributive burden are separated explicitly, so that small averages are neither read as vindication of inherited boundaries nor suppressed as uninteresting nulls.

The remainder of the paper develops the framework and literatures (Section 2), formalizes the estimand (Section 3), introduces the Kyoto–Shiga setting (Section 4), describes data and methods (Section 5), reports results (Section 6), discusses implications for place-based strategy (Section 7), states limitations prominently (Section 8), and concludes (Section 9).

## 2. Place-based strategy and territorial congruence

Place-based strategy treats place as a spatial locus of interdependent public services rather than a single administrative unit. In public-service-ecosystem terms, the same lived place hosts overlapping service systems — schooling, health care, representation, mobility — each with its own functional geography (Osborne, Radnor, & Nasi, 2013; Radnor, Osborne, Kinder, & Mutton, 2014; Osborne, 2018). Public service logic emphasizes that value is created at the point of use in these systems, so the boundaries managers draw around services are themselves value-relevant design choices (Osborne, Radnor, & Strokosch, 2016; Alford, 2016).

Yet administrative containers are rarely chosen by those who operate inside them. Prefectural and municipal boundaries in Japan, as elsewhere, are institutional inheritances whose persistence is explained by path dependence and coordination costs, not by current functional fit (Brenner, 2004). The public-management literature on inter-municipal cooperation shows that jurisdictions routinely respond to the mismatch not by redrawing boundaries but by layering cooperative arrangements over them — shared services, joint delivery, cross-jurisdiction contracting — whose cost savings depend on service characteristics, governance structure, and transaction costs (Hulst & van Montfort, 2007; Bel & Warner, 2015; Ansell & Gash, 2008). What that literature does not usually supply is a measurement of what the container costs in the first place: cooperation is motivated by visible friction, not by a priced estimand.

This paper defines territorial congruence as the requirement that multiple public functions respect the same inherited administrative boundary. Congruence is a variable, not a fact of nature: it can be imposed, relaxed selectively, or abolished, and each choice has a function-specific price. Measuring that price requires a counterfactual — the same function designed with and without the boundary restriction — which is what the framework in Section 3 formalizes. The approach is complementary to the accessibility and spatial-equity literature, which measures realized access to services (Hansen, 1959) but rarely isolates the contribution of the administrative boundary itself.

We deliberately avoid presuming that different functions should have different territories. The claim is weaker and more operational: the cost of forcing functions into the same territory is measurable per function, and where it lands — aggregate or locally concentrated — is itself evidence for strategy.

## 3. Framework: pricing territorial congruence

For a public function s, let F be its feasible set of service plans and L a declared objective (lower is better). Requiring plans to respect a boundary set B restricts the feasible set. Figure 1 shows the framework and the design decision it produces. Define

C(B) = L(Boundary ON) − L(Boundary OFF),

where the first term is the minimized objective over the boundary-respecting feasible set and the second is the minimum over the unrestricted set, computed with identical demand geography, supply set, distance metric, and all other settings. This difference is non-negative by construction: the alignment opportunity cost of boundary B for function s.

Three properties of this estimand matter for what follows. First, honesty of status: where the design problem requires optimization, the minimized objective may only be bounded, and the bound's status (FEASIBLE incumbent versus proven OPTIMAL) is part of the result, not a footnote. Where the design rule is a closed-form argmin — as in uncapacitated nearest-facility assignment — no optimality gap exists and none should be implied. Second, distribution beyond the mean: the same aggregate boundary cost can arise from a uniform small penalty or a concentrated border penalty. We therefore report, alongside the mean, the quantiles, the share of demand reassigned across the boundary under OFF, and worst-decile gaps between border-adjacent and interior demand units. Third, function specificity: the cost is expressed in function s's own objective units. Costs across functions are comparable in sign and profile, not in raw magnitude; the cross-function comparison is descriptive, never a welfare ranking.

Selective territorial permeability enters as the design implication of a particular cost profile: where the aggregate cost is low but the burden is concentrated in identifiable border locations for identifiable functions, the strategy question shifts from "should the boundary move?" to "which crossings should be permitted?" This is a hypothesis-generating implication, not a tested policy; whether permeability improves value net of coordination, legal, fiscal-transition, and transaction costs is unmeasured here and is stated as such.

## 4. Empirical setting: Kyoto–Shiga

Kyoto-fu and Shiga-ken share a boundary that is short, densely inhabited, and institutionally salient. The two prefectural government offices, in Kyoto City and Otsu City, are approximately 10.5 km apart by geodesic distance (10.45188 km) — the closest pair among all 1,081 unordered pairs of Japan's 47 prefectural offices (rank 1). The border region spans the southern shore of Lake Biwa and the Kyoto urban fringe; Otsu and several neighbouring Shiga municipalities function partly as Kyoto commuter territory.

Figure 2 maps the setting: the prefectural boundary, the 11,978 small-area demand units, and the facility locations used below. Functional entanglement is measurable rather than rhetorical. In the 2020 census, 79,466 daily commuting and schooling trips cross the Kyoto–Shiga boundary; Kyoto is the largest external destination for 18 of 19 Shiga municipalities, and Shiga-to-Kyoto trips account for 7.2% of all trips originating in Shiga — 65.5% of Shiga's out-of-prefecture trips. An honest comparator keeps the claim calibrated: the Kyoto–Osaka boundary carries 176,231 daily cross-prefecture trips, more than double, so Kyoto–Shiga is not the most integrated border in Japan. Its sharpness comes instead from the combination of a hard statutory constraint, extreme institutional proximity, and a small prefecture whose functional reach points overwhelmingly at one neighbour. The normalized border-crossing share used in the electoral study (S ≈ 1.99%) is itself moderate — below the Osaka–Hyogo table maximum of 2.91% — which is precisely why it is a useful test: if an inherited boundary is costly, the cost should be measurable even where entanglement is only middling.

The same boundary is therefore (i) legally binding inside one public function — House-of-Representatives single-member districts may not straddle prefectural boundaries under the Public Offices Election Act — and (ii) an unpriced default inside everyday service access, since residents are formally free to cross it but service planning, school catchments, and healthcare administration are organized prefecture by prefecture.

## 5. Data and methods

Table 1 summarizes the functions, data, demand and supply units, ON/OFF rules, and objectives.


### 5.1 Electoral representation

The electoral analysis prices the statutory no-straddle rule inside a spatial districting problem (the companion electoral study reports the full specification and results; companion manuscript in preparation) with legally grounded objectives (population equality within statutory tolerance, contiguity, and compactness). Two resolutions are used: Level A (55 municipal/ward units: 36 in Kyoto including Kyoto City's 11 wards, and 19 in Shiga) and Level B (11,978 census small areas). For each level, the constrained problem (Boundary ON: districts confined within a single prefecture) is solved against an identical unconstrained problem (Boundary OFF), with K = 9 districts (Kyoto 6, Shiga 3) in both. Because large combinatorial problems admit bounded rather than proven-optimal solutions, solver status is reported explicitly; negative incumbent differences are treated as search artefacts, not costs. The real border is additionally benchmarked against 200 statistically matched placebo borders — synthetic prefecture partitions of comparable geometry — of which 78 yielded feasible ON/OFF incumbent pairs and 122 yielded no feasible constrained incumbent (not proven infeasible).

### 5.2 Healthcare access

Supply is the MLIT National Land Numerical Information P04-20 medical-institution register (2020 vintage; per-prefecture files P04-20_25 and P04-20_26, SHA-256 logged). Following the register's classification (P04_001), hospitals (n = 221; 164 Kyoto, 57 Shiga) and general clinics (n = 3,584; 2,505 Kyoto, 1,079 Shiga) are analysed as separate tiers; dental clinics are excluded. Demand is the canonical 11,978 census small-area units with 2020 population weights (total 3,991,697); multi-fragment small areas are merged on their census key and weighted by population. Each demand unit's representative point is the population-weighted centroid of its fragment representative coordinates (JGD2000); 1,043 zero-population units are retained with zero weight. For each tier, Boundary ON assigns every unit to its nearest same-prefecture facility by WGS84 geodesic distance; Boundary OFF removes the prefecture restriction with everything else identical. The assignment is a closed-form argmin — no solver, no seed, no optimality gap. Demand-side weights use total population; a household-count (SETAI) sensitivity is reported. No capacity attribute exists in P04, so the analysis is uncapacitated by design and declared as such.

### 5.3 Education access

Supply is the MLIT P29-21 school register (2021 data year, the vintage closest to the 2020 census), filtered to Kyoto and Shiga and to open, publicly operated schools: 571 elementary and 256 junior-high schools. Levels are analysed separately — elementary demand is assigned only to elementary schools and junior-high demand only to junior-high schools — because a pooled assignment would not measure valid access cost for either level. Demand geography, boundary encoding, distance metric, and the ON/OFF pairing are identical to §5.2. Because small-area tabulations do not publish school-age population, the demand weight is total population, with the household-count sensitivity; this proxy is stated as a limitation rather than adjusted post hoc.

### 5.4 Cross-function comparison

The three domains share a logic — the same boundary toggled on and off under otherwise identical settings — but not a common unit. The electoral objective is a weighted districting criterion; access objectives are geodesic kilometres. Comparison therefore proceeds on direction, normalized structure (cross-boundary share; border-versus-interior concentration), and qualitative profile, never on raw magnitudes pooled across objectives.

## 6. Results

### 6.1 Electoral representation

At Level A (55 municipal/ward units), the true boundary cost is bounded at [0, 532,293] objective units; solver status is FEASIBLE, not OPTIMAL, so the cost may be anywhere in that interval including zero. At Level B (11,978 small areas), the best-found ON and OFF objectives are identical at 0.6245294675 — a best-found boundary cost of exactly zero. The real border is also cheap relative to counterfactual borders: it crosses 39,733 daily trips, fewer than all 200 matched placebo borders, and the placebo median normalized crossing is ≈ 0.0647 (IQR 0.0222–0.0727). In 122 of 200 placebos no feasible constrained incumbent was found at all — meaning most synthetic borders make the statutory problem harder, not easier. The electoral boundary cost is therefore small and possibly zero; we report it as bounded, not as high.

### 6.2 Healthcare access

For hospitals, mean population-weighted access distance is 1.6306 km under Boundary ON and 1.6260 km under OFF — an alignment opportunity cost of +0.0046 km, about five metres. The distribution is nearly unchanged (median 1.006 vs 1.004 km; p95 5.389 vs 5.389 km), and only 45 of 11,978 units change assignment, all near the border; the largest single-unit gain is +8.38 km. For general clinics the cost is smaller still: +0.0005 km on a mean of 0.453 km, with 41 units reassigned and a maximum unit gain of +3.08 km. Under OFF, 0.17% of population is assigned across the prefecture for hospitals and 0.11% for clinics. Costs concentrate in the 11 border municipalities: their mean hospital access penalty under ON is +0.0143 km (interior: zero), and the border–interior gap in the worst decile narrows from 0.66 km (ON) to 0.46 km (OFF); the corresponding clinic gap narrows 0.22 to 0.17 km.

### 6.3 Education access

Elementary schools: mean access distance 0.7521 km (ON) vs 0.7461 km (OFF), a boundary cost of +0.0060 km; 70 units change assignment, all in or immediately adjoining the border region (67 in the 11 border municipalities), with a maximum unit gain of +14.11 km; OFF cross-boundary share is 0.20% of population. Junior-high schools: 1.1458 km (ON) vs 1.1415 km (OFF), +0.0042 km; 81 units reassigned (79 in the border municipalities); maximum unit gain +16.55 km; cross-boundary share 0.19%. The border tail is where the boundary binds: the worst-decile border–interior gap narrows from 0.75 km to 0.28 km for elementary and from 0.57 km to 0.45 km for junior-high when the boundary is relaxed. Six border municipalities contain units reassigned across the line for elementary access, and nine for junior-high.

### 6.4 Cross-function pattern

Table 2 summarizes the completed results across functions, and Figure 3 plots the mean opportunity costs. Across representation, healthcare access, and education access, the aggregate cost of the inherited boundary is small; what varies is where that cost appears and how concentrated it is. Ordered by mean access cost the functions form a tight band — clinic +0.0005 km, junior-high +0.0042 km, hospital +0.0046 km, elementary +0.0060 km — while their tails differ: unit-level gains reach 3–17 km depending on function, and the border–interior worst-decile gap reduction ranges from 0.05 km (clinic) to 0.46 km (elementary) (Figure 4). Sensitivity checks — household weights, travel-time proxies, tier definitions, and the declared capacity-neutrality — leave the conclusions unchanged (Table 3). The evidence supports function-specificity in the distribution of cost, not in its average magnitude: the boundary is nearly costless on average everywhere measured, and differently concentrated at the margin.

## 7. Discussion

**Small average cost does not mean zero territorial consequence.** Every measured mean is near zero, yet the reassigned units are real: 45–81 small areas per function, clustered in a handful of border municipalities, with unit-level gains an order of magnitude larger than any mean. An aggregate-first reading would miss them; a distribution-aware reading finds them immediately.

**Mismatch is not inefficiency.** The Kyoto–Shiga border exhibits every visible signature of administrative–functional mismatch — closest prefectural offices in the country, tens of thousands of daily crossings, one prefecture oriented toward the other — and yet its measured price is small in all three domains. Visible entanglement did not imply inefficiency, because a boundary's cost is determined by whether alternatives are actually better, not by whether flows cross the line. This is the measurement the framework exists to supply.

**Aggregate efficiency vs local distributive burden.** The results separate two public-value questions that territorial debates often fuse: whether the boundary is expensive overall (it is not) and whether it is expensive for a particular set of places (it is, for the border tail). Public value may depend not only on whether a boundary exists, but on where and for which functions permeability is permitted (Moore, 1995; Bozeman, 2007).

**Selective permeability as a design problem.** Where average opportunity cost is low, wholesale territorial redesign buys little; where border penalties are concentrated, a targeted relaxation — mutual recognition of cross-boundary school attendance, cross-prefecture referral or catchment exceptions — addresses the measured burden without disturbing the container. We offer selective permeability as the strategy-design implication of the measured cost profile, not as a tested policy: its coordination, legal, fiscal-transition, and transaction costs are unmeasured here, and current Japanese healthcare and school governance may not permit all such arrangements.

**Why low averages still justify examining border exceptions.** For place-based strategy, the operative question the results pose is not "should the boundary move?" but "which crossings should be permitted?" A place-based public-service ecosystem need not be represented by a single common territorial boundary; however, the evidence here suggests the main management problem may be where to allow permeability rather than where to redraw the entire map.

## 8. Limitations

The healthcare and education analyses are access-opportunity analyses, not service-system optimization. They are uncapacitated (no beds, specialties, enrollment capacities, or assignment rules are modelled, because the official registers carry no such attributes and inventing them is not permitted); nearest-facility based (no patient choice, referral networks, or actual school catchments); and geodesic rather than road-network travel time (the frozen sensitivity converts distance to time at stated speeds — 40 km/h road and 4 km/h walk proxies — which leaves the conclusions unchanged). Education demand is weighted by total population (with a household-count sensitivity), because official small-area tabulations do not publish school-age population. Coordination, legal, fiscal, and institutional costs of cross-boundary provision are unmeasured throughout. The evidence is one Japanese border pair, chosen for sharpness, not representativeness. Finally, the electoral objective scale is not commensurate with access kilometres: cross-function comparison is descriptive and is not a common-unit ranking.

## 9. Conclusion

Territorial congruence should be measured at both the aggregate and the local level before governments infer either that inherited boundaries are inefficient or that they are harmless. On the Kyoto–Shiga boundary, requiring representation, healthcare access, and education access to respect the same inherited line costs almost nothing on average — and measurably burdens a thin band of border municipalities. Where average boundary cost is low but local penalties are concentrated, selective permeability may be more relevant than wholesale redrawing: keep the container, and let the measurement say where it should be allowed to leak.

## Acknowledgements

None.

## Data availability

All inputs are public official statistics (2020 Population Census small-area boundaries and population, Statistics Bureau of Japan; MLIT National Land Numerical Information P04-20 and P29-21; 2020 Census commuting/schooling OD). Code, processed inputs, run logs, and the prospective analysis freeze are provided in the reproducibility bundle; acquisition URLs, versions, UTC timestamps, and SHA-256 checksums are recorded in the provenance ledger.

## References

Alford, J. (2016). Co-production, interdependence and publicness: Extending public service-dominant logic. Public Management Review, 18(5), 673–691. https://doi.org/10.1080/14719037.2015.1111659

Ansell, C., & Gash, A. (2008). Collaborative governance in theory and practice. Journal of Public Administration Research and Theory, 18(4), 543–571. https://doi.org/10.1093/jopart/mum032

Bel, G., & Warner, M. E. (2015). Inter-municipal cooperation and costs: Expectations and evidence. Public Administration, 93(1), 52–67. https://doi.org/10.1111/padm.12104

Bozeman, B. (2007). Public values and public interest: Counterbalancing economic individualism. Georgetown University Press.

Brenner, N. (2004). New state spaces: Urban governance and the rescaling of statehood. Oxford University Press.

Hansen, W. G. (1959). How accessibility shapes land use. Journal of the American Institute of Planners, 25(2), 73–76. https://doi.org/10.1080/01944365908978307

Hulst, J. R., & van Montfort, A. J. G. M. (Eds.). (2007). Inter-municipal cooperation in Europe. Springer.

Ministry of Internal Affairs and Communications. Public Offices Election Act (Kōshoku Senkyo Hō), Act No. 100 of 1950, as amended.

Ministry of Land, Infrastructure, Transport and Tourism. National Land Numerical Information: Medical Institutions (P04, 2020 vintage); School Locations (P29, 2021 vintage). https://nlftp.mlit.go.jp/ksj/

Moore, M. H. (1995). Creating public value: Strategic management in government. Harvard University Press.

Osborne, S. P. (2018). From public service-dominant logic to public service logic: Are public service organizations capable of co-production and value co-creation? Public Management Review, 20(2), 225–231. https://doi.org/10.1080/14719037.2017.1350461

Osborne, S. P., Radnor, Z., & Nasi, G. (2013). A new theory for public service management? Toward a (public) service-dominant approach. American Review of Public Administration, 43(2), 135–158. https://doi.org/10.1177/0275074012466935

Osborne, S. P., Radnor, Z., & Strokosch, K. (2016). Co-production and the co-creation of value in public services: A suitable case for treatment? Public Management Review, 18(5), 639–653. https://doi.org/10.1080/14719037.2015.1111927

[Author]. (in preparation). The administrative boundary constraint in electoral districting: The Kyoto–Shiga case. Manuscript in preparation; bibliographic details withheld for double-anonymous review.

Radnor, Z., Osborne, S. P., Kinder, T., & Mutton, J. (2014). Operationalizing co-production in public services delivery: The contribution of service blueprinting. Public Management Review, 16(3), 402–423. https://doi.org/10.1080/14719037.2013.848923

Statistics Bureau of Japan. (2020). 2020 Population Census: Small-area boundaries and population (r2ka25, r2ka26); commuting and schooling origin–destination tabulations. https://www.e-stat.go.jp/

## Figures and tables

Figure 1. Conceptual framework: one inherited boundary, multiple functions, and the selective-permeability decision.

Figure 2. Kyoto–Shiga case geography: the prefectural boundary, small-area demand centroids, and facility locations.

Figure 3. Mean population-weighted access opportunity cost of the boundary by function (km; electoral shown separately as bounded objective units).

Figure 4. Localized burden in the 11 border municipalities: worst-decile border–interior access gap under Boundary ON versus OFF, by function.

Table 1. Functions, datasets, demand units, supply units, ON/OFF rule, and objective.

Table 2. Cross-function summary of completed results.

Table 3. Sensitivity and robustness summary.
