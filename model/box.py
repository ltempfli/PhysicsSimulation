import pybullet as p
import math

class Box:
    def __init__(self,
                 half_extends: list = (0.5, 0.5, 0.5),
                 start_position: list = (0, 0, 0.5),
                 rotation: list = (0, 0, 0),
                 mass: int = 10,
                 color: list = (1,0,0,1),
                 scaling_factor = 1.0,
                 friction = None):
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

    def create_wal(self, width: float = 0.05, margin = 0.05)-> int :
        shape = [self.half_extents[0],
                 0.05,
                 self.half_extents[2] + self.max_height -margin
                 ]
        position = [0.5,-0.060,0.5]
        #back
        #position[1] = -self.start_position[1]+ width - self.half_extents[1]+0.01
        position[2] = margin + 0.5
        #front
        #position[1] = -self.start_position[1] - width
        #left
        #position[1] = -self.start_position[0] - width
        #right
        #position[1] = -self.start_position[0] - width
        wall_size = [0.5, 0.05, 0.5]  # Wall with height 0.5, thin width 0.05
        position_back = [0.5, 1.35, 0.45]
        parent_position= [0, 0.55, 0.6]

        self.create_constraint(position_back,parent_position, wall_size)

        position_front = [0.5, -1.35, 0.5]
        parent_position= [0, -0.55, 0.6]

        self.create_constraint(position_front,parent_position, wall_size)

        wall_size = [0.05, 0.6, 0.5]
        position_left = [0, 0.5, 0.5]
        parent_position = [-0.55, 0, 0.6]

        self.create_constraint(position_left, parent_position, wall_size)

        wall_size = [0.05, 0.6, 0.5]
        position_right = [1.35, 0.5, 0.5]
        parent_position = [0.55, 0, 0.6]

        self.create_constraint(position_right, parent_position, wall_size)
        return 1

    def create_constraint(self, position: list, parent_position: list, wall_size: list, rotate: bool = False) -> tuple:
        wall_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=wall_size)
        wall_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=wall_size, rgbaColor=[0.8, 0.8, 0.8, 0.2])

        # Create the wall at an initial position
        wall = p.createMultiBody(baseMass=1,  # Dynamic object
                                 baseCollisionShapeIndex=wall_collision_shape,
                                 baseVisualShapeIndex=wall_visual_shape,
                                 basePosition=position
                                 )
        p.changeDynamics(wall, -1, collisionMargin=0.0)

        # Attach the wall to the pallet using a fixed joint
        constraint_id = p.createConstraint(
            parentBodyUniqueId=self.id,
            parentLinkIndex=-1,
            childBodyUniqueId=wall,
            childLinkIndex=-1,
            jointType=p.JOINT_FIXED,
            jointAxis=[0, 0, 0],  # Not used for fixed joints
            parentFramePosition=parent_position,
            childFramePosition=[0, 0, 0])

        return constraint_id, wall


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