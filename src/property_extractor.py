import re

def extract_properties(vision_data):
    properties = {
        'name': 'Unknown',
        'type': 'Unknown',
        'color': [],
        'size': 'Unknown',
        'additional_attributes': {
            'condition': 'Unknown',
            'features': [],
            'setting': 'Unknown',
            'associated_items': [],
            'brand': 'Unknown',
            'character': 'Unknown'
        }
    }

    # Extract each property using regex
    name_match = re.search(r'1\.\s*Name:\s*(.+)', vision_data)
    if name_match:
        properties['name'] = name_match.group(1).strip()

    type_match = re.search(r'2\.\s*Type:\s*(.+)', vision_data)
    if type_match:
        properties['type'] = type_match.group(1).strip()

    colors_match = re.search(r'3\.\s*Colors:\s*(.+)', vision_data)
    if colors_match:
        properties['color'] = [color.strip() for color in colors_match.group(1).split(',')]

    size_match = re.search(r'4\.\s*Size:\s*(.+)', vision_data)
    if size_match:
        properties['size'] = size_match.group(1).strip()

    condition_match = re.search(r'5\.\s*Condition:\s*(.+)', vision_data)
    if condition_match:
        properties['additional_attributes']['condition'] = condition_match.group(1).strip()

    features_match = re.search(r'6\.\s*Features:\s*(.+)', vision_data)
    if features_match:
        properties['additional_attributes']['features'] = [feature.strip() for feature in features_match.group(1).split(',')]

    setting_match = re.search(r'7\.\s*Setting:\s*(.+)', vision_data)
    if setting_match:
        properties['additional_attributes']['setting'] = setting_match.group(1).strip()

    associated_items_match = re.search(r'8\.\s*Associated Items:\s*(.+)', vision_data)
    if associated_items_match:
        items = associated_items_match.group(1).strip()
        if items.lower() not in ['none', 'none prominent']:
            properties['additional_attributes']['associated_items'] = [item.strip() for item in items.split(',')]

    brand_match = re.search(r'9\.\s*Brand:\s*(.+)', vision_data)
    if brand_match:
        brand = brand_match.group(1).strip()
        if brand.lower() not in ['unknown', 'unidentifiable']:
            properties['additional_attributes']['brand'] = brand

    character_match = re.search(r'10\.\s*Character:\s*(.+)', vision_data)
    if character_match:
        character = character_match.group(1).strip()
        if character.lower() not in ['none', 'unknown']:
            properties['additional_attributes']['character'] = character

    # Remove empty fields
    properties['additional_attributes'] = {k: v for k, v in properties['additional_attributes'].items() if v and v not in ['Unknown', []]}

    return properties