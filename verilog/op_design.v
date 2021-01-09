module op_design (

    input logic clk,
    input logic step,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    input logic [15:0] y_stride,
    output logic [15:0] addr
);

    logic [15:0] scan_inter_10;
    logic [15:0] scan_inter_14;
    logic [15:0] scan_inter_15;

    scan10 scan10 (
        .clk(clk),
        .step(step),
        .scan_var_10(scan_inter_10),
        .x_max(x_max)
    );

    scan14 scan14 (
        .clk(clk),
        .step(step),
        .scan_var_14(scan_inter_14),
        .scan_output_10(scan_inter_10),
        .x_max(x_max),
        .y_stride(y_stride),
        .x_stride(x_stride)
    );

    scan15 scan15 (
        .step(step),
        .scan_output_14(scan_inter_14),
        .offset(offset),
        .scan_var_15(scan_inter_15)
    );

    always_comb begin
         addr = scan_inter_15;
    end
endmodule

module scan10 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_10,
    input logic [15:0] x_max
);
    logic [15:0] x41; 
    logic x42; 
    logic [15:0] x45; 
    logic [15:0] x46; 

    always_comb begin 
        if (step) begin
            x41 = x_max - 16'd1; 
            x42 = scan_var_10 == x41; 
            x45 = scan_var_10 + 16'd1; 
            x46 = x42 ? 16'd0 : x45; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_10 <= x46;
        end 
    end
endmodule

module scan14 (
    input logic step,
    input logic clk, 
    output logic [15:0] scan_var_14,
    input logic [15:0] scan_output_10,
    input logic [15:0] x_max,
    input logic [15:0] y_stride,
    input logic [15:0] x_stride
);
    logic [15:0] x35; 
    logic x36; 
    logic [15:0] x37; 
    logic [15:0] x38; 

    always_comb begin 
        if (step) begin
            x35 = x_max - 16'd1; 
            x36 = scan_output_10 == x35; 
            x37 = x36 ? y_stride : x_stride; 
            x38 = scan_var_14 + x37; 
        end 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            scan_var_14 <= x38;
        end 
    end
endmodule

module scan15 (
    input logic step,
    output logic [15:0] scan_var_15, 
    input logic [15:0] scan_output_14,
    input logic [15:0] offset
);
    logic [15:0] x32; 

    always_comb begin 
        if (step) begin
            x32 = scan_output_14 + offset; 
            scan_var_15 = x32; 
        end 
    end 
endmodule

