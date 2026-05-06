import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mstats
import os

os.makedirs("figures", exist_ok=True)

merged = pd.read_csv("processed/merged_pls_acs.csv", low_memory=False)
fe = merged[merged["pop_lsa"].notna() & (merged["pop_lsa"] > 0)].copy()

PC_PAIRS = [
    ("visits",                "visits_pc"),
    ("total_circ",            "circ_pc"),
    ("registered_borrowers",  "regbor_pc"),
    ("total_programs",        "programs_pc"),
    ("total_attendance",      "attendance_pc"),
    ("hrs_open",              "hrs_open_pc"),
    ("public_internet_terminals", "terminals_pc"),
    ("wifi_sessions",         "wifi_pc"),
    ("total_opex",            "opex_pc"),
    ("total_income",          "income_pc"),
    ("total_staff_fte",       "staff_fte_pc"),
]
for raw_col, pc_col in PC_PAIRS:
    fe[pc_col] = fe[raw_col] / fe["pop_lsa"]

PC_COLS = [pc for _, pc in PC_PAIRS]
LOG_TARGETS = PC_COLS + ["visits", "total_circ", "total_opex", "median_hh_income", "per_capita_income"]
for col in LOG_TARGETS:
    if col in fe.columns:
        fe[f"log_{col}"] = np.log1p(fe[col].clip(lower=0))

fe["cost_per_visit"]         = fe["total_opex"] / fe["visits"].replace(0, np.nan)
fe["cost_per_circ"]          = fe["total_opex"] / fe["total_circ"].replace(0, np.nan)
fe["circ_per_visit"]         = fe["total_circ"] / fe["visits"].replace(0, np.nan)
fe["digital_share_circ"]     = fe["elec_mat_circ"] / fe["total_circ"].replace(0, np.nan)
fe["staff_per_1k_pop"]       = fe["total_staff_fte"] / fe["pop_lsa"] * 1000
fe["attendance_per_program"] = fe["total_attendance"] / fe["total_programs"].replace(0, np.nan)

def winsorize_col(series, limits=(0.01, 0.01)):
    clean = series.dropna()
    if len(clean) == 0:
        return series
    arr = mstats.winsorize(clean, limits=limits)
    result = series.copy()
    result[series.notna()] = arr
    return result

derived = ["cost_per_visit", "cost_per_circ", "circ_per_visit",
           "digital_share_circ", "staff_per_1k_pop", "attendance_per_program"]
for col in PC_COLS + derived:
    if col in fe.columns:
        fe[f"w_{col}"] = winsorize_col(fe[col])

fe.to_csv("processed/features_pls_acs.csv", index=False)
print(f"Saved: processed/features_pls_acs.csv - {fe.shape[0]:,} rows x {fe.shape[1]} columns")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
if "visits_pc" in fe.columns:
    fe["visits_pc"].dropna().hist(bins=80, ax=axes[0], color="steelblue", alpha=0.8)
axes[0].set_title("visits_pc (raw)"); axes[0].set_xlabel("Visits per capita")
if "w_visits_pc" in fe.columns:
    fe["w_visits_pc"].dropna().hist(bins=80, ax=axes[1], color="coral", alpha=0.8)
axes[1].set_title("visits_pc (winsorized 1-99%)"); axes[1].set_xlabel("Visits per capita")
plt.tight_layout()
plt.savefig("figures/fig_winsorize_comparison.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: figures/fig_winsorize_comparison.png")