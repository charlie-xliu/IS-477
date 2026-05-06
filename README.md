# Public Library Usage and Socioeconomic Conditions: A County-Level Analysis
 
## Contributors
 
- Charlie Liu
- Vincent Cui
---

## DOI
https://zenodo.org/records/20059881

## Summary
Public libraries serve as a cornerstone of community infrastructure, providing free access to information, technology, programming, and professional resources regardless of a patron's economic circumstances. Yet despite their role as a publicly funded equalizer, the factors that drive their usage remain incompletely understood. This project investigates the relationship between socioeconomic conditions and public library utilization across the United States by integrating two federal datasets: the Institute of Museum and Library Services (IMLS) Public Library Survey (PLS) for FY2023 and the U.S. Census Bureau's American Community Survey (ACS) 5-Year Estimates for 2019–2023.
Our central research questions are:
- To what extent do socioeconomic indicators predict per-capita library visits?
- Do these relationships differ across rural, suburban, and urban library contexts?
To answer these questions, we merged over 9,000 public library agency records from the PLS with county-level economic characteristics from the ACS using a shared county FIPS code key. Because library legal service areas do not align neatly with county boundaries, constructing this key required a two-step geographic fallback: direct extraction for libraries whose service area is a county, and census tract centroids for all others. We then cleaned, normalized, and engineered a set of per-capita and composite features that allow libraries of vastly different sizes to be compared on equal footing.
Exploratory analysis revealed substantial right-skewness in all library usage metrics, consistent with the unequal distribution of large urban library systems versus small rural ones. A single large urban system can have visits and circulation orders of magnitude greater than a rural branch, making raw counts misleading without normalization. Correlation analysis showed that median household income and per-capita income are positively correlated with library visits and circulation, while poverty rate and SNAP participation are negatively correlated.
Our OLS regression model, estimated with heteroskedasticity-robust standard errors, found that operating expenditure per capita is the strongest positive predictor of visits per capita, confirming that funding drives usage independent of the surrounding community's economic profile. Among socioeconomic predictors, counties with higher SNAP participation showed significantly lower per-capita visits. This may reflect that deeply economically distressed communities face structural barriers to library access, such as limited transportation, reduced library hours, or competing demands on residents' time, that outweigh the potential draw of free services. However, when we stratified by locale (rural, suburban, urban), the effects of poverty and income became more heterogeneous: poverty rate was negatively associated with visits in urban and suburban settings but showed a weaker, less consistent signal in rural libraries, where libraries may serve a different role in the community fabric and where residents may have fewer alternative resources.
These findings suggest that the relationship between economic disadvantage and library usage is mediated by geography, funding, and local context. Simply knowing a county's poverty rate is insufficient to predict library engagement without accounting for how well-resourced that library system is. Future work should incorporate geographic visualization, panel data across multiple survey years, and multilevel modeling to more fully untangle these dynamics.


## Data Profile
 
### Dataset 1: IMLS Public Library Survey (PLS), FY2023 — Agency-Level Microdata
 
**Location in repository:** `data/raw/PLS_FY23_AE_pud23i.csv`

