from stable_baselines3.ppo.ppo import PPO
from src.hls_env import HlsEnv
import src.constants as constants
from src.loops import Loop
import os


def initialize_vitis():
    """
    Runs the command to initialize the vitis project and solution
    Also acts as a reset 
    """
    log = os.popen("vitis_hls -f " + constants.RUN_HLS_FILE)
    return log.read()


row = Loop(name="Row", iteration_count=7, parent_loop=None, rank=0)
col = Loop(name="Col", iteration_count=7, parent_loop=row)
product = Loop(name="Product", iteration_count=7, parent_loop=col)
row.add_child(col)
col.add_child(product)
row1 = Loop(name="Row1", iteration_count=7, parent_loop=None, rank=1)
col1 = Loop(name="Col1", iteration_count=7, parent_loop=row1)
row1.add_child(col1)
matrixmul_project_loops = [row, col, product, row1, col1]

initialize_vitis()
env = HlsEnv(
    project_dir=os.getcwd(),
    project_name="matrixmul_prj",
    solution_name="solution1",
    top_name="matrixmul",
    initial_directive_file_name="./directives.tcl",
    loop_list=matrixmul_project_loops,
)

trainer = PPO("MlpPolicy", env, verbose=1)
trainer.learn(total_timesteps=100)

