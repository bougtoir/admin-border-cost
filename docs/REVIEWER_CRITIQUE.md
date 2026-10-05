# Reviewer-style critique (self-review before packaging)

Anticipated objections and our answers/status:

1. **"Constraint cost confounds objective weights."** ON/OFF share identical
   weights, τ, seeds, solver — the only difference is the constraint set;
   sensitivity over τ and seeds reported (T4, S4). ✔ by design.

2. **"Heuristic Level B results are not optima."** Correct — reported as
   heuristic estimates with seed dispersion, never as optima; exact Level A
   carries bounds/gaps. Estimand is stated per level.

3. **"Boundary-ON severed cross-border flow is trivially zero."** Addressed:
   we report *retention inside districts* and total severed flow — ON forces
   compensating cuts around Ōtsu; not a tautology.

4. **"Placebo borders aren't comparable."** Matched on pop share, interface
   length, two-sided contiguity; we publish borders.csv + matching tolerances.
   Residual caveat stated in LIMITATIONS.

5. **"Municipal-share severed flow approximation biased."** Exact at Level A;
   Level B approximation stated; S3 normalization sensitivity included.

6. **"K=9 small."** Acknowledged — K is statutory; cost computed in objective
   units AND in interpretable metrics (dev, PP, splits, severed trips).

7. **"Why is dev allowed up to 20% when Japan's rule is 2x ratio?"** τ=0.20
   covers both tails; the statutory max/min 2.0 corresponds to |dev|≤~0.33 —
   τ sensitivity includes 0.30. Stated in methods.

8. **"CP-SAT gaps open at time limit."** Reported transparently (bound, gap);
   objective-values basis for cost uses achieved solutions at both sides,
   consistent solver budget.

9. **"r2ka prefecture-boundary mismatch."** 30 m tolerance documented; S2
   tolerance sweep in supplement.

10. **Double-blind**: manuscript contains no author identity; title page
    separate. Figures/tables cited in order. APA 7th references — numbered
    list must be converted (pending packaging step).
