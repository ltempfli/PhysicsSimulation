import pybullet as p

class Box:
    def __init__(self, half_extends, start_position, rotation, mass, color):
        self.half_extents = half_extends
        self.start_position = start_position
        self.rotation = rotation
        self.mass = mass
        self.color = color

    def render(self) -> int:
        collision_shape = p.createCollisionShape(
            shapeType=p.GEOM_BOX, halfExtents=self.half_extents,
        )
        visual_shape = p.createVisualShape(
            shapeType=p.GEOM_BOX, halfExtents=self.half_extents, rgbaColor=self.color
        )
        return p.createMultiBody(
            baseMass=self.mass,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=self.start_position,
            baseOrientation=p.getQuaternionFromEuler(self.rotation),
        )

    def stringify(self) -> str:
        return (f"Box(half_extents={self.half_extents}, start_position={self.start_position}, "
                f"rotation={self.rotation}, mass={self.mass}, color={self.color})")