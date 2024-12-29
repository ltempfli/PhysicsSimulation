import json
import numpy as np

def extract_data(data_batch: int, file_path: str, scaling_factor: float, uld_height: float) -> dict:
    uld_dict = {}

    with open(file_path) as file:
        json_uld = json.load(file)

    if data_batch ==1:
        uld_dict["uld_half_extents"] = np.array([json_uld['properties']["width"] * scaling_factor / 2,
                                     json_uld['properties']["depth"] * scaling_factor / 2,
                                     uld_height * scaling_factor / 2])

    else:
        uld_dict["uld_half_extents"] = np.array([json_uld["properties"]["bottomArea"][2]["y"] * scaling_factor / 2,
                                                json_uld["properties"]["bottomArea"][2]["x"] * scaling_factor / 2,
                                                uld_height * scaling_factor / 2])
    uld_dict["uld_position"] = np.zeros(3) + uld_dict["uld_half_extents"]
    uld_dict["uld_mass"] = json_uld['properties']['standardWeight']
    uld_dict["total_weight"] = json_uld['properties']['standardWeight']
    scaling_factor = scaling_factor
    items = []
    for item in json_uld["placedItems"]:
        item_half_extents = np.array([
            item['shape']["width"] * scaling_factor / 2,
            item['shape']["depth"] * scaling_factor / 2,
            item['shape']["height"] * scaling_factor / 2
        ])
        item_start_position = np.array(
            [item['x'], item['z'], item['y'] + uld_height]) * scaling_factor + item_half_extents
        item_mass = item['weight']
        uld_dict["total_weight"] += item_mass
        items.append({"item_half_extents": item_half_extents, "item_start_position": item_start_position, "item_mass": item_mass})
        uld_dict["items"] = items

    return uld_dict

def rotate_uld(uld_data: dict, degree: int) -> dict:
    return {}

def mirror_uld_horizontal(uld_data: dict) -> dict:
    return {}