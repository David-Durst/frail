module rewrite (

    input logic clk,
    input logic step,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    input logic [15:0] y_max,
    input logic [15:0] y_stride,
    output logic [15:0] addr_out
);

    logic [15:0] counter_val_99;
    logic [15:0] counter_at_max_99;
    logic [15:0] counter_val_102;
    logic [15:0] counter_at_max_102;
    logic [15:0] counter_val_115;
    logic [15:0] counter_at_max_115;
    logic [15:0] counter_val_121;
    logic [15:0] counter_at_max_121;
    logic [15:0] scan_inter_123;

    scan99 scan99 (
        .clk(clk),
        .step(step),
        .counter_val_99(counter_val_99),
        .counter_at_max_99(counter_at_max_99),
        .x_max(x_max)
    );

    scan102 scan102 (
        .clk(clk),
        .step(step),
        .counter_val_102(counter_val_102),
        .counter_at_max_102(counter_at_max_102),
        .y_max(y_max)
    );

    scan115 scan115 (
        .clk(clk),
        .step(step),
        .counter_val_115(counter_val_115),
        .counter_at_max_115(counter_at_max_115),
        .counter_at_max_99(counter_at_max_99),
        .x_stride(x_stride)
    );

    scan121 scan121 (
        .clk(clk),
        .step(step),
        .counter_val_121(counter_val_121),
        .counter_at_max_121(counter_at_max_121),
        .counter_at_max_99(counter_at_max_99),
        .counter_at_max_102(counter_at_max_102),
        .y_stride(y_stride)
    );

    scan123 scan123 (
        .step(step),
        .offset(offset),
        .counter_val_115(counter_val_115),
        .counter_val_121(counter_val_121),
        .scan_var_123(scan_inter_123)
    );

    always_comb begin
         addr_out = scan_inter_123;
    end
endmodule

module scan99 (
    input logic step,
    output logic [15:0] counter_at_max_99,
    output logic [15:0] counter_val_99,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_99 = counter_val_99 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_99 <= 1'b1 ? (counter_at_max_99 ? 16'b0 : counter_val_99 + 16'd1): counter_val_99; 
        end 
    end
endmodule

module scan102 (
    input logic step,
    output logic [15:0] counter_at_max_102,
    output logic [15:0] counter_val_102,
    input logic [15:0] y_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_102 = counter_val_102 == y_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_102 <= counter_at_max_102 ? (counter_at_max_102 ? 16'b0 : counter_val_102 + 16'd1): counter_val_102; 
        end 
    end
endmodule

module scan115 (
    input logic step,
    output logic [15:0] counter_at_max_115,
    output logic [15:0] counter_val_115,
    input logic [15:0] counter_at_max_99,
    input logic [15:0] x_stride,
    input logic clk
);

    always_comb begin 
            counter_at_max_115 = counter_at_max_99;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_115 <= 1'b1 ? (counter_at_max_115 ? 16'b0 : counter_val_115 + x_stride): counter_val_115; 
        end 
    end
endmodule

module scan121 (
    input logic step,
    output logic [15:0] counter_at_max_121,
    output logic [15:0] counter_val_121,
    input logic [15:0] counter_at_max_99,
    input logic [15:0] counter_at_max_102,
    input logic [15:0] y_stride,
    input logic clk
);

    always_comb begin 
            counter_at_max_121 = counter_at_max_102;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_121 <= counter_at_max_99 ? (counter_at_max_121 ? 16'b0 : counter_val_121 + y_stride): counter_val_121; 
        end 
    end
endmodule

module scan123 (
    input logic step,
    output logic [15:0] scan_var_123, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_115,
    input logic [15:0] counter_val_121
);
    logic [15:0] x109; 
    logic [15:0] x110; 

    always_comb begin 
            x109 = counter_val_115 + counter_val_121; 
            x110 = offset + x109; 
            scan_var_123 = x110; 
    end 
endmodule