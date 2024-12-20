import pybullet as p

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
        p.changeDynamics(object_id, -1 , lateralFriction=self.friction)
        self.id = object_id
        return object_id

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

    def print_velocity(self) -> None:
        linear_velocity, angular_velocity = p.getBaseVelocity(self.id)
        return linear_velocity