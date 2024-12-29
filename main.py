import os
import multiprocessing
from simulation.simulation import simulate
import plotly.express as px
import numpy as np
from model.data_loading_transformation import extract_data, rotate_uld_right, mirror_uld_horizontal

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
    uld_dict = extract_data(1, file_path= file_path, scaling_factor= 0.01, uld_height=20)
    #rotated_uld = mirror_uld_horizontal(rotate_uld_right(uld_dict, 270))
    rotated_uld = mirror_uld_horizontal(uld_dict)
    nfb, nfb_rel, acceleration_traj, acceleration_traj_y, acceleration_traj_z = simulate(rotated_uld,
                            duration=4,
                            max_g_force=0.2,
                            force_duration=3,
                            force_direction_vector=direction,
                            ground_friction=1,
                            uld_friction=0.5,
                            item_friction=0.8,
                            scaling_factor=0.01,
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

    results = pool.map(run_simulation, tasks)
    pool.close()
    pool.join()
    """

    #nfb, nfb_rel, acceleration_traj, acceleration_traj_y, acceleration_traj_z = run_simulation((loading_pattern_directory+'H1_Class_3_Instance_45_ULD_0.json', [1, 0, 0]))
    nfb, nfb_rel, acceleration_traj, acceleration_traj_y, acceleration_traj_z = run_simulation((loading_pattern_directory + 'H1_Class_3_Instance_45_ULD_0.json', [1, 0, 0]))

    fig = px.line(y=acceleration_traj, x=np.arange(4 * 240 - 1), title='Simple Line Graph X')
    #fig2 = px.line(y=acceleration_traj_y, x=np.arange(4 * 240 - 1), title='Simple Line Graph Y')
    #fig3 = px.line(y=acceleration_traj_z, x=np.arange(4 * 240 - 1), title='Simple Line Graph Z')

    # Show the graph
    fig.show()
    #fig2.show()
    #fig3.show()