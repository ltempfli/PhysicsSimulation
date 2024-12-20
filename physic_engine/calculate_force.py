import numpy as np


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
