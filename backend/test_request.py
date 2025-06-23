import requests

# Point to your local server
url = "http://127.0.0.1:8000/buildable-sets"

# Replace with real set numbers you want to test with
data = {
    "owned_sets": ["31058-1", "31087-1"]  # These are small Creator sets
}

response = requests.post(url, json=data)

if response.status_code == 200:
    sets = response.json().get("buildable_sets", [])
    print(f"\n✅ Found {len(sets)} buildable sets:\n")
    for s in sets:
        print(f"- {s['set_num']}: {s['name']}")
else:
    print(f"\n❌ Error {response.status_code}: {response.text}")
