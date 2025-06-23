import os
import requests
import time 

from collections import defaultdict
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
REBRICKABLE_API_KEY = os.getenv("REBRICKABLE_KEY")

BASE_URL = "https://rebrickable.com/api/v3/lego"
HEADERS = {"Authorization": f"key {REBRICKABLE_API_KEY}"}


def get_set_parts(set_num):
    """
    Retrieves parts for a given LEGO set number.
    Returns a dictionary with (part_num, color_id) as keys and quantities as values.
    """
    parts_url = f"{BASE_URL}/sets/{set_num}/parts/"
    results = {}
    page = 1

    while True:
        response = requests.get(parts_url, headers=HEADERS, params={"page": page})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch parts for set {set_num}: {response.text}")

        data = response.json()
        for item in data["results"]:
            part_key = (item["part"]["part_num"], item["color"]["id"])
            results[part_key] = results.get(part_key, 0) + item["quantity"]

        if data["next"] is None:
            break
        page += 1

    return results


def get_all_sets(page_limit=5):
    """
    Fetches a subset of all sets from the Rebrickable database (limited by page_limit for now).
    Returns a list of set metadata (each with set_num and name).
    """
    all_sets = []
    page = 1

    while page <= page_limit:
        response = requests.get(f"{BASE_URL}/sets/", headers=HEADERS, params={"page": page})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch set list: {response.text}")

        data = response.json()
        all_sets.extend(data["results"])

        if data["next"] is None:
            break
        page += 1

    return all_sets


def aggregate_user_parts(user_sets):
    """
    Combines all parts from a list of user sets into one master inventory.
    """
    combined_parts = defaultdict(int)

    for set_num in user_sets:
        try:
            set_parts = get_set_parts(set_num)
            for part_key, qty in set_parts.items():
                combined_parts[part_key] += qty
        except Exception as e:
            print(f"Skipping {set_num} due to error: {e}")

    return combined_parts


def can_build(target_parts, user_parts):
    """
    Checks if a set can be built from user parts inventory.
    """
    for part_key, required_qty in target_parts.items():
        if user_parts.get(part_key, 0) < required_qty:
            return False
    return True


def find_buildable_sets(user_sets, page_limit=5):
    """
    Main function: given user sets, return a list of buildable sets from all available.
    """
    user_inventory = aggregate_user_parts(user_sets)
    potential_sets = get_all_sets(page_limit=page_limit)
    buildable_sets = []

    for lego_set in potential_sets:
        set_num = lego_set["set_num"]
        try:
            target_parts = get_set_parts(set_num)
            if can_build(target_parts, user_inventory):
                buildable_sets.append({
                    "set_num": set_num,
                    "name": lego_set["name"],
                    "year": lego_set.get("year"),
                    "num_parts": lego_set.get("num_parts"),
                    "set_img_url": lego_set.get("set_img_url"),
                })
        except Exception as e:
            print(f"Error checking set {set_num}: {e}")
        time.sleep(1.1)

    return buildable_sets
