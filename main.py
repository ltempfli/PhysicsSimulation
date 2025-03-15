import os
import multiprocessing
import time
import csv
import pandas as pd
from simulation.simulation import simulate
from model.data_loading_transformation import extract_data, get_uld_transformations

# loading_pattern_directory = "./data/uld_loading_patterns/data_1/"
loading_pattern_directory = "/home/shared_asim_ws_24_25_pm/data_2/Ulds_scenario_1/"

force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [0, -1, 0],
]


def run_simulation(args):
    file_path, direction, uld, lock = args
    print("Starting simulation... (" + file_path + ")")
    result = simulate(uld,
                      duration=5,
                      force_duration=4,
                      max_g_force=1.5,
                      force_direction_vector=direction,
                      ground_friction=0.55,
                      uld_friction=0.55,
                      item_friction=0.55,
                      threshold_fb_relative=0.04,
                      visual_simulation=False,
                      acceleration_graph=False,
                      num_solver_iterations=200,
                      sim_time_step=240
                      )
    result["filename"] = os.path.basename(file_path)

    with lock:
        with open('simulation_results_scenario_1.csv', 'a', newline='') as csvfile:
            fieldnames = ['filename', 'total_nb', 'nfb', 'nfb_static', 'nfb_rel', 'nfb_rel_static', 'fallen_boxes',
                          'fallen_boxes_static', 'force_direction_vector', 'max_g_force', 'item_friction',
                          'uld_friction', 'simulation_duration', 'uld_half_extents', 'items']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(result)
    
    print("Finnished simulation. (" + file_path + ")")

    return result


if __name__ == "__main__":
    max_workers = 10
    pool = multiprocessing.Pool(processes=max_workers)
    lock = multiprocessing.Manager().Lock()

    results = pd.read_csv("/home/lmancilik_pm/simulation_results_scenario_1.csv", usecols=['filename'])

    tasks = []
    start = time.time()
    for filename in os.listdir(loading_pattern_directory):
        file_path = os.path.join(loading_pattern_directory, filename)

        if filename in results["filename"].to_list():
            print("Skipping simulation... (" + file_path + ")")
            continue

        uld_dict = extract_data(1, file_path=file_path)
        uld_list = get_uld_transformations(uld_dict)
        for uld in uld_list:
            for direction in force_direction_vectors:
                tasks.append((file_path, direction, uld, lock))

    print("Creating result file if not already created...")

    with open('simulation_results_scenario_1.csv', 'a', newline='') as csvfile:
        fieldnames = ['filename', 'total_nb', 'nfb', 'nfb_static', 'nfb_rel', 'nfb_rel_static', 'fallen_boxes',
                      'fallen_boxes_static',
                      'force_direction_vector', 'max_g_force', 'item_friction', 'uld_friction', 'simulation_duration',
                      'uld_half_extents', 'items']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    print("Success")

    results = pool.map(run_simulation, tasks)

    print("Finnished all tasks.")

    pool.close()
    pool.join()
