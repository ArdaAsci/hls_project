from src.hls_env import HlsEnv
from loops import Loop


row = Loop(name="row", iteration_count=7, parent_loop=None,)
col = Loop(name="col", iteration_count=7, parent_loop=row)
product = Loop(name="product", iteration_count=7, parent_loop=col)
row.add_child(col)
col.add_child(product)
row1 = Loop(name="row1", iteration_count=7, parent_loop=None)
col1 = Loop(name="col1", iteration_count=7, parent_loop=row1)
row1.add_child(col1)
matrixmul_project_loops = [row, col, product, row1, col1]


env = HlsEnv(project_dir="D:/vivado/vitis_rl/",
             project_name="matrixmul_prj",
             solution_name="solution1",
             top_name="matrixmul",
             initial_directive_file="./directives.tcl",
             loop_list=matrixmul_project_loops)
