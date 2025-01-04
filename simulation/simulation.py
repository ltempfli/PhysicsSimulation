import pybullet as p
import pybullet_data
import time
import numpy as np
import plotly.express as px

from model.uld import Uld


def simulate(uld_dict=None,
             visual_simulation=False,
             duration=None,
             max_g_force=None,
             force_duration=None,
             force_direction_vector=None,
             ground_friction=None,
             uld_friction=None,
             item_friction=None,
             scaling_factor=None,
             visualization=False,
             num_solver_iterations=200,
             sim_time_step= 240
             ) -> dict:
    start = time.time()
    if visual_simulation:
        client_id = p.connect(p.GUI)
    else:
        client_id = p.connect(p.DIRECT)
    p.setPhysicsEngineParameter(numSolverIterations=num_solver_iterations)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0, 0, -9.80665)
    plane_id = p.loadURDF("plane.urdf")
    p.setTimeStep(1/sim_time_step)
    p.changeDynamics(plane_id, -1, lateralFriction=ground_friction)

    uld = Uld(uld_dict, scaling_factor=scaling_factor,
              uld_friction=uld_friction, item_friction=item_friction)
    uld_id = uld.body.render()
    for item in uld.items:
        item.render()

    velocity = []

    nfb: int
    nfb_rel: int
    nfb_static: int
    nfb_rel_static: int
    fallen_boxes: list
    fallen_boxes_static: list

    for i in range(sim_time_step * duration):
        if sim_time_step == i:
            nfb_static, nfb_rel_static, fallen_boxes_static = uld.evaluate_nfb()
        if sim_time_step <= i:  # wait one second before force is applies
            com = uld.get_com()
            force = calculate_force(uld_friction * ground_friction, uld.total_weight, force_direction_vector, i - sim_time_step,
                    max_g_force, force_duration, sim_time_step)
            p.applyExternalForce(uld_id, -1, force, com, p.WORLD_FRAME)

        move_camera(uld_id)
        p.stepSimulation()

        if visualization:
            velocity.append(uld.get_velocity(abs(np.argmax(force_direction_vector))))
        #time.sleep(1 / sim_time_step)

    nfb, nfb_rel, fallen_boxes = uld.evaluate_nfb()
    p.disconnect()
    end = time.time()

    if visualization:
        fig = px.line(y=calculate_acceleration(velocity, sim_time_step), x=np.arange(duration * sim_time_step - 1), title='Simple Line Graph')
        fig.show()
    return {"nfb": nfb,
            "nfb_static": nfb_static,
            "nfb_rel": nfb_rel,
            "nfb_rel_static": nfb_rel_static,
            "fallen_boxes": fallen_boxes,
            "fallen_boxes_static": fallen_boxes_static,
            "force_direction_vector": force_direction_vector,
            "max_g_force": max_g_force,
            "item_friction": item_friction,
            "uld_friction": uld_friction,
            "simulation_duration": end-start,
            "uld_half_extents": uld.body.half_extents,
            "items": [{
                       "id": item.id,
                       "start_position": item.start_position,
                       "half_extents": item.half_extents,
                       "mass": item.mass
                       } for item in uld.items]
            }


def calculate_force(friction: float, mass: float, direction_vector: list, elapsed_seconds: int,
                                     max_g_force: float, force_duration: int, sim_time_step: int ) -> np.array:
    acceleration = max_g_force * 9.80665
    sinusoidal_force = mass * acceleration * np.sin(np.pi * (elapsed_seconds/ (force_duration * sim_time_step))) + friction * mass * 9.80665
    return np.array(direction_vector) * sinusoidal_force


def calculate_next_velocity(current_velocity: float, elapsed_seconds: int, apply_force_seconds: int, step_time: int, max_g_force: float)-> float:
    acceleration = max_g_force * 9.80665
    #return current_velocity + np.sin(np.pi * (elapsed_seconds/ (apply_force_seconds * 240))) * acceleration * (1/step_time)
    return current_velocity + acceleration * (1 / step_time)

def move_camera(box_id: int, camera_distance: int = 5) -> None:
    position, orientation = p.getBasePositionAndOrientation(box_id)
    p.resetDebugVisualizerCamera(camera_distance, -30, -45, position)


def calculate_acceleration(linear_velocity: list, sim_time_step: int) -> list:
    acceleration = []
    for i in range(1, len(linear_velocity)):
        acceleration.append(
            (linear_velocity[i] - linear_velocity[i-1]) / (1 / sim_time_step)
        )
    return acceleration