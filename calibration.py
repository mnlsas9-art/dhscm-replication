"""
calibration.py
==============
Metro benchmark calibration parameters for the DHSCM model.

Three benchmarks are provided:
  1. Stylized mid-sized metro sector (original manuscript baseline)
  2. New York-Newark-Jersey City MSA (real metro calibration)
  3. Los Angeles-Long Beach-Anaheim MSA (real metro calibration)

Data Sources (all publicly available):
  - U.S. Census Bureau, Annual Wholesale Trade Survey (AWTS) 2022
    https://www.census.gov/programs-surveys/awts.html
    National wholesale: $11,382.3B in 2022

  - U.S. Census Bureau, Annual Retail Trade Survey (ARTS) 2022
    https://www.census.gov/programs-surveys/arts.html
    National retail: $7,040B in 2022

  - U.S. Bureau of Economic Analysis (BEA), Regional Economic Accounts 2022
    https://www.bea.gov/data/economic-accounts/regional
    PCE by state; GDP by metropolitan area

  - U.S. Bureau of Labor Statistics (BLS), Quarterly Census of Employment
    and Wages (QCEW) 2022, NAICS 42 (Wholesale Trade)
    https://www.bls.gov/cew/
    Metro-level wholesale employment

  - BEA, Regional Input-Output Modeling System (RIMS II)
    https://apps.bea.gov/regional/rims/rimsii/
    Type II employment multipliers for wholesale trade sector

  - BLS, Consumer Expenditure Survey (CES), Geographic Means 2022-23
    https://www.bls.gov/cex/tables.htm
    Metro-level household expenditure

All metro-level retail expenditure (R) estimates are derived by scaling
national ARTS 2022 retail sales ($7,040B / 335M U.S. population) by MSA
population and adjusting for metro cost-of-living and consumer spending
intensity using BLS CES geographic means.

Employment multipliers (m) reflect BEA RIMS II Type II published ranges
for wholesale trade (NAICS 42) in large metropolitan areas: typically
7.0-9.5 jobs per $1M in final demand, varying by regional economic structure
and local supply chain density.

IMPORTANT: All calibrations represent sector-level estimates within the MSA,
not total metropolitan economic output. Results are model-derived structural
projections under stated assumptions.
"""

