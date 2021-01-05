module design_a (

    input logic clk,
    input logic [31:0] offset,
    input logic [31:0] x_max,
    input logic [31:0] x_stride,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_3;
    logic [31:0] scan_inter_4;
    logic [31:0] scan_inter_5;
    logic [31:0] scan_inter_6;
    logic [31:0] scan_inter_7;
    logic [31:0] scan_inter_8;

    scan3 scan3 (
        .clk(clk),
        .scan_var_3(scan_inter_3),
        .x_max(x_max)
    );

    scan4 scan4 (
        .clk(clk),
        .scan_var_4(scan_inter_4),
        .scan_output_3(scan_inter_3),
        .x_max(x_max),
        .y_max(y_max)
    );

    scan5 scan5 (
        .scan_output_3(scan_inter_3),
        .x_stride(x_stride),
        .scan_var_5(scan_inter_5)
    );

    scan6 scan6 (
        .scan_output_4(scan_inter_4),
        .y_stride(y_stride),
        .scan_var_6(scan_inter_6)
    );

    scan7 scan7 (
        .scan_output_5(scan_inter_5),
        .scan_output_6(scan_inter_6),
        .scan_var_7(scan_inter_7)
    );

    scan8 scan8 (
        .scan_output_7(scan_inter_7),
        .offset(offset),
        .scan_var_8(scan_inter_8)
    );

    always_ff @(posedge clk) begin
         addr <= scan_inter_8;
    end
endmodule

module scan3 (
    input logic clk, 
    output logic [31:0] scan_var_3,
    input logic [31:0] x_max
);
    logic [31:0] x23; 
    logic [31:0] x24; 

    always_comb begin 
        x23 = scan_var_3 + 32'd1; 
        x24 = x23 % x_max; 
    end 

    always_ff @(posedge clk) begin
        scan_var_3 <= x24;
    end
endmodule

module scan4 (
    input logic clk, 
    output logic [31:0] scan_var_4,
    input logic [31:0] scan_output_3,
    input logic [31:0] x_max,
    input logic [31:0] y_max
);
    logic [31:0] x32; 
    logic x33; 
    logic [31:0] x36; 
    logic [31:0] x37; 
    logic [31:0] x38; 

    always_comb begin 
        x32 = x_max - 32'd1; 
        x33 = scan_output_3 == x32; 
        x36 = x33 ? 32'd1 : 32'd0; 
        x37 = scan_var_4 + x36; 
        x38 = x37 % y_max; 
    end 

    always_ff @(posedge clk) begin
        scan_var_4 <= x38;
    end
endmodule

module scan5 (
    output logic [31:0] scan_var_5, 
    input logic [31:0] scan_output_3,
    input logic [31:0] x_stride
);
    logic [31:0] x20; 

    always_comb begin 
        x20 = scan_output_3 * x_stride; 
        scan_var_5 = x20; 
    end 
endmodule

module scan6 (
    output logic [31:0] scan_var_6, 
    input logic [31:0] scan_output_4,
    input logic [31:0] y_stride
);
    logic [31:0] x28; 

    always_comb begin 
        x28 = scan_output_4 * y_stride; 
        scan_var_6 = x28; 
    end 
endmodule

module scan7 (
    output logic [31:0] scan_var_7, 
    input logic [31:0] scan_output_5,
    input logic [31:0] scan_output_6
);
    logic [31:0] x16; 

    always_comb begin 
        x16 = scan_output_5 + scan_output_6; 
        scan_var_7 = x16; 
    end 
endmodule

module scan8 (
    output logic [31:0] scan_var_8, 
    input logic [31:0] scan_output_7,
    input logic [31:0] offset
);
    logic [31:0] x12; 

    always_comb begin 
        x12 = scan_output_7 + offset; 
        scan_var_8 = x12; 
    end 
endmodule
