module og_design (

    input logic clk,
    input logic [31:0] offset,
    input logic [31:0] x_max,
    input logic [31:0] x_stride,
    input logic [31:0] y_max,
    input logic [31:0] y_stride,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_4;
    logic [31:0] scan_inter_5;
    logic [31:0] scan_inter_6;
    logic [31:0] scan_inter_7;
    logic [31:0] scan_inter_8;
    logic [31:0] scan_inter_9;

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
        .scan_output_4(scan_inter_4),
        .x_max(x_max),
        .scan_var_6(scan_inter_6),
        .x_stride(x_stride)
    );

    scan7 scan7 (
        .clk(clk),
        .scan_output_4(scan_inter_4),
        .x_max(x_max),
        .scan_var_7(scan_inter_7),
        .y_stride(y_stride)
    );

    scan8 scan8 (
        .scan_output_5(scan_inter_5),
        .y_max(y_max),
        .scan_output_7(scan_inter_7),
        .scan_var_8(scan_inter_8)
    );

    scan9 scan9 (
        .scan_output_6(scan_inter_6),
        .scan_output_8(scan_inter_8),
        .offset(offset),
        .scan_var_9(scan_inter_9)
    );

    always_ff @(posedge clk) begin
         addr <= scan_inter_9;
    end
endmodule

module scan4 (
    input logic clk, 
    output logic [31:0] scan_var_4,
    input logic [31:0] x_max
);
    logic [31:0] x26; 
    logic x27; 
    logic [31:0] x30; 
    logic [31:0] x31; 

    always_comb begin 
        x26 = x_max - 32'd1; 
        x27 = scan_var_4 == x26; 
        x30 = scan_var_4 + 32'd1; 
        x31 = x27 ? 32'd0 : x30; 
    end 

    always_ff @(posedge clk) begin
        scan_var_4 <= x31;
    end
endmodule

module scan5 (
    input logic clk, 
    output logic [31:0] scan_var_5,
    input logic [31:0] scan_output_4,
    input logic [31:0] x_max
);
    logic [31:0] x43; 
    logic x44; 
    logic [31:0] x46; 
    logic [31:0] x47; 

    always_comb begin 
        x43 = x_max - 32'd1; 
        x44 = scan_output_4 == x43; 
        x46 = scan_var_5 + 32'd1; 
        x47 = x44 ? x46 : scan_var_5; 
    end 

    always_ff @(posedge clk) begin
        scan_var_5 <= x47;
    end
endmodule

module scan6 (
    input logic clk, 
    output logic [31:0] scan_var_6,
    input logic [31:0] scan_output_4,
    input logic [31:0] x_max,
    input logic [31:0] x_stride
);
    logic [31:0] x19; 
    logic x20; 
    logic [31:0] x22; 
    logic [31:0] x23; 

    always_comb begin 
        x19 = x_max - 32'd1; 
        x20 = scan_output_4 == x19; 
        x22 = scan_var_6 + x_stride; 
        x23 = x20 ? 32'd0 : x22; 
    end 

    always_ff @(posedge clk) begin
        scan_var_6 <= x23;
    end
endmodule

module scan7 (
    input logic clk, 
    output logic [31:0] scan_var_7,
    input logic [31:0] scan_output_4,
    input logic [31:0] x_max,
    input logic [31:0] y_stride
);
    logic [31:0] x51; 
    logic x52; 
    logic [31:0] x53; 
    logic [31:0] x54; 

    always_comb begin 
        x51 = x_max - 32'd1; 
        x52 = scan_output_4 == x51; 
        x53 = scan_var_7 + y_stride; 
        x54 = x52 ? x53 : scan_var_7; 
    end 

    always_ff @(posedge clk) begin
        scan_var_7 <= x54;
    end
endmodule

module scan8 (
    output logic [31:0] scan_var_8, 
    input logic [31:0] scan_output_5,
    input logic [31:0] y_max,
    input logic [31:0] scan_output_7
);
    logic [31:0] x35; 
    logic x36; 
    logic [31:0] x39; 

    always_comb begin 
        x35 = y_max - 32'd1; 
        x36 = scan_output_5 == x35; 
        x39 = x36 ? 32'd0 : scan_output_7; 
        scan_var_8 = x39; 
    end 
endmodule

module scan9 (
    output logic [31:0] scan_var_9, 
    input logic [31:0] scan_output_6,
    input logic [31:0] scan_output_8,
    input logic [31:0] offset
);
    logic [31:0] x13; 
    logic [31:0] x15; 

    always_comb begin 
        x13 = scan_output_6 + scan_output_8; 
        x15 = x13 + offset; 
        scan_var_9 = x15; 
    end 
endmodule

