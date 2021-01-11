module og_design (

    input logic clk,
    input logic step,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    input logic [15:0] y_stride,
    output logic [15:0] addr_out
);

    logic [15:0] scan_inter_5;
    logic [15:0] scan_inter_7;
    logic [15:0] scan_inter_8;
    logic [15:0] scan_inter_9;

    scan5 scan5 (
        .clk(clk),
        .step(step),
        .scan_var_5(scan_inter_5),
        .x_max(x_max)
    );

    scan7 scan7 (
        .clk(clk),
        .step(step),
        .scan_output_5(scan_inter_5),
        .x_max(x_max),
        .scan_var_7(scan_inter_7),
        .x_stride(x_stride)
    );

    scan8 scan8 (
        .clk(clk),
        .step(step),
        .scan_output_5(scan_inter_5),
        .x_max(x_max),
        .scan_var_8(scan_inter_8),
        .y_stride(y_stride)
    );

    scan9 scan9 (
        .step(step),
        .scan_output_7(scan_inter_7),
        .scan_output_8(scan_inter_8),
        .offset(offset),
        .scan_var_9(scan_inter_9)
    );

    always_comb begin
         addr_out = scan_inter_9;
    end
endmodule

module scan5 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_5,
    input logic [15:0] x_max
);
    logic [15:0] x45; 
    logic x46; 
    logic [15:0] x49; 
    logic [15:0] x50; 

    always_comb begin 
        if (step) begin
            x45 = x_max - 16'd1; 
            x46 = scan_var_5 == x45; 
            x49 = scan_var_5 + 16'd1; 
            x50 = x46 ? 16'd0 : x49; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_5 <= x50;
        end 
    end
endmodule

module scan7 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_7,
    input logic [15:0] scan_output_5,
    input logic [15:0] x_max,
    input logic [15:0] x_stride
);
    logic [15:0] x38; 
    logic x39; 
    logic [15:0] x41; 
    logic [15:0] x42; 

    always_comb begin 
        if (step) begin
            x38 = x_max - 16'd1; 
            x39 = scan_output_5 == x38; 
            x41 = scan_var_7 + x_stride; 
            x42 = x39 ? 16'd0 : x41; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_7 <= x42;
        end 
    end
endmodule

module scan8 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_8,
    input logic [15:0] scan_output_5,
    input logic [15:0] x_max,
    input logic [15:0] y_stride
);
    logic [15:0] x54; 
    logic x55; 
    logic [15:0] x56; 
    logic [15:0] x57; 

    always_comb begin 
        if (step) begin
            x54 = x_max - 16'd1; 
            x55 = scan_output_5 == x54; 
            x56 = scan_var_8 + y_stride; 
            x57 = x55 ? x56 : scan_var_8; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_8 <= x57;
        end 
    end
endmodule

module scan9 (
    input logic step,
    output logic [15:0] scan_var_9, 
    input logic [15:0] scan_output_7,
    input logic [15:0] scan_output_8,
    input logic [15:0] offset
);
    logic [15:0] x33; 
    logic [15:0] x34; 

    always_comb begin 
        if (step) begin
            x33 = scan_output_7 + scan_output_8; 
            x34 = x33 + offset; 
            scan_var_9 = x34; 
        end 
    end 
endmodule

