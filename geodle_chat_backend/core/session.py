import datetime
import json
import random

session_store = {}

DAILY_COUNTRY_FILE = "geodle_chat_backend/data/daily_country.json"
COUNTRIES_FILE = "geodle_chat_backend/data/countries.json"

def select_daily_country():
    """Selects a random country for the day and stores it in a JSON file."""
    today = datetime.date.today().isoformat()  # "YYYY-MM-DD"

    # Load history of picked countries (if exists)
    try:
        with open(DAILY_COUNTRY_FILE, "r") as f:
            countries_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        countries_history = []

    # Check if today's country is already selected
    for entry in countries_history:
        if entry["date"] == today:
            return entry["country"]

    # Select a new country from the countries list and add it to the selected countries file
    with open(COUNTRIES_FILE, "r") as f:
        countries = json.load(f)
    daily_country = random.choice(countries)
    countries_history.append({"date": today, "country": daily_country})

    # Update the history of picked countries with today's daily country
    with open(DAILY_COUNTRY_FILE, "w") as f:
        json.dump(countries_history, f, indent=4)

    return daily_country