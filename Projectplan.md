## Overview

The goal of this project is to analyze how local demographic and socioeconomic factors influence public library usage across the United States. We were drawn to the idea of libraries as they were an influential part of our childhood and teenage years, and continue to serve as important community resources. Furthermore, they can serve as a place of knowledge, collaboration, and cultural gatherings, making them critical for a thriving community. However, library usage varies widely by region, and understanding the drivers of engagement can help decision makers (such as policy makers) understand more about how to support their local neighborhood.

## Team


## Research Questions


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
