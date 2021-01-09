module og_design (

    input logic clk,
    input logic [15:0] x_stride,
    input logic [31:0] offset,
    input logic [31:0] x_max,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [15:0] addr
);

    logic [15:0] scan_inter_5;
    logic [15:0] scan_inter_6;
    logic [15:0] scan_inter_7;
    logic [15:0] scan_inter_8;
    logic [31:0] scan_inter_9;

    scan5 scan5 (
        .clk(clk),
        .scan_var_5(scan_inter_5),
        .x_max(x_max)
    );

    scan6 scan6 (
        .clk(clk),
        .scan_output_5(scan_inter_5),
        .x_max(x_max),
        .scan_var_6(scan_inter_6)
    );

    scan7 scan7 (
        .clk(clk),
        .scan_output_5(scan_inter_5),
        .x_max(x_max),
        .scan_var_7(scan_inter_7),
        .x_stride(x_stride)
    );

    scan8 scan8 (
        .clk(clk),
        .scan_output_5(scan_inter_5),
        .x_max(x_max),
        .scan_var_8(scan_inter_8),
        .y_stride(y_stride)
    );

    scan9 scan9 (
        .scan_output_6(scan_inter_6),
        .y_max(y_max),
        .scan_output_7(scan_inter_7),
        .scan_output_8(scan_inter_8),
        .offset(offset),
        .scan_var_9(scan_inter_9)
    );

    always_comb begin
         addr = scan_inter_9;
    end
endmodule

module scan5 (
    input logic clk, 
    output logic [15:0] scan_var_5,
    input logic [31:0] x_max
);
    logic [31:0] x49; 
    logic x50; 
    logic [31:0] x53; 
    logic [31:0] x54; 

    always_comb begin 
        x49 = x_max - 32'd1; 
        x50 = scan_var_5 == x49; 
        x53 = scan_var_5 + 32'd1; 
        x54 = x50 ? 32'd0 : x53; 
    end 

    always_ff @(posedge clk) begin
        scan_var_5 <= x54;
    end
endmodule

module scan6 (
    input logic clk, 
    output logic [15:0] scan_var_6,
    input logic [15:0] scan_output_5,
    input logic [31:0] x_max
);
    logic [31:0] x42; 
    logic x43; 
    logic [31:0] x45; 
    logic [31:0] x46; 

    always_comb begin 
        x42 = x_max - 32'd1; 
        x43 = scan_output_5 == x42; 
        x45 = scan_var_6 + 32'd1; 
        x46 = x43 ? x45 : scan_var_6; 
    end 

    always_ff @(posedge clk) begin
        scan_var_6 <= x46;
    end
endmodule

module scan7 (
    input logic clk, 
    output logic [15:0] scan_var_7,
    input logic [15:0] scan_output_5,
    input logic [31:0] x_max,
    input logic [15:0] x_stride
);
    logic [31:0] x58; 
    logic x59; 
    logic [15:0] x61; 
    logic [31:0] x62; 

    always_comb begin 
        x58 = x_max - 32'd1; 
        x59 = scan_output_5 == x58; 
        x61 = scan_var_7 + x_stride; 
        x62 = x59 ? 32'd0 : x61; 
    end 

    always_ff @(posedge clk) begin
        scan_var_7 <= x62;
    end
endmodule

module scan8 (
    input logic clk, 
    output logic [15:0] scan_var_8,
    input logic [15:0] scan_output_5,
    input logic [31:0] x_max,
    input logic [31:0] y_stride
);
    logic [31:0] x66; 
    logic x67; 
    logic [31:0] x68; 
    logic [31:0] x69; 

    always_comb begin 
        x66 = x_max - 32'd1; 
        x67 = scan_output_5 == x66; 
        x68 = scan_var_8 + y_stride; 
        x69 = x67 ? x68 : scan_var_8; 
    end 

    always_ff @(posedge clk) begin
        scan_var_8 <= x69;
    end
endmodule

module scan9 (
    output logic [31:0] scan_var_9, 
    input logic [15:0] scan_output_6,
    input logic [31:0] y_max,
    input logic [15:0] scan_output_7,
    input logic [15:0] scan_output_8,
    input logic [31:0] offset
);
    logic x32; 
    logic [15:0] x36; 
    logic [31:0] x37; 
    logic [31:0] x38; 

    always_comb begin 
        x32 = scan_output_6 == y_max; 
        x36 = scan_output_7 + scan_output_8; 
        x37 = x36 + offset; 
        x38 = x32 ? 32'd0 : x37; 
        scan_var_9 = x38; 
    end 
endmodule

