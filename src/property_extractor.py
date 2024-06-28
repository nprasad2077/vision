import json
import re

def extract_properties(vision_data):
    # Define patterns for each property
    patterns = {
        'name': r'name:\s*(.+)',
        'type': r'type:\s*(.+)',
        'color': r'color:\s*(.+)',
        'size': r'size:\s*(.+)'
    }

    properties = {}

    for prop, pattern in patterns.items():
        match = re.search(pattern, vision_data, re.IGNORECASE)
        if match:
            properties[prop] = match.group(1).strip()
        else:
            properties[prop] = "Unknown"

    # Extract any additional attributes
    additional_attrs = re.findall(r'(\w+):\s*(.+)', vision_data)
    for attr, value in additional_attrs:
        if attr.lower() not in properties:
            properties[attr.lower()] = value.strip()

    return properties