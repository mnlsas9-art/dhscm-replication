"""
plots.py
========
Reproduce all manuscript figures and generate new comparative metro figures.

Figures produced:
  Fig 2: LVRR vs alpha — stylized (manuscript original)
  Fig 3: LST vs theta  — stylized (manuscript original)
  Fig 4: WasteRed vs alpha — stylized (manuscript original)
  Fig 6: LVRR comparison across all three metros (NEW)
  Fig 7: Employment at alpha=0.25 and 0.35 — all metros (NEW)
  Fig 8: LST comparison across all three metros (NEW)

Usage:
    python src/plots.py

Outputs saved to outputs/figures/
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.dirname(__file__))
from sensitivity import (lvrr_sensitivity, lst_sensitivity, waste_sensitivity,
                          recovery_sensitivity, cross_metro_lvrr, cross_metro_lst,
                          ALPHA_RANGE, THETA_RANGE)
from dhscm_model import delta_employment, labor_stabilization_threshold
from calibration import METRO_BENCHMARKS, SCENARIO_ALPHAS

FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Style settings — clean academic style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.linewidth': 0.8,
    'axes.grid': True,
    'grid.alpha': 0.35,
    'grid.linestyle': '--',
    'lines.linewidth': 2.0,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

METRO_COLORS = {
    "stylized":    "#2C6FAC",
    "new_york":    "#B44040",
    "los_angeles": "#3A8A55",
}
METRO_LABELS = {
    "stylized":    "Stylized mid-sized metro",
    "new_york":    "New York-NJ-PA MSA",
    "los_angeles": "Los Angeles-LB-Anaheim MSA",
}
SCENARIO_POINTS = [0.00, 0.25, 0.35, 0.50]

DISCLAIMER = (
    "Note: All values are model-derived structural projections\n"
    "under stated assumptions, not empirical measurements."
)


# ---------------------------------------------------------------------------
# Figure 2 — LVRR vs alpha (stylized, manuscript original)
# ---------------------------------------------------------------------------
def fig_lvrr_stylized():
    alpha, mid, low, high = lvrr_sensitivity("stylized")
    m = METRO_BENCHMARKS["stylized"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.fill_between(alpha, low, high, alpha=0.15, color=METRO_COLORS["stylized"],
                    label="Sensitivity band")
    ax.plot(alpha, low,  color=METRO_COLORS["stylized"], lw=1.2, ls='--')
    ax.plot(alpha, high, color=METRO_COLORS["stylized"], lw=1.2, ls='--')
    ax.plot(alpha, mid,  color=METRO_COLORS["stylized"], lw=2.5,
            label=f"Calibrated (R=${m['R']}B, ΔR=${m['delta_R']}B)")

    pts_alpha = [a for a in SCENARIO_POINTS]
    pts_lvrr  = [m["lvrr_base"] + a * m["delta_R"] / m["R"] for a in pts_alpha]
    ax.scatter(pts_alpha, pts_lvrr, color='black', zorder=5, s=40, label="Scenario points")

    ax.set_xlabel("Localization share α")
    ax.set_ylabel("LVRR(α)")
    ax.set_xlim(0, 0.60); ax.set_ylim(0.10, 0.42)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Fig 2. Local Value Retention Ratio — Stylized Benchmark", fontsize=11)
    ax.text(0.98, 0.03, DISCLAIMER, transform=ax.transAxes,
            fontsize=7, ha='right', va='bottom', color='gray', style='italic')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig2_lvrr_stylized.png")
    plt.savefig(path); plt.close()
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 3 — LST vs theta (stylized, manuscript original)
# ---------------------------------------------------------------------------
def fig_lst_stylized():
    theta, mid, low, high = lst_sensitivity("stylized")
    m = METRO_BENCHMARKS["stylized"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.fill_between(theta, low, high, alpha=0.15, color=METRO_COLORS["stylized"],
                    label="Sensitivity band")
    ax.plot(theta, low,  color=METRO_COLORS["stylized"], lw=1.2, ls='--')
    ax.plot(theta, high, color=METRO_COLORS["stylized"], lw=1.2, ls='--')
    ax.plot(theta, mid,  color=METRO_COLORS["stylized"], lw=2.5,
            label=f"Calibrated (m={m['m_mid']}, ΔR=${m['delta_R']}B)")
    ax.axvline(0.15, color='gray', ls=':', lw=1.5, label="θ=0.15 reference")

    ax.set_xlabel("Automation displacement rate θ")
    ax.set_ylabel("Minimum localization α_min")
    ax.set_xlim(0.05, 0.30); ax.set_ylim(0, 0.45)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title(f"Fig 3. Labor Stabilization Threshold — Stylized Benchmark\n"
                 f"(J_base={m['J_base']:,}; θ treated as exogenous)", fontsize=11)
    ax.text(0.98, 0.03, DISCLAIMER, transform=ax.transAxes,
            fontsize=7, ha='right', va='bottom', color='gray', style='italic')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig3_lst_stylized.png")
    plt.savefig(path); plt.close()
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 4 — WasteRed vs alpha (manuscript original)
# ---------------------------------------------------------------------------
def fig_waste():
    alpha, mid, low, high = waste_sensitivity()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.fill_between(alpha, low, high, alpha=0.15, color="#7B4FAB",
                    label="Sensitivity band η∈[0.3, 0.7]")
    ax.plot(alpha, low,  color="#7B4FAB", lw=1.2, ls='--')
    ax.plot(alpha, high, color="#7B4FAB", lw=1.2, ls='--')
    ax.plot(alpha, mid,  color="#7B4FAB", lw=2.5, label="Calibrated (η=0.5)")

    for a in [0.25, 0.35, 0.50]:
        ax.scatter([a], [mid[np.argmin(np.abs(alpha - a))]], color='black', zorder=5, s=40)

    ax.set_xlabel("Localization share α")
    ax.set_ylabel("Overproduction dampening proxy (%)")
    ax.set_xlim(0, 0.60); ax.set_ylim(0, 50)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Fig 4. Structural Overproduction Dampening Proxy\n"
                 "(Bullwhip compression only; NOT end-of-life circular loop waste)", fontsize=11)
    ax.text(0.98, 0.03, DISCLAIMER, transform=ax.transAxes,
            fontsize=7, ha='right', va='bottom', color='gray', style='italic')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig4_waste_reduction.png")
    plt.savefig(path); plt.close()
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 6 — LVRR comparison across all three metros (NEW)
# ---------------------------------------------------------------------------
def fig_lvrr_comparative():
    alpha, curves = cross_metro_lvrr()

    fig, ax = plt.subplots(figsize=(9, 5))
    for key, curve in curves.items():
        ax.plot(alpha, curve, color=METRO_COLORS[key], lw=2.5,
                label=METRO_LABELS[key])
        # Mark alpha=0.25 and 0.35 points
        for a in [0.25, 0.35]:
            idx = np.argmin(np.abs(alpha - a))
            ax.scatter([a], [curve[idx]], color=METRO_COLORS[key], zorder=5, s=40)

    # Shade hybrid equilibrium zone
    ax.axvspan(0.25, 0.35, alpha=0.08, color='gold', label="Candidate equilibrium zone\nα ∈ [0.25, 0.35]")

    ax.set_xlabel("Localization share α")
    ax.set_ylabel("LVRR(α)")
    ax.set_xlim(0, 0.60)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Fig 6. LVRR Comparison Across Three Metro Calibrations\n"
                 "(Absolute LVRR gains comparable; baseline levels differ by metro structure)", fontsize=11)
    ax.text(0.98, 0.03, DISCLAIMER, transform=ax.transAxes,
            fontsize=7, ha='right', va='bottom', color='gray', style='italic')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig6_lvrr_comparative.png")
    plt.savefig(path); plt.close()
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 7 — Employment at alpha=0.25 and 0.35 across metros (NEW)
# ---------------------------------------------------------------------------
def fig_employment_comparative():
    alphas = [0.25, 0.35]
    metro_keys = list(METRO_BENCHMARKS.keys())
    x = np.arange(len(alphas))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, key in enumerate(metro_keys):
        m = METRO_BENCHMARKS[key]
        jobs = [delta_employment(a, m["delta_R"], m["m_mid"]) for a in alphas]
        bars = ax.bar(x + i * width, jobs, width, label=METRO_LABELS[key],
                      color=METRO_COLORS[key], alpha=0.85)
        # Sensitivity whiskers (m_low to m_high)
        jobs_low  = [delta_employment(a, m["delta_R"], m["m_low"])  for a in alphas]
        jobs_high = [delta_employment(a, m["delta_R"], m["m_high"]) for a in alphas]
        err_low  = [j - jl for j, jl in zip(jobs, jobs_low)]
        err_high = [jh - j for j, jh in zip(jobs, jobs_high)]
        ax.errorbar(x + i * width, jobs,
                    yerr=[err_low, err_high],
                    fmt='none', color='black', capsize=4, lw=1.5)

    ax.set_xlabel("Localization share α")
    ax.set_ylabel("Incremental employment (jobs)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([f"α = {a}" for a in alphas])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Fig 7. Model-Projected Employment Generation Across Metro Calibrations\n"
                 "(Bars = midpoint m; whiskers = m_low to m_high sensitivity range)", fontsize=11)
    ax.text(0.98, 0.03, DISCLAIMER, transform=ax.transAxes,
            fontsize=7, ha='right', va='bottom', color='gray', style='italic')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig7_employment_comparative.png")
    plt.savefig(path); plt.close()
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Figure 8 — LST comparison across metros (NEW)
# ---------------------------------------------------------------------------
def fig_lst_comparative():
    theta, curves = cross_metro_lst()

    fig, ax = plt.subplots(figsize=(9, 5))
    for key, curve in curves.items():
        ax.plot(theta, curve, color=METRO_COLORS[key], lw=2.5,
                label=METRO_LABELS[key])

    ax.axvline(0.15, color='gray', ls=':', lw=1.5, label="θ=0.15 reference")
    ax.axhline(0.35, color='brown', ls=':', lw=1.0, alpha=0.5,
               label="Hybrid equilibrium upper bound (α=0.35)")

    ax.set_xlabel("Automation displacement rate θ")
    ax.set_ylabel("Minimum localization α_min")
    ax.set_xlim(0.05, 0.30); ax.set_ylim(0, 0.30)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Fig 8. Labor Stabilization Threshold Across Metro Calibrations\n"
                 "(θ treated as exogenous; curves reflect J_base, m, and ΔR differences)", fontsize=11)
    ax.text(0.98, 0.03, DISCLAIMER, transform=ax.transAxes,
            fontsize=7, ha='right', va='bottom', color='gray', style='italic')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig8_lst_comparative.png")
    plt.savefig(path); plt.close()
    print(f"  Saved: {path}")


def main():
    print("\nGenerating all figures...")
    fig_lvrr_stylized()
    fig_lst_stylized()
    fig_waste()
    fig_lvrr_comparative()
    fig_employment_comparative()
    fig_lst_comparative()
    print(f"\nAll figures saved to: {FIG_DIR}")


if __name__ == "__main__":
    main()
