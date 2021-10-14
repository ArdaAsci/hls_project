// ==============================================================
// RTL generated by Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
// Version: 2021.1
// Copyright (C) Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module matrixmul_matrixmul_Pipeline_Row_Col_Product (
        ap_clk,
        ap_rst,
        ap_start,
        ap_done,
        ap_idle,
        ap_ready,
        res_address0,
        res_ce0,
        res_we0,
        res_d0,
        a_address0,
        a_ce0,
        a_q0,
        b_address0,
        b_ce0,
        b_q0
);

parameter    ap_ST_fsm_pp0_stage0 = 1'd1;

input   ap_clk;
input   ap_rst;
input   ap_start;
output   ap_done;
output   ap_idle;
output   ap_ready;
output  [3:0] res_address0;
output   res_ce0;
output   res_we0;
output  [15:0] res_d0;
output  [3:0] a_address0;
output   a_ce0;
input  [7:0] a_q0;
output  [3:0] b_address0;
output   b_ce0;
input  [7:0] b_q0;

reg ap_idle;
reg res_ce0;
reg res_we0;
reg a_ce0;
reg b_ce0;

(* fsm_encoding = "none" *) reg   [0:0] ap_CS_fsm;
wire    ap_CS_fsm_pp0_stage0;
wire    ap_enable_reg_pp0_iter0;
reg    ap_enable_reg_pp0_iter1;
reg    ap_idle_pp0;
wire    ap_block_state1_pp0_stage0_iter0;
wire    ap_block_state2_pp0_stage0_iter1;
wire    ap_block_pp0_stage0_subdone;
wire   [0:0] icmp_ln57_fu_154_p2;
reg    ap_condition_exit_pp0_iter0_stage0;
wire    ap_loop_exit_ready;
reg    ap_ready_int;
wire   [0:0] or_ln59_fu_248_p2;
reg   [0:0] or_ln59_reg_456;
wire    ap_block_pp0_stage0_11001;
wire   [3:0] add_ln60_fu_274_p2;
reg   [3:0] add_ln60_reg_461;
wire   [0:0] icmp_ln62_1_fu_326_p2;
reg   [0:0] icmp_ln62_1_reg_476;
wire   [63:0] zext_ln63_2_fu_290_p1;
wire    ap_block_pp0_stage0;
wire   [63:0] zext_ln63_3_fu_315_p1;
wire   [63:0] zext_ln60_1_fu_384_p1;
reg   [15:0] empty_fu_58;
wire   [15:0] grp_fu_400_p3;
wire    ap_loop_init;
reg   [1:0] k_fu_62;
reg   [1:0] ap_sig_allocacmp_k_load;
wire   [1:0] add_ln62_fu_320_p2;
reg   [1:0] j_fu_66;
reg   [1:0] ap_sig_allocacmp_j_load;
wire   [1:0] select_ln59_2_fu_262_p3;
reg   [3:0] indvar_flatten_fu_70;
reg   [3:0] ap_sig_allocacmp_indvar_flatten_load_1;
reg   [3:0] ap_sig_allocacmp_indvar_flatten_load;
wire   [3:0] select_ln59_3_fu_341_p3;
reg   [1:0] i_fu_74;
reg   [1:0] ap_sig_allocacmp_i_load;
wire   [1:0] select_ln57_1_fu_198_p3;
reg   [4:0] indvar_flatten15_fu_78;
reg   [4:0] ap_sig_allocacmp_indvar_flatten15_load;
wire   [4:0] add_ln57_1_fu_160_p2;
wire   [0:0] icmp_ln59_fu_184_p2;
wire   [1:0] add_ln57_fu_178_p2;
wire   [3:0] tmp_fu_210_p3;
wire   [3:0] zext_ln63_fu_206_p1;
wire   [0:0] icmp_ln62_fu_230_p2;
wire   [0:0] xor_ln57_fu_224_p2;
wire   [1:0] select_ln57_fu_190_p3;
wire   [0:0] and_ln57_fu_236_p2;
wire   [1:0] add_ln59_fu_242_p2;
wire   [3:0] sub_ln63_fu_218_p2;
wire   [3:0] zext_ln60_fu_270_p1;
wire   [1:0] select_ln59_fu_254_p3;
wire   [3:0] zext_ln63_1_fu_280_p1;
wire   [3:0] add_ln63_1_fu_284_p2;
wire   [3:0] tmp_1_fu_295_p3;
wire   [3:0] sub_ln63_1_fu_303_p2;
wire   [3:0] add_ln63_2_fu_309_p2;
wire   [3:0] add_ln59_1_fu_335_p2;
wire   [15:0] grp_fu_400_p2;
reg    ap_done_reg;
wire    ap_continue_int;
reg    ap_done_int;
reg   [0:0] ap_NS_fsm;
wire    ap_enable_pp0;
wire    ap_start_int;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 ap_CS_fsm = 1'd1;
#0 ap_enable_reg_pp0_iter1 = 1'b0;
#0 ap_done_reg = 1'b0;
end

