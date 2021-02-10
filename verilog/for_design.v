module for_design (

    input logic clk,
    input logic step,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    input logic [15:0] y_stride,
    output logic [15:0] addr_out
);

    logic [15:0] scan_inter_5;
    logic [15:0] scan_inter_6;
    logic [15:0] scan_inter_7;

    scan5 scan5 (
        .clk(clk),
        .step(step),
        .scan_var_5(scan_inter_5),
        .x_max(x_max)
    );

    scan6 scan6 (
        .clk(clk),
        .step(step),
        .scan_output_5(scan_inter_5),
        .x_max(x_max),
        .scan_var_6(scan_inter_6)
    );

    scan7 scan7 (
        .step(step),
        .scan_output_5(scan_inter_5),
        .x_stride(x_stride),
        .scan_output_6(scan_inter_6),
        .y_stride(y_stride),
        .offset(offset),
        .scan_var_7(scan_inter_7)
    );

    always_comb begin
         addr_out = scan_inter_7;
    end
endmodule

module scan5 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_5,
    input logic [15:0] x_max
);
    logic [15:0] x42; 
    logic x43; 
    logic [15:0] x46; 
    logic [15:0] x47; 

    always_comb begin 
        if (step) begin
            x42 = x_max - 16'd1; 
            x43 = scan_var_5 == x42; 
            x46 = scan_var_5 + 16'd1; 
            x47 = x43 ? 16'd0 : x46; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_5 <= x47;
        end 
    end
endmodule

module scan6 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_6,
    input logic [15:0] scan_output_5,
    input logic [15:0] x_max
);
    logic [15:0] x51; 
    logic x52; 
    logic [15:0] x54; 
    logic [15:0] x55; 

    always_comb begin 
        if (step) begin
            x51 = x_max - 16'd1; 
            x52 = scan_output_5 == x51; 
            x54 = scan_var_6 + 16'd1; 
            x55 = x52 ? x54 : scan_var_6; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_6 <= x55;
        end 
    end
endmodule

module scan7 (
    input logic step,
    output logic [15:0] scan_var_7, 
    input logic [15:0] scan_output_5,
    input logic [15:0] x_stride,
    input logic [15:0] scan_output_6,
    input logic [15:0] y_stride,
    input logic [15:0] offset
);
    logic [15:0] x35; 
    logic [15:0] x37; 
    logic [15:0] x38; 
    logic [15:0] x39; 

    always_comb begin 
        if (step) begin
            x35 = scan_output_5 * x_stride; 
            x37 = scan_output_6 * y_stride; 
            x38 = x35 + x37; 
            x39 = x38 + offset; 
            scan_var_7 = x39; 
        end 
    end 
endmodule

