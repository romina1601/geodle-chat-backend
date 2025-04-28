import datetime
import hashlib
import json
import os
import random

from geodle_chat.core.data_fetcher import logger

session_store = {}

DAILY_COUNTRY_FILE = "geodle_chat/data/daily_country.json"
COUNTRIES_FILE = "geodle_chat/data/countries.json"

def select_daily_country():
    """Deterministically picks a country based on today's date and appends it to history."""
    today = datetime.date.today().isoformat()  # "YYYY-MM-DD"

    with open(COUNTRIES_FILE, "r") as f:
        countries = json.load(f)

    # Load existing daily country history
    if os.path.exists(DAILY_COUNTRY_FILE):
        try:
            with open(DAILY_COUNTRY_FILE, "r") as f:
                countries_history = json.load(f)
        except json.JSONDecodeError:
            countries_history = []
    else:
        countries_history = []

    for entry in countries_history:
        if entry["date"] == today:
            return entry["country"]

    # Select today's country deterministically
    seed = int(hashlib.sha256(today.encode('utf-8')).hexdigest(), 16)
    random.seed(seed)
    daily_country = random.choice(countries)
    logger.info(f"Today\'s secret country is: {daily_country}")

    # Append today's country to history
    countries_history.append({
        "date": today,
        "country": daily_country
    })

    with open(DAILY_COUNTRY_FILE, "w") as f:
        json.dump(countries_history, f, indent=4)

    return daily_country
