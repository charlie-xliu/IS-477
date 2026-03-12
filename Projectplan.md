## Overview

The goal of this project is to analyze how local demographic and socioeconomic factors influence public library usage across the United States. We were drawn to the idea of libraries as they were an influential part of our childhood and teenage years, and continue to serve as important community resources. Furthermore, they can serve as a place of knowledge, collaboration, and cultural gatherings, making them critical for a thriving community. However, library usage varies widely by region, and understanding the drivers of engagement can help decision makers (such as policy makers) understand more about how to support their local neighborhood.

Using the U.S. Census Bureau’s 5-year ACS Dataset and the IMLS’ public library usage survey, we will conduct an analysis that will explore how socioeconomic characteristics such as poverty, unemployment rate, and median household income relate to per-capita library usage. We will then identify which factors are the strongest predictors, and examine whether these relationships differ across regions. We will use exploratory data analysis, visualization, and modeling to convey patterns and create conclusions. Ultimately, we hope this work contributes to a better understanding of who libraries serve and which communities need more investment.


## Team
As a team, we expect to have equal amounts of collaboration on assignments and projects. This means that we need to have consistent communication so we are on the same page. We will both keep each other responsible because for a lot of the parts, we must build off of what the other team member did (data analysis can’t happen before the cleaning). We will probably have member roles in finding, cleaning, and analyzing datasets along with identifying their ethical sourcing. Eventually we will also have to have someone work on the automated workflow, make sure it is reproducible and that someone is documenting it. 

## Research Questions
***Our guiding question:*** How well do local demographic and socioeconomic characteristics predict public library usage rates across U.S. counties, and which factors are the strongest predictors? Specifically, we will examine:
- Do counties with higher poverty rates have higher per-capita library usage, suggesting libraries serve as an essential resource for economically disadvantaged communities?
- Are counties with higher unemployment rates associated with greater library engagement, due to the increased usage of library resources for job searching and digital access?
- How does median household income relate to library usage, and what kind of pattern does it follow?
- Finally, do the questions above differ depending on rural or urban settings?

## Datasets

### Dataset 1: Public Library Survey (IMLS), FY 2023

Our approach involves two datasets which we found online from a quick Google search. The first is a public library usage dataset from a survey conducted by the Institute of Museum and Library Services (IMLS). This dataset includes columns such as zip code, county, library name, and identifiers. More importantly, this dataset can be trusted due to its origins from the IMLS, an independent federal agency. This dataset is under Creative Commons Zero (CC0), meaning there is free use and adaptation with no permission required. Furthermore, the survey data has been accumulated without individually identifiable information, which means that data that can be tied to a single individual are removed. Instead, the scope of the dataset is for every U.S. county, making it specific enough to identify niche differences while being broad enough to create large-scale conclusions about library usage across the United States. 

- **Source:** https://www.imls.gov/research-evaluation/surveys/public-libraries-survey-pls
- **License:** CC0 1.0 Universal (public domain); citation of source required

### Dataset 2: American Community Survey (ACS), 2019–2023 5-Year Estimates

The other dataset we will be using today is the American Community Survey (ACS) 5-Year Estimates, produced by the U.S. Census Bureau. The ACS is produced by the U.S. Census Bureau, another federal agency, and is fully in the public domain with no licensing restrictions on use. The data we will be using is reported at the county level, meaning no individually identifiable information is present, making it not a concern ethically. We use the 2019–2023 5-Year Estimates at the county level, specifically looking at metrics in DP03, the Selected Economics Characteristics table of the ACS Estimates. We specifically decided to use the 5-year estimates rather than the 1-year estimates due to the fact that the 1-year data covers counties with populations of 65,000 or more, which would exclude a large share of U.S. counties, creating bias towards largely populated areas. 


From the DP03 table, we are able to find important socioeconomic variables including median household income, unemployment rate, poverty rate, and health coverage. These variables provide the demographic and economic context that the IMLS dataset alone cannot offer. While the PLS does tell us how much libraries are being used, the ACS expands on the former by explaining why usage varies across communities. Both datasets share the FIPS county code as a common geographic identifier, which allows us to merge them at the county level and construct a single unified dataset for analysis.

- **Source:** https://data.census.gov/table/ACSDP5Y2023.DP03?q=DP03&g=010XX00US$0500000
- **License:** U.S. federal government public domain; no restrictions on use

## Timeline

_February 17th:_ Team creation
_March 9th:_ Started work on Step 2: Project Plan
_March 12th:_ (Current): Submission of Step 2: Project Plan
_March 14th - 24th:_ (Spring Break): Data Acquisition & Merging, download and inspect both datasets. Confirm you can merge datasets using the FIPS county code.
_March 24th - 27th:_ Data Cleaning & Preprocessing. Handle missing values, normalize columns, merge PLS and ACS on FIPS code, determine which columns are relevant (there are a lot of columns to sort through.)
_March 27th - 30th:_ Some Exploratory Data Analysis, Summary statistics, check distributions of library usage metrics. See if there’s any skewness, outliers, or anything else unusual. Generate a correlation matrix between socioeconomic predictors (such as poverty rate, median household income…) and library usage variables
_March 30th:_ Begin write-up of Step 3: Interim Status Report
_March 31st:_ Confirmation that Step 3: Interim status report is complete, finish any gaps in the write-up.
_April 1st - 6th:_ Feature engineering, converting data into per-capita basis
_April 7th - 12th:_ Data quality documentation, documentation of reproducibility, how it is organized (this is for use in the final project), Metadata and data documentation. 
_April 13th - 17th:_ Data modeling and reproducibility: linear regression, creating a conceptual model (ER)
_April 18th - 23rd:_ Visualization & Interpretation: Finalize charts, maps, plots; start interpreting model outputs
_April 24th - 27th:_ Workflow automation and provenance. Snakemake workflow automating from acquisition to result.
_April 28th - April 30th:_ Review deliverables, ensure we are fulfilling are requirements of the assignment
_May 1st - May 3rd:_ Final Project write-up: Assemble all individual parts of project and create a report that summarizes all work accomplished

## Constraints:
- The ACS dataset is from 2019-2023 while the IMLS is only from September 2022 to October 2023
- There are many confounding variables that we should keep in mind during our analysis

## Gaps
- We don’t have many confounding variables so our analysis could be off from that
- There will not be an even representation of all the counties, this could lead to bias for rural areas where the library structure is the weakest. 

