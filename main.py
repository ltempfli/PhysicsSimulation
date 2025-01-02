import os
import multiprocessing
from simulation.simulation import simulate
import numpy as np
import time
from model.data_loading_transformation import extract_data, get_uld_transformations
import pandas as pd

loading_pattern_directory = "./data/uld_loading_patterns/data_1/"

force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [0, -1, 0],
]

def run_simulation(args):
    file_path, direction, uld = args

    return simulate(uld,
                            duration=4,
                            max_g_force=0.2,
                            force_duration=3,
                            force_direction_vector=direction,
                            ground_friction=1,
                            uld_friction=0.5,
                            item_friction=0.8,
                            scaling_factor=0.01,
                            visual_simulation=False,
                            visualization=True,
                            num_solver_iterations=200,
                            sim_time_step=240
                            )
if __name__ == "__main__":
    max_workers = 12
    pool = multiprocessing.Pool(processes=max_workers)
    
    tasks = []
    start = time.time()
    for filename in os.listdir(loading_pattern_directory):
        file_path = os.path.join(loading_pattern_directory, filename)
        uld_dict = extract_data(1, file_path= file_path, scaling_factor= 0.01, uld_height=20)
        uld_list = get_uld_transformations(uld_dict)
        for uld in uld_list:
            for direction in force_direction_vectors:

                tasks.append((file_path, direction, uld))

    results = pool.map(run_simulation, tasks)
    pool.close()
    pool.join()

    df = pd.DataFrame(results)
    df.head()
    df.to_csv('simulation_results.csv')

