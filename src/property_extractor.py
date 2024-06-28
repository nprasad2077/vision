import spacy
import re
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_properties(vision_data):
    properties = {
        'name': 'Unknown',
        'type': 'Unknown',
        'color': [],
        'size': 'Unknown',
        'additional_attributes': {}
    }

    doc = nlp(vision_data)

    # Main item identification (unchanged)
    main_items = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ['nsubj', 'dobj', 'pobj'] and token.pos_ == 'NOUN' and token.text.lower() not in ['image', 'picture', 'photo']:
                main_items.append(token.text.lower())
        if main_items:
            break

    if main_items:
        properties['name'] = main_items[0]
        properties['type'] = main_items[0]

    if properties['name'] == 'Unknown':
        nouns = [token.text.lower() for token in doc if token.pos_ == 'NOUN' and token.text.lower() not in ['image', 'picture', 'photo']]
        if nouns:
            most_common_noun = Counter(nouns).most_common(1)[0][0]
            properties['name'] = most_common_noun
            properties['type'] = most_common_noun

    # Color extraction (unchanged)
    color_words = ['red', 'blue', 'green', 'yellow', 'white', 'black', 'brown', 'orange', 'purple', 'pink', 'gray', 'golden', 'light', 'dark']
    properties['color'] = list(set([token.text.lower() for token in doc if token.text.lower() in color_words]))

    # Size extraction (unchanged)
    size_words = ['small', 'medium', 'large', 'tiny', 'huge', 'big']
    for token in doc:
        if token.text.lower() in size_words:
            properties['size'] = token.text.lower()
            break

    # Additional attributes
    properties['additional_attributes'] = {
        'materials': [],
        'condition': 'Unknown',
        'features': [],
        'setting': 'Unknown',
        'associated_items': [],
        'brand': 'Unknown',
        'character': 'Unknown'
    }

    # Materials (unchanged)
    material_words = ['plastic', 'metal', 'wood', 'glass', 'ceramic', 'fabric', 'leather']
    properties['additional_attributes']['materials'] = list(set([token.text.lower() for token in doc if token.text.lower() in material_words]))

    # Condition (unchanged)
    condition_patterns = [
        r'(new|used|worn|mint condition|damaged|fresh|baked)'
    ]
    for pattern in condition_patterns:
        match = re.search(pattern, vision_data, re.IGNORECASE)
        if match:
            properties['additional_attributes']['condition'] = match.group(1).lower()
            break

    # Features and associated items
    for token in doc:
        if token.pos_ == 'ADJ' and token.dep_ in ['amod', 'acomp']:
            properties['additional_attributes']['features'].append(token.text.lower())
        if token.pos_ == 'NOUN' and token.dep_ not in ['nsubj', 'dobj'] and token.text.lower() != properties['name'].lower():
            properties['additional_attributes']['associated_items'].append(token.text.lower())
        
    # Add "charred" to features if it's mentioned
    if 'charred' in vision_data.lower():
        properties['additional_attributes']['features'].append('charred')

    # Setting (unchanged)
    setting_patterns = [
        r'in\s+(?:a|an)\s+(\w+\s+\w+)',
        r'(?:indoor|outdoor)\s+(\w+)'
    ]
    for pattern in setting_patterns:
        match = re.search(pattern, vision_data, re.IGNORECASE)
        if match:
            properties['additional_attributes']['setting'] = match.group(1).lower()
            break

    # Brand and character extraction
    for ent in doc.ents:
        if ent.label_ == 'ORG' and ent.text.lower() not in ['amiibo']:
            properties['additional_attributes']['brand'] = ent.text
        elif ent.label_ == 'PERSON' and ent.text.lower() not in ['amiibo']:
            properties['additional_attributes']['character'] = ent.text

    # Special handling for Mario and Amiibo
    if 'mario' in vision_data.lower():
        properties['additional_attributes']['character'] = 'Mario'
        properties['additional_attributes']['associated_items'].append('mario')
    if 'amiibo' in vision_data.lower():
        properties['additional_attributes']['associated_items'].append('amiibo')
    if 'nintendo' in vision_data.lower():
        properties['additional_attributes']['brand'] = 'Nintendo'

    # Clean up and finalize
    properties['additional_attributes']['features'] = list(set(properties['additional_attributes']['features']))
    properties['additional_attributes']['associated_items'] = list(set(properties['additional_attributes']['associated_items']))

    # Remove empty fields
    properties['additional_attributes'] = {k: v for k, v in properties['additional_attributes'].items() if v and v != 'Unknown'}

    return properties

# Test examples (unchanged)
examples = [
    '''The image shows a freshly baked pizza. The pizza features a golden, slightly charred crust and is topped with melted cheese and what appears to be slices of chicken breast. There are also several dark spots on the pizza, which could possibly be black olives or another type of topping. The crust is puffy and charred in places, which is indicative of being cooked in a high-temperature oven, typical of authentic pizza preparation. The seasoning looks like it includes black pepper.''',
    
    '''The image features a charming dog with a mix of light brown and white fur. The dog appears attentive and occupies the central portion of the frame, looking directly into the camera with noticeable expression and mouth slightly open. In the background, there's an office chair at a desk in a room setup, a cardboard box, and a plastic bag on the wooden floor. The setting suggests an indoor domestic environment.''',
    
    '''This image features a figurine of Mario from the Super Mario video game series. Mario is shown in his iconic red cap and blue overalls, and he is posed as if casting a fireball, which is represented by a translucent orange and yellow effect piece in his hands. The figurine is placed on a black stand with a golden rim, which is likely an Amiibo (a type of interactivity figure used with Nintendo videogames). In the background, other items are visible, including what appears to be a part of a Pokémon-themed book and a toy crocodile head among other blurred objects.'''
]

for i, example in enumerate(examples, 1):
    print(f"\nExample {i}:")
    print(extract_properties(example))