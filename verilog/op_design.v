module op_design (

    input logic clk,
    input logic [15:0] x_stride,
    input logic [31:0] offset,
    input logic [31:0] x_max,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [15:0] addr
);

    logic [15:0] scan_inter_10;
    logic [15:0] scan_inter_11;
    logic [15:0] scan_inter_14;
    logic [31:0] scan_inter_15;

    scan10 scan10 (
        .clk(clk),
        .scan_var_10(scan_inter_10),
        .x_max(x_max)
    );

    scan11 scan11 (
        .clk(clk),
        .scan_output_10(scan_inter_10),
        .x_max(x_max),
        .scan_var_11(scan_inter_11)
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
        .scan_output_11(scan_inter_11),
        .y_max(y_max),
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
    output logic [15:0] scan_var_10,
    input logic [31:0] x_max
);
    logic [31:0] x47; 
    logic x48; 
    logic [31:0] x51; 
    logic [31:0] x52; 

    always_comb begin 
        x47 = x_max - 32'd1; 
        x48 = scan_var_10 == x47; 
        x51 = scan_var_10 + 32'd1; 
        x52 = x48 ? 32'd0 : x51; 
    end 

    always_ff @(posedge clk) begin
        scan_var_10 <= x52;
    end
endmodule

module scan11 (
    input logic clk, 
    output logic [15:0] scan_var_11,
    input logic [15:0] scan_output_10,
    input logic [31:0] x_max
);
    logic [31:0] x40; 
    logic x41; 
    logic [31:0] x43; 
    logic [31:0] x44; 

    always_comb begin 
        x40 = x_max - 32'd1; 
        x41 = scan_output_10 == x40; 
        x43 = scan_var_11 + 32'd1; 
        x44 = x41 ? x43 : scan_var_11; 
    end 

    always_ff @(posedge clk) begin
        scan_var_11 <= x44;
    end
endmodule

module scan14 (
    input logic clk, 
    output logic [15:0] scan_var_14,
    input logic [15:0] scan_output_10,
    input logic [31:0] x_max,
    input logic [31:0] y_stride,
    input logic [15:0] x_stride
);
    logic [31:0] x55; 
    logic x56; 
    logic [31:0] x57; 
    logic [31:0] x58; 

    always_comb begin 
        x55 = x_max - 32'd1; 
        x56 = scan_output_10 == x55; 
        x57 = x56 ? y_stride : x_stride; 
        x58 = scan_var_14 + x57; 
    end 

    always_ff @(posedge clk) begin
        scan_var_14 <= x58;
    end
endmodule

module scan15 (
    output logic [31:0] scan_var_15, 
    input logic [15:0] scan_output_11,
    input logic [31:0] y_max,
    input logic [15:0] scan_output_14,
    input logic [31:0] offset
);
    logic x32; 
    logic [31:0] x35; 
    logic [31:0] x36; 

    always_comb begin 
        x32 = scan_output_11 == y_max; 
        x35 = scan_output_14 + offset; 
        x36 = x32 ? 32'd0 : x35; 
        scan_var_15 = x36; 
    end 
endmodule

