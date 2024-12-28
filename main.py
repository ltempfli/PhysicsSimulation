import os
import multiprocessing
from simulation.simulation import simulate
import plotly.express as px
import numpy as np

loading_pattern_directory = "./data/uld_loading_patterns/"

force_direction_vectors = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [-1, 0, 0],
    [0, -1, 0],
]

def run_simulation(args):
    file_path, direction = args
    nfb, nfb_rel, acceleration_traj, acceleration_traj_y, acceleration_traj_z = simulate(file_path,
                            duration=4,
                            max_g_force=0.5,
                            force_duration=3,
                            force_direction_vector=direction,
                            ground_friction=1,
                            uld_friction=0.5,
                            item_friction=10,
                            scaling_factor=0.02,
                            visual_simulation=True)
    print("File: {}. Direction: {}, NFB: {}, NFB_rel: {}".format(file_path, direction, nfb, nfb_rel))

    return nfb, nfb_rel, acceleration_traj, acceleration_traj_y, acceleration_traj_z

if __name__ == "__main__":
    """
    max_workers = 1
    pool = multiprocessing.Pool(processes=max_workers)

    tasks = []
    for filename in os.listdir(loading_pattern_directory):
        file_path = os.path.join(loading_pattern_directory, filename)
        for direction in force_direction_vectors:
            tasks.append((file_path, direction))

    pool.map(run_simulation, tasks)
    pool.close()
    pool.join()
    """
    nfb, nfb_rel, acceleration_traj, acceleration_traj_y, acceleration_traj_z = run_simulation((loading_pattern_directory+'H1_Class_3_Instance_45_ULD_0.json', [1, 0, 0]))

    print(nfb)

    fig = px.line(y=acceleration_traj, x=np.arange(4 * 240 - 1), title='Simple Line Graph X')
    #fig2 = px.line(y=acceleration_traj_y, x=np.arange(4 * 240 - 1), title='Simple Line Graph Y')
    #fig3 = px.line(y=acceleration_traj_z, x=np.arange(4 * 240 - 1), title='Simple Line Graph Z')

    # Show the graph
    fig.show()
    #fig2.show()
    #fig3.show()