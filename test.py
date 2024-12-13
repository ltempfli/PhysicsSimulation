import pybullet as p
import time
import pybullet_data


# Connect to PyBullet (GUI)
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set gravity
p.setGravity(0, 0, -9.8)


plane_id = p.loadURDF("plane.urdf")



def create_box(box_half_extents: list, box_start_pos: list, box_rotation: list, mass: int, rgbaColor: list) -> int:


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
def move_camera(box_id: int, camera_offset: int = [5, 0, 3]) -> None:
    box_position, _ = p.getBasePositionAndOrientation(box_id)

    # Compute the new camera position by adding the offset to the box's position
    camera_position = [
        box_position[0] + camera_offset[0],  # x = box's x + offset
        box_position[1] + camera_offset[1],  # y = box's y + offset
        box_position[2] + camera_offset[2]   # z = box's z + offset
    ]

    # Set the camera's position relative to the box's position
    p.resetDebugVisualizerCamera(cameraDistance=5, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=box_position)


box_half_extents = [0.5, 0.5, 0.5]
box_start_pos = [0,0,0.5]
rgbaColor=[1, 0, 0, 1]
box_rotation =[0, 0 , 0]
mass = 10

big_box = create_box(
    box_half_extents,
    box_start_pos,
    box_rotation,
    mass,
    rgbaColor
)

small_box = create_box(
    [0.2,0.2,0.2],
    [0,0,1.2],
    box_rotation,
    1,
    [0, 0, 1, 1]
)

position = [0, 0, 0.5]
force = [80, 0, 0]  # Force to apply to the car to simulate acceleration
#p.applyExternalForce(big_box, -1, force, position, p.WORLD_FRAME)



# Adjust the camera to make sure we can see the box
#p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=50, cameraPitch=-30, cameraTargetPosition=[0, 0, 0])

# Simulation loop
for _ in range(10000):
    p.applyExternalForce(big_box, -1, force, position, p.WORLD_FRAME)
    move_camera(big_box)
    p.stepSimulation()
    time.sleep(1/240)

# Disconnect from PyBullet
p.disconnect()

