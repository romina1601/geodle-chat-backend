# Utility file that fetches data once from the REST Countries API
import requests
import json


def fetch_all_countries():
    """Fetches a list of all country names and saves them as a JSON file."""
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching country data")
        return

    countries = [country["name"]["common"] for country in response.json()]

    # Save country names to a JSON file
    with open("geodle_chat_backend/data/countries.json", "w") as f:
        json.dump(countries, f, indent=4)

    print(f"Saved {len(countries)} countries to JSON.")


# Run the script once when installing the repo, if countries.json file is not present
fetch_all_countries()
