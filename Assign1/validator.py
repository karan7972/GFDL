import json
import math
from datetime import datetime, timezone, timedelta
import sys

def load_config(filename="validate_config.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

try:
    config = load_config()
except (OSError, json.JSONDecodeError) as error:
    print(f"FAIL: Configuration error: {error}")
    sys.exit(1)

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "sample.json"


try:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

except FileNotFoundError:
    print(f"FAIL: File not found: {filename}")
    sys.exit(1)

except json.JSONDecodeError as error:
    print(f"FAIL: Invalid JSON format: {error}")
    sys.exit(1)

if not isinstance(data, dict):
    print("FAIL: JSON must contain an object.")
    sys.exit(1)


required_fields = config["required_fields"]
price_fields = config["price_fields"]
timestamp_fields = config["timestamp_fields"]

errors = []


for field in required_fields:
    if field not in data:
        errors.append(f"Missing field: {field}")


for field in required_fields:
    if field in data and data[field] is None:
        errors.append(f"Null value: {field}")


for field in price_fields:
    if field not in data or data[field] is None:
        continue

    value = data[field]

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"Invalid numeric value: {field}")

    elif not math.isfinite(value):
        errors.append(f"Invalid numeric value: {field}")

    elif value < 0:
        errors.append(f"Negative price: {field}")


valid_timestamps = {}

for field in timestamp_fields:

    if field not in data or data[field] is None:
        continue

    value = data[field]

    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"Invalid timestamp: {field}")
        continue

    try:
        utc_time = datetime.fromtimestamp(
            value, tz=timezone.utc
        )
        valid_timestamps[field] = utc_time

    except (ValueError, OverflowError, OSError):
        errors.append(f"Out-of-range timestamp: {field}")


ist_timezone = timezone(timedelta(hours=5, minutes=30))

for field, utc_time in valid_timestamps.items():
    ist_time = utc_time.astimezone(ist_timezone)

    print(f"{field} UTC: {utc_time.isoformat()}")
    print(f"{field} IST: {ist_time.isoformat()}")


print("\n========== VALIDATION REPORT ==========")

if errors:
    print("Status: FAIL")
    print("Total errors:", len(errors))

    for number, error in enumerate(errors, start=1):
        print(f"{number}. {error}")

else:
    print("Status: PASS")
    print("All validation checks passed.")

print("=======================================")