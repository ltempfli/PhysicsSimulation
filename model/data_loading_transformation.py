import json
import numpy as np

def extract_data(data_batch: int, file_path: str) -> dict:
    uld_dict = {}

    with open(file_path) as file:
        json_uld = json.load(file)
        width = json_uld['properties']["width"]
        scaling_factor = 1 / width
        uld_height = width * 0.2

    if data_batch == 1:
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


def rotate_uld_right(uld_dict: dict, degree: int) -> dict:
    rotated_uld_dict = {}

    uld_width = uld_dict["uld_half_extents"][0] *2
    uld_depth = uld_dict["uld_half_extents"][1]* 2

    if degree == 90 or degree == 270:
        rotated_uld_dict["uld_half_extents"] = np.array([uld_dict["uld_half_extents"][1], uld_dict["uld_half_extents"][0], uld_dict["uld_half_extents"][2]])
    else:
        rotated_uld_dict["uld_half_extents"] = uld_dict["uld_half_extents"]

    rotated_uld_dict["uld_position"] = np.zeros(3) + rotated_uld_dict["uld_half_extents"]
    rotated_uld_dict["uld_mass"] = uld_dict["uld_mass"]
    rotated_uld_dict["total_weight"] = uld_dict["total_weight"]

    if degree == 90:
        rotated_uld_dict["items"] = [{"item_half_extents": np.array([
                                          item["item_half_extents"][1],
                                          item["item_half_extents"][0],
                                          item["item_half_extents"][2],
                                      ]),
                                      "item_start_position": np.array([
                                          item["item_start_position"][1],
                                          uld_width -item["item_start_position"][0],
                                          item["item_start_position"][2]
                                      ]),
                                      "item_mass": item["item_mass"]
                                      }
                                     for item in uld_dict["items"]]
    elif degree == 180:
        rotated_uld_dict["items"] = [{"item_half_extents": item["item_half_extents"],
                                      "item_start_position": np.array([
                                          uld_width -item["item_start_position"][0],
                                          uld_depth -item["item_start_position"][1],
                                          item["item_start_position"][2]
                                      ]),
                                      "item_mass": item["item_mass"]
                                      }
                                     for item in uld_dict["items"]]
    elif degree == 270:
        rotated_uld_dict["items"] = [{"item_half_extents": np.array([
                                          item["item_half_extents"][1],
                                          item["item_half_extents"][0],
                                          item["item_half_extents"][2],
                                      ]),
                                      "item_start_position": np.array([
                                          uld_depth- item["item_start_position"][1],
                                          item["item_start_position"][0],
                                          item["item_start_position"][2]
                                      ]),
                                      "item_mass": item["item_mass"]
                                      }
                                     for item in uld_dict["items"]]
    return rotated_uld_dict


def mirror_uld_horizontal(uld_dict: dict) -> dict:

    mirrored_uld_dict = {}

    uld_width = uld_dict["uld_half_extents"][0] * 2

    mirrored_uld_dict["uld_half_extents"] = uld_dict["uld_half_extents"]
    mirrored_uld_dict["uld_position"] = np.zeros(3) + mirrored_uld_dict["uld_half_extents"]
    mirrored_uld_dict["uld_mass"] = uld_dict["uld_mass"]
    mirrored_uld_dict["total_weight"] = uld_dict["total_weight"]
    mirrored_uld_dict["items"] = [{
        "item_half_extents": item["item_half_extents"],
        "item_start_position": np.array([
            uld_width - item["item_start_position"][0],
            item["item_start_position"][1],
            item["item_start_position"][2]
        ]),
        "item_mass": item["item_mass"]
    }
        for item in uld_dict["items"]]

    return mirrored_uld_dict


def get_uld_transformations(uld_dict: dict) -> list:
    uld_list = [uld_dict, mirror_uld_horizontal(uld_dict)]
    for degree in [90, 180, 270]:
        rotated_uld = rotate_uld_right(uld_dict, degree)
        mirrored_uld = mirror_uld_horizontal(rotated_uld)
        uld_list.append(rotated_uld)
        uld_list.append(mirrored_uld)
    return uld_list