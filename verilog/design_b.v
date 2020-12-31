module design_b (

    input logic clk,
    input logic [11:0] x_delta,
    input logic [31:0] y_delta,
    output logic [31:0] addr
);

    logic [31:0] scan_inter_0;

    scan0 scan0 (
        .clk(clk),
        .scan_var_0(scan_inter_0),
        .x_delta(x_delta),
        .y_delta(y_delta)
    );

    assign addr = scan_inter_0;

endmodule

module scan0 (
    input logic clk, 
    output logic [31:0] scan_var_0,
    input logic [11:0] x_delta,
    input logic [31:0] y_delta
);
    logic [31:0] x11; 
    logic [11:0] x12; 
    logic x14; 
    logic [31:0] x17; 
    logic [31:0] x18; 

    always_comb begin 
        x11 = scan_var_0 + x_delta; 
        x12 = x11[11 : 0]; 
        x14 = x12 == 32'd0; 
        x17 = x14 ? y_delta : 32'd0; 
        x18 = x11 + x17; 
    end 

    always_ff @(posedge clk) begin
        scan_var_0 <= x18;
    end
endmodule

