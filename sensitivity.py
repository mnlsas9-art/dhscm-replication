"""
sensitivity.py
==============
Sensitivity analysis for the DHSCM model.

Covers:
  - LVRR sensitivity over R and delta_R
  - Labor Stabilization Threshold sensitivity over m and delta_R
  - WasteRed sensitivity over eta
  - Recovery sensitivity over gamma
  - Cross-metro sensitivity comparison

Usage:
    python src/sensitivity.py
"""

import os
import sys
import numpy as np
import csv

sys.path.insert(0, os.path.dirname(__file__))
from dhscm_model import (lvrr, labor_stabilization_threshold,
                          waste_reduction, recovery_reduction_pct)
from calibration import METRO_BENCHMARKS, SENSITIVITY

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALPHA_RANGE = np.linspace(0, 0.60, 200)
THETA_RANGE = np.linspace(0.05, 0.30, 200)


def lvrr_sensitivity(metro_key="stylized"):
    """
    LVRR sensitivity over R and delta_R ranges.
    Returns alpha array, midline, lower bound, upper bound.
    """
    m = METRO_BENCHMARKS[metro_key]
    R_low  = m["R"] * 0.80
    R_mid  = m["R"]
    R_high = m["R"] * 1.20
    dR_low  = m["delta_R"] * 0.833
    dR_mid  = m["delta_R"]
    dR_high = m["delta_R"] * 1.167

    mid   = lvrr(ALPHA_RANGE, R_mid,  dR_mid,  m["lvrr_base"])
    low   = lvrr(ALPHA_RANGE, R_high, dR_low,  m["lvrr_base"])   # worst case
    high  = lvrr(ALPHA_RANGE, R_low,  dR_high, m["lvrr_base"])   # best case
    return ALPHA_RANGE, mid, low, high


def lst_sensitivity(metro_key="stylized"):
    """
    Labor Stabilization Threshold sensitivity over m and delta_R.
    Returns theta array, midline, lower, upper.
    """
    m = METRO_BENCHMARKS[metro_key]
    lst_mid  = labor_stabilization_threshold(THETA_RANGE, m["J_base"], m["m_mid"],  m["delta_R"])
    lst_low  = labor_stabilization_threshold(THETA_RANGE, m["J_base"], m["m_high"], m["delta_R"] * 1.167)
    lst_high = labor_stabilization_threshold(THETA_RANGE, m["J_base"], m["m_low"],  m["delta_R"] * 0.833)
    return THETA_RANGE, lst_mid, lst_low, lst_high


def waste_sensitivity():
    """WasteRed sensitivity over eta range."""
    eta_low, eta_mid, eta_high = SENSITIVITY["eta"]
    return (ALPHA_RANGE,
            waste_reduction(ALPHA_RANGE, eta_mid),
            waste_reduction(ALPHA_RANGE, eta_low),
            waste_reduction(ALPHA_RANGE, eta_high))


def recovery_sensitivity():
    """Recovery reduction sensitivity over gamma range."""
    g_low, g_mid, g_high = SENSITIVITY["gamma"]
    return (ALPHA_RANGE,
            recovery_reduction_pct(ALPHA_RANGE, g_mid),
            recovery_reduction_pct(ALPHA_RANGE, g_low),
            recovery_reduction_pct(ALPHA_RANGE, g_high))


def cross_metro_lvrr():
    """LVRR curves for all three metros at their midpoint calibrations."""
    curves = {}
    for key, metro in METRO_BENCHMARKS.items():
        curves[key] = lvrr(ALPHA_RANGE, metro["R"], metro["delta_R"], metro["lvrr_base"])
    return ALPHA_RANGE, curves


def cross_metro_lst():
    """LST curves for all three metros."""
    curves = {}
    for key, metro in METRO_BENCHMARKS.items():
        curves[key] = labor_stabilization_threshold(
            THETA_RANGE, metro["J_base"], metro["m_mid"], metro["delta_R"]
        )
    return THETA_RANGE, curves


