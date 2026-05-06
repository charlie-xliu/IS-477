import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

os.makedirs("figures", exist_ok=True)

merged = pd.read_csv("processed/merged_pls_acs.csv", low_memory=False)
df = merged[merged["pop_lsa"].notna() & (merged["pop_lsa"] > 0)].copy()

CORR_USAGE = ["visits", "total_circ", "registered_borrowers",
              "total_programs", "total_attendance",
              "hrs_open", "wifi_sessions", "internet_uses"]
CORR_SOC   = ["median_hh_income", "poverty_rate_all_pct",
              "unemployment_rate_pct", "per_capita_income",
              "snap_pct", "no_health_insurance_pct", "work_from_home_pct"]

corr_df = df[CORR_USAGE + CORR_SOC].copy()
for col in CORR_USAGE:
    corr_df[f"log_{col}"] = np.log1p(corr_df[col])

log_usage   = [f"log_{c}" for c in CORR_USAGE]
corr_matrix = corr_df[log_usage + CORR_SOC].corr(method="spearman")
cross_corr  = corr_matrix.loc[log_usage, CORR_SOC]

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(cross_corr, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, linewidths=0.5, ax=ax,
            yticklabels=[c.replace("log_", "") for c in log_usage])
ax.set_title("Spearman Correlation: Library Usage (log) x Socioeconomic Predictors", fontsize=13)
plt.tight_layout()
plt.savefig("figures/fig_correlation_heatmap.png", dpi=130, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_correlation_heatmap.png")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, (x, y, title) in zip(axes, [
    ("median_hh_income",     "visits",     "Median HH Income vs. Visits"),
    ("poverty_rate_all_pct", "total_circ", "Poverty Rate vs. Total Circulation"),
]):
    sub = df[[x, y]].dropna()
    ax.scatter(sub[x], np.log1p(sub[y]), alpha=0.25, s=10, color="steelblue")
    m, b, r, p, _ = stats.linregress(sub[x], np.log1p(sub[y]))
    xr = np.linspace(sub[x].min(), sub[x].max(), 200)
    ax.plot(xr, m*xr + b, color="firebrick", lw=2, label=f"r={r:.2f}, p={p:.3f}")
    ax.set_xlabel(x); ax.set_ylabel(f"log1p({y})")
    ax.set_title(title); ax.legend()
plt.tight_layout()
plt.savefig("figures/fig_scatter_preview.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_scatter_preview.png")

fig = plt.figure(figsize=(12, 7))
sns.scatterplot(data=df, x="local_govt_revenue", y="visits",
                hue="median_hh_income", palette="magma", alpha=0.5)
plt.xscale("log"); plt.yscale("log")
plt.title("Raw Funding vs. Raw Visits (Colored by Income)", fontsize=14)
plt.xlabel("Local Government Revenue ($)"); plt.ylabel("Total Annual Library Visits")
plt.legend(title="Median HH Income", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig("figures/fig_funding_vs_usage.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_funding_vs_usage.png")

USAGE_COLS = ["visits", "total_circ", "registered_borrowers",
              "total_programs", "total_attendance", "hrs_open",
              "public_internet_terminals", "wifi_sessions"]

fig, axes = plt.subplots(len(USAGE_COLS), 2, figsize=(14, len(USAGE_COLS) * 3))
for i, col in enumerate(USAGE_COLS):
    series = df[col].dropna()
    axes[i, 0].hist(series, bins=60, color="steelblue", edgecolor="none", alpha=0.8)
    axes[i, 0].set_title(f"{col} (raw)", fontsize=10)
    axes[i, 0].set_xlabel(col); axes[i, 0].set_ylabel("Count")
    axes[i, 1].hist(np.log1p(series), bins=60, color="coral", edgecolor="none", alpha=0.8)
    axes[i, 1].set_title(f"log1p({col})", fontsize=10)
    axes[i, 1].set_xlabel("log1p value"); axes[i, 1].set_ylabel("Count")
plt.tight_layout()
plt.savefig("figures/fig_distributions.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_distributions.png")