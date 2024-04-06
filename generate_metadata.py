import json

def generate_metadata(farm_data):
    """
    Generate metadata JSON from farm data.
    """
    metadata = {
        "name": f"{farm_data['farm_name']} NFT",
        "description": f"An NFT representing a farm named {farm_data['farm_name']} located in {farm_data['location']}.",
        "attributes": farm_data
    }
    return json.dumps(metadata, indent=2)

def save_metadata(metadata_json, filename):
    """
    Save metadata JSON to a file.
    """
    with open(filename, 'w') as f:
        f.write(metadata_json)
    print(f"Metadata JSON file '{filename}' created successfully!")

# Example hashmap for farm data
farm_data = {
    "farm_name": "redfarm",
    "location": "Lebanon",
    "size": "100 hectares"
}

# Generate metadata JSON
metadata_json = generate_metadata(farm_data)

# Save metadata JSON to a file
save_metadata(metadata_json, 'redfarm_metadata.json')
