from dataclasses import dataclass, asdict

@dataclass
class ItemData:
    name: str
    type: str
    color: str
    size: str
    additional_attributes: dict
    
def format_item_data(properties):
    standard_props = ['name', 'type', 'color', 'size']
    additional_attrs = {k: v for k, v in properties.items() if k not in standard_props}
    
    item_data = ItemData(
        name=properties.get('name', 'Unknown'),
        type=properties.get('type', 'Unknown'),
        color=properties.get('color', 'Unknown'),
        size=properties.get('size', 'Unknown'),
        additional_attributes=additional_attrs
    )
    
    return item_data


def item_to_dict(item_data):
    return asdict(item_data)