from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class ItemData:
    name: str
    type: str
    color: List[str]
    size: str
    additional_attributes: Dict[str, any]


def format_item_data(properties: Dict[str, any]) -> ItemData:
    return ItemData(
        name=properties["name"],
        type=properties["type"],
        color=properties["color"],
        size=properties["size"],
        additional_attributes=properties["additional_attributes"],
    )


def item_to_dict(item_data: ItemData) -> Dict[str, any]:
    return asdict(item_data)
