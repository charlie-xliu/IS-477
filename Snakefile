rule run_all:
    input:
        "figures/fig_ols_coefficients.png",
        "figures/fig_locale_comparison.png",
        "figures/fig_correlation_heatmap.png",
        "figures/fig_scatter_preview.png",
        "figures/fig_funding_vs_usage.png",
        "figures/fig_distributions.png",
        "figures/fig_winsorize_comparison.png",
        "processed/features_pls_acs.csv"

rule acquire_data:
    output:
        "raw/PLS_FY23_AE_pud23i.csv",
        "raw/pls_fy23_outlet_pud23i.csv",
        "raw/ACSDP5Y2023.DP03-Data.csv",
        "raw/ACSDP5Y2023.DP03-Column-Metadata.csv"
    shell:
        "python scripts/acquire.py"

rule clean_and_merge:
    input:
        "raw/PLS_FY23_AE_pud23i.csv",
        "raw/pls_fy23_outlet_pud23i.csv",
        "raw/ACSDP5Y2023.DP03-Data.csv",
        "raw/ACSDP5Y2023.DP03-Column-Metadata.csv"
    output:
        "processed/merged_pls_acs.csv"
    shell:
        "python scripts/clean_merge.py"

rule eda:
    input:
        "processed/merged_pls_acs.csv"
    output:
        "figures/fig_correlation_heatmap.png",
        "figures/fig_scatter_preview.png",
        "figures/fig_funding_vs_usage.png",
        "figures/fig_distributions.png"
    shell:
        "python scripts/eda.py"

rule feature_engineering:
    input:
        "processed/merged_pls_acs.csv"
    output:
        "processed/features_pls_acs.csv",
        "figures/fig_winsorize_comparison.png"
    shell:
        "python scripts/features.py"

rule modeling:
    input:
        "processed/features_pls_acs.csv"
    output:
        "figures/fig_ols_coefficients.png",
        "figures/fig_locale_comparison.png"
    shell:
        "python scripts/model.py"