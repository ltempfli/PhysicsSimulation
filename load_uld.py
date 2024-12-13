import json

import pybullet as p
import os
import numpy as np
import random


class Uld:
    def __init__(self, file_path, uld_height=0.2, uld_color=[0, 0, 0, 1]):
        with open(file_path) as file:
            json_uld = json.load(file)

        self.half_extents = np.array([json_uld['properties']["width"] / 100 / 2,
                             json_uld['properties']["depth"] / 100 / 2,
                             uld_height / 2])
        self.uld_mass = json_uld['properties']['standardWeight']

        self.uld_body = create_box(
            self.half_extents,
             np.zeros(3) + self.half_extents,
            [0, 0, 0],
            self.uld_mass,
            uld_color
        )

        self.items = []
        for item in json_uld["placedItems"]:
            item_half_extents = np.array([
                item['shape']["width"] / 100 / 2,
                item['shape']["depth"] / 100 / 2,
                item['shape']["height"] / 100 / 2
            ])
            item_start_position = np.array([item['x'], item['z'], item['y'] + uld_height]) + item_half_extents
            print(item_start_position)
            item_mass = item['weight']
            self.items.append(
                create_box(
                    item_half_extents,
                    item_start_position,
                    [0, 0, 0],
                    item_mass,
                    create_random_color()
                )
            )


def create_random_color():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return [r, g, b, 1]


def create_box(box_half_extents: np.array, box_start_pos: np.array, box_rotation: list, mass: int,
               rgbaColor: list) -> int:
    collision_shape = p.createCollisionShape(
        shapeType=p.GEOM_BOX, halfExtents=box_half_extents
    )
    # Create the visual shape (used for rendering in GUI)
    visual_shape = p.createVisualShape(
        shapeType=p.GEOM_BOX, halfExtents=box_half_extents, rgbaColor=rgbaColor  # Red box
    )
    # Create the multi-body object (combines collision and visual shapes)
    return p.createMultiBody(
        baseMass=mass,  # Mass of the box
        baseCollisionShapeIndex=collision_shape,
        baseVisualShapeIndex=visual_shape,
        basePosition=box_start_pos,
        baseOrientation=p.getQuaternionFromEuler(box_rotation)
    )
