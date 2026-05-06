import pandas as pd
import numpy as np

PATH_ACS_META = "raw/ACSDP5Y2023.DP03-Column-Metadata.csv"
PATH_ACS_DATA = "raw/ACSDP5Y2023.DP03-Data.csv"
PATH_PLS_AE   = "raw/PLS_FY23_AE_pud23i.csv"
PATH_PLS_OUT  = "raw/pls_fy23_outlet_pud23i.csv"

acs_meta   = pd.read_csv(PATH_ACS_META)
acs_raw    = pd.read_csv(PATH_ACS_DATA, skiprows=[1], low_memory=False)
pls_raw    = pd.read_csv(PATH_PLS_AE, low_memory=False, encoding="latin1")
outlet_raw = pd.read_csv(PATH_PLS_OUT, low_memory=False, encoding="latin1")

ACS_KEEP = {
    "DP03_0005PE": "unemployment_rate_pct",
    "DP03_0062E":  "median_hh_income",
    "DP03_0063E":  "mean_hh_income",
    "DP03_0086E":  "per_capita_income",
    "DP03_0099PE": "poverty_rate_all_pct",
    "DP03_0100PE": "poverty_rate_under18_pct",
    "DP03_0101PE": "poverty_rate_18to64_pct",
    "DP03_0074PE": "snap_pct",
    "DP03_0096PE": "no_health_insurance_pct",
    "DP03_0042PE": "work_from_home_pct",
}
acs_sel = acs_raw[["GEO_ID", "NAME"] + list(ACS_KEEP.keys())].copy().rename(columns=ACS_KEEP)
acs_sel["county_fips"] = acs_sel["GEO_ID"].str.extract(r"US(\d{5})$")
acs_sel = acs_sel.drop(columns=["GEO_ID"])
for col in list(ACS_KEEP.values()):
    acs_sel[col] = pd.to_numeric(acs_sel[col], errors="coerce")

PLS_KEEP = {
    "STABR": "state", "FSCSKEY": "fscskey", "LIBID": "libid", "LIBNAME": "lib_name",
    "CNTY": "county_name", "LSAGEOID": "lsa_geoid", "LSAGEOTYPE": "lsa_geotype",
    "LONGITUD": "longitude", "LATITUDE": "latitude", "POPU_LSA": "pop_lsa",
    "LIBRARIA": "librarians_fte", "OTHPAID": "other_paid_fte", "TOTSTAFF": "total_staff_fte",
    "LOCGVT": "local_govt_revenue", "STGVT": "state_govt_revenue", "FEDGVT": "federal_revenue",
    "TOTINCM": "total_income", "SALARIES": "salaries_exp", "TOTOPEXP": "total_opex",
    "BKVOL": "print_volumes", "EBOOK": "ebook_titles", "VISITS": "visits",
    "TOTCIR": "total_circ", "KIDCIRCL": "kids_circ", "ELMATCIR": "elec_mat_circ",
    "REGBOR": "registered_borrowers", "ELINFO": "elec_info_retrievals",
    "ELCONT": "elec_content_uses", "GPTERMS": "public_internet_terminals",
    "PITUSR": "internet_uses", "WIFISESS": "wifi_sessions", "TOTPRO": "total_programs",
    "TOTATTEN": "total_attendance", "ONPRO": "online_programs", "OFFPRO": "inperson_programs",
    "HRS_OPEN": "hrs_open", "CENTLIB": "central_libs", "BRANLIB": "branch_libs",
    "BKMOB": "bookmobiles", "F_VISITS": "f_visits", "F_TOTCIR": "f_totcir",
    "F_REGBOR": "f_regbor", "F_TOTSTF": "f_totstf",
}
pls = pls_raw[list(PLS_KEEP.keys())].copy().rename(columns=PLS_KEEP)

NUMERIC_COLS = [
    "pop_lsa", "librarians_fte", "other_paid_fte", "total_staff_fte",
    "local_govt_revenue", "state_govt_revenue", "federal_revenue",
    "total_income", "salaries_exp", "total_opex", "print_volumes", "ebook_titles",
    "visits", "total_circ", "kids_circ", "elec_mat_circ", "registered_borrowers",
    "elec_info_retrievals", "elec_content_uses", "public_internet_terminals",
    "internet_uses", "wifi_sessions", "total_programs", "total_attendance",
    "online_programs", "inperson_programs", "hrs_open", "central_libs",
    "branch_libs", "bookmobiles",
]
pls[NUMERIC_COLS] = pls[NUMERIC_COLS].replace([-1, -3, -9], np.nan)

def derive_county_fips(row):
    if row["lsa_geotype"] == "COUNTY":
        try:
            return str(int(row["lsa_geoid"])).zfill(5)
        except (ValueError, TypeError):
            return np.nan
    return np.nan

pls["county_fips_direct"] = pls.apply(derive_county_fips, axis=1)
pls_raw_geo = pls_raw[["FSCSKEY", "CENTRACT", "LSAGEOTYPE"]].copy()
pls_raw_geo["CENTRACT"] = pls_raw_geo["CENTRACT"].astype(str).str.zfill(11)
pls_raw_geo["county_fips_tract"] = pls_raw_geo["CENTRACT"].str[:5]
pls_raw_geo.loc[~pls_raw_geo["county_fips_tract"].str.match(r"^\d{5}$"), "county_fips_tract"] = np.nan
pls = pls.merge(pls_raw_geo[["FSCSKEY", "county_fips_tract"]], left_on="fscskey", right_on="FSCSKEY", how="left")
pls["county_fips"] = pls["county_fips_direct"].fillna(pls["county_fips_tract"])

merged = pls.merge(acs_sel, on="county_fips", how="left", suffixes=("_pls", "_acs"))
print(f"Merged: {merged.shape}")

pls.to_csv("processed/pls_cleaned.csv", index=False)
acs_sel.to_csv("processed/acs_cleaned.csv", index=False)
merged.to_csv("processed/merged_pls_acs.csv", index=False)
print("Saved: processed/merged_pls_acs.csv")