import requests
import csv
import os

BASE_URL = "https://jellybellywikiapi.onrender.com/api"

# Endpoints to fetch (you can add more)
ENDPOINTS = {
    "beans": "beans.csv",
    "recipes": "recipes.csv",
    "combinations": "combinations.csv",
    "facts": "facts.csv",
    "mileStones": "milestones.csv"

}

def fetch_paged(endpoint: str, page_size: int = 5000):
    """Fetch all records from a paged endpoint."""
    page_index = 1
    records = []

    while True:
        url = f"{BASE_URL}/{endpoint}?pageIndex={page_index}&pageSize={page_size}"
        print(f"Fetching {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Stop: got {resp.status_code}")
            break

        data = resp.json()

        # The API usually returns { 'items': [...], 'pageIndex': x, 'pageSize': y, 'count': n }
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
        elif isinstance(data, list):
            items = data
        else:
            print(f"Unexpected format for {endpoint}: {type(data)}")
            break

        if not items:
            break

        records.extend(items)

        # Stop if we’ve got everything
        if len(items) < page_size:
            break

        page_index += 1

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
            data = fetch_paged(endpoint, page_size=2000)  # adjust size if needed
            write_csv(csv_name, data)
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")

if __name__ == "__main__":
    main()
