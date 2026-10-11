# API Response Validator

## Description
A Python utility that validates market-data JSON responses and identifies missing or invalid fields.

## Technologies Used
- Python
- JSON

## Project Files
- `validator.py` – Main validation code
- `sample.json` – Sample market-data input
- `validate_config.json` – Validation rules
- `README.md` – Project documentation

## How to Run

Run the default sample file:

```bash
python validator.py
```

To validate another JSON file:

```bash
python validator.py filename.json
```

## Validation Checks
- Missing required fields
- Null values
- Invalid numeric and negative price values
- Invalid timestamps
- Conversion of timestamps into UTC and IST
- Clear PASS/FAIL validation report

## Timestamp Handling
The program accepts Unix epoch timestamps in seconds and converts them into UTC and IST.

IST is 5 hours and 30 minutes ahead of UTC.

## Assumptions
- The input must be a valid JSON object.
- Required fields must be present and non-null.
- Price fields must contain valid, finite, non-negative numbers.
- Timestamp fields must contain valid integer Unix epoch timestamps in seconds.

## Output
- **PASS:** All validation checks passed.
- **FAIL:** The report displays the detected errors.

## Conclusion
This project helps identify missing or invalid values in market-data JSON responses and produces a clear validation report.