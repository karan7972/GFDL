import pandas as pd

for df in pd.read_csv("sampledata.csv", chunksize=10000):
    print("Processing", len(df), "records")
   


duplicates = df[df.duplicated(keep="first")]

print("\nDuplicate records:")
print(duplicates)
print("Total duplicates:", len(duplicates))

missing_symbols = df[
    df["Symbol"].isna() |
    (df["Symbol"].astype(str).str.strip() == "")
]

print("\nRecords with missing symbols:")
print(missing_symbols)
print("Total missing symbols:", len(missing_symbols))

dates = pd.to_datetime(df["TradingDate"], errors="coerce")
invalid_dates = df[dates.isna()]

print("\nRecords with invalid dates:")
print(invalid_dates)
print("Total invalid dates:", len(invalid_dates))

times = pd.to_datetime(
    df["TradeTime"], format="%H:%M:%S", errors="coerce"
)

invalid_times = df[times.isna()]

print("\nRecords with invalid times:")
print(invalid_times)
print("Total invalid times:", len(invalid_times))


columns = ["Last", "Open", "High", "Low", "Close", "Volume"]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nInvalid numeric values:")
print(df[df[columns].isna().any(axis=1)])

prices = ["Last", "Open", "High", "Low", "Close"]

print("\nInvalid prices:")
print(df[(df[prices] <= 0).any(axis=1)])

print("\nHigh less than Low:")
print(df[df["High"] < df["Low"]])

print("\nNegative quantity:")
print(df[df["Volume"] < 0])


summary = df.groupby(
    ["Symbol", "TradingDate"],
    dropna=False
).size().reset_index(name="RecordCount")

print("\nRecords by symbol and trading date:")
print(summary)

summary.to_csv("summary_report.csv", index=False)

print("\nSummary report saved successfully!")

errors = []

for i in df[df.duplicated()].index:
    errors.append([i + 2, "Duplicate record"])

for i in df[df["Symbol"].isna()].index:
    errors.append([i + 2, "Missing symbol"])

dates = pd.to_datetime(df["TradingDate"], errors="coerce")
for i in df[dates.isna()].index:
    errors.append([i + 2, "Invalid trading date"])

times = pd.to_datetime(
    df["TradeTime"], format="%H:%M:%S", errors="coerce"
)
for i in df[times.isna()].index:
    errors.append([i + 2, "Invalid trade time"])

report = pd.DataFrame(errors, columns=["CSV_Row", "Error"])
report.to_csv("validation_report.csv", index=False)

