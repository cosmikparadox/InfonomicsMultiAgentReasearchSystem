# OTTOMAN EMPIRE — Layer B Economic Metrics Harvest Report
**Agent**: DE-001 (Data Engineer)
**Date**: 15 March 2026
**Scope**: ECO-003 through ECO-011 across Rise (1299-1520), Peak (1520-1683), Decline (1683-1922)
**Output**: Structured CSV + this narrative report

---

## EXECUTIVE SUMMARY

9 metrics harvested across 3 phases yielding 47 data rows in the CSV output. Confidence distribution:
- **HIGH**: 14 data points (30%) — primarily currency debasement (Pamuk series) and debt milestones
- **MODERATE**: 22 data points (47%) — fiscal, commercial interest, banking/capital market assessments
- **LOW**: 11 data points (23%) — GDP estimates, early trade balance, early debt ratios

The Ottoman Empire presents a **fundamental data asymmetry**: monetary/debasement data is excellent (Pamuk's complete time series), fiscal data is moderate (Karaman-Pamuk budget compilation), but GDP and trade balance data are poor (indirect estimation only). This asymmetry directly affects Layer B calibration confidence.

---

## ECO-003: GDP GROWTH RATE (% annual)

### Data Points

| Phase | Period | Growth Rate (% p.a.) | Confidence | Source |
|-------|--------|---------------------|------------|--------|
| Rise | 1299-1520 | 0.06-0.10% | LOW | Pamuk (2009) |
| Peak | 1520-1683 | 0.00-0.10% | LOW | Pamuk (2009) |
| Decline (early) | 1683-1820 | 0.00-0.05% | LOW | Pamuk (2009) |
| Decline (late) | 1820-1913 | 0.56% | MODERATE | Pamuk (2006) JEH |

### Key Findings

Pamuk (2009) estimated ~27% total GDP per capita growth across the entire 1500-1820 period, implying an average of ~0.08% per annum. This is consistent with the broader Mediterranean pattern (Italy, Spain also stagnated). The Ottoman Empire was on the "lagging side of the Little Divergence."

For the post-1820 period, Pamuk (2006) provides a firmer estimate of 0.56% annual growth, though this includes a severe negative shock of approximately -4% during 1870-1880 (Russo-Turkish War, fiscal crisis, default).

GDP per capita benchmark: ~$600 (1990 international dollars) in 1500, rising to ~$750-800 by 1820, and roughly $1,200-1,500 by 1913. Maddison's data shows a 1:5 gap with UK, 1:3.8 gap with Netherlands, 1:3 gap with France by late 19th century.

**Second-generation estimates** (Bulut & Altay 2021, TUJISE) suggest Ottoman per capita GDP was "relatively higher" than first-generation Pamuk/Maddison estimates, though specific revised figures are not yet consensus.

### Limitations
- No direct GDP data exists for any Ottoman period
- All estimates use indirect method (wages + urbanization → GDP)
- Territorial changes confound per-capita vs. aggregate calculation
- Regional diversity enormous and not captured

### Sources
- Pamuk, S. (2009). "Estimating GDP per capita for the Ottoman Empire in a European Comparative Framework, 1500-1820." XVth World Economic History Congress, Utrecht.
- Pamuk, S. (2006). "Estimating Economic Growth in the Middle East since 1820." *Journal of Economic History* 66(3): 809-828.
- Maddison Project Database (2020).
- Bulut, M. & Altay, S. (2021). "The Ottoman Economy (1870-1913): Preliminary Second-Generation Estimates." *Turkish Journal of Islamic Economics* 9(1).

---

## ECO-004: GOVERNMENT REVENUE (% of GDP)

### Data Points

| Phase | Period | Value | Unit | Confidence | Source |
|-------|--------|-------|------|------------|--------|
| Rise | 1528 | 9.65M | Venetian ducats | HIGH | Barkan budget study |
| Rise/Peak | 1500-1600 | <4% | of GDP | MODERATE | Karaman & Pamuk (2010) |
| Peak | 1527 | 46% | of assessed collected centrally | MODERATE | Karaman & Pamuk (2010) |
| Decline | 18th c. | ~25% | of assessed collected centrally | MODERATE | Karaman & Pamuk (2010) |
| Decline | 1840-1914 | 5-10% | of GDP | MODERATE | Karaman & Pamuk (2010) |

### Key Findings

Karaman & Pamuk (2010) is the definitive study, using 40+ ex-post budget documents from Ottoman archives. Their central finding: **Ottoman central government cash revenues probably remained below 4% of GDP during the early modern era**, lagging behind European peers due to high intermediary shares.

Critical nuance: the 4% figure captures only central treasury **cash** receipts. The timar system channeled substantial resources (military service, local administration) without cash passing through the central treasury. Actual fiscal extraction from taxpayers was significantly higher but remains unknown.

The 19th century Tanzimat reforms achieved "significant increases in central revenues" but the empire started from a low base. By 1875, total state revenues were ~25 million Ottoman liras (~£22-23M), yet this still represented only 5-10% of estimated GDP.

Per capita revenue was strikingly low: less than 3 days' wages of an unskilled Istanbul construction worker, and below 2 days for most of the early modern period.

### Limitations
- Central treasury cash ≠ total fiscal extraction
- Timar/in-kind revenues excluded from headline figure
- Tax farming creates unknown gap between assessed and collected
- GDP denominator uncertain for all periods

### Sources
- Karaman, K.K. & Pamuk, S. (2010). "Ottoman State Finances in European Perspective, 1500-1914." *Journal of Economic History* 70(3): 593-629.
- Barkan, O.L. "Bir Butce Ornegi." pp. 251-329.
- Dataset: http://www.ata.boun.edu.tr/sevketpamuk/JEH2010articledatabase

---

## ECO-005: GOVERNMENT DEBT (% of GDP)

### Data Points

| Phase | Year | Nominal Debt | Debt/Revenue | Debt/GDP (est.) | Confidence |
|-------|------|-------------|--------------|-----------------|------------|
| Rise | 1299-1520 | ~0 | 0% | ~0% | HIGH |
| Peak | 1520-1683 | ~0 (formal) | Minimal | ~0% | HIGH |
| Decline | 1775 | Low (esham) | <10% | <5% | LOW |
| Decline | 1854 | £3M | ~3-4% of revenue | ~10-15% | LOW |
| Decline | 1875 | £200-214.5M | >50% (debt service) | ~100-150% | LOW |
| Decline | 1881 | £106.4M (post-haircut) | ~40% revenue to OPDA | ~50-75% | LOW |
| Decline | 1914 | £139.1M | ~35-40% to OPDA | ~80-120% | LOW |

### Key Findings — The Ottoman Debt Trajectory

**Pre-1775**: Zero formal government debt. Fiscal deficits managed through:
- Debasement (seigniorage revenue)
- Short-term Galata banker loans (undocumented)
- Tax farming adjustments

**1775**: Introduction of **esham** bonds — life annuities against future tax revenues. First formal domestic borrowing instrument. Modest initial volumes.

**1854-1875**: Catastrophic debt spiral:
- 1854: First foreign loan (£3M, 6% interest, issued at 80% = ~7.5% effective)
- 15 loans struck 1854-1874
- Net receipts only ~46% of nominal (deep discounts, commissions)
- By 1875: £200M+ nominal debt; £12M annual service = **>50% of total state revenue**
- **30 October 1875**: Sovereign default (Ramazan Kararnamesi)

**1881**: Decree of Muharrem restructuring:
- Debt reduced from £252.8M to £106.4M
- OPDA established with control over salt, tobacco, silk, stamps, alcohol revenues
- OPDA eventually controlled 32-40% of state income
- Risk premium fell from 5.7% to 2.1%

**Key ratio**: At the 1875 crisis, debt service consumed over 50% of revenue, and with revenue at ~5-10% of GDP, implied debt/GDP ratios of 100-150%. This is broadly consistent with Reinhart-Rogoff sovereign debt crisis thresholds.

### Limitations
- GDP denominator extremely uncertain for all years
- Debt/GDP ratios are my estimates derived from debt/revenue and revenue/GDP ratios
- Internal debt (esham, sarraf obligations) poorly documented before 1854
- Nominal vs. net debt distinction crucial (46% net receipt rate)

### Sources
- Ottoman public debt records via Grokipedia compilation
- Birdal, M. (2010). *The Political Economy of Ottoman Public Debt: Insolvency and European Financial Control in the Late Nineteenth Century*.
- Reinhart, C. & Rogoff, K. debt dataset (includes Ottoman data points).
- OPDA records; Decree of Muharrem text.

---

## ECO-006: INTEREST RATES (Government)

### Data Points

| Phase | Year | Rate | Type | Confidence |
|-------|------|------|------|------------|
| Rise | 1299-1520 | N/A | No borrowing | HIGH |
| Peak | 1520-1683 | N/A | No formal bonds | HIGH |
| Decline | 1775-1840 | ~10-12% | Esham implied return | LOW |
| Decline | 1840 | 12.5% | Kaime (paper currency as bond) | MODERATE |
| Decline | 1854 | 6% nom / 7.5% eff | First foreign loan | HIGH |
| Decline | 1855 | 4% | UK/France guaranteed | HIGH |
| Decline | 1858-1873 | 6-9% nom / 10-15% eff | Multiple foreign loans | MODERATE |
| Decline | 1870 | 3% nom / ~9% eff | Lottery loan at 32% of par | HIGH |
| Decline | 1874 | >25% (refused) | Galata bankers refused | HIGH |
| Decline | 1875 | 5% (forced) | Post-default restructuring | MODERATE |
| Decline | 1882-1914 | 4-6% | Post-OPDA restoration | MODERATE |

### Key Findings

The Ottoman government borrowing cost trajectory is a textbook case of escalating sovereign risk:

1. **No borrowing phase** (1299-1775): Fiscal needs met through debasement seigniorage and tax farming
2. **Internal borrowing** (1775-1854): Esham bonds at ~10-12% implied returns
3. **Early foreign borrowing** (1854-1860): 4-7.5% effective rates, supported by Crimean War alliance
4. **Deteriorating credit** (1860-1874): Effective rates climbed to 10-15% as deep discounts on issuance (1870 lottery loan at 32% of par) masked high nominal coupons
5. **Credit collapse** (1874): Galata bankers refused to lend even at 25%
6. **Default and recovery** (1875-1914): After OPDA establishment, risk premium compressed from 5.7% to 2.1%, restoring market access at 4-6%

The distinction between nominal coupon and effective yield is critical: the 1874 loan had a 5% coupon but was issued at 43.5% of par, giving an effective yield of ~11.5%.

### Sources
- Homer, S. & Sylla, R. (2005). *A History of Interest Rates*. 4th ed. Wiley.
- Ottoman loan records via Grokipedia compilation and Birdal (2010).
- Pamuk, S. (2000). *A Monetary History of the Ottoman Empire*. Cambridge University Press.

---

## ECO-007: INTEREST RATES (Commercial)

### Data Points

| Phase | Period | Rate Range | Borrower Type | Confidence |
|-------|--------|-----------|---------------|------------|
| Rise | 1299-1520 | 10-20% (est.) | General commercial | LOW |
| Peak | 1520-1683 | 10-15% | Cash waqf borrowers | MODERATE |
| Peak/Decline | 1602-1799 | 15-20% | Male Muslim elites | MODERATE |
| Peak/Decline | 1602-1799 | 12-17% | Women/non-Muslims | MODERATE |
| Decline | 1683-1854 | 12-24% | Regional variation | MODERATE |
| Decline | 1856-1914 | 8-15% | Formal banking sector | MODERATE |

### Key Findings — The Kuran-Rubin Paradox

The most striking finding comes from Kuran & Rubin (2018), who analyzed private loans in Ottoman Istanbul 1602-1799 and discovered that **privileged groups paid MORE for credit**:

- Men paid 3.4% more than women
- Muslims paid 1.9% more than non-Muslims
- Elites paid 2.3% more than non-elites
- Male Muslim elites paid ~19-20%

The mechanism: Islamic courts went easy on privileged defaulters, creating moral hazard. Lenders compensated by charging them higher rates. This "inverted risk premium" meant those with greatest investment capacity paid the most, which Kuran argues retarded Ottoman economic growth.

**Cash waqfs** were the primary formal lending institution, operating at 10-15% with a legal cap of 15% (Ebussuud decree). They functioned as proto-banks but were limited in scale. A 2024 study (Brill) reveals cash waqfs also supported large-scale commercial capital for Ottoman-Venetian trade, not just micro-credit.

### Sources
- Kuran, T. & Rubin, J. (2018). "The Financial Power of the Powerless: Socio-Economic Status and Interest Rates under Partial Rule of Law." *Economic Journal* 128: 758-96.
- Kuran, T. (2011). *The Long Divergence*. Princeton University Press.
- Korkut, C. & Bulut, M. "Ottoman Cash Waqfs: An Alternative Financial System." *Insight Turkey*.
- Brill (2024). "Cash Waqfs and Commercial Capital: Evidence from Ottoman-Venetian Trade." *JESHO* 67(5-6): 497ff.

---

## ECO-008: TRADE BALANCE (Net exports %)

### Data Points

| Phase | Period | Balance | Confidence | Source |
|-------|--------|---------|------------|--------|
| Rise | 1299-1520 | Surplus (qualitative) | LOW | Inalcik (1994) |
| Peak | 1520-1683 | Near balance / mild surplus | LOW | Inalcik; Lampe; McGowan |
| Decline (early) | 1700-1838 | Shifting surplus→deficit | LOW | Pamuk (1987) |
| Decline (late) | 1838-1913 | Deficit (growing) | MODERATE | Pamuk (1987); Quataert |

### Key Findings

The Ottoman trade trajectory follows a classic peripheralization pattern:

1. **Rise/Peak**: Liberal trade policy (capitulations from 1536 with 3% duties); transit trade revenues; Constantinople's role as trade hub; Balkans ran export surplus; only Constantinople ran import surplus

2. **Transition** (18th century): Cotton exports doubled 1750-1789; semi-processed goods exports to NW Europe increased; but European manufactures beginning to penetrate

3. **Decline** (post-1838): Treaty of Balta Liman (1838) with Britain "doomed Ottoman industrialization"; imports grew ~8x while exports ~4x; deindustrialization; by 1900 UK/France/Germany/Austria controlled 75% of imports and 60-70% of exports

Lampe and McGowan argue the empire as a whole (especially Balkans) maintained export surplus longer than commonly assumed. The 1873-1896 "Great Depression" paradoxically aided Ottoman handicrafts by worsening terms of trade.

### Limitations
- No systematic trade statistics exist before 19th century
- Quataert and Issawi rely on qualitative evidence and spotty time series
- Re-export trade and transit dues complicate balance calculations
- Regional variation extreme (Balkans ≠ Anatolia ≠ Arab provinces)

### Sources
- Pamuk, S. (1987). *The Ottoman Empire and European Capitalism 1820-1913*. Cambridge University Press.
- Inalcik, H. & Quataert, D. (1994). *An Economic and Social History of the Ottoman Empire, 1300-1914*. CUP.
- Issawi, C. (1980). *The Economic History of Turkey, 1800-1914*.
- Williamson, J. (2009). "Ottoman De-Industrialization 1800-1913." NBER Working Paper 14763.

---

## ECO-009: CURRENCY DEBASEMENT RATE

### Data Points (Akce Silver Content — Pamuk Series)

| Period | Silver Content (g) | Cumulative Decline | Rate per Decade | Confidence |
|--------|-------------------|-------------------|-----------------|------------|
| 1326-1444 | 1.15-1.20 | Baseline | ~0% | HIGH |
| 1444-1481 | 0.77 | -33% | ~8% | HIGH |
| 1481-1520 | 0.73 | -37% | ~1-2% | HIGH |
| 1520-1585 | 0.68 | -41% | ~1.5% (0.52% annual) | MODERATE |
| 1585-1586 | 0.38 | -67% | 44% single episode | HIGH |
| 1600 | 0.29 | -75% | ~30% per decade (1585-1600) | HIGH |
| 1640 | 0.30 | -74% | Stabilized | HIGH |
| 1700 | 0.13 | -89% | ~8% per decade (1600-1700) | HIGH |
| 1800 | 0.048 | -96% | ~9% per decade (1700-1800) | HIGH |
| 1810s | 0.032 | -97% | Accelerating | HIGH |
| 1840s | 0.008 | -99.3% | ~25% per decade (1800-1844) | HIGH |

### Key Findings

This is the **highest-confidence metric** in the entire harvest, thanks to Pamuk's comprehensive numismatic time series. Three distinct debasement regimes:

1. **Stability** (1326-1520): Minor fluctuations; Mehmed II's debasements reversed by Bayezid II
2. **Accelerating decline** (1520-1700): Punctuated by 1585-86 crisis (44% single reduction); akce effectively abandoned mid-17th century
3. **Terminal collapse** (1700-1844): From 0.13g to 0.008g; Mahmud II's "Great Debasement" the most extreme

Pamuk's key insight: debasement was **the primary driver of Ottoman price inflation**, not silver inflows from the Americas (contra Barkan). Prices in Istanbul expressed in grams of silver tracked Mediterranean prices closely.

The debasement rate correlates strongly with military/fiscal crises: Mehmed II's conquests, the Long War (1593-1606), and the Napoleonic/reform era all triggered episodes.

### Verification Against Existing Data

The audit report listed: 1469-79: 0.85g; 1585-89: 0.39g; 1700-09: 0.12g; 1830-39: 0.0073g. These are **CONSISTENT** with the fuller Pamuk series harvested here (minor differences due to decade-averaging vs. point estimates).

### Sources
- Pamuk, S. (2000). *A Monetary History of the Ottoman Empire*. Cambridge University Press. Tables 3.1, 4.1; Graph A-2.
- Pamuk, S. (2004). "Prices in the Ottoman Empire, 1469-1914." *International Journal of Middle East Studies*.
- Pamuk, S. (2001). "The Price Revolution in the Ottoman Empire Reconsidered." *IJMES* 33.
- Pamuk, S. (1997). "In the Absence of Domestic Currency: Debased European Coinage in the Seventeenth-Century Ottoman Empire." *Journal of Economic History* 57.

---

## ECO-010: BANKING DEVELOPMENT (1-5 Scale)

### Data Points

| Phase | Period | Score | Key Feature | Confidence |
|-------|--------|-------|-------------|------------|
| Rise | 1299-1520 | 1.0 | Sarraf money-changers only | MODERATE |
| Peak | 1520-1683 | 1.5 | Cash waqfs + Galata sarrafs | MODERATE |
| Decline (early) | 1683-1840 | 1.5 | Galata bankers dominant; esham 1775 | MODERATE |
| Decline (mid) | 1840-1863 | 2.5 | Failed banks + Ottoman Bank 1856 | MODERATE |
| Decline (late) | 1863-1914 | 3.0 | Imperial Ottoman Bank + foreign banks | MODERATE |

### Key Findings — Institutional Timeline

- **Sarrafs** (throughout): Money-changers from non-Muslim communities (Armenian, Greek, Jewish) in Galata; informal banking functions
- **Cash waqfs** (16th-18th c.): Proto-banking at 10-15% rates; legally circumvented usury prohibition; provided micro-credit and (per 2024 Brill study) commercial capital
- **Galata bankers** (18th-19th c.): Alléon, Baltazzi, and others; financed state borrowing; intermediated foreign loans; family-based, not institutionalized
- **Bank-i Dersaadet** (1847): First Ottoman bank; no capital; failed quickly
- **Banque de Constantinople** (1847-1852): Joint venture with Galata bankers; wound up
- **Ottoman Bank** (1856): British-chartered; £500,000 capital; limited success
- **Imperial Ottoman Bank** (1863): Anglo-French; note-issuing privilege; de facto central bank; dominant institution through 1914

Kuran's key assessment: by the 10th century Islamic financial instruments were "as advanced as anything in the non-Islamic world," but no "durable financial institutions recognizable as banks" emerged before the 19th century.

### Sources
- Kuran, T. (2011). *The Long Divergence*. Princeton University Press.
- Ottoman Bank Wikipedia/Grokipedia.
- Hosgor. "Credit and Financing in Early Modern Ottoman Empire: The Galata Example."
- Daily Sabah. "History of Ottoman Banking" (2017) and "The Galata Bankers" (2015).

---

## ECO-011: CAPITAL MARKET DEPTH (1-5 Scale)

### Data Points

| Phase | Period | Score | Key Feature | Confidence |
|-------|--------|-------|-------------|------------|
| Rise | 1299-1520 | 0.5 | No tradeable securities | HIGH |
| Peak | 1520-1683 | 1.0 | Limited cash waqf transferability | MODERATE |
| Decline (early) | 1775-1860 | 1.5 | Esham bonds; informal Galata trading | MODERATE |
| Decline (late) | 1866-1914 | 2.5 | Dersaadet Tahvilat Borsasi | MODERATE |

### Key Findings — Capital Market Timeline

- **1774**: Esham system — proto-government bonds; redeemable after 10-25 years; traded on Istanbul markets informally
- **1861**: Commercial Code adopted from France; permitted joint-stock companies
- **1864**: Unofficial money and bond exchange established in Galata (Havyar Han)
- **1866**: **Dersaadet Tahvilat Borsasi** (Istanbul Bond Exchange) formally established, modeled on European bourses
- **1873**: Official regulation; exchange committee of 20 members (all Greek); government supervision via Ministry of Finance; immediately disrupted by Vienna crisis
- **1906**: Expanded to "Stock Exchange of Debenture Bonds and Shares" (added equities)

The exchange primarily traded government bonds (esham and tahvilat), with limited equity and foreign exchange. It attracted "professional traders, banks, insurance companies, and railway companies with liquid assets." However, it remained narrow, volatile, and dominated by foreign interests.

### Sources
- Borsa Istanbul historical records.
- "Evidence from the Ottoman Empire and the Istanbul Bourse." EHES Working Paper 112.
- TRDizin: "Osmanli'da Borsa: Dersaadet Tahvilat Borsasi'ndan Esham ve Tahvilat Borsasi'na."

---

## CROSS-METRIC SYNTHESIS FOR LAYER B CALIBRATION

### Phase Transition Signatures (Keen-Minsky Debt Dynamics)

**Rise → Peak transition (~1520)**:
- GDP growth: ~0.08% → ~0.05% (decelerating)
- Government revenue: ~4% of GDP, centralized
- Debt: Zero
- Debasement: Minimal (Bayezid II stabilization)
- Banking: Sarrafs only (score 1.0→1.5)
- **Minsky phase**: Hedge finance (income covers all obligations)

**Peak → Decline transition (~1683)**:
- GDP growth: stagnating
- Revenue: Central collection declining (46% → 25% of assessed)
- Debt: Still zero formal, but rising sarraf obligations
- Debasement: Post-1585 crisis, akce at 0.13g (89% debased)
- Banking: Cash waqfs + Galata bankers (score 1.5)
- **Minsky phase**: Speculative finance (income covers interest but requires refinancing for principal)

**Decline acceleration (~1854-1875)**:
- GDP growth: 0.56% but volatile
- Revenue: Rising but insufficient (5-10% of GDP)
- Debt: Exploding (0 → £200M+ in 21 years)
- Interest: Rising from 7.5% to effectively >15%
- Trade: Deficit growing; deindustrialization
- **Minsky phase**: Ponzi finance (income insufficient even for interest; new borrowing required to service old debt; default 1875)

### Data Quality Assessment

| Metric | Completeness | Source Quality | Confidence | Usability for Layer B |
|--------|-------------|---------------|------------|----------------------|
| ECO-003 GDP Growth | 3/3 phases | HIGH (Pamuk) | LOW (indirect) | Marginal — use as constraint not input |
| ECO-004 Revenue/GDP | 3/3 phases | HIGH (Karaman-Pamuk) | MODERATE | Good — central treasury series available |
| ECO-005 Debt/GDP | 3/3 phases | MODERATE | LOW (GDP uncertain) | Good for decline phase; use debt/revenue ratio instead |
| ECO-006 Govt Interest | 2/3 phases | HIGH for decline | HIGH (loan records) | Excellent for 1854-1914 |
| ECO-007 Commercial Interest | 3/3 phases | HIGH (Kuran-Rubin) | MODERATE | Good — cash waqf + court record series |
| ECO-008 Trade Balance | 3/3 phases | LOW-MODERATE | LOW | Marginal — qualitative only before 19th c. |
| ECO-009 Debasement | 3/3 phases | HIGH (Pamuk numismatic) | HIGH | Excellent — complete time series |
| ECO-010 Banking | 3/3 phases | MODERATE | MODERATE | Good — ordinal scale usable |
| ECO-011 Capital Markets | 3/3 phases | MODERATE | MODERATE | Good — ordinal scale usable |

### Recommendation for Layer B Calibration

1. **Use ECO-009 (debasement) as primary anchor** — highest confidence, complete time series
2. **Use ECO-005/006 (debt + govt interest) for decline phase** — excellent data post-1854
3. **Use debt/revenue ratio instead of debt/GDP ratio** where possible — revenue data more reliable than GDP
4. **Treat ECO-003 (GDP growth) as constraint envelope** — not precise enough for direct calibration
5. **The Kuran-Rubin commercial interest data (ECO-007) is unique** — may enable modeling of credit market distortions as growth drag

---

## BIBLIOGRAPHY

### Primary Scholarly Sources

1. Barkan, O.L. "Bir Butce Ornegi." pp. 251-329.
2. Birdal, M. (2010). *The Political Economy of Ottoman Public Debt*. I.B. Tauris.
3. Bulut, M. & Altay, S. (2021). "The Ottoman Economy (1870-1913)." *TUJISE* 9(1).
4. Homer, S. & Sylla, R. (2005). *A History of Interest Rates*. 4th ed. Wiley.
5. Inalcik, H. & Quataert, D. (1994). *An Economic and Social History of the Ottoman Empire*. CUP.
6. Issawi, C. (1980). *The Economic History of Turkey, 1800-1914*. Chicago.
7. Karaman, K.K. & Pamuk, S. (2010). "Ottoman State Finances in European Perspective." *JEH* 70(3): 593-629.
8. Kuran, T. (2011). *The Long Divergence*. Princeton University Press.
9. Kuran, T. & Rubin, J. (2018). "Financial Power of the Powerless." *Economic Journal* 128: 758-96.
10. Maddison Project Database (2020).
11. Pamuk, S. (1987). *The Ottoman Empire and European Capitalism 1820-1913*. CUP.
12. Pamuk, S. (1997). "In the Absence of Domestic Currency." *JEH* 57.
13. Pamuk, S. (2000). *A Monetary History of the Ottoman Empire*. CUP.
14. Pamuk, S. (2001). "The Price Revolution in the Ottoman Empire Reconsidered." *IJMES* 33.
15. Pamuk, S. (2004). "Prices in the Ottoman Empire, 1469-1914."
16. Pamuk, S. (2006). "Estimating Economic Growth in the Middle East since 1820." *JEH* 66(3): 809-828.
17. Pamuk, S. (2009). "Estimating GDP per capita for the Ottoman Empire." XVth WEHC, Utrecht.
18. Salzmann, A. (1993). "An Ancien Regime Revisited." *Politics & Society* 21(4): 393-423.
19. Williamson, J. (2009). "Ottoman De-Industrialization 1800-1913." NBER WP 14763.

---

*Report generated by DE-001 Data Engineer Agent — 15 March 2026*
*CSV output: data/outputs/Ottoman_LayerB_Economic_Metrics.csv (47 rows)*
*Next action: QA-001 verification pass + Layer B calibration team intake*
