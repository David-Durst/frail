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
        .x_stride(x_stride),
        .y_stride(y_stride)
    );

    scan12 scan12 (
        .clk(clk),
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
    input logic [15:0] x_stride,
    input logic [31:0] y_stride
);
    logic x21; 
    logic x17; 
    logic [31:0] x18; 
    logic [31:0] x19; 
    logic [31:0] x20; 
    logic [31:0] x23; 

    always_comb begin 
        x21 = scan_output_14 == y_max; 
        x17 = scan_output_12 == x_max; 
        x18 = x_stride + y_stride; 
        x19 = x17 ? x18 : x_stride; 
        x20 = scan_var_4 + x19; 
        x23 = x21 ? 32'd0 : x20; 
    end 

    always_ff @(posedge clk) begin
        scan_var_4 <= x23;
    end
endmodule

module scan12 (
    input logic clk, 
    output logic [31:0] scan_var_12
);
    logic [31:0] x31; 

    always_comb begin 
        x31 = scan_var_12 + 32'd1; 
    end 

    always_ff @(posedge clk) begin
        scan_var_12 <= x31;
    end
endmodule

module scan14 (
    input logic clk, 
    output logic [31:0] scan_var_14,
    input logic [31:0] scan_output_12,
    input logic [31:0] x_max
);
    logic x25; 
    logic [31:0] x27; 
    logic [31:0] x28; 

    always_comb begin 
        x25 = scan_output_12 == x_max; 
        x27 = scan_var_14 + 32'd1; 
        x28 = x25 ? x27 : scan_var_14; 
    end 

    always_ff @(posedge clk) begin
        scan_var_14 <= x28;
    end
endmodule

