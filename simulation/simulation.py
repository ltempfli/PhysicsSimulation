import pybullet as p
import pybullet_data
import time
import numpy as np

from model.uld import Uld


def simulate(file_path=None,
             visual_simulation=False,
             duration=None,
             max_g_force=None,
             force_duration=None,
             force_direction_vector=None,
             ground_friction=None,
             uld_friction=None,
             item_friction=None,
             scaling_factor=None) -> tuple:
    if visual_simulation:
        p.connect(p.GUI)
    else:
        p.connect(p.DIRECT)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0, 0, -9.80665)
    plane_id = p.loadURDF("plane.urdf")

    p.changeDynamics(plane_id, -1, lateralFriction=ground_friction)

    uld = Uld(file_path, scaling_factor=scaling_factor,
              uld_friction=uld_friction, item_friction=item_friction)
    uld_id = uld.body.render()
    for item in uld.items:
        item.render()

    position, _ = p.getBasePositionAndOrientation(uld_id)

    for i in range(240 * duration):
        if int(i / 240) >= 1:  # wait one second before force is applied
            force, _ = calculate_force_and_acceleration(item_friction, uld.body.mass, force_direction_vector, int((i - 240) / 240),
                                                        max_g_force, force_duration)
            p.applyExternalForce(uld_id, -1, force, position, p.WORLD_FRAME)
        move_camera(uld_id)
        p.stepSimulation()
        time.sleep(1 / 240)

    nfb, nfb_rel = uld.evaluate_nfb()
    p.disconnect()
    return nfb, nfb_rel


def calculate_force_and_acceleration(friction: float, mass: float, direction_vector: list, elapsed_seconds: int,
                                     max_g_force: float, apply_force_seconds: int) -> tuple:
    if elapsed_seconds >= apply_force_seconds:
        return np.array(direction_vector) * 0, 0

    amplitude = max_g_force * 9.80665
    frequency = 1 / (apply_force_seconds * 2)

    sinusoidal_force = amplitude * np.sin(2 * np.pi * frequency * elapsed_seconds)
    frictional_force = friction * mass * 9.80665

    total_force = mass * sinusoidal_force - frictional_force
    if total_force <= 0:
        total_force = 0
    acceleration = total_force / mass

    return np.array(direction_vector) * total_force, acceleration


def move_camera(box_id: int, camera_distance: int = 5) -> None:
    position, orientation = p.getBasePositionAndOrientation(box_id)
    p.resetDebugVisualizerCamera(camera_distance, -30, -45, position)
