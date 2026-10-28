# PMR Kyoto–Shiga Extension — Function Selection Freeze

Date: 2026-10-05 (UTC). Status: **FROZEN before any new analysis.**
Purpose: decide, on relevance/data grounds alone (not on results — none
exist yet), which additional public functions the PMR paper may price for
the Kyoto–Shiga boundary. At most two additional functions may be
selected. Selection must not be revisited based on favorable or
unfavorable results.

## 1. Decision rule

A candidate function is eligible only if: (a) an official/public facility
or service geography exists for both Kyoto and Shiga at usable spatial
resolution; (b) a measurable access/equity objective can be stated;
(c) a Boundary ON/OFF formulation is definable (Boundary ON: prefecture
of residence constrains assignment; OFF: nearest/least-cost assignment
ignores the prefectural line); (d) the pipeline is reproducible from
public data with the same provenance rules as the electoral study.

## 2. Candidate assessment

| Candidate function | Policy relevance | Official/public data availability | Spatial resolution | Measurable objective | Boundary ON/OFF formulation | Accessibility/equity outcomes | Major limits | Reproducibility |
|---|---|---|---|---|---|---|---|---|
| Electoral representation | High | Done (canonical) | Municipal + small area | Weighted districting objective | No-straddle rule on/off | Population equality, severed commuting flow | — | Validated end-to-end |
| **Healthcare access (SELECTED)** | High — aging region, cross-border care documented in Keiji corridor | MLIT National Land Numerical Information P04 (medical/welfare facilities); hospital capacity tiers definable | Facility points + 11,978 small areas | Population-weighted travel distance/time to nearest tiered facility | ON: assignment restricted to same-prefecture facilities; OFF: unrestricted | Mean/max distance, population beyond threshold, small-area disparity | Capacity/queueing unobserved; road-network travel time requires assumed speeds | High — public facility points + existing geography/OD assets |
| **Education access (SELECTED)** | High — school catchment is a canonical municipal boundary function | MLIT National Land Numerical Information school dataset (public elementary/junior-high school points) | School points + small areas | Population-weighted distance to assigned school under capacity-neutral proxy | ON: catchment confined to prefecture; OFF: nearest-school assignment | Distance distribution, municipal splits, equity gap between border vs interior areas | Private schools, school choice, and capacity not modeled — stated as limits | High |
| Emergency-service access | Medium-high | Fire stations less standardized in public releases; ambulance/hospital interaction complex | Facility points | Response-time proxy by distance | Same ON/OFF pattern | Coverage thresholds | Statutory dispatch already cross-border in places — ON constraint weaker realism | Medium |
| Administrative-service access | Medium | City/ward office locations derivable from official registers | Office points | Distance to own-prefecture service office | ON: must use own-prefecture office | Distance gap | Administrative services not spatially exclusive — weak realism | Medium |
| Transport accessibility | Medium | Rail stations and timetables partially public; road network licensing frictions | Station points | Network distance to rail access | Prefecture line irrelevant to stations — ON/OFF formulation does not map naturally onto the boundary constraint | — | **Boundary ON/OFF does not apply cleanly** (rail network already crosses the line); unsuitable for the paired-estimand design | Medium |

## 3. Selection (frozen)

**Selected (2):** healthcare access; education access.
Rationale: strongest combination of statutory/organizational boundary
relevance, official point-level data availability inside the same
Kyoto–Shiga geography, and a clean Boundary ON/OFF estimand that mirrors
the electoral design. Selection was made on feasibility criteria only;
no result was observed or computed.

**Not selected:** emergency services (boundary-constraint realism weak —
dispatch already interoperates across the line); administrative services
(same weakness); transport accessibility (the rail network is not
partitioned by the prefecture, so a meaningful Boundary ON does not exist
and the paired estimand is not definable).

## 4. Guardrails

- No function substitution after this freeze except as explicitly
  labelled exploratory.
- Null or mixed results are reported, not swapped out.
- If official data prove unavailable or unusable at acquisition time,
  the affected function reverts to conceptual discussion only; the paper
  falls back to the validated electoral worked example.
- All new data follow `docs/PMR_KYOTO_SHIGA_NEW_DATA_PROVENANCE.md` and
  the raw-data persistence rules (original snapshot, SHA-256 ledger,
  acquisition metadata).
