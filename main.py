import os
import multiprocessing
from simulation.simulation import simulate

loading_pattern_directory = "./data/uld_loading_patterns/"

force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [-1, 0, 0],
    [0, -1, 0],
    [0, 0, -1],
]

def run_simulation(args):
    file_path, direction = args
    nfb, nfb_rel = simulate(file_path,
                            duration=10,
                            max_g_force=10,
                            force_duration=2,
                            force_direction_vector=direction,
                            ground_friction=0.8,
                            uld_friction=0.5,
                            item_friction=0.3,
                            scaling_factor=0.02,
                            visual_simulation=False)
    print("File: {}. Direction: {}, NFB: {}, NFB_rel: {}".format(file_path, direction, nfb, nfb_rel))

if __name__ == "__main__":
    max_workers = 8
    pool = multiprocessing.Pool(processes=max_workers)

    tasks = []
    for filename in os.listdir(loading_pattern_directory):
        file_path = os.path.join(loading_pattern_directory, filename)
        for direction in force_direction_vectors:
            tasks.append((file_path, direction))

    pool.map(run_simulation, tasks)
    pool.close()
    pool.join()