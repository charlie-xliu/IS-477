import hashlib

files = [
    "raw/PLS_FY23_AE_pud23i.csv",
    "raw/pls_fy23_outlet_pud23i.csv",
    "raw/ACSDP5Y2023.DP03-Data.csv",
    "raw/ACSDP5Y2023.DP03-Column-Metadata.csv",
]

for f in files:
    with open(f, "rb") as fh:
        checksum = hashlib.sha256(fh.read()).hexdigest()
    print(f"{f}: {checksum}")