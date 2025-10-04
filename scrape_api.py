import requests
import csv
import os
import json

BASE_URL = "https://jellybellywikiapi.onrender.com/api"

# Endpoints to fetch
ENDPOINTS = {
    "beans": "beans.csv",
    "recipes": "recipes.csv",
    "combinations": "combinations.csv",
    "facts": "facts.csv",
    "mileStones": "milestones.csv"
}

def fetch_paged(endpoint: str, page_size: int = 5000):
    """Fetch all records from a paged endpoint and save raw API response."""
    page_index = 1
    records = []
    all_raw_responses = []  # store each page’s raw JSON

    while True:
        url = f"{BASE_URL}/{endpoint}?pageIndex={page_index}&pageSize={page_size}"
        print(f"Fetching {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Stop: got {resp.status_code}")
            break

        # Save the full raw text response (not prettified, so exact)
        try:
            json_data = resp.json()
        except Exception as e:
            print(f"JSON parse error for {endpoint}: {e}")
            break

        all_raw_responses.append(json_data)

        # Extract data from the API response
        if isinstance(json_data, dict) and "items" in json_data:
            items = json_data["items"]
        elif isinstance(json_data, list):
            items = json_data
        else:
            print(f"Unexpected format for {endpoint}: {type(json_data)}")
            break

        if not items:
            break

        records.extend(items)

        if len(items) < page_size:
            break

        page_index += 1

    # Save raw JSON file (combine all pages)
    os.makedirs("output", exist_ok=True)
    raw_json_path = os.path.join("output", f"{endpoint}_api_response.json")
    with open(raw_json_path, "w", encoding="utf-8") as jf:
        json.dump(all_raw_responses, jf, ensure_ascii=False, indent=2)
    print(f"Saved raw API response → {raw_json_path}")

    return records

def write_csv(filename: str, records):
    """Write list of dicts to CSV with dynamic headers."""
    if not records:
        print(f"No records for {filename}")
        return

    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)

    fieldnames = sorted({key for rec in records for key in rec.keys()})

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records → {filepath}")

def main():
    for endpoint, csv_name in ENDPOINTS.items():
        try:
            data = fetch_paged(endpoint, page_size=2000)
            write_csv(csv_name, data)
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")

if __name__ == "__main__":
    main()
