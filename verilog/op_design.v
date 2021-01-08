module op_design (

    input logic clk,
    input logic [31:0] offset,
    input logic [31:0] x_max,
    input logic [31:0] x_stride,
    input logic [31:0] y_stride,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_10;
    logic [31:0] scan_inter_14;
    logic [31:0] scan_inter_15;

    scan10 scan10 (
        .clk(clk),
        .scan_var_10(scan_inter_10),
        .x_max(x_max)
    );

    scan14 scan14 (
        .clk(clk),
        .scan_var_14(scan_inter_14),
        .scan_output_10(scan_inter_10),
        .x_max(x_max),
        .y_stride(y_stride),
        .x_stride(x_stride)
    );

    scan15 scan15 (
        .scan_output_14(scan_inter_14),
        .offset(offset),
        .scan_var_15(scan_inter_15)
    );

    always_comb begin
         addr = scan_inter_15;
    end
endmodule

module scan10 (
    input logic clk, 
    output logic [31:0] scan_var_10,
    input logic [31:0] x_max
);
    logic [31:0] x27; 
    logic x28; 
    logic [31:0] x31; 
    logic [31:0] x32; 

    always_comb begin 
        x27 = x_max - 32'd1; 
        x28 = scan_var_10 == x27; 
        x31 = scan_var_10 + 32'd1; 
        x32 = x28 ? 32'd0 : x31; 
    end 

    always_ff @(posedge clk) begin
        scan_var_10 <= x32;
    end
endmodule

module scan14 (
    input logic clk, 
    output logic [31:0] scan_var_14,
    input logic [31:0] scan_output_10,
    input logic [31:0] x_max,
    input logic [31:0] y_stride,
    input logic [31:0] x_stride
);
    logic [31:0] x21; 
    logic x22; 
    logic [31:0] x23; 
    logic [31:0] x24; 

    always_comb begin 
        x21 = x_max - 32'd1; 
        x22 = scan_output_10 == x21; 
        x23 = x22 ? y_stride : x_stride; 
        x24 = scan_var_14 + x23; 
    end 

    always_ff @(posedge clk) begin
        scan_var_14 <= x24;
    end
endmodule

module scan15 (
    output logic [31:0] scan_var_15, 
    input logic [31:0] scan_output_14,
    input logic [31:0] offset
);
    logic [31:0] x18; 

    always_comb begin 
        x18 = scan_output_14 + offset; 
        scan_var_15 = x18; 
    end 
endmodule

