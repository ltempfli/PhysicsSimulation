import json

import numpy as np
import util.color as color
from model.box import Box
import pybullet as p


class Uld:
    def __init__(self, uld_dict: dict, uld_color=None, uld_friction=0.5, item_friction=0.3):
        if uld_color is None:
            uld_color = [0, 0, 0, 1]

        self.uld_mass = uld_dict["uld_mass"]
        self.body = Box(uld_dict["uld_half_extents"].tolist(), uld_dict["uld_position"].tolist(), [0, 0, 0],
                        self.uld_mass, uld_color, uld_friction)
        self.total_weight = uld_dict["total_weight"]
        self.items = [
            Box(item["item_half_extents"].tolist(), item["item_start_position"].tolist(), [0, 0, 0], item["item_mass"],
                color.create_random(), item_friction)
            for item in uld_dict["items"]]
        self.item_count = len(uld_dict["items"])

    def evaluate_nfb(self, threshold_relative: float = 0.01) -> tuple:
        if len(self.items) == 0:
            return 0, 0
        nfb_counter = 0
        boxes = []
        for item in self.items:
            threshold = (self.body.half_extents[0] + self.body.half_extents[1]) / 2 * threshold_relative
            if item.has_fallen(threshold):
                nfb_counter += 1
                boxes.append(item.id)
        return nfb_counter, nfb_counter / len(self.items), boxes

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

        x_numerator, y_numerator, z_numerator, denominator = add_pos_weight(x_numerator,
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
            [ x_numerator/ denominator, y_numerator / denominator, z_numerator / denominator]
            # [x_numerator / denominator, y_numerator / denominator, 0.2]
        )

    def create_walls(self, width: float = 0.05, height: float = None, margin=None) -> None:
        half_extents = self.body.half_extents
        start_position = self.body.start_position

        if height is None:
            if half_extents[0] > half_extents[1]:
                height = half_extents[0]
            else:
                height = half_extents[1]

        def create_constraint(position: list, parent_position: list, wall_size: list, parent_body_id) -> tuple:
            wall_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=wall_size)
            wall_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=wall_size, rgbaColor=[0.8, 0.8, 0.8, 0.4])

            # Create the wall at an initial position
            wall = p.createMultiBody(baseMass=1,  # Dynamic object
                                     baseCollisionShapeIndex=wall_collision_shape,
                                     baseVisualShapeIndex=wall_visual_shape,
                                     basePosition=position
                                     )
            p.changeDynamics(wall, -1, collisionMargin=0.0)

            # Attach the wall to the pallet using a fixed joint
            constraint_id = p.createConstraint(
                parentBodyUniqueId=parent_body_id,
                parentLinkIndex=-1,
                childBodyUniqueId=wall,
                childLinkIndex=-1,
                jointType=p.JOINT_FIXED,
                jointAxis=[0, 0, 0],
                parentFramePosition=parent_position,
                childFramePosition=[0, 0, 0])

            return constraint_id, wall

        # Back Wall
        wall_size = [half_extents[0], width, height + half_extents[2]]
        position_back = [start_position[0],
                         start_position[1] + half_extents[1] + width + margin + 1,
                         start_position[2] + wall_size[2]]
        parent_position_back = [0, half_extents[1] + width + margin, wall_size[2]]
        create_constraint(position_back, parent_position_back, wall_size, self.body.id)

        # Front Wall
        position_front = [start_position[0],
                          start_position[1] - half_extents[1] - width - margin - 1,
                          start_position[2] + wall_size[2]]
        parent_position_front = [0, -half_extents[1] - width - margin, wall_size[2]]
        create_constraint(position_front, parent_position_front, wall_size, self.body.id)

        # Left Wall
        wall_size = [width, half_extents[1], height + half_extents[2]]
        position_left = [start_position[0] - half_extents[0] - width - margin - 1,
                         start_position[1], start_position[2] + wall_size[2]]
        parent_position_left = [-half_extents[0] - width - margin, 0, wall_size[2]]
        create_constraint(position_left, parent_position_left, wall_size, self.body.id)

        # Right Wall
        position_right = [start_position[0] + half_extents[0] + width + margin + 1,
                          start_position[1], start_position[2] + wall_size[2]]
        parent_position_right = [half_extents[0] + width + margin, 0, wall_size[2]]
        create_constraint(position_right, parent_position_right, wall_size, self.body.id)

        # Ceiling
        wall_size = [half_extents[0], half_extents[1], width]
        position_top = [start_position[0], start_position[1], start_position[2] + 2 * height + margin + 1]
        parent_position_top = [0, 0, half_extents[2] + 2 * height + margin]
        create_constraint(position_top, parent_position_top, wall_size, self.body.id)
