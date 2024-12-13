import json

import numpy as np
import util.color as color
from box import Box


class Uld:
    def __init__(self, file_path, uld_height=0.2, uld_color=[0, 0, 0, 1]):
        with open(file_path) as file:
            json_uld = json.load(file)

        uld_half_extents = np.array([json_uld['properties']["width"] / 100 / 2,
                                     json_uld['properties']["depth"] / 100 / 2,
                                     uld_height / 2])
        uld_position = np.zeros(3) + uld_half_extents
        uld_mass = json_uld['properties']['standardWeight']
        uld_color = uld_color
        self.body = Box(uld_half_extents, uld_position, [0, 0, 0], uld_mass, uld_color)

        self.items = []
        for item in json_uld["placedItems"]:
            item_half_extents = np.array([
                item['shape']["width"] / 100 / 2,
                item['shape']["depth"] / 100 / 2,
                item['shape']["height"] / 100 / 2
            ])
            item_start_position = np.array(
                [item['x'], item['z'], item['y'] + uld_height*100]) / 100 + item_half_extents
            item_mass = item['weight']
            self.items.append(Box(item_half_extents, item_start_position, [0, 0, 0], item_mass, color.create_random()))
