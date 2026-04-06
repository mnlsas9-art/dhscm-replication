"""
run_scenarios.py
================
Generate DHSCM scenario tables for all metro benchmarks.
Reproduces Table 1 from the manuscript and extends it to NY and LA MSAs.

Usage:
    python src/run_scenarios.py

Outputs (saved to outputs/):
    - scenarios_stylized.csv
    - scenarios_new_york.csv
    - scenarios_los_angeles.csv
    - scenarios_comparative.csv  (all three metros at alpha=0.25, 0.35)
    - console summary table
"""

import os
import sys
import csv

sys.path.insert(0, os.path.dirname(__file__))
from dhscm_model import run_scenario
from calibration import METRO_BENCHMARKS, SCENARIO_ALPHAS, SENSITIVITY

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_metro(key, metro, alphas=SCENARIO_ALPHAS, eta=0.5, gamma=0.6):
    """Run all scenarios for a given metro benchmark."""
    results = []
    for alpha in alphas:
        r = run_scenario(
            alpha=alpha,
            R=metro["R"],
            delta_R=metro["delta_R"],
            lvrr_base=metro["lvrr_base"],
            J_base=metro["J_base"],
            m=metro["m_mid"],
            eta=eta,
            gamma=gamma,
        )
        r["metro"] = key
        r["metro_name"] = metro["name"]
        results.append(r)
    return results


def format_table(results, metro_name):
    """Print a formatted scenario table to console."""
    print(f"\n{'='*80}")
    print(f"  {metro_name}")
    print(f"{'='*80}")
    print(f"{'Alpha':>8} {'LVRR':>8} {'ΔR_L ($M)':>12} {'ΔEmployment':>14} "
          f"{'Waste (%)':>11} {'Recovery (%)':>14} {'CCS':>6}")
    print(f"{'-'*80}")
    for r in results:
        label = "Centralized" if r["alpha"] == 0.0 else f"DHSCM-{int(r['alpha']*100)}"
        print(f"  {label:<12} {r['alpha']:>4.2f}  {r['LVRR']:>8.3f}  "
              f"{r['delta_RL_M']:>10,.0f}  {r['delta_employment']:>14,.0f}  "
              f"{r['waste_pct']:>9.1f}%  {r['recovery_pct']:>12.1f}%  {r['CCS']:>5}")
    print()


def save_csv(results, filename):
    """Save results to CSV."""
    if not results:
        return
    path = os.path.join(OUTPUT_DIR, filename)
    keys = ["metro", "alpha", "LVRR", "delta_RL_M", "delta_employment",
            "waste_pct", "recovery_pct", "CCS", "redundancy_index",
            "recovery_time_ratio"]
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    print(f"  Saved: {path}")


def comparative_summary(all_results):
    """Print comparative table for alpha=0.25 and 0.35 across metros."""
    print(f"\n{'='*90}")
    print("  COMPARATIVE SCENARIO RESULTS — alpha = 0.25 and 0.35")
    print(f"{'='*90}")
    print(f"{'Metro':<28} {'Alpha':>6} {'LVRR':>8} {'ΔEmpl.':>10} "
          f"{'Waste%':>8} {'Rec.%':>8} {'LVRR_base':>10} {'J_base':>10}")
    print(f"{'-'*90}")
    for key, metro, results in all_results:
        for r in results:
            if r["alpha"] in (0.25, 0.35):
                print(f"  {metro['name'][:26]:<26} {r['alpha']:>6.2f}  "
                      f"{r['LVRR']:>7.3f}  {r['delta_employment']:>9,.0f}  "
                      f"{r['waste_pct']:>7.1f}%  {r['recovery_pct']:>7.1f}%  "
                      f"{metro['lvrr_base']:>9.2f}  {metro['J_base']:>9,}")


def main():
    print("\nDHSCM Replication Package — Scenario Generator")
    print("Mudiganti (2026), Frontiers in Sustainability, MS-ID 1820269")
    print("Model outputs are directional structural projections under stated assumptions.")

    all_results_flat = []
    all_for_comparison = []

    for key, metro in METRO_BENCHMARKS.items():
        print(f"\nRunning: {metro['name']}")
        print(f"  R=${metro['R']}B | delta_R=${metro['delta_R']}B | "
              f"J_base={metro['J_base']:,} | m={metro['m_mid']}")
        print(f"  Source: {metro['data_note']}")

        results = run_metro(key, metro)
        format_table(results, metro["name"])
        save_csv(results, f"scenarios_{key}.csv")
        all_results_flat.extend(results)
        all_for_comparison.append((key, metro, results))

    # Comparative summary
    comparative_summary(all_for_comparison)

    # Save combined CSV
    save_csv(all_results_flat, "scenarios_all_metros.csv")

    # Key finding summary
    print(f"\n{'='*80}")
    print("  KEY STRUCTURAL FINDINGS (alpha = 0.35, eta=0.5, gamma=0.6)")
    print(f"{'='*80}")
    for key, metro, results in all_for_comparison:
        r35 = next(r for r in results if r["alpha"] == 0.35)
        print(f"\n  {metro['name']}")
        print(f"    LVRR: {metro['lvrr_base']:.2f} → {r35['LVRR']:.3f} "
              f"(+{(r35['LVRR']-metro['lvrr_base'])*100:.1f}pp)")
        print(f"    Additional employment: {r35['delta_employment']:,.0f} jobs")
        print(f"    Retained revenue: ${r35['delta_RL_M']:,.0f}M")
        print(f"    Overproduction dampening proxy: {r35['waste_pct']:.1f}%")
        print(f"    Recovery time reduction: {r35['recovery_pct']:.1f}%")
        print(f"    Coordination Complexity: CCS={r35['CCS']} (ordinal index, not cost model)")

    print(f"\n{'='*80}")
    print("  NOTE: The hybrid equilibrium range alpha ≈ 0.25-0.35 is robust")
    print("  across all three metro calibrations, though absolute employment")
    print("  and retention magnitudes differ substantially by metro scale.")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
