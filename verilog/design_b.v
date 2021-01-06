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
    logic [31:0] scan_inter_17;
    logic [31:0] scan_inter_19;

    scan4 scan4 (
        .clk(clk),
        .scan_output_19(scan_inter_19),
        .y_max(y_max),
        .scan_var_4(scan_inter_4),
        .scan_output_17(scan_inter_17),
        .x_max(x_max),
        .y_stride(y_stride),
        .x_stride(x_stride)
    );

    scan5 scan5 (
        .scan_output_4(scan_inter_4),
        .offset(offset),
        .scan_var_5(scan_inter_5)
    );

    scan17 scan17 (
        .clk(clk),
        .scan_output_17(scan_inter_17),
        .x_max(x_max),
        .scan_var_17(scan_inter_17)
    );

    scan19 scan19 (
        .clk(clk),
        .scan_output_17(scan_inter_17),
        .x_max(x_max),
        .scan_var_19(scan_inter_19)
    );

    always_ff @(posedge clk) begin
         addr <= scan_inter_5;
    end
endmodule

module scan4 (
    input logic clk, 
    output logic [31:0] scan_var_4,
    input logic [31:0] scan_output_19,
    input logic [31:0] y_max,
    input logic [31:0] scan_output_17,
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
        x25 = scan_output_19 == y_max; 
        x22 = scan_output_17 == x_max; 
        x23 = x22 ? y_stride : x_stride; 
        x24 = scan_var_4 + x23; 
        x27 = x25 ? 32'd0 : x24; 
    end 

    always_ff @(posedge clk) begin
        scan_var_4 <= x27;
    end
endmodule

module scan5 (
    output logic [31:0] scan_var_5, 
    input logic [31:0] scan_output_4,
    input logic [31:0] offset
);
    logic [31:0] x15; 

    always_comb begin 
        x15 = scan_output_4 + offset; 
        scan_var_5 = x15; 
    end 
endmodule

module scan17 (
    input logic clk, 
    output logic [31:0] scan_var_17,
    input logic [31:0] scan_output_17,
    input logic [31:0] x_max
);
    logic x34; 
    logic [31:0] x37; 
    logic [31:0] x38; 

    always_comb begin 
        x34 = scan_output_17 == x_max; 
        x37 = scan_var_17 + 32'd1; 
        x38 = x34 ? 32'd0 : x37; 
    end 

    always_ff @(posedge clk) begin
        scan_var_17 <= x38;
    end
endmodule

module scan19 (
    input logic clk, 
    output logic [31:0] scan_var_19,
    input logic [31:0] scan_output_17,
    input logic [31:0] x_max
);
    logic x29; 
    logic [31:0] x31; 
    logic [31:0] x32; 

    always_comb begin 
        x29 = scan_output_17 == x_max; 
        x31 = scan_var_19 + 32'd1; 
        x32 = x29 ? x31 : scan_var_19; 
    end 

    always_ff @(posedge clk) begin
        scan_var_19 <= x32;
    end
endmodule

