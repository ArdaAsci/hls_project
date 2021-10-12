set SynModuleInfo {
  {SRCNAME matrixmul_Pipeline_Row_Col_Product MODELNAME matrixmul_Pipeline_Row_Col_Product RTLNAME matrixmul_matrixmul_Pipeline_Row_Col_Product
    SUBMODULES {
      {MODELNAME matrixmul_mac_muladd_8s_8s_16ns_16_1_1 RTLNAME matrixmul_mac_muladd_8s_8s_16ns_16_1_1 BINDTYPE op TYPE add IMPL dsp LATENCY 0 ALLOW_PRAGMA 1}
      {MODELNAME matrixmul_flow_control_loop_pipe_sequential_init RTLNAME matrixmul_flow_control_loop_pipe_sequential_init BINDTYPE interface TYPE internal_upc_flow_control INSTNAME matrixmul_flow_control_loop_pipe_sequential_init_U}
    }
  }
  {SRCNAME matrixmul_Pipeline_Row1_Col2 MODELNAME matrixmul_Pipeline_Row1_Col2 RTLNAME matrixmul_matrixmul_Pipeline_Row1_Col2
    SUBMODULES {
      {MODELNAME matrixmul_mac_muladd_16s_16s_16ns_16_1_1 RTLNAME matrixmul_mac_muladd_16s_16s_16ns_16_1_1 BINDTYPE op TYPE add IMPL dsp LATENCY 0 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME matrixmul MODELNAME matrixmul RTLNAME matrixmul IS_TOP 1}
}
