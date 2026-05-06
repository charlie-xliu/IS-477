# IS477 Status Report (April 14th)
**Charlie Liu and Vincent Cui**

**Project Repository:** charlie-xliu/IS-477

## 1. Project Status Summary and Timeline

We have completed the Data Cleaning, Exploratory Data Analysis, Feature Engineering, and Data Quality & Documentation portions as scheduled in our project timeline. The dataset now successfully merges FY2023 Public Library Survey (PLS) data with 2023 ACS 5-Year Estimates. To do this, we had to first clean the two datasets which each had hundreds of columns and select which columns we wanted to conduct our socioeconomic analysis with. Then, we generated summary statistics, outlier detection, correlation matrix (based on socioeconomic and library usage metrics), and generated graphs focusing on poverty rate and median household income for our exploratory data analysis portion. Then, we conducted feature engineering by making libraries of different sizes comparable, and reduced outlier influence with our data. Finally, we looked at data quality and reproducibility with these two datasets, primarily by saving our cleaned datasets into new csv files and creating data dictionaries for the merged dataset.

### Current Timeline

| Dates | Task |
|---|---|
| March 14th – March 24th (Spring Break) | Data Acquisition & Merging | (Complete)
| March 24th – 27th | Data Cleaning & Preprocessing | (Complete)
| March 27th – 30th | Some Exploratory Data Analysis | (Complete)
| March 30th | Write-up of Step 3 — *Delayed to April 14th: Interim Status Report* | (Complete)
| April 1st – 6th | Feature Engineering | (Complete)
| April 7th – 12th | Data Quality Documentation | (Complete)
| April 13th – 17th | Data Modeling and Reproducibility: linear regression, creating a conceptual model (ER) *(IN PROGRESS)* |
| April 18th – 23rd | Visualization & Interpretation: Finalize charts, maps, plots; start interpreting model outputs |
| April 24th – 27th | Workflow Automation and Provenance: Snakemake workflow automating from acquisition to result |
| April 28th – 30th | Review deliverables, ensure we are fulfilling the requirements of the assignment |

---

## 2. Completion of Milestones

To merge datasets and to conduct further analysis, we integrated using the County FIPS codes, which identifies each county in America with a unique code. After removing sentinel values, missing data, and instances where library agencies serve multiple counties, we get our cleaned dataset. Then, we analyzed distributions of key predictors, discovering significant right-skewness in library visits and local revenue. Notably, we found a strong correlation between Median Household Income and Local Government Revenue, suggesting that community wealth is a primary driver of library funding levels, potentially impacting the amount of library visits in a given location. We also produced correlation heatmaps and scatter plots to identify relationships between poverty rates (and other socioeconomic factors) and library usage metrics.

For our next step, Feature Engineering, we created per-capita metrics (variables: `visits_pc`, `circ_pc`, `opex_pc`) to ensure libraries in different-sized service areas can be compared equitably. This is to isolate socioeconomic metrics related to poverty so that size is not an undiscovered factor. To further polish our data, we implemented Winsorization at the 1st and 99th percentiles to mitigate the impact of outliers and data entry errors that might have slipped through. With feature engineering, we hope to use our new data to turn our observations from our exploratory analysis into conclusions.

The last step completed before submitting this status report was Data Quality & Documentation, where we built a comprehensive data dictionary that maps complicated variables into understandable features (e.g., `pop_lsa` = Population of legal service area). Notably, we also documented some limitations of our dataset and our approach, specifically highlighting the timing mismatch between the FY2023 Public Library Survey and the 2019–2023 ACS 5-year averages. We also addressed our approach of geographic merging, where libraries serving multiple counties were assigned to a single county based on census tract centroids. While this simplifies our data, it also doesn't fully represent the distribution of libraries as they exist in real life. To ensure the integrity of future modeling, we standardized our features through population normalization and log-transformations while applying Winsorization to manage the influence of extreme outliers. However, we could have gone further in our Winsorization efforts and applied a 5th and 95th percentile approach.


## 3. Project Plan Changes

Currently, there have been no changes to the project plan. We have finished everything projected in the timeline, and we have enough to work with in our datasets to not warrant any changes in our project. As for TA feedback on our Project Plan, they projected that integrating based on county data may prove difficult; however, we were able to get through this concern mostly comfortably. Our feedback also noted that the team member roles were a bit vague, which we will clarify in Section 5.


## 4. Project Challenges

The most significant challenge was geographic merging. PLS libraries are identified by their legal service area while ACS data is organized strictly at the county level. To bridge this, we derived 5-digit county FIPS codes from PLS using a two-step fallback: direct extraction for libraries whose service area is a county, and census tract centroids for all others. Libraries spanning multiple counties were assigned to just one, which is a known simplification.
Data quality in the PLS also required attention. The survey encodes non-response with multiple sentinel values (-1, -3, -9), and some records contained implausible values that survived initial filtering. Winsorization at the 1st and 99th percentiles addressed the worst cases, though a stricter threshold may be needed during modeling.
Finally, there is a temporal mismatch between the sources: the PLS reflects FY2022–23 activity while the ACS 5-year estimates average 2019–2023 data, meaning our socioeconomic predictors partially reflect pre-pandemic conditions.

## 5. Team Member Summary

- **Vincent:** Brainstormed ideas on how to clean and merge the dataset, conducted exploratory analysis including exploring the relationship between local government revenue, library attendance, and median household income. Drafted most of the status report in the markdown file, summarizing work done between both team members.

- **Charlie:** I handled data cleaning and merging. This involved removing PLS sentinel values (-1, -3, -9), selecting relevant columns from both the 550-column ACS table and 187-column PLS file, and constructing a shared county FIPS key to join the two datasets. For libraries not directly mapped to a county, census tract centroids served as a geographic fallback. The resulting merged dataset formed the foundation for all subsequent analysis.

