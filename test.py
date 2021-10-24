from src.tcl_reader import Tcl

tcl_tester = Tcl("./directives.tcl", "matrixmul", read_only=True)
print(tcl_tester.get_loop_parameter("Product", "pipeline"))
print(tcl_tester.set_loop_parameter("Product", "unroll", 3))
print(tcl_tester.get_loop_parameter("Product", "unroll"))
tcl_tester.update_directives()

