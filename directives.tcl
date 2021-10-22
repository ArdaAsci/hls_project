open_project matrixmul_prj
open_solution solution1
set_directive_top -name matrixmul "matrixmul"
set_directive_pipeline -II 1 "matrixmul/Product"
set_directive_unroll -factor 1 "matrixmul/Product"
csim_design
csynth_design
cosim_design
exit