# FINAL WORDING AUDIT — evidentiary-strength corrections (wording only)

No optimization, simulation, table, or figure data changed. All canonical
numerical results preserved verbatim: Level A interval [0, 532,293]; Level A
status FEASIBLE (not OPTIMAL); Level B best-found difference 0; cross-OD
39,733 vs placebo median ~99,420 (real below all 200); placebo 200/78/122;
feasible placebo cost median 0.0647; real-border cost 10th percentile.

## Changes (manuscript_text.md unless noted)

1. Highlights bullet
   - OLD: "...consistent with a real topographic divide."
   - NEW: "...a pattern consistent with the border's broad alignment with the
     Lake Biwa watershed."
   - REASON: "real topographic divide" asserted an unmeasured ontological
     claim; rephrased to alignment + consistency.

2. Results §3.2 (functional-interface sentence)
   - OLD: "The line follows the Lake Biwa watershed, and the commuting field
     is already split along it — the border coincides with a genuine
     functional divide rather than cutting through one."
   - NEW: "The administrative boundary broadly aligns with the Lake Biwa
     watershed, a geographic pattern consistent with the relatively weak
     functional connectivity observed across it: the observed cross-border
     flow indicates an unusually weak functional interface relative to the
     matched placebo borders."
   - REASON: removed "genuine functional divide"; functional-interface claim
     now explicitly grounded in the measured 200-border placebo comparison.

3. Discussion §4
   - OLD: "The flow metrics explain why the cost can be so low: the real
     border crosses 39,733 daily trips — fewer than all 200 matched placebo
     borders — because the inherited line largely coincides with the Lake
     Biwa watershed, so the functional-geography cuts a border-respecting
     optimizer must make are almost the same ones an unconstrained optimizer
     chooses anyway."
   - NEW: "The flow metrics are consistent with the low measured cost: the
     real border crosses only 39,733 daily trips — fewer than all 200 matched
     placebo borders — and the border's broad alignment with the Lake Biwa
     watershed is consistent with this relatively weak functional
     connectivity, so the functional-geography cuts a border-respecting
     optimizer must make are almost the same ones an unconstrained optimizer
     chooses anyway."
   - REASON: removed causal "because ... watershed"; recast as
     consistency/association between alignment and observed weak
     connectivity. The optimizer-side clause is a statement about the
     optimization maps, retained as supported.

4. Discussion §4 (lesson sentence)
   - OLD: "...when the line tracks real geography."
   - NEW: "...when the line broadly aligns with the underlying functional
     geography."
   - REASON: "tracks real geography" implied established functional reality;
     replaced with alignment framing.

5. Cover letter
   - OLD: "the constraint's measured cost is within solver noise, and the
     placebo analysis explains why — most matched alternative borders are
     infeasible or costlier"
   - NEW: "the constraint's best-found cost is zero at small-area scale and
     bounded at municipality scale, and the placebo benchmark points the same
     way — most matched alternative borders admit no feasible constrained
     incumbent or are costlier"
   - REASON: removes the over-broad "within solver noise" and the causal
     "explains why"; aligns with corrected Level-A interval and Level-B
     best-found wording already established in the forensic revision.

## Terms searched and cleared
- "genuine functional divide" / "natural divide" / "true functional divide":
  none remain.
- "watershed": remaining uses are descriptive (the border "is also the
  watershed of the Lake Biwa basin" — geographic fact) or
  alignment/consistency framing; no causal watershed claim remains.
- "because" linking watershed to results: none remain (remaining "because"
  instances are mathematical-logical: CP-SAT nesting argument, r2ka
  boundary tolerance, "because, as here" rhetorical use).
- "explain(s)": no causal watershed use remains.
- "tracks real geography", "geographically optimal", "naturally aligned":
  none remain.
- "real topographic divide": removed.

## Confirmation checklist
- [x] no unsupported causal watershed statement remains
- [x] "genuine functional divide" and equivalents absent
- [x] watershed language is alignment/association/consistency only
- [x] functional-interface language reflects the placebo comparison
- [x] Abstract/Results/Discussion/Conclusion/Highlights/cover letter consistent
- [x] no numerical value changed
- [x] no table or figure data changed (F6 annotation already fixed in the
      finishing pass: "borders with no feasible incumbent")
- [x] forensic corrections intact (interval reporting, best-found zero,
      no-incumbent phrasing)
- [x] CP-SAT not described as proving global optimum
- [x] Level-B zero remains explicitly a best-found difference
- [x] placebo no-incumbent outcomes not called proven infeasible
- QC: 36/36 checks pass after rebuild; manuscript.docx and
  manuscript_inline.docx regenerated with all placeholders filled.
