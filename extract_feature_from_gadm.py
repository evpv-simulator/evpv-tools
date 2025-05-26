import json

# Set the name you want to keep
TARGET_NAME = "AddisAbeba"  # Change this to the desired NAME_1 value
INPUT_FILE = "gadm41_ETH_1.json"
OUTPUT_FILE = "AddisAbeba.json"

# Load the GeoJSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter features by NAME_1
data["features"] = [feature for feature in data["features"]
                    if feature["properties"].get("NAME_1") == TARGET_NAME]

# Save the filtered GeoJSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Filtered GeoJSON saved to {OUTPUT_FILE}")