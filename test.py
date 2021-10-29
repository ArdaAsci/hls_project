import os

from src.csynth import Csynth, CsynthModule
from src.loops import Loop
from src.tcl_reader import Tcl

row = Loop(name="Row", iteration_count=7, parent_loop=None, rank=0)
col = Loop(name="Col", iteration_count=7, parent_loop=row)
product = Loop(name="Product", iteration_count=7, parent_loop=col)
# row.add_child(col)
# col.add_child(product)
row1 = Loop(name="Row1", iteration_count=7, parent_loop=None, rank=1)
col1 = Loop(name="Col1", iteration_count=7, parent_loop=row1)
# row1.add_child(col1)
matrixmul_project_loops = [row, col, product, row1, col1]
"""
tcl_tester = Tcl("./directives.tcl", "matrixmul", read_only=True)
print(tcl_tester.get_loop_parameter("Product", "pipeline"))
print(tcl_tester.set_loop_parameter("Product", "unroll", 3))
print(tcl_tester.get_loop_parameter("Product", "unroll"))
tcl_tester.update_directives()
"""
csynth_tester = Csynth(
    "/home/arda/dev/hls_project/matrixmul_prj/solution1/syn/report/csynth.xml"
)
print(csynth_tester.get_module_data_from_loop(col1))
print(csynth_tester.top_module_data)
print("exit")

print(row.total_nested_depth)
