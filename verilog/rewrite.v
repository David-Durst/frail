module rewrite (

    input logic clk,
    input logic step,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    output logic [15:0] addr_out
);

    logic [15:0] counter_val_25;
    logic [15:0] counter_at_max_25;
    logic [15:0] counter_val_34;
    logic [15:0] counter_at_max_34;

    scan25 scan25 (
        .clk(clk),
        .step(step),
        .counter_val_25(counter_val_25),
        .counter_at_max_25(counter_at_max_25),
        .x_max(x_max)
    );

    scan34 scan34 (
        .clk(clk),
        .step(step),
        .counter_val_34(counter_val_34),
        .counter_at_max_34(counter_at_max_34),
        .counter_at_max_25(counter_at_max_25),
        .x_stride(x_stride)
    );

    always_comb begin
         addr_out = counter_val_34;
    end
endmodule

module scan25 (
    input logic step,
    output logic [15:0] counter_at_max_25,
    output logic [15:0] counter_val_25,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_25 = counter_val_25 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_25 <= 1'b1 ? (counter_at_max_25 ? 16'b0 : counter_val_25 + 16'd1): counter_val_25; 
        end 
    end
endmodule

module scan34 (
    input logic step,
    output logic [15:0] counter_at_max_34,
    output logic [15:0] counter_val_34,
    input logic [15:0] counter_at_max_25,
    input logic [15:0] x_stride,
    input logic clk
);

    always_comb begin 
            counter_at_max_34 = counter_val_34 == counter_at_max_25 - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_34 <= 1'b1 ? (counter_at_max_34 ? 16'b0 : counter_val_34 + x_stride): counter_val_34; 
        end 
    end
endmodule