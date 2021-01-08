module design_b (

    input logic clk,
    input logic [15:0] x_stride,
    input logic [31:0] offset,
    input logic [31:0] x_max,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_4;
    logic [31:0] scan_inter_5;
    logic [31:0] scan_inter_6;
    logic [31:0] scan_inter_7;

    scan4 scan4 (
        .clk(clk),
        .scan_var_4(scan_inter_4),
        .x_max(x_max)
    );

    scan5 scan5 (
        .clk(clk),
        .scan_output_4(scan_inter_4),
        .x_max(x_max),
        .scan_var_5(scan_inter_5)
    );

    scan6 scan6 (
        .clk(clk),
        .scan_output_5(scan_inter_5),
        .y_max(y_max),
        .scan_var_6(scan_inter_6),
        .scan_output_4(scan_inter_4),
        .x_max(x_max),
        .y_stride(y_stride),
        .x_stride(x_stride)
    );

    scan7 scan7 (
        .scan_output_6(scan_inter_6),
        .offset(offset),
        .scan_var_7(scan_inter_7)
    );

    always_ff @(posedge clk) begin
         addr <= scan_inter_7;
    end
endmodule

module scan4 (
    input logic clk, 
    output logic [31:0] scan_var_4,
    input logic [31:0] x_max
);
    logic x35; 
    logic [31:0] x38; 
    logic [31:0] x39; 

    always_comb begin 
        x35 = scan_var_4 == x_max; 
        x38 = scan_var_4 + 32'd1; 
        x39 = x35 ? 32'd0 : x38; 
    end 

    always_ff @(posedge clk) begin
        scan_var_4 <= x39;
    end
endmodule

module scan5 (
    input logic clk, 
    output logic [31:0] scan_var_5,
    input logic [31:0] scan_output_4,
    input logic [31:0] x_max
);
    logic x30; 
    logic [31:0] x32; 
    logic [31:0] x33; 

    always_comb begin 
        x30 = scan_output_4 == x_max; 
        x32 = scan_var_5 + 32'd1; 
        x33 = x30 ? x32 : scan_var_5; 
    end 

    always_ff @(posedge clk) begin
        scan_var_5 <= x33;
    end
endmodule

module scan6 (
    input logic clk, 
    output logic [31:0] scan_var_6,
    input logic [31:0] scan_output_5,
    input logic [31:0] y_max,
    input logic [31:0] scan_output_4,
    input logic [31:0] x_max,
    input logic [31:0] y_stride,
    input logic [15:0] x_stride
);
    logic x25; 
    logic x22; 
    logic [31:0] x23; 
    logic [31:0] x24; 
    logic [31:0] x27; 

    always_comb begin 
        x25 = scan_output_5 == y_max; 
        x22 = scan_output_4 == x_max; 
        x23 = x22 ? y_stride : x_stride; 
        x24 = scan_var_6 + x23; 
        x27 = x25 ? 32'd0 : x24; 
    end 

    always_ff @(posedge clk) begin
        scan_var_6 <= x27;
    end
endmodule

module scan7 (
    output logic [31:0] scan_var_7, 
    input logic [31:0] scan_output_6,
    input logic [31:0] offset
);
    logic [31:0] x17; 

    always_comb begin 
        x17 = scan_output_6 + offset; 
        scan_var_7 = x17; 
    end 
endmodule

