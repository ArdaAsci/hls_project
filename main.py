import os

import numpy as np
from stable_baselines3.ppo.ppo import PPO

import src.constants as constants
from src.hls_env import HlsEnv
from src.loops import Loop, LoopList


def initialize_vitis():
    """
    Runs the command to initialize the vitis project and solution
    Also acts as a reset 
    """
    log = os.popen("vitis_hls -f " + constants.RUN_HLS_FILE)
    return log.read()


row = Loop(
    name="Row", iteration_count=7, parent_loop=None, rank=0, pragma=np.array([1, 10])
)
col = Loop(name="Col", iteration_count=7, parent_loop=row, pragma=np.array([1, 10]))
product = Loop(
    name="Product", iteration_count=7, parent_loop=col, pragma=np.array([1, 10])
)
row1 = Loop(
    name="Row1", iteration_count=7, parent_loop=None, rank=1, pragma=np.array([1, 10])
)
col1 = Loop(name="Col1", iteration_count=7, parent_loop=row1, pragma=np.array([1, 10]))
matrixmul_project_loops = LoopList(row, col, product, row1, col1)

# initialize_vitis()
env = HlsEnv(
    project_dir=os.getcwd(),
    project_name="matrixmul_prj",
    solution_name="solution1",
    top_name="matrixmul",
    loop_list=matrixmul_project_loops,
)

trainer = PPO("MlpPolicy", env, verbose=1)
trainer.learn(total_timesteps=1)