def save_sensitivity_csv():
    """Save all sensitivity arrays to CSV for independent verification."""
    path = os.path.join(OUTPUT_DIR, "sensitivity_arrays.csv")
    alpha, waste_mid, waste_low, waste_high = waste_sensitivity()
    _, rec_mid, rec_low, rec_high = recovery_sensitivity()
    _, lvrr_mid_s, lvrr_low_s, lvrr_high_s = lvrr_sensitivity("stylized")
    _, lvrr_mid_ny, lvrr_low_ny, lvrr_high_ny = lvrr_sensitivity("new_york")
    _, lvrr_mid_la, lvrr_low_la, lvrr_high_la = lvrr_sensitivity("los_angeles")

    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "alpha",
            "waste_mid_eta0.5", "waste_low_eta0.3", "waste_high_eta0.7",
            "recovery_mid_gamma0.6", "recovery_low_gamma0.5", "recovery_high_gamma0.7",
            "lvrr_stylized_mid", "lvrr_stylized_low", "lvrr_stylized_high",
            "lvrr_new_york_mid", "lvrr_new_york_low", "lvrr_new_york_high",
            "lvrr_los_angeles_mid", "lvrr_los_angeles_low", "lvrr_los_angeles_high",
        ])
        for i in range(len(alpha)):
            writer.writerow([
                round(alpha[i], 4),
                round(waste_mid[i], 3), round(waste_low[i], 3), round(waste_high[i], 3),
                round(rec_mid[i], 3), round(rec_low[i], 3), round(rec_high[i], 3),
                round(lvrr_mid_s[i], 4), round(lvrr_low_s[i], 4), round(lvrr_high_s[i], 4),
                round(lvrr_mid_ny[i], 4), round(lvrr_low_ny[i], 4), round(lvrr_high_ny[i], 4),
                round(lvrr_mid_la[i], 4), round(lvrr_low_la[i], 4), round(lvrr_high_la[i], 4),
            ])
    print(f"  Saved sensitivity arrays: {path}")

    # LST arrays
    path2 = os.path.join(OUTPUT_DIR, "sensitivity_lst_arrays.csv")
    theta, lst_curves = cross_metro_lst()
    _, lst_mid_s, lst_low_s, lst_high_s = lst_sensitivity("stylized")
    with open(path2, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["theta", "lst_stylized_mid", "lst_stylized_low", "lst_stylized_high",
                          "lst_new_york_mid", "lst_los_angeles_mid"])
        for i in range(len(theta)):
            writer.writerow([
                round(theta[i], 4),
                round(lst_mid_s[i], 4), round(lst_low_s[i], 4), round(lst_high_s[i], 4),
                round(lst_curves["new_york"][i], 4),
                round(lst_curves["los_angeles"][i], 4),
            ])
    print(f"  Saved LST arrays: {path2}")


def print_key_sensitivity_points():
    """Print key sensitivity check points at alpha = 0.25 and 0.35."""
    print("\n  Sensitivity check at alpha = 0.25:")
    print(f"    WasteRed (eta=0.3): {waste_reduction(0.25, 0.3):.1f}%  "
          f"(eta=0.5): {waste_reduction(0.25, 0.5):.1f}%  "
          f"(eta=0.7): {waste_reduction(0.25, 0.7):.1f}%")
    print(f"    Recovery (gamma=0.5): {recovery_reduction_pct(0.25, 0.5):.1f}%  "
          f"(gamma=0.6): {recovery_reduction_pct(0.25, 0.6):.1f}%  "
          f"(gamma=0.7): {recovery_reduction_pct(0.25, 0.7):.1f}%")

    print("\n  Sensitivity check at alpha = 0.35:")
    print(f"    WasteRed (eta=0.3): {waste_reduction(0.35, 0.3):.1f}%  "
          f"(eta=0.5): {waste_reduction(0.35, 0.5):.1f}%  "
          f"(eta=0.7): {waste_reduction(0.35, 0.7):.1f}%")
    print(f"    Recovery (gamma=0.5): {recovery_reduction_pct(0.35, 0.5):.1f}%  "
          f"(gamma=0.6): {recovery_reduction_pct(0.35, 0.6):.1f}%  "
          f"(gamma=0.7): {recovery_reduction_pct(0.35, 0.7):.1f}%")

    print("\n  LST at theta=0.15 across metros:")
    for key, metro in METRO_BENCHMARKS.items():
        lst_val = labor_stabilization_threshold(0.15, metro["J_base"], metro["m_mid"], metro["delta_R"])
        print(f"    {metro['name'][:40]}: alpha_min = {lst_val:.3f}")


if __name__ == "__main__":
    print("\nDHSCM Sensitivity Analysis")
    print("Mudiganti (2026), Frontiers in Sustainability, MS-ID 1820269\n")
    print_key_sensitivity_points()
    save_sensitivity_csv()
    print("\nDone. Arrays saved for independent verification and plot generation.")
