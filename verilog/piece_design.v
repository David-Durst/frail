module piece_design (

    input logic clk,
    input logic step,
    input logic [15:0] i0_piece,
    input logic [15:0] i1_piece,
    input logic [15:0] offset_0,
    input logic [15:0] offset_1,
    input logic [15:0] offset_2,
    input logic [15:0] offset_3,
    input logic [15:0] x_max,
    input logic [15:0] x_stride_0,
    input logic [15:0] x_stride_1,
    input logic [15:0] y_stride_0,
    input logic [15:0] y_stride_1,
    output logic [15:0] addr_out
);

    logic [15:0] scan_inter_20;
    logic [15:0] scan_inter_21;
    logic [15:0] scan_inter_22;

    scan20 scan20 (
        .clk(clk),
        .step(step),
        .scan_var_20(scan_inter_20),
        .x_max(x_max)
    );

    scan21 scan21 (
        .clk(clk),
        .step(step),
        .scan_output_20(scan_inter_20),
        .x_max(x_max),
        .scan_var_21(scan_inter_21)
    );

    scan22 scan22 (
        .step(step),
        .scan_output_20(scan_inter_20),
        .i0_piece(i0_piece),
        .scan_output_21(scan_inter_21),
        .i1_piece(i1_piece),
        .x_stride_0(x_stride_0),
        .y_stride_0(y_stride_0),
        .offset_0(offset_0),
        .y_stride_1(y_stride_1),
        .offset_1(offset_1),
        .x_stride_1(x_stride_1),
        .offset_2(offset_2),
        .offset_3(offset_3),
        .scan_var_22(scan_inter_22)
    );

    always_comb begin
         addr_out = scan_inter_22;
    end
endmodule

module scan20 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_20,
    input logic [15:0] x_max
);
    logic [15:0] x84; 
    logic x85; 
    logic [15:0] x88; 
    logic [15:0] x89; 

    always_comb begin 
        if (step) begin
            x84 = x_max - 16'd1; 
            x85 = scan_var_20 == x84; 
            x88 = scan_var_20 + 16'd1; 
            x89 = x85 ? 16'd0 : x88; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_20 <= x89;
        end 
    end
endmodule

module scan21 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_21,
    input logic [15:0] scan_output_20,
    input logic [15:0] x_max
);
    logic [15:0] x93; 
    logic x94; 
    logic [15:0] x96; 
    logic [15:0] x97; 

    always_comb begin 
        if (step) begin
            x93 = x_max - 16'd1; 
            x94 = scan_output_20 == x93; 
            x96 = scan_var_21 + 16'd1; 
            x97 = x94 ? x96 : scan_var_21; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_21 <= x97;
        end 
    end
endmodule

module scan22 (
    input logic step,
    output logic [15:0] scan_var_22, 
    input logic [15:0] scan_output_20,
    input logic [15:0] i0_piece,
    input logic [15:0] scan_output_21,
    input logic [15:0] i1_piece,
    input logic [15:0] x_stride_0,
    input logic [15:0] y_stride_0,
    input logic [15:0] offset_0,
    input logic [15:0] y_stride_1,
    input logic [15:0] offset_1,
    input logic [15:0] x_stride_1,
    input logic [15:0] offset_2,
    input logic [15:0] offset_3
);
    logic x50; 
    logic x52; 
    logic [15:0] x54; 
    logic [15:0] x56; 
    logic [15:0] x57; 
    logic [15:0] x58; 
    logic [15:0] x60; 
    logic [15:0] x62; 
    logic [15:0] x63; 
    logic [15:0] x64; 
    logic [15:0] x65; 
    logic x67; 
    logic [15:0] x69; 
    logic [15:0] x71; 
    logic [15:0] x72; 
    logic [15:0] x73; 
    logic [15:0] x75; 
    logic [15:0] x77; 
    logic [15:0] x78; 
    logic [15:0] x79; 
    logic [15:0] x80; 
    logic [15:0] x81; 

    always_comb begin 
        if (step) begin
            x50 = scan_output_20 < i0_piece; 
            x52 = scan_output_21 < i1_piece; 
            x54 = scan_output_20 * x_stride_0; 
            x56 = scan_output_21 * y_stride_0; 
            x57 = x54 + x56; 
            x58 = x57 + offset_0; 
            x60 = scan_output_20 * x_stride_0; 
            x62 = scan_output_21 * y_stride_1; 
            x63 = x60 + x62; 
            x64 = x63 + offset_1; 
            x65 = x52 ? x58 : x64; 
            x67 = scan_output_21 < i1_piece; 
            x69 = scan_output_20 * x_stride_1; 
            x71 = scan_output_21 * y_stride_0; 
            x72 = x69 + x71; 
            x73 = x72 + offset_2; 
            x75 = scan_output_20 * x_stride_1; 
            x77 = scan_output_21 * y_stride_1; 
            x78 = x75 + x77; 
            x79 = x78 + offset_3; 
            x80 = x67 ? x73 : x79; 
            x81 = x50 ? x65 : x80; 
            scan_var_22 = x81; 
        end 
    end 
endmodule