matrixmul_mac_muladd_8s_8s_16ns_16_1_1 #(
    .ID( 1 ),
    .NUM_STAGE( 1 ),
    .din0_WIDTH( 8 ),
    .din1_WIDTH( 8 ),
    .din2_WIDTH( 16 ),
    .dout_WIDTH( 16 ))
mac_muladd_8s_8s_16ns_16_1_1_U1(
    .din0(b_q0),
    .din1(a_q0),
    .din2(grp_fu_400_p2),
    .dout(grp_fu_400_p3)
);

matrixmul_flow_control_loop_pipe_sequential_init flow_control_loop_pipe_sequential_init_U(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst),
    .ap_start(ap_start),
    .ap_ready(ap_ready),
    .ap_done(ap_done),
    .ap_start_int(ap_start_int),
    .ap_loop_init(ap_loop_init),
    .ap_ready_int(ap_ready_int),
    .ap_loop_exit_ready(ap_condition_exit_pp0_iter0_stage0),
    .ap_loop_exit_done(ap_done_int),
    .ap_continue_int(ap_continue_int),
    .ap_done_int(ap_done_int)
);

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_CS_fsm <= ap_ST_fsm_pp0_stage0;
    end else begin
        ap_CS_fsm <= ap_NS_fsm;
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_done_reg <= 1'b0;
    end else begin
        if ((ap_continue_int == 1'b1)) begin
            ap_done_reg <= 1'b0;
        end else if (((ap_loop_exit_ready == 1'b1) & (1'b0 == ap_block_pp0_stage0_subdone) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
            ap_done_reg <= 1'b1;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_enable_reg_pp0_iter1 <= 1'b0;
    end else begin
        if ((1'b1 == ap_condition_exit_pp0_iter0_stage0)) begin
            ap_enable_reg_pp0_iter1 <= 1'b0;
        end else if (((1'b0 == ap_block_pp0_stage0_subdone) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
            ap_enable_reg_pp0_iter1 <= ap_start_int;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if ((ap_loop_init == 1'b1)) begin
            empty_fu_58 <= 16'd0;
        end else if ((ap_enable_reg_pp0_iter1 == 1'b1)) begin
            empty_fu_58 <= grp_fu_400_p3;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln57_fu_154_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            i_fu_74 <= select_ln57_1_fu_198_p3;
        end else if ((ap_loop_init == 1'b1)) begin
            i_fu_74 <= 2'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln57_fu_154_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            indvar_flatten15_fu_78 <= add_ln57_1_fu_160_p2;
        end else if ((ap_loop_init == 1'b1)) begin
            indvar_flatten15_fu_78 <= 5'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln57_fu_154_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            indvar_flatten_fu_70 <= select_ln59_3_fu_341_p3;
        end else if ((ap_loop_init == 1'b1)) begin
            indvar_flatten_fu_70 <= 4'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln57_fu_154_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            j_fu_66 <= select_ln59_2_fu_262_p3;
        end else if ((ap_loop_init == 1'b1)) begin
            j_fu_66 <= 2'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln57_fu_154_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            k_fu_62 <= add_ln62_fu_320_p2;
        end else if ((ap_loop_init == 1'b1)) begin
            k_fu_62 <= 2'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((icmp_ln57_fu_154_p2 == 1'd0) & (1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        add_ln60_reg_461 <= add_ln60_fu_274_p2;
        icmp_ln62_1_reg_476 <= icmp_ln62_1_fu_326_p2;
        or_ln59_reg_456 <= or_ln59_fu_248_p2;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        a_ce0 = 1'b1;
    end else begin
        a_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((icmp_ln57_fu_154_p2 == 1'd1) & (1'b0 == ap_block_pp0_stage0_subdone) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b1;
    end else begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b0;
    end
end

always @ (*) begin
    if (((ap_loop_exit_ready == 1'b1) & (1'b0 == ap_block_pp0_stage0_subdone) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_done_int = 1'b1;
    end else begin
        ap_done_int = ap_done_reg;
    end
end

always @ (*) begin
    if (((ap_start_int == 1'b0) & (ap_idle_pp0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter1 == 1'b0) & (ap_enable_reg_pp0_iter0 == 1'b0))) begin
        ap_idle_pp0 = 1'b1;
    end else begin
        ap_idle_pp0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_subdone) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_ready_int = 1'b1;
    end else begin
        ap_ready_int = 1'b0;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_sig_allocacmp_i_load = 2'd0;
    end else begin
        ap_sig_allocacmp_i_load = i_fu_74;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_sig_allocacmp_indvar_flatten15_load = 5'd0;
    end else begin
        ap_sig_allocacmp_indvar_flatten15_load = indvar_flatten15_fu_78;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_sig_allocacmp_indvar_flatten_load = 4'd0;
    end else begin
        ap_sig_allocacmp_indvar_flatten_load = indvar_flatten_fu_70;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_sig_allocacmp_indvar_flatten_load_1 = 4'd0;
    end else begin
        ap_sig_allocacmp_indvar_flatten_load_1 = indvar_flatten_fu_70;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_sig_allocacmp_j_load = 2'd0;
    end else begin
        ap_sig_allocacmp_j_load = j_fu_66;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_sig_allocacmp_k_load = 2'd0;
    end else begin
        ap_sig_allocacmp_k_load = k_fu_62;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        b_ce0 = 1'b1;
    end else begin
        b_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        res_ce0 = 1'b1;
    end else begin
        res_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((icmp_ln62_1_reg_476 == 1'd1) & (1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        res_we0 = 1'b1;
    end else begin
        res_we0 = 1'b0;
    end
end

always @ (*) begin
    case (ap_CS_fsm)
        ap_ST_fsm_pp0_stage0 : begin
            ap_NS_fsm = ap_ST_fsm_pp0_stage0;
        end
        default : begin
            ap_NS_fsm = 'bx;
        end
    endcase
end

assign a_address0 = zext_ln63_2_fu_290_p1;

assign add_ln57_1_fu_160_p2 = (ap_sig_allocacmp_indvar_flatten15_load + 5'd1);

assign add_ln57_fu_178_p2 = (ap_sig_allocacmp_i_load + 2'd1);

assign add_ln59_1_fu_335_p2 = (ap_sig_allocacmp_indvar_flatten_load + 4'd1);

assign add_ln59_fu_242_p2 = (select_ln57_fu_190_p3 + 2'd1);

assign add_ln60_fu_274_p2 = (sub_ln63_fu_218_p2 + zext_ln60_fu_270_p1);

assign add_ln62_fu_320_p2 = (select_ln59_fu_254_p3 + 2'd1);

assign add_ln63_1_fu_284_p2 = (sub_ln63_fu_218_p2 + zext_ln63_1_fu_280_p1);

assign add_ln63_2_fu_309_p2 = (sub_ln63_1_fu_303_p2 + zext_ln60_fu_270_p1);

assign and_ln57_fu_236_p2 = (xor_ln57_fu_224_p2 & icmp_ln62_fu_230_p2);

assign ap_CS_fsm_pp0_stage0 = ap_CS_fsm[32'd0];

assign ap_block_pp0_stage0 = ~(1'b1 == 1'b1);

assign ap_block_pp0_stage0_11001 = ~(1'b1 == 1'b1);

assign ap_block_pp0_stage0_subdone = ~(1'b1 == 1'b1);

assign ap_block_state1_pp0_stage0_iter0 = ~(1'b1 == 1'b1);

assign ap_block_state2_pp0_stage0_iter1 = ~(1'b1 == 1'b1);

assign ap_enable_pp0 = (ap_idle_pp0 ^ 1'b1);

assign ap_enable_reg_pp0_iter0 = ap_start_int;

assign ap_loop_exit_ready = ap_condition_exit_pp0_iter0_stage0;

assign b_address0 = zext_ln63_3_fu_315_p1;

assign grp_fu_400_p2 = ((or_ln59_reg_456[0:0] == 1'b1) ? 16'd0 : empty_fu_58);

assign icmp_ln57_fu_154_p2 = ((ap_sig_allocacmp_indvar_flatten15_load == 5'd27) ? 1'b1 : 1'b0);

assign icmp_ln59_fu_184_p2 = ((ap_sig_allocacmp_indvar_flatten_load_1 == 4'd9) ? 1'b1 : 1'b0);

assign icmp_ln62_1_fu_326_p2 = ((add_ln62_fu_320_p2 == 2'd3) ? 1'b1 : 1'b0);

assign icmp_ln62_fu_230_p2 = ((ap_sig_allocacmp_k_load == 2'd3) ? 1'b1 : 1'b0);

assign or_ln59_fu_248_p2 = (icmp_ln59_fu_184_p2 | and_ln57_fu_236_p2);

assign res_address0 = zext_ln60_1_fu_384_p1;

assign res_d0 = grp_fu_400_p3;

assign select_ln57_1_fu_198_p3 = ((icmp_ln59_fu_184_p2[0:0] == 1'b1) ? add_ln57_fu_178_p2 : ap_sig_allocacmp_i_load);

assign select_ln57_fu_190_p3 = ((icmp_ln59_fu_184_p2[0:0] == 1'b1) ? 2'd0 : ap_sig_allocacmp_j_load);

assign select_ln59_2_fu_262_p3 = ((and_ln57_fu_236_p2[0:0] == 1'b1) ? add_ln59_fu_242_p2 : select_ln57_fu_190_p3);

assign select_ln59_3_fu_341_p3 = ((icmp_ln59_fu_184_p2[0:0] == 1'b1) ? 4'd1 : add_ln59_1_fu_335_p2);

assign select_ln59_fu_254_p3 = ((or_ln59_fu_248_p2[0:0] == 1'b1) ? 2'd0 : ap_sig_allocacmp_k_load);

assign sub_ln63_1_fu_303_p2 = (tmp_1_fu_295_p3 - zext_ln63_1_fu_280_p1);

assign sub_ln63_fu_218_p2 = (tmp_fu_210_p3 - zext_ln63_fu_206_p1);

assign tmp_1_fu_295_p3 = {{select_ln59_fu_254_p3}, {2'd0}};

assign tmp_fu_210_p3 = {{select_ln57_1_fu_198_p3}, {2'd0}};

assign xor_ln57_fu_224_p2 = (icmp_ln59_fu_184_p2 ^ 1'd1);

assign zext_ln60_1_fu_384_p1 = add_ln60_reg_461;

assign zext_ln60_fu_270_p1 = select_ln59_2_fu_262_p3;

assign zext_ln63_1_fu_280_p1 = select_ln59_fu_254_p3;

assign zext_ln63_2_fu_290_p1 = add_ln63_1_fu_284_p2;

assign zext_ln63_3_fu_315_p1 = add_ln63_2_fu_309_p2;

assign zext_ln63_fu_206_p1 = select_ln57_1_fu_198_p3;

endmodule //matrixmul_matrixmul_Pipeline_Row_Col_Product