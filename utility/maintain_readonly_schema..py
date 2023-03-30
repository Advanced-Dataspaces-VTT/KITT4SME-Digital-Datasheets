import json

def get_all_keys(json_file_path):
    with open(json_file_path) as f:
        data = json.load(f)
    keys = []
    for key in data.keys():
        keys.append(key)
        if isinstance(data[key], dict):
            keys += [f"{key}.{subkey}" for subkey in get_all_keys_dict(data[key])]
    return keys

def get_all_keys_dict(data_dict):
    keys = []
    for key in data_dict.keys():
        keys.append(key)
        if isinstance(data_dict[key], dict):
            keys += [f"{key}.{subkey}" for subkey in get_all_keys_dict(data_dict[key])]
    return keys

# Get all keys from JSON file
json_file_path = '../frontend/src/static/content.json'
all_keys = get_all_keys(json_file_path)

# Create dictionary of keys with default values
key_objects = {}
for key in all_keys:
    key_objects[key] = {"ui:readonly": True, "ui:disabled": True}

# Write key objects to new JSON file
with open('key_objects.json', 'w') as f:
    json.dump(key_objects, f, indent=2)
