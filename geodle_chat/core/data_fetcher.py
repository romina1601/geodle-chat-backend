import requests
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data/jsons")

os.makedirs(DATA_DIR, exist_ok=True)

def fetch_country_details(country_name: str) -> {}:
    """Fetches details about a country from REST Countries API and stores them as JSON."""
    api_url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    response = requests.get(api_url)

    if response.status_code != 200:
        return "Country details could not be fetched."

    country_data = response.json()[0]  # Extract first match

    details = {
        "Name": country_data.get("name", {}).get("common", "Unknown"),
        "Capital": country_data.get("capital", ["Unknown"])[0],
        "Region": country_data.get("region", "Unknown"),
        "Subregion": country_data.get("subregion", "Unknown"),
        "Population": country_data.get("population", "Unknown"),
        "Currency": ", ".join(country_data.get("currencies", {}).keys()),
        "Languages": ", ".join(country_data.get("languages", {}).values()),
        "Borders": ", ".join(country_data.get("borders", [])) if country_data.get("borders") else "None",
    }

    # Save the details to a JSON file for future retrieval
    file_path = os.path.join(DATA_DIR, f"{country_name}.json")
    with open(file_path, "w") as f:
        json.dump(details, f, indent=4)

    return details

def retrieve_facts_from_json(country: str) -> str:
    """Retrieves stored country facts from a JSON file as a string
    (to be passed as context to gen AI model)
    """
    file_path = os.path.join(DATA_DIR, f"{country}.json")

    if not os.path.exists(file_path):
        return "No additional facts found."

    with open(file_path, "r") as f:
        country_data = json.load(f)

    # Format facts as a readable text string
    return "\n".join([f"{key}: {value}" for key, value in country_data.items()])