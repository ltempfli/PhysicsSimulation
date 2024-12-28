import json

import numpy as np
import util.color as color
from model.box import Box
import pybullet as p


class Uld:
    def __init__(self, file_path, uld_height=20, uld_color=None, scaling_factor=1.0, uld_friction=0.5, item_friction=0.3):
        if uld_color is None:
            uld_color = [0, 0, 0, 1]

        with open(file_path) as file:
            json_uld = json.load(file)

        # Apply scaling factor to dimensions
        uld_half_extents = np.array([json_uld['properties']["width"] * scaling_factor / 2,
                                     json_uld['properties']["depth"] * scaling_factor / 2,
                                     uld_height * scaling_factor / 2])
        uld_position = np.zeros(3) + uld_half_extents
        self.uld_mass = json_uld['properties']['standardWeight']
        self.body = Box(uld_half_extents.tolist(), uld_position.tolist(), [0, 0, 0], self.uld_mass, uld_color, scaling_factor, uld_friction)
        self.total_weight = json_uld['properties']['standardWeight']
        self.scaling_factor = scaling_factor
        self.items = []
        for item in json_uld["placedItems"]:
            item_half_extents = np.array([
                item['shape']["width"] * scaling_factor / 2,
                item['shape']["depth"] * scaling_factor / 2,
                item['shape']["height"] * scaling_factor / 2
            ])
            item_start_position = np.array(
                [item['x'], item['z'], item['y'] + uld_height]) * scaling_factor + item_half_extents
            item_mass = item['weight']
            self.total_weight += item_mass
            self.items.append(Box(item_half_extents.tolist(), item_start_position.tolist(), [0, 0, 0], item_mass, color.create_random(), scaling_factor, item_friction))

    def evaluate_nfb(self) -> tuple:
        if len(self.items) == 0:
            return 0, 0
        nfb_counter = 0
        for item in self.items:
            if item.has_fallen():
                nfb_counter += 1
        return nfb_counter, nfb_counter/len(self.items)

    def get_velocity(self, position: int) -> float:
        linear_velocity, angular_velocity = p.getBaseVelocity(self.body.id)
        return linear_velocity[position]


    def get_com(self) -> np.array:
        x_numerator = 0
        y_numerator = 0
        z_numerator = 0
        denominator = 0

        def add_pos_weight(x: int, y: int, z: int, sum_weight: int, position: list, mass: int) -> (int, int, int, int):
            x += position[0] * mass
            y += position[1] * mass
            z += position[2] * mass
            sum_weight += mass
            return x, y, z, sum_weight
        x_numerator, y_numerator, z_numerator, denominator =add_pos_weight(x_numerator,
                                                                           y_numerator,
                                                                           z_numerator,
                                                                           denominator,
                                                                           self.body.get_position(),
                                                                           self.uld_mass
                                                                           )
        for item in self.items:
            x_numerator, y_numerator, z_numerator, denominator = add_pos_weight(x_numerator,
                                                                                y_numerator,
                                                                                z_numerator,
                                                                                denominator,
                                                                                item.get_position(),
                                                                                item.mass)
        return np.array(
            #[ x_numerator/ denominator, y_numerator / denominator, z_numerator / denominator]
            [x_numerator / denominator, y_numerator / denominator, 0.2]
        )


