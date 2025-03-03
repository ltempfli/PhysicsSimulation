import os
import multiprocessing
import time
import csv
from simulation import simulate
from model.data_loading_transformation import extract_data, get_uld_transformations
from model.static_stability import is_statically_stable

path = "../data/uld_loading_patterns/data_1/H1_Class_3_Instance_45_ULD_0.json"


force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [0, -1, 0],
]

def run_simulation(args):
    file_path, direction, uld, lock = args
    result = simulate(uld,
                      duration=5,
                      max_g_force=1,
                      force_duration=4,
                      force_direction_vector=direction,
                      ground_friction=1,
                      uld_friction=0.5,
                      item_friction=0.8,
                      scaling_factor=0.01,
                      visual_simulation=True,
                      acceleration_graph=True,
                      num_solver_iterations=200,
                      sim_time_step=240
                      )
    result["filename"] = os.path.basename(file_path)

    return result


uld_dict = extract_data(1, file_path=path, scaling_factor=0.01, uld_height=20)
print(uld_dict)
uld_list = get_uld_transformations(uld_dict)

print(run_simulation(
    (path, force_direction_vectors[0], uld_list[0], None)
))