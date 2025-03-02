import os
import multiprocessing
import time
import csv
from simulation.simulation import simulate
from model.data_loading_transformation import extract_data, get_uld_transformations
from model.static_stability import is_statically_stable

loading_pattern_directory = "./data/uld_loading_patterns/data_1/"
#loading_pattern_directory = "../../asim-data/Data/ULDs/Batch_2"
static_stability_result_directory = "../../asim-data/Data/Results"

force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [0, -1, 0],
]

def run_simulation(args):
    file_path, direction, uld, lock = args
    result = simulate(uld,
                      duration=15,
                      max_g_force=0.2,
                      force_duration=8,
                      force_direction_vector=direction,
                      ground_friction=1,
                      uld_friction=0.5,
                      item_friction=0.8,
                      scaling_factor=1.0,
                      visual_simulation=True,
                      visualization=False,
                      num_solver_iterations=200,
                      sim_time_step=240
                      )
    result["filename"] = os.path.basename(file_path)

    with lock:
        with open('simulation_results.csv', 'a', newline='') as csvfile:
            fieldnames = ['filename', 'nfb', 'nfb_static', 'nfb_rel', 'nfb_rel_static', 'fallen_boxes', 'fallen_boxes_static',
                          'force_direction_vector', 'max_g_force', 'item_friction', 'uld_friction',
                          'simulation_duration', 'uld_half_extents', 'items']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(result)

    return result

if __name__ == "__main__":
    max_workers = 1
    pool = multiprocessing.Pool(processes=max_workers)
    lock = multiprocessing.Manager().Lock()

    tasks = []
    start = time.time()
    for filename in os.listdir(loading_pattern_directory):
        result_file_path = os.path.abspath(static_stability_result_directory + "/Data_2_Ulds_scenario_1_" + filename)
        if not is_statically_stable(result_file_path):
            pass
        file_path = os.path.join(loading_pattern_directory, filename)
        uld_dict = extract_data(1, file_path=file_path, scaling_factor=0.01, uld_height=20)
        uld_list = get_uld_transformations(uld_dict)
        for uld in uld_list:
            for direction in force_direction_vectors:
                tasks.append((file_path, direction, uld, lock))

    with open('simulation_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['filename', 'nfb', 'nfb_static', 'nfb_rel', 'nfb_rel_static', 'fallen_boxes', 'fallen_boxes_static',
                      'force_direction_vector', 'max_g_force', 'item_friction', 'uld_friction', 'simulation_duration',
                      'uld_half_extents', 'items']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    print(tasks)
    print("test")
    results = pool.map(run_simulation, tasks)

    pool.close()
    pool.join()