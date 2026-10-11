# CSV Historical Data Integrity Checker

## Project Description

This Python program checks historical market data stored in a CSV file
and identifies common data-quality issues.

## Technologies Used

-   Python
-   Pandas
-   CSV

## Validation Rules

-   Detect duplicate records.
-   Check for missing symbols.
-   Validate trading dates and times.
-   Check whether numeric fields contain valid numbers.
-   Detect zero or negative prices.
-   Flag records where High is less than Low.
-   Detect negative trading volume.
-   Count records by symbol and trading date.

## How to Run

1.  Install Python.

2.  Install Pandas:

    ``` bash
    pip install pandas
    ```

3.  Place `sampledata.csv` in the project folder.

4.  Run the program:

    ``` bash
    python csv_integrity.py
    ```

Make sure the input filename in the Python script matches your CSV
filename.

## Output

-   `summary_report.csv` contains record counts grouped by symbol and
    trading date.
-   `validation_report.csv` contains validation issues if the script is
    configured to generate it.

## Complexity

Let `N` be the number of records and `C` be the number of columns.

-   **Time complexity:** Approximately `O(N × C)` for reading and
    checking data. Duplicate detection and grouping may add processing
    overhead.
-   **Space complexity:** Approximately `O(N × C)` when the full CSV is
    loaded into memory.

## Bonus: Large-File Handling

Large CSV files can be processed in smaller chunks using Pandas
`read_csv()` with the `chunksize` parameter. The validation rules must
be applied to each chunk, and duplicates across chunks need separate
handling.

## Conclusion

This project helps find common data-quality issues in historical market
data and creates a summary report for easier review.
