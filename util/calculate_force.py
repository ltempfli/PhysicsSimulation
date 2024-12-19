import pybullet as p
import numpy as np

def calculate_force(friction: float, mass: int, acceleration: int, direction_vector: list) -> np.array:
    newton =   mass * (acceleration + friction * 9.80665)
    return np.array(direction_vector) * newton
