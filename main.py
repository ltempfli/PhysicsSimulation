import os
import multiprocessing
import time
import csv
from simulation.simulation import simulate
from model.data_loading_transformation import extract_data, get_uld_transformations

loading_pattern_directory = "./data/uld_loading_patterns/data_1/"
# loading_pattern_directory = "../../asim-data/Data/ULDs/Batch_2"

force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [0, -1, 0],
]


def run_simulation(args):
    file_path, direction, uld, lock = args
    result = simulate(uld,
                      duration=7,
                      force_duration=6,
                      max_g_force=2.0,
                      force_direction_vector=direction,
                      ground_friction=0.55,
                      uld_friction=0.55,
                      item_friction=0.55,
                      threshold_fb_relative=0.05,
                      visual_simulation=True,
                      acceleration_graph=True,
                      num_solver_iterations=200,
                      sim_time_step=240
                      )
    result["filename"] = os.path.basename(file_path)

    with lock:
        with open('simulation_results.csv', 'a', newline='') as csvfile:
            fieldnames = ['filename', 'total_nb', 'nfb', 'nfb_static', 'nfb_rel', 'nfb_rel_static', 'fallen_boxes',
                          'fallen_boxes_static', 'force_direction_vector', 'max_g_force', 'item_friction',
                          'uld_friction', 'simulation_duration', 'uld_half_extents', 'items']
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
        file_path = os.path.join(loading_pattern_directory, filename)
        uld_dict = extract_data(1, file_path=file_path, scaling_factor=0.01, uld_height=20)
        uld_list = get_uld_transformations(uld_dict)
        for uld in uld_list:
            for direction in force_direction_vectors:
                tasks.append((file_path, direction, uld, lock))

    with open('simulation_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['filename', 'total_nb', 'nfb', 'nfb_static', 'nfb_rel', 'nfb_rel_static', 'fallen_boxes',
                      'fallen_boxes_static',
                      'force_direction_vector', 'max_g_force', 'item_friction', 'uld_friction', 'simulation_duration',
                      'uld_half_extents', 'items']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    print(tasks)
    print("test")
    results = pool.map(run_simulation, tasks)

    pool.close()
    pool.join()
