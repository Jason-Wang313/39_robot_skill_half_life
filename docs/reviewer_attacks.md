# Reviewer Attacks

1. Half-life is arbitrary because the threshold can be chosen after the fact.
2. Censoring makes long-lived policies look infinite.
3. Sparse observation cadence inflates the reported crossing time.
4. The suite is analytic and may not reflect real robot deployment.
5. Maintenance policies are proxies rather than trained algorithms.
6. Cost weights are subjective.
7. A single scalar can hide nonmonotonic recovery.
8. Static final success might be enough for some benchmarks.
9. Oracle maintenance dominates and is not deployable.
10. Hardware survival analysis is missing.

## Final Responses

- V3 reports threshold sensitivity, horizon sensitivity, cadence delay, shock recovery, and cost-aware uptime.
- The manuscript states that half-life is meaningful only with the full curve, threshold, horizon, censoring, cadence, and cost.
- Oracle maintenance is explicitly an upper bound, not a proposed policy.
- Overfit rapid adaptation is included as a negative control showing that half-life alone can be gamed.
- Hardware deployment and survival confidence intervals are listed as future work, not claimed.
- The released artifacts include seed rows, aggregate rows, stress CSVs, generated figures, generated tables, validation metadata, and a final visually checked PDF.