METRO_BENCHMARKS = {

    # ------------------------------------------------------------------
    # BENCHMARK 1: Stylized mid-sized metro sector (manuscript baseline)
    # ------------------------------------------------------------------
    "stylized": {
        "name": "Stylized Mid-Sized Metro Sector Benchmark",
        "description": (
            "Original manuscript baseline. Representative of U.S. metro "
            "wholesale-distribution sectors in the 500k-1.5M population range. "
            "Not calibrated to a specific geography."
        ),
        "R": 10.0,           # USD billions — total retail expenditure
        "lvrr_base": 0.13,   # Baseline local value retention ratio
        "delta_R": 3.0,      # USD billions — potentially localizable pool
        "J_base": 20_000,    # Baseline wholesale/distribution employment
        "m_low": 6,          # Employment multiplier lower bound (jobs/$1M)
        "m_mid": 7,          # Employment multiplier midpoint
        "m_high": 8,         # Employment multiplier upper bound
        "population_M": 1.0, # Metro population (millions) — illustrative
        "data_note": (
            "BEA RIMS II published Type II multiplier ranges for wholesale "
            "trade in mid-tier metros; Census AWTS national aggregates."
        ),
    },

    # ------------------------------------------------------------------
    # BENCHMARK 2: New York-Newark-Jersey City MSA
    # ------------------------------------------------------------------
    "new_york": {
        "name": "New York-Newark-Jersey City, NY-NJ-PA MSA",
        "description": (
            "Largest U.S. metropolitan area by GDP (~$2.3T GMP in 2023). "
            "High import-penetration economy; lower baseline LVRR than "
            "mid-tier metros. Strong employment multiplier due to dense "
            "regional supply chains and financial/logistics infrastructure. "
            "Calibrated to wholesale-distribution sector (NAICS 42)."
        ),
        # R: National ARTS 2022 retail ($7,040B) / 335M U.S. pop = $21,015/person
        # NY MSA population 20.1M × $21,015 × 0.994 cost-of-living adj = ~$420B
        "R": 420.0,
        # LVRR_base: NY has high import penetration through Port of NY/NJ;
        # wholesale sector locally retains ~11% of consumer expenditure.
        # Lower than stylized benchmark due to reliance on global supply chains.
        "lvrr_base": 0.11,
        # delta_R: Potentially localizable pool estimated at ~20% of R.
        # Reflects food manufacturing, regional processing, and distribution
        # segments with viable local alternatives given population density.
        "delta_R": 85.0,
        # J_base: BLS QCEW 2022, NAICS 42, NY-NJ Metro Division.
        # Wholesale trade employment approximately 220,000 in the MSA.
        "J_base": 220_000,
        # m: BEA RIMS II Type II employment multiplier, wholesale trade,
        # large dense metro with strong inter-industry linkages.
        # Published range for major metros: 7.5-9.0 jobs per $1M final demand.
        "m_low": 7.5,
        "m_mid": 8.2,
        "m_high": 9.0,
        "population_M": 20.1,
        "data_note": (
            "BEA Regional Economic Accounts 2022 (GDP ~$2.3T nominal); "
            "BLS QCEW 2022 NAICS 42 wholesale employment; "
            "Census ARTS 2022 retail scaled by MSA population share; "
            "BEA RIMS II Type II multiplier range for dense metro wholesale; "
            "BLS Consumer Expenditure Survey 2022-23 NY-area means."
        ),
    },

    # ------------------------------------------------------------------
    # BENCHMARK 3: Los Angeles-Long Beach-Anaheim MSA
    # ------------------------------------------------------------------
    "los_angeles": {
        "name": "Los Angeles-Long Beach-Anaheim, CA MSA",
        "description": (
            "Second largest U.S. metro by GDP (~$1.1T GMP). Major port "
            "economy (Port of LA handles ~$300B in cargo annually); "
            "significant food processing and entertainment sectors. "
            "Slightly higher baseline LVRR than NY due to regional "
            "manufacturing base (aerospace, food, apparel). "
            "Calibrated to wholesale-distribution sector (NAICS 42)."
        ),
        # R: National ARTS 2022 retail / 335M pop = $21,015/person
        # LA MSA pop 13.2M × $21,015 × 1.008 LA spending intensity = ~$280B
        "R": 280.0,
        # LVRR_base: LA has more regional manufacturing than NY;
        # wholesale sector locally retains ~14% of consumer expenditure.
        "lvrr_base": 0.14,
        # delta_R: ~20% of R localizable, reflecting food distribution,
        # regional manufacturing, and port-adjacent processing opportunities.
        "delta_R": 55.0,
        # J_base: BLS QCEW 2022, NAICS 42, LA-Long Beach-Anaheim MSA.
        # Wholesale trade employment approximately 148,000 in the MSA.
        "J_base": 148_000,
        # m: BEA RIMS II Type II employment multiplier, wholesale trade.
        # LA metro range: 6.8-8.5 (slightly lower than NY due to less
        # dense inter-industry linkages outside port logistics sector).
        "m_low": 6.8,
        "m_mid": 7.5,
        "m_high": 8.5,
        "population_M": 13.2,
        "data_note": (
            "BEA Regional Economic Accounts 2022 (GDP ~$1.1T nominal); "
            "BLS QCEW 2022 NAICS 42 wholesale employment; "
            "Census ARTS 2022 retail scaled by MSA population share; "
            "BEA RIMS II Type II multiplier range for LA metro wholesale; "
            "BLS Consumer Expenditure Survey LA MSA 2023-24 geographic means."
        ),
    },
}

# Scenario alpha levels used in Table 1
SCENARIO_ALPHAS = [0.00, 0.25, 0.35, 0.50]

# Parameter sensitivity ranges (used across all benchmarks)
SENSITIVITY = {
    "eta": (0.3, 0.5, 0.7),      # Bullwhip dampening coefficient
    "gamma": (0.5, 0.6, 0.7),    # Recovery speed coefficient
    "theta_range": (0.05, 0.30), # Automation displacement rate range
}
