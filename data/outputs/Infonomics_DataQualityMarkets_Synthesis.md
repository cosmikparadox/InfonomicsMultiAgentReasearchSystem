# Data Marketplaces under Unobservable Quality — Synthesis

## Question
Under what conditions does a data marketplace achieve efficient
allocation when data quality is unobservable ex-ante?

## Answer (compressed)
A data marketplace can reach efficient allocation under ex-ante
quality asymmetry iff at least one of four mechanism families is
operative AND the privacy externality on data subjects is
independently internalised. The four families are:

  1. **Continuous signaling** (schemas, lineage, summary stats) —
     raises the unraveling threshold sigma_q*(pi) but does not by
     itself separate types.
  2. **Reputation under bounded replicability** — sustains efficient
     allocation iff seller discount factor delta exceeds the
     replicability-adjusted threshold delta*'(L, rho).
  3. **Verifiable screening** (protocol-attested samples,
     outcome-contingent royalties with bounded attribution noise) —
     dominates when the dispersed dimension is observable
     post-purchase.
  4. **Skin-in-the-game certification** — restores allocation when
     the dispersed dimension requires expertise to verify and the
     certifier holds a liability stake correlated with realised
     quality.

Mechanism dominance is **dimension-specific**, not universal:

| Dispersed dimension | Dominant mechanism                |
|---------------------|-----------------------------------|
| Recency             | Outcome-contingent / royalties    |
| Completeness        | Protocol-attested samples + audit |
| Accuracy            | Third-party certification         |
| Fit-for-purpose     | Reputation + try-before-buy       |

The privacy externality on data subjects survives any buyer-seller
mechanism and requires either Coasean transfers (infeasible at scale)
or regulatory disclosure caps.

## Contribution
- **Six refined propositions** (P1' through P6) with explicit
  assumptions and identified failure modes.
- **A dimension-to-mechanism mapping** that resolves the existing
  literature's tension between reputation, screening, and
  certification — they are not substitutes but specialists.
- **A unified treatment of asymmetry, replicability, and privacy**
  showing that mechanism design on the buyer-seller pair is
  necessary but not sufficient for first-best.

## Scope and limitations
- Cleanest application: experience-good data (ML training sets,
  research datasets). Extrapolation to search-good data (geo,
  weather) is straightforward but uninformative — those markets
  already work.
- Survivorship bias warning: existing marketplace evidence
  concentrates in easy categories. The interesting empirical test
  is the population of data products that *failed* to clear.
- Mechanism mapping is conjectural pending calibration on
  marketplace transaction data.

## Future research
1. **Empirical calibration** of the dimension-to-mechanism mapping
   against Snowflake Marketplace, AWS Data Exchange, and Dawex
   transaction data; identify which mechanism each market actually
   uses for each dimension.
2. **Experimental test** of outcome-contingent pricing vs fixed
   pricing in a controlled data-product setting; measure attribution-
   noise tolerance.
3. **Privacy-externality calibration**: estimate the wedge between
   social and private optima for representative ML training datasets.
4. **Bridge to Shapley attribution**: link the dimension-to-mechanism
   mapping to data-Shapley value decomposition, so seller compensation
   can be made dimension-specific.
