module design_b (

    input logic clk,
    input logic [11:0] x_stride,
    input logic [31:0] x_max,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_2;

    scan2 scan2 (
        .clk(clk),
        .scan_var_2(scan_inter_2),
        .x_stride(x_stride),
        .x_max(x_max),
        .y_stride(y_stride),
        .y_max(y_max)
    );

    always_ff @(posedge clk) begin
         addr <= scan_inter_2;
    end
endmodule

module scan2 (
    input logic clk, 
    output logic [31:0] scan_var_2,
    input logic [11:0] x_stride,
    input logic [31:0] x_max,
    input logic [31:0] y_stride,
    input logic [31:0] y_max
);
    logic [31:0] x11; 
    logic [11:0] x12; 
    logic x13; 
    logic [31:0] x16; 
    logic [31:0] x17; 
    logic x18; 
    logic [31:0] x20; 

    always_comb begin 
        x11 = scan_var_2 + x_stride; 
        x12 = x11[11 : 0]; 
        x13 = x12 == x_max; 
        x16 = x13 ? y_stride : x_stride; 
        x17 = scan_var_2 + x16; 
        x18 = x17 == y_max; 
        x20 = x18 ? 32'd0 : x17; 
    end 

    always_ff @(posedge clk) begin
        scan_var_2 <= x20;
    end
endmodule