The PLS is an annual census of all public libraries in the United States conducted by the Institute of Museum and Library Services. The raw file contains approximately 9,000 rows and 187 columns, covering a wide range of administrative, geographic, financial, usage, and staffing variables.
Key variables selected for analysis include: 
- total annual visits (VISITS)
- total circulation (TOTCIR)
- registered borrowers (REGBOR)
- population of legal service area (POPU_LSA)
- total operating expenditures (TOTOPEXP)
- local government revenue (LOCGVT)
- total paid staff in FTE (TOTSTAFF)
- public internet terminals (GPTERMS)
- Wi-Fi sessions (WIFISESS)
- total programs offered (TOTPRO)
- total program attendance (TOTATTEN
- annual public service hours (HRS_OPEN)

Geographic linkage variables include: 
- LSAGEOID (legal service area GeoID)
- LSAGEOTYPE (the type of geographic entity — county, place, etc.)
- CENTRACT (census tract of the library's central outlet)
- 
The dataset is released as public-use microdata by IMLS and is freely available for download. There are no known legal constraints on redistribution or analysis. The unit of analysis is the library administrative entity; outlet-level data (branches, bookmobiles) are available in a companion file (pls_fy23_outlet_pud23i.csv) but were not used directly in this analysis.
An important ethical consideration is that the PLS includes several sentinel values (-1 for not applicable, -3 for confidential/suppressed, -9 for missing/not reported) which must be treated as missing data rather than as numeric values. Failing to handle these sentinels would introduce severe distortions into any quantitative analysis.
### Dataset 2: American Community Survey (ACS) 5-Year Estimates 2023, Table DP03
**Location in repository:** `data/raw/ACSDP5Y2023_DP03-Data.csv` and `data/raw/ACSDP5Y2023_DP03-Column-Metadata.csv`
The ACS DP03 table provides selected economic characteristics at the county level for all counties in the United States. The 5-year estimates pool survey responses from 2019 through 2023, providing more stable estimates for small geographic areas than single-year estimates. The raw data file contains one row per county (approximately 3,200 rows) and several hundred columns encoding estimates and margins of error for a range of employment, income, and poverty indicators.
Variables selected for analysis include: 
- unemployment rate (DP03_0005PE)
- median household income (DP03_0062E)
- mean household income (DP03_0063E)
- per-capita income (DP03_0086E)
- overall poverty rate (DP03_0099PE)
- poverty rate for children under 18 (DP03_0100PE)
- poverty rate for adults 18–64 (DP03_0101PE)
- SNAP/food stamp receipt rate (DP03_0074PE)
- percentage without health insurance (DP03_0096PE)
- work-from-home rate (DP03_0042PE)

These variables collectively represent multiple dimensions of economic wellbeing that may influence residents' patterns of library use.
The ACS is a public federal dataset with no restrictions on use. Margin-of-error columns (suffix 'M') were retained in the raw file but were dropped from the analytical subset to simplify the dataset; for inference on small counties, these should be restored to implement uncertainty-aware modeling.
The ACS DP03 data file includes a non-data header row (row index 1 contains human-readable column labels rather than data values), which must be skipped during loading to avoid type coercion errors.
### Relationship Between Datasets
The two datasets are linked at the county level using 5-digit FIPS codes. Because library service areas do not always align with county boundaries, constructing this key required a two-step geographic fallback strategy described in detail in the Data Cleaning section. The merged dataset enables direct comparison of library agency-level metrics with the socioeconomic characteristics of the surrounding county population.

## Data Quality
 
### PLS Data Quality
The most pervasive quality issue in the PLS is the use of sentinel values to encode non-response. Three codes are used: -1 (not applicable), -3 (confidential or suppressed), and -9 (missing or not reported). These values appear in numeric columns and, if left uncorrected, would produce incorrect and misleading summary statistics and model estimates. Before any analysis, we replaced these codes with NaN using a systematic replacement pass across all numeric columns.
There were also several columns that had lots of missing values. Electronic content uses and electronic information retrievals had some of the most missing cells, likely because libraries do not consistently track these digital metrics. Key usage metrics like visits and total_circ had most cells populated, making them suitable as primary outcome variables.

The PLS also includes quality flag columns (e.g., F_VISITS, F_TOTCIR) that encode additional codes indicating whether values were revised, imputed, or recorded for a library that closed and reopened during the fiscal year. These flag columns were retained in the cleaned output file for reference but were not used to filter or adjust the analysis in the current phase.
### ACS Data Quality
The ACS data had minimal structural issues. The primary concern is that ACS 5-year estimates are subject to sampling uncertainty, particularly for small-population counties. Margin-of-error values were not incorporated into the analysis due to scope constraints but represent a meaningful limitation. A small number of cells used ACS-specific suppression codes (such as "(X)" for not applicable) which were coerced to NaN via pd.to_numeric(errors='coerce').
### Merge Quality
Approximately 90% or more of PLS library agencies were successfully matched to an ACS county record via the FIPS key construction procedure. Libraries that failed to match were predominantly those serving non-county geographic entities where the census tract centroid fallback also failed to produce a valid 5-digit FIPS code. The unmatched libraries tend to be in unusual jurisdictional arrangements (e.g., special districts, tribal lands) and represent a small fraction of total agencies.
### Outlier Assessment
Outlier analysis using the IQR ×1.5 rule identified substantial proportions of statistical outliers across most usage metrics, which is expected given the extreme size range of public library systems in the United States. A single large urban library system (e.g., New York Public Library) can have visits and circulation orders of magnitude larger than a rural single-branch library. This motivates the per-capita normalization and Winsorization applied in the feature engineering phase.

## Data Cleaning
### Handling PLS Sentinel Values
The first and most critical cleaning step was replacing the PLS sentinel values (-1, -3, -9) with NaN across all numeric columns. A list of 30 numeric columns was explicitly defined to scope this replacement, avoiding unintended modification of categorical or flag columns. The number of sentinel values replaced was tracked and logged for transparency.
### ACS Type Coercion
ACS columns were imported as strings due to the presence of non-numeric suppression codes. Each selected socioeconomic column was converted to a numeric type using pd.to_numeric(errors='coerce'), which silently converts non-parseable values to NaN. This approach is robust to the varied suppression codes used across different ACS variables.
Constructing the County FIPS Key for PLS
This was the most technically complex cleaning operation. The PLS records each library's legal service area (LSA) geography in two fields: LSAGEOTYPE (the type of geography) and LSAGEOID (the geographic identifier). When LSAGEOTYPE equals "COUNTY", the LSAGEOID can be zero-padded to five digits to directly obtain the county FIPS code. For libraries in other geographic types (primarily "PLACE"), no direct FIPS code is available. In these cases, the CENTRACT field — an 11-digit census tract FIPS code for the library's central outlet — was used, with the first five digits extracted as the county FIPS code.

Libraries whose legal service area spans multiple counties (flagged by LSABOUND='Y') present an inherent limitation: they were assigned to a single county using this procedure, which does not fully capture the geographic footprint of multi-county systems.

The derived FIPS key from both methods was combined using a fillna strategy (prefer direct county match, fall back to tract-derived), and the result was merged with the ACS dataset using a left join on county_fips.
### Removing Implausible Records
Libraries with missing or zero population in their legal service area (pop_lsa) were excluded from the working analytical dataset, as they cannot be meaningfully used in per-capita calculations. This filtering step reduced the dataset from the full merged count to the analytical subset used in EDA and modeling.
### Saving Cleaned Outputs
Three intermediate CSV files were saved at the conclusion of the cleaning phase: pls_cleaned.csv (cleaned PLS data), acs_cleaned.csv (cleaned ACS subset), and merged_pls_acs.csv (the joined dataset). This makes a checkpoint between the cleaning and analysis phases and allows either dataset to be reused independently.
### Feature Engineering Transformations
In the feature engineering phase, three additional cleaning-adjacent operations were performed. Per-capita metrics (visits_pc, circ_pc, opex_pc) were created by dividing raw usage and financial variables by pop_lsa, making libraries of different sizes directly comparable. Winsorization at 1% and 99% was applied to these per-capita metrics to limit the influence of extreme outliers and data entry errors that survived initial sentinel filtering. Finally, log transformations were applied to skewed usage variables for use in correlation analysis and regression modeling.

## Findings
### Correlation Structure
Spearman correlation analysis between log-transformed library usage metrics and socioeconomic predictors revealed a consistent pattern. Median household income and per-capita income showed positive correlations with visits, circulation, registered borrowers, and program attendance. Wealthier counties tend to have more heavily used libraries. Conversely, poverty rate, SNAP participation, and lack of health insurance showed negative correlations with the same usage metrics. Work-from-home rate showed a notably positive correlation with library digital metrics (Wi-Fi sessions, internet uses), suggesting that communities with more remote workers are also heavier library digital service users.
### OLS Regression Results
The full national OLS model explained a meaningful share of variance in log per-capita visits. Among library-side variables, operating expenditure per capita was the strongest positive predictor, reinforcing the view that funding drives service intensity. Among socioeconomic variables, SNAP participation rate was the most statistically significant negative predictor: counties with higher proportions of households receiving food assistance had fewer library visits per capita, even after controlling for income and poverty rate. This may reflect that the most economically distressed communities face barriers to library access (transportation, hours of operation, competing time demands) that offset the potential demand for free resources.
Median household income showed a positive and statistically significant coefficient, while unemployment rate and poverty rate showed coefficients in the expected negative direction but with weaker significance in the full national model.
### Locale-Stratified Analysis
When the regression was stratified by locale (rural, suburban, urban), the socioeconomic coefficients showed meaningful heterogeneity. Poverty rate had a larger negative association with visits in urban and suburban libraries than in rural ones. Median household income was positively associated with visits across all three locale types. These patterns suggest that library usage decisions are shaped differently depending on local geographic and demographic context, and that national-level models may mask important regional variation.

## Future Work
There are several ways that we could improve this project with future work. The most immediate opportunity is to incorporate the quality flag columns from the PLS (e.g., F_VISITS, F_TOTCIR) into the analysis to assess whether imputed or revised values meaningfully affect model estimates. The PLS encodes multiple imputation codes that we retained in the cleaned output file but did not act on during modeling. A sensitivity analysis comparing results with and without flagged observations would strengthen confidence in the findings and make the analysis more transparent about where the underlying data is uncertain.

On the modeling side, moving beyond OLS to multilevel or hierarchical models would allow explicit modeling of the nested structure of the data (library agencies within counties, counties within states). State-level fixed effects or random effects could absorb unobserved state-level policy variation — for example, differences in state library funding formulas, broadband infrastructure investment, or rural library subsidy programs — that currently confounds county-level estimates and makes it difficult to isolate the effect of local socioeconomic conditions alone.

The temporal mismatch between the FY2023 PLS and the 2019–2023 ACS 5-year estimates is an inherent limitation of this cross-sectional design. Because the ACS estimates average over five years, our socioeconomic predictors reflect a blend of pre-pandemic, pandemic-era, and recovery-period conditions rather than a clean snapshot of 2023. Future work could address this by pairing PLS data from multiple survey years with contemporaneous single-year ACS estimates, enabling a panel or longitudinal analysis that captures changes over time. This is especially relevant given the disruption to both library usage and economic conditions caused by the COVID-19 pandemic, during which library visits dropped sharply before recovering.

A major analytical gap in the current work is the absence of geographic visualization. Mapping per-capita library visits and the key socioeconomic predictors at the county level would reveal spatial clustering patterns — for example, whether high-visit, low-income counties cluster in particular regions, or whether the SNAP effect we observed is concentrated in specific parts of the country. This would be a natural next step using tools such as GeoPandas or Folium, and would make the findings considerably more communicable to a non-technical audience.

The Winsorization threshold of 1% and 99% was a little conservative; for smaller analytical subsets such as within a single state or locale type, a stricter 5%/95% split would better control for the influence of extreme values. A comparison of model results under both thresholds would clarify how sensitive the findings are to this choice. Similarly, the ACS margin-of-error columns should be restored for any inference focused on small-population counties, where sampling uncertainty is substantial enough to meaningfully affect coefficient estimates.

Finally, the outlet-level PLS file was acquired but not used in this analysis. Branch-level data could enable considerably more granular analyses — for example, examining whether individual library outlets located in census tracts with higher poverty rates have systematically different usage patterns than branches of the same library system located in wealthier tracts nearby. This within-system comparison would help isolate the effect of local neighborhood conditions from system-wide funding and policy decisions, which the agency-level analysis cannot disentangle.


## Challenges
- Geographic merging was the single most significant technical challenge in this project. Public library legal service areas are defined by library administrators and do not correspond directly to standard Census geographies. A library system might serve an entire county, a single municipality, a township, or some other jurisdictional unit that has no direct equivalent in Census data. Bridging the PLS's place-based service area definitions to the ACS's strictly county-level organization required a layered approach: direct FIPS extraction for libraries whose service area is classified as a county, and a census tract centroid fallback for all others. Even with this two-step strategy, a small number of libraries could not be matched and were excluded from the merged dataset (the ones in unusual jurisdictional arrangements such as special districts, multi-jurisdictional compacts, or tribal lands). Libraries serving multiple counties presented an additional complication: they were assigned to a single county using whichever FIPS code the fallback procedure produced, which is an acknowledged simplification that introduces geographic measurement error for multi-county systems.
- Sentinel value handling required more careful attention than it might initially appear. The PLS uses three distinct non-response codes (-1 for not applicable, -3 for confidential or suppressed, and -9 for missing or not reported) with meaningfully different interpretations, yet all three must be treated as missing data in quantitative analysis. Identifying and replacing these values correctly without accidentally affecting legitimate numeric data required explicitly scoping the replacement to a defined list of numeric columns. The PLS also includes quality flag columns that encode additional imputation and revision codes, which we retained in the cleaned output file but did not fully incorporate into the analysis. Doing so would have added another layer of complexity to the filtering and modeling pipeline that was out of scope for this phase.
- Scale heterogeneity was a persistent challenge throughout the analysis. Library systems in the United States range from small rural single-branch operations serving populations of a few hundred people to large urban systems with dozens of branches serving millions. No single normalization strategy fully resolves this heterogeneity. Per-capita metrics address population size differences but do not account for variation in the number of outlets, the geographic spread of service areas, or the fundamentally different roles that libraries play in dense urban versus sparsely populated rural communities. This made it difficult to build a model that performs equally well across all library types, and is part of the motivation for the locale-stratified analysis in Section 5.
- Temporal alignment between the two data sources cannot be fully resolved given what is publicly available. The FY2023 PLS reflects a single fiscal year of library activity, while the ACS 5-year estimates average survey responses from 2019 through 2023. This means our socioeconomic predictors do not cleanly represent conditions at the same moment as our outcome variables, limiting the causal interpretability of the regression results. This is a standard challenge in cross-sectional social science research using ACS data, but it is worth being explicit about when interpreting the findings.

## Reproducing

There are two ways to reproduce the full analysis from scratch.

### Option A — Snakemake (Recommended)

Snakemake automates the complete end-to-end pipeline from raw data validation through cleaning, EDA, feature engineering, modeling, and figure generation.

1. **Clone the repository:**
   ```
   git clone https://github.com/charlie-xliu/IS-477.git
   cd IS-477
   ```

2. **Obtain the raw data files** and place them in `raw/`:
   - `PLS_FY23_AE_pud23i.csv` — download from https://www.imls.gov/research-evaluation/data-collection/public-libraries-survey
   - `pls_fy23_outlet_pud23i.csv` — same source
   - `ACSDP5Y2023.DP03-Data.csv` — download from https://data.census.gov (Table DP03, ACS 5-Year 2023, All Counties)
   - `ACSDP5Y2023.DP03-Column-Metadata.csv` — downloaded alongside the DP03 data table

   To verify file integrity, confirm the SHA-256 checksums match the following:
   ```
   raw/PLS_FY23_AE_pud23i.csv:              3e2a498c116e4a6a067c89fcbc3d73d99bca3adb3e832e861fbedb48c2306b6a
   raw/pls_fy23_outlet_pud23i.csv:           2b4aad2fb91b0d29eaa51d0c0a1f934779f19c382247551a563df0540954fb68
   raw/ACSDP5Y2023.DP03-Data.csv:            6ebfc17ced4026d2ba266ae59b63232d0759b56d3d6af3e9ef67b284c692fd91
   raw/ACSDP5Y2023.DP03-Column-Metadata.csv: b8e425f7e5651eb7d4a48de21d7efad7a50fe41c51b0b104e9832d3e1ef8a16d
   ```
   You can verify by running `python scripts/acquire.py` from the project root.

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Install Snakemake** (if not already installed):
   ```
   pip install snakemake
   ```
   Verify the installation by running:
   ```
   snakemake --version
   ```

5. **Run the full pipeline:**
   ```
   snakemake --cores 1
   ```
   Snakemake will execute the following steps in order:
   - `acquire_data` — validates raw data files and computes SHA-256 checksums
   - `clean_and_merge` — removes sentinel values, selects columns, merges PLS × ACS on county FIPS
   - `eda` — generates correlation heatmap, scatter plots, and distribution figures
   - `feature_engineering` — creates per-capita metrics, log transforms, Winsorization, and derived ratios
   - `modeling` — fits OLS regression, produces coefficient plot and locale comparison figure

6. **Verify outputs** — all files will be written to `processed/` and `figures/`. Run `snakemake --cores 1` a second time — if it prints "Nothing to be done", all outputs are present and up to date.

To preview the pipeline without executing:
```
snakemake --cores 1 --dry-run
```

### Option B — Jupyter Notebook

To reproduce using 'library_analysis.ipynb', follow these steps:
1. **Clone the repository** from `charlie-xliu/IS-477` on GitHub.
2. **Obtain the raw data files** and place them in `data/raw/`:
   - `PLS_FY23_AE_pud23i.csv` — download from the IMLS Public Library Survey FY2023 page at https://www.imls.gov/research-evaluation/data-collection/public-libraries-survey
   - `pls_fy23_outlet_pud23i.csv` — same source
   - `ACSDP5Y2023_DP03-Data.csv` — download from https://data.census.gov (Table DP03, ACS 5-Year 2023, Geography: All Counties)
   - `ACSDP5Y2023_DP03-Column-Metadata.csv` — downloaded alongside the DP03 data table
3. **Install dependencies** by running:
   ```
   pip install -r requirements.txt
   ```
 
4. **Run the notebook** by opening `notebooks/01_cleaning_eda_features.ipynb` in Jupyter and selecting Kernel → Restart & Run All. All intermediate CSV files, figures, and documentation will be written to their respective directories (`data/processed/`, `figures/`, `docs/`).
5. **Verify outputs** — the final cell of the notebook prints a checklist of expected output files. All items should show a checkmark.


## References
 
- Institute of Museum and Library Services (IMLS). *Public Library Survey, FY2023: Agency-Level and Outlet-Level Public Use Data*. Washington, DC: IMLS, 2024. https://www.imls.gov/research-evaluation/data-collection/public-libraries-survey
- U.S. Census Bureau. *American Community Survey 5-Year Estimates, 2019–2023, Table DP03: Selected Economic Characteristics*. Washington, DC: U.S. Census Bureau, 2024. https://data.census.gov
- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 445, 51–56.
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*, 57–61.
- Waskom, M. L. (2021). Seaborn: Statistical data visualization. *Journal of Open Source Software*, 6(60), 3021. https://doi.org/10.21105/joss.03021
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95.



