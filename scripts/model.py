import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats.mstats import winsorize
import os

os.makedirs("figures", exist_ok=True)

fe = pd.read_csv("processed/features_pls_acs.csv", low_memory=False)

PREDICTORS = {
    "poverty_rate_all_pct":    "Poverty Rate (%)",
    "unemployment_rate_pct":   "Unemployment Rate (%)",
    "median_hh_income":        "Median HH Income ($)",
    "snap_pct":                "SNAP Recipients (%)",
    "work_from_home_pct":      "Work From Home (%)",
    "opex_pc":                 "Operating Expenditure / Capita ($)",
    "staff_per_1k_pop":        "Staff per 1,000 Population",
    "hrs_open":                "Annual Hours Open",
}
TARGET = "log_visits_pc"

if TARGET not in fe:
    base = "w_visits_pc" if "w_visits_pc" in fe else "visits_pc"
    fe[TARGET] = np.log1p(fe[base].clip(lower=0))

fe["locale"] = pd.cut(
    fe["pop_lsa"],
    bins=[0, 25_000, 250_000, float("inf")],
    labels=["Rural", "Suburban", "Urban"]
)

cols = [TARGET] + list(PREDICTORS)
mdf = fe[cols].dropna().copy()

for col in ["opex_pc", "staff_per_1k_pop", "hrs_open"]:
    if col in mdf:
        mdf[col] = winsorize(mdf[col], limits=(0.01, 0.01))

mdf = (mdf - mdf.mean()) / mdf.std()
mdf["locale"] = fe["locale"]

X = sm.add_constant(mdf[list(PREDICTORS)])
y = mdf[TARGET]
model = sm.OLS(y, X).fit(cov_type="HC3")
print(model.summary2())

coef_df = pd.DataFrame({
    "coef":  model.params[1:],
    "ci_lo": model.conf_int()[0][1:],
    "ci_hi": model.conf_int()[1][1:],
    "pval":  model.pvalues[1:]
})
coef_df.index = [PREDICTORS[c] for c in coef_df.index]
coef_df["sig"] = coef_df["pval"].apply(
    lambda p: "***" if p<0.001 else ("**" if p<0.01 else ("*" if p<0.05 else ""))
)
coef_df = coef_df.sort_values("coef")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    coef_df.index, coef_df["coef"],
    color=["steelblue" if c >= 0 else "firebrick" for c in coef_df["coef"]],
    xerr=[coef_df["coef"] - coef_df["ci_lo"], coef_df["ci_hi"] - coef_df["coef"]],
    capsize=4
)
ax.axvline(0, color="black", linestyle="--", lw=0.8)
ax.set_xlabel("Standardized beta (effect of 1 SD change)")
ax.set_title("OLS Coefficients (95% CI)")
for i, (_, row) in enumerate(coef_df.iterrows()):
    if row["sig"]:
        ax.text(row["ci_hi"] + 0.01, i, row["sig"], va="center")
plt.tight_layout()
plt.savefig("figures/fig_ols_coefficients.png", dpi=130, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_ols_coefficients.png")

CORE_PREDS  = ["poverty_rate_all_pct", "unemployment_rate_pct", "median_hh_income"]
CORE_LABELS = {
    "poverty_rate_all_pct":  "Poverty Rate",
    "unemployment_rate_pct": "Unemployment Rate",
    "median_hh_income":      "Median HH Income",
}

results = []
for loc in ["Rural", "Suburban", "Urban"]:
    sub = mdf[mdf["locale"] == loc][CORE_PREDS + [TARGET]].dropna()
    m = sm.OLS(sub[TARGET], sm.add_constant(sub[CORE_PREDS])).fit(cov_type="HC3")
    for pred in CORE_PREDS:
        results.append({
            "locale":    loc,
            "predictor": CORE_LABELS[pred],
            "coef":      m.params[pred],
            "ci_lo":     m.conf_int().loc[pred, 0],
            "ci_hi":     m.conf_int().loc[pred, 1],
        })

res_df = pd.DataFrame(results)
fig, ax = plt.subplots(figsize=(9, 5))
colors  = {"Rural": "#2c7bb6", "Suburban": "#f4a261", "Urban": "#d7191c"}
offsets = {"Rural": -0.25, "Suburban": 0, "Urban": 0.25}
x = range(len(CORE_LABELS))

for loc in ["Rural", "Suburban", "Urban"]:
    sub = res_df[res_df["locale"] == loc]
    pos = [i + offsets[loc] for i in x]
    ax.bar(pos, sub["coef"], 0.25, label=loc, color=colors[loc], alpha=0.85)
    ax.errorbar(pos, sub["coef"],
                yerr=[sub["coef"] - sub["ci_lo"], sub["ci_hi"] - sub["coef"]],
                fmt="none", ecolor="gray", capsize=4)

ax.set_xticks(list(x))
ax.set_xticklabels(list(CORE_LABELS.values()))
ax.axhline(0, color="black", lw=0.8, linestyle="--")
ax.set_ylabel("Standardized beta")
ax.set_title("Effect of Socioeconomic Predictors by Locale")
ax.legend()
plt.tight_layout()
plt.savefig("figures/fig_locale_comparison.png", dpi=130, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_locale_comparison.png")