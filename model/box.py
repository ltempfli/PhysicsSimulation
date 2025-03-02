import pybullet as p
import math

class Box:
    def __init__(self,
                 half_extends: list = (0.5, 0.5, 0.5),
                 start_position: list = (0, 0, 0.5),
                 rotation: list = (0, 0, 0),
                 mass: int = 10,
                 color: list = (1, 0, 0, 1),
                 scaling_factor=1.0,
                 friction=None):
        self.half_extents = half_extends
        self.start_position = start_position
        self.rotation = rotation
        self.mass = mass
        self.color = color
        self.scaling_factor = scaling_factor
        self.friction = friction
        self.id = None
        self.max_height = 1

    def render(self) -> int:
        collision_shape = p.createCollisionShape(
            shapeType=p.GEOM_BOX, halfExtents=self.half_extents,
        )
        visual_shape = p.createVisualShape(
            shapeType=p.GEOM_BOX, halfExtents=self.half_extents, rgbaColor=self.color
        )
        object_id = p.createMultiBody(
            baseMass=self.mass,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=self.start_position,
            baseOrientation=p.getQuaternionFromEuler(self.rotation),
        )

        self.id = object_id
        return object_id

    def create_walls(self, width: float = 0.05, height: float = None, margin=0.02) -> None:
        half_extents = self.half_extents
        start_position = self.start_position

        if height is None:
            if half_extents[0] > half_extents[1]:
                height = half_extents[0]
            else:
                height = half_extents[1]

        # Back Wall
        wall_size = [half_extents[0], width, height + half_extents[2]]
        position_back = [start_position[0],
                         start_position[1] + half_extents[1] + width + margin,
                         start_position[2]]
        parent_position_back = [0, half_extents[1] + width + margin, 0]
        create_constraint(position_back, parent_position_back, wall_size, self.id)

        # Front Wall
        position_front = [start_position[0],
                          start_position[1] - half_extents[1] - width - margin,
                          start_position[2]]
        parent_position_front = [0, -half_extents[1] - width - margin, 0]
        create_constraint(position_front, parent_position_front, wall_size, self.id)

        # Left Wall
        wall_size = [width, half_extents[1], height + half_extents[2]]
        position_left = [start_position[0] - half_extents[0] - width - margin,
                         start_position[1], start_position[2]]
        parent_position_left = [-half_extents[0] - width - margin, 0, 0]
        create_constraint(position_left, parent_position_left, wall_size, self.id)

        # Right Wall
        position_right = [start_position[0] + half_extents[0] + width + margin,
                          start_position[1], start_position[2]]
        parent_position_right = [half_extents[0] + width + margin, 0, 0]
        create_constraint(position_right, parent_position_right, wall_size, self.id)

        wall_size = [half_extents[0], half_extents[1], width]
        position_top = [start_position[0], start_position[1], start_position[2] + 2 * height + 10 * margin]
        parent_position_top = [0, 0, half_extents[2] + 2 * height + margin]
        create_constraint(position_top, parent_position_top, wall_size, self.id)

    def has_fallen(self):
        return abs(self.start_position[2] - self.get_position()[2]) > 1 * self.scaling_factor

    def stringify(self) -> str:
        return (f"Box(half_extents={self.half_extents}, start_position={self.start_position}, "
                f"rotation={self.rotation}, mass={self.mass}, color={self.color})")

    def get_friction(self) -> float:
        dynamics_info = p.getDynamicsInfo(self.id, -1)
        lateral_friction = dynamics_info[1]
        return lateral_friction

    def get_position(self) -> list:
        position, orientation = p.getBasePositionAndOrientation(self.id)
        return [position[0], position[1], position[2]]

    def get_velocity(self) -> None:
        linear_velocity, angular_velocity = p.getBaseVelocity(self.id)
        return linear_velocity

    def print_velocity(self) -> None:
        linear_velocity, angular_velocity = p.getBaseVelocity(self.id)
        print(linear_velocity)

    def print_friction(self) -> None:
        dynamics_info = p.getDynamicsInfo(self.id, -1)
        lateral_friction = dynamics_info[1]
        print(lateral_friction)

    def print_position(self) -> None:
        position, orientation = p.getBasePositionAndOrientation(self.id)
        print([position[0], position[1], position[2]])

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
        jointAxis=[0, 0, 0],  # Not used for fixed joints
        parentFramePosition=parent_position,
        childFramePosition=[0, 0, 0])

    return constraint_id, wall