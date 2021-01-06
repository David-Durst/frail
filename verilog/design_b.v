module design_b (

    input logic clk,
    input logic [15:0] x_stride,
    input logic [31:0] x_max,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_4;
    logic [31:0] scan_inter_12;
    logic [31:0] scan_inter_14;

    scan4 scan4 (
        .clk(clk),
        .scan_output_14(scan_inter_14),
        .y_max(y_max),
        .scan_var_4(scan_inter_4),
        .scan_output_12(scan_inter_12),
        .x_max(x_max),
        .y_stride(y_stride),
        .x_stride(x_stride)
    );

    scan12 scan12 (
        .clk(clk),
        .scan_output_12(scan_inter_12),
        .x_max(x_max),
        .scan_var_12(scan_inter_12)
    );

    scan14 scan14 (
        .clk(clk),
        .scan_output_12(scan_inter_12),
        .x_max(x_max),
        .scan_var_14(scan_inter_14)
    );

    always_ff @(posedge clk) begin
         addr <= scan_inter_4;
    end
endmodule

module scan4 (
    input logic clk, 
    output logic [31:0] scan_var_4,
    input logic [31:0] scan_output_14,
    input logic [31:0] y_max,
    input logic [31:0] scan_output_12,
    input logic [31:0] x_max,
    input logic [31:0] y_stride,
    input logic [15:0] x_stride
);
    logic x20; 
    logic x17; 
    logic [31:0] x18; 
    logic [31:0] x19; 
    logic [31:0] x22; 

    always_comb begin 
        x20 = scan_output_14 == y_max; 
        x17 = scan_output_12 == x_max + 1; 
        x18 = x17 ? y_stride : x_stride; 
        x19 = scan_var_4 + x18; 
        x22 = x20 ? 32'd0 : x19; 
    end 

    always_ff @(posedge clk) begin
        scan_var_4 <= x22;
    end
endmodule

module scan12 (
    input logic clk, 
    output logic [31:0] scan_var_12,
    input logic [31:0] scan_output_12,
    input logic [31:0] x_max
);
    logic x29; 
    logic [31:0] x32; 
    logic [31:0] x33; 

    always_comb begin 
        x29 = scan_output_12 == x_max + 1; 
        x32 = scan_var_12 + 32'd1; 
        x33 = x29 ? 32'd0 : x32; 
    end 

    always_ff @(posedge clk) begin
        scan_var_12 <= x33;
    end
endmodule

module scan14 (
    input logic clk, 
    output logic [31:0] scan_var_14,
    input logic [31:0] scan_output_12,
    input logic [31:0] x_max
);
    logic x24; 
    logic [31:0] x26; 
    logic [31:0] x27; 

    always_comb begin 
        x24 = scan_output_12 == x_max + 1; 
        x26 = scan_var_14 + 32'd1; 
        x27 = x24 ? x26 : scan_var_14; 
    end 

    always_ff @(posedge clk) begin
        scan_var_14 <= x27;
    end
endmodule

