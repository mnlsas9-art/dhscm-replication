"""
dhscm_model.py
==============
Core equations of the Distributed Hybrid Supply Chain Model (DHSCM).

Reference:
    Mudiganti, N. L. K. (2026). WholeLocal: A Distributed Hybrid Approach to the
    Design of Resilient and Sustainable Supply Chains.
    Frontiers in Sustainability, Manuscript ID 1820269.

All functions implement the structural framework from Section 2 of the manuscript.
Results represent model-derived directional insights under stated assumptions,
not empirical measurements or predictive forecasts.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Section 2.1 — WholeLocal Analytical Framework
# ---------------------------------------------------------------------------

def lvrr(alpha, R, delta_R, lvrr_base):
    """
    Local Value Retention Ratio as a function of localization share.

    LVRR(alpha) = LVRR_base + alpha * (delta_R / R)

    Parameters
    ----------
    alpha     : float or ndarray  Localization share in [0, 1]
    R         : float             Total metro retail expenditure (USD billions)
    delta_R   : float             Potentially localizable revenue pool (USD billions)
    lvrr_base : float             Baseline LVRR under centralized architecture

    Returns
    -------
    float or ndarray : LVRR at given alpha
    """
    return lvrr_base + alpha * (delta_R / R)


def delta_RL(alpha, delta_R):
    """
    Incremental locally retained revenue (USD billions).

    delta_RL(alpha) = alpha * delta_R
    """
    return alpha * delta_R


def delta_employment(alpha, delta_R, m):
    """
    Incremental employment generation (jobs).

    Delta_L(alpha) = m * (alpha * delta_R * 1e9 / 1e6)
                   = m * alpha * delta_R * 1e3

    Parameters
    ----------
    alpha   : float or ndarray  Localization share
    delta_R : float             Localizable pool (USD billions)
    m       : float             Employment multiplier (jobs per $1M)

    Returns
    -------
    float or ndarray : Additional jobs generated
    """
    return m * alpha * delta_R * 1e3   # delta_R in $B → multiply by 1e3 for $M


def automation_displacement(theta, J_base):
    """
    Jobs lost to automation at displacement rate theta.

    J_loss(theta) = theta * J_base
    """
    return theta * J_base


def labor_stabilization_threshold(theta, J_base, m, delta_R):
    """
    Minimum localization share required to offset automation displacement.

    alpha_min(theta) = (theta * J_base) / (m * delta_R * 1e3)

    Parameters
    ----------
    theta   : float or ndarray  Automation displacement rate in [0, 1]
    J_base  : float             Baseline employment (jobs)
    m       : float             Employment multiplier (jobs per $1M)
    delta_R : float             Localizable pool (USD billions)

    Returns
    -------
    float or ndarray : Minimum alpha to offset displacement
    """
    return (theta * J_base) / (m * delta_R * 1e3)


# ---------------------------------------------------------------------------
# Section 2.2 — DHSCM Resilience Mechanisms
# ---------------------------------------------------------------------------

def redundancy_index(alpha, n_central=1):
    """
    Redundancy index: ratio of total production nodes to centralized nodes.

    rho(alpha) = (|Pc| + |Pl|) / |Pc|

    In the linear approximation, distributed nodes scale with alpha:
    rho(alpha) = 1 + alpha * n_central  (one distributed node per alpha unit)

    Parameters
    ----------
    alpha     : float or ndarray  Localization share
    n_central : int               Number of centralized production nodes (default 1)

    Returns
    -------
    float or ndarray : Redundancy index (>= 1)
    """
    return 1 + alpha * n_central


def recovery_speed(alpha, tau_c=1.0, gamma=0.6):
    """
    Recovery time relative to centralized baseline.

    tau(alpha) = tau_c * (1 - gamma * alpha)

    Parameters
    ----------
    alpha  : float or ndarray  Localization share
    tau_c  : float             Centralized baseline recovery time (normalized to 1.0)
    gamma  : float             Recovery speed coefficient (default 0.6, range [0.5, 0.7])
                               Anchored to Tang (2006) and Ivanov (2021): 15-30%
                               recovery advantage for distributed configurations.

    Returns
    -------
    float or ndarray : Recovery time (fraction of centralized baseline)
    """
    return tau_c * (1.0 - gamma * alpha)


def recovery_reduction_pct(alpha, gamma=0.6):
    """Recovery time reduction as percentage of centralized baseline."""
    return 100.0 * gamma * alpha


def amplification_intensity(alpha, kappa_c=1.0, eta=0.5):
    """
    Production amplification (bullwhip) intensity.

    kappa(alpha) = kappa_c * (1 - eta * alpha)

    Parameters
    ----------
    alpha   : float or ndarray  Localization share
    kappa_c : float             Centralized baseline amplification intensity
    eta     : float             Dampening coefficient (default 0.5, range [0.3, 0.7])

    Returns
    -------
    float or ndarray : Amplification intensity (fraction of baseline)
    """
    return kappa_c * (1.0 - eta * alpha)


# ---------------------------------------------------------------------------
# Section 2.3 — Bullwhip Dampening and Waste Reduction Proxy
# ---------------------------------------------------------------------------

def waste_reduction(alpha, eta=0.5):
    """
    Structural overproduction dampening proxy.

    WasteRed(alpha, eta) = 100 * eta * alpha

    IMPORTANT: This is a first-order structural proxy for overproduction
    dampening via bullwhip compression. It does NOT represent:
      - An empirical waste measurement
      - An LCA-derived quantity
      - End-of-life circular loop waste reduction

    The eta range [0.3, 0.7] is grounded in:
      - Lee, Padmanabhan & Whang (1997): variance amplification 1.5x-4x+
      - Chen et al. (2000): quantified bullwhip in simple supply chains
      - Disney & Towill (2003): 20-50% variance reduction from lead-time
        compression interventions (VMI, information sharing)

    Parameters
    ----------
    alpha : float or ndarray  Localization share
    eta   : float             Dampening coefficient (default 0.5)

    Returns
    -------
    float or ndarray : Directional waste reduction (%) — structural proxy only
    """
    return 100.0 * eta * alpha


# ---------------------------------------------------------------------------
# Section 2.5 — Coordination Complexity Score
# ---------------------------------------------------------------------------

# Ordinal CCS mapping: alpha level → CCS value and description
CCS_LEVELS = {
    0.00: (1, "Centralized baseline: single governance layer, standardized IT, no inter-node sync"),
    0.25: (2, "25% distributed: regional node integration, limited IT interoperability, modest overhead"),
    0.35: (3, "35% distributed: multi-node governance, reverse logistics coordination, high sync burden"),
    0.50: (4, "50% distributed: full circular node integration, real-time cross-node flows required"),
}

def coordination_complexity_score(alpha):
    """
    Ordinal Coordination Complexity Score (CCS).

    CCS is a qualitative structural index only. It is NOT a cost model.
    Values are ordinal; differences are not proportional.

    Parameters
    ----------
    alpha : float  Localization share (must be one of {0, 0.25, 0.35, 0.50})

    Returns
    -------
    int : CCS value (1-4)
    str : Operational description
    """
    # Find nearest scenario level
    closest = min(CCS_LEVELS.keys(), key=lambda k: abs(k - alpha))
    return CCS_LEVELS[closest]


# ---------------------------------------------------------------------------
# Scenario runner
# ---------------------------------------------------------------------------

def run_scenario(alpha, R, delta_R, lvrr_base, J_base, m, eta=0.5, gamma=0.6):
    """
    Run a single DHSCM scenario and return all key metrics.

    Parameters
    ----------
    alpha     : float  Localization share
    R         : float  Total metro retail expenditure (USD billions)
    delta_R   : float  Localizable revenue pool (USD billions)
    lvrr_base : float  Baseline LVRR
    J_base    : float  Baseline employment
    m         : float  Employment multiplier (jobs per $1M)
    eta       : float  Dampening coefficient (default 0.5)
    gamma     : float  Recovery speed coefficient (default 0.6)

    Returns
    -------
    dict : All scenario metrics
    """
    ccs_val, ccs_desc = coordination_complexity_score(alpha)
    return {
        "alpha": alpha,
        "LVRR": round(lvrr(alpha, R, delta_R, lvrr_base), 4),
        "delta_RL_M": round(delta_RL(alpha, delta_R) * 1e3, 1),   # $M
        "delta_employment": round(delta_employment(alpha, delta_R, m)),
        "waste_pct": round(waste_reduction(alpha, eta), 1),
        "recovery_pct": round(recovery_reduction_pct(alpha, gamma), 1),
        "CCS": ccs_val,
        "CCS_description": ccs_desc,
        "redundancy_index": round(redundancy_index(alpha), 3),
        "recovery_time_ratio": round(recovery_speed(alpha, gamma=gamma), 3),
    }
