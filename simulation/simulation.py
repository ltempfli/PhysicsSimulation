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

    p.setPhysicsEngineParameter(numSolverIterations=400)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0, 0, -9.80665)
    plane_id = p.loadURDF("plane.urdf")

    p.changeDynamics(plane_id, -1, lateralFriction=ground_friction)

    uld = Uld(file_path, scaling_factor=scaling_factor,
              uld_friction=uld_friction, item_friction=item_friction)
    uld_id = uld.body.render()
    for item in uld.items:
        item.render()



    velocity_x = []
    velocity_y = []
    velocity_z = []

    for i in range(240 * duration):
        if 240 <= i:  # wait one second before force is applied
            """
            current_velocity = uld.get_velocity(0)
            print(current_velocity)
            next_velocity = calculate_next_velocity(current_velocity, i-240, force_duration, 240, max_g_force)
            print(next_velocity)
            p.resetBaseVelocity(uld_id, linearVelocity=[next_velocity, 0, 0], angularVelocity=[0, 0, 0])
            """
            com = uld.get_com()
            force = calculate_force(uld_friction * ground_friction, uld.total_weight, force_direction_vector, i - 240,
                    max_g_force, force_duration)
            p.applyExternalForce(uld_id, -1, force, com, p.WORLD_FRAME)

        move_camera(uld_id)
        p.stepSimulation()
        velocity_x.append(uld.get_velocity(0))
        velocity_y.append(uld.get_velocity(1))
        velocity_z.append(uld.get_velocity(2))
        #time.sleep(1 / 240)

    nfb, nfb_rel = uld.evaluate_nfb()
    p.disconnect()
    return nfb, nfb_rel, calculate_acceleration(velocity_x), calculate_acceleration(velocity_y), calculate_acceleration(velocity_z)


def calculate_force(friction: float, mass: float, direction_vector: list, elapsed_seconds: int,
                                     max_g_force: float, apply_force_seconds: int ) -> np.array:
    acceleration = max_g_force * 9.80665
    sinusoidal_force = mass * acceleration * np.sin(np.pi * (elapsed_seconds/ (apply_force_seconds * 240))) + friction * mass * 9.80665
    return np.array(direction_vector) * sinusoidal_force


def calculate_next_velocity(current_velocity: float, elapsed_seconds: int, apply_force_seconds: int, step_time: int, max_g_force: float)-> float:
    acceleration = max_g_force * 9.80665
    #return current_velocity + np.sin(np.pi * (elapsed_seconds/ (apply_force_seconds * 240))) * acceleration * (1/step_time)
    return current_velocity + acceleration * (1 / step_time)

def move_camera(box_id: int, camera_distance: int = 5) -> None:
    position, orientation = p.getBasePositionAndOrientation(box_id)
    p.resetDebugVisualizerCamera(camera_distance, -30, -45, position)


def calculate_acceleration(linear_velocity: list) -> list:
    acceleration = []
    for i in range(1, len(linear_velocity)):
        acceleration.append(
            (linear_velocity[i] - linear_velocity[i-1]) / (1 / 240)
        )
    return acceleration


