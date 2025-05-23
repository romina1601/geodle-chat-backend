import requests
import json
import os

from geodle_chat.utils.logger import setup_logger

logger = setup_logger(__name__)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data/jsons")

os.makedirs(DATA_DIR, exist_ok=True)

def fetch_country_details(country_name: str) -> {}:
    """Fetches details about a country either from:
        - REST Countries API and stores them as JSON.
        - local JSON file if it was already fetched from the REST API
    """
    # Normalize file name: lowercased and underscores instead of spaces
    filename = f"{country_name.lower().replace(' ', '_')}.json"
    filepath = os.path.join(DATA_DIR, filename)

    # If the file exists, load and return it
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            print(f"Reading country data from {filepath}")
            return json.load(f)

    api_url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    response = requests.get(api_url)

    if response.status_code != 200:
        logger.error("Country details could not be fetched.")
        return None

    country_data = response.json()[0]  # Extract first match

    details = {
        "name": country_data.get("name", {}).get("common", "Unknown"),
        "capital": country_data.get("capital", ["Unknown"])[0],
        "region": country_data.get("region", "Unknown"),
        "subregion": country_data.get("subregion", "Unknown"),
        "population": country_data.get("population", "Unknown"),
        "currency": ", ".join(country_data.get("currencies", {}).keys()),
        "languages": ", ".join(country_data.get("languages", {}).values()),
        "flag": country_data.get("flag", ""),
        "borders": ", ".join(country_data.get("borders", [])) if country_data.get("borders") else "None",
    }

    # Save the details to a JSON file for future retrieval
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    return details

def retrieve_facts_from_json(country: str) -> str:
    """Retrieves stored country facts from a JSON file as a string
    (to be passed as context to gen AI model)
    """
    file_path = os.path.join(DATA_DIR, f"{country}.json")

    if not os.path.exists(file_path):
        return "No additional facts found."

    with open(file_path, "r", encoding="utf-8") as f:
        country_data = json.load(f)

    # Format facts as a readable text string
    return "\n".join([f"{key}: {value}" for key, value in country_data.items()])