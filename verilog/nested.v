module nested (

    input logic clk,
    input logic step,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    input logic [15:0] y_max,
    input logic [15:0] y_stride_op,
    output logic [15:0] addr_out
);

    logic [15:0] counter_val_109;
    logic [15:0] counter_at_max_109;
    logic [15:0] counter_val_112;
    logic [15:0] counter_at_max_112;
    logic [15:0] counter_val_138;
    logic [15:0] counter_at_max_138;
    logic [15:0] scan_inter_140;

    scan109 scan109 (
        .clk(clk),
        .step(step),
        .counter_val_109(counter_val_109),
        .counter_at_max_109(counter_at_max_109),
        .x_max(x_max)
    );

    scan112 scan112 (
        .clk(clk),
        .step(step),
        .counter_val_112(counter_val_112),
        .counter_at_max_112(counter_at_max_112),
        .counter_at_max_109(counter_at_max_109),
        .y_max(y_max)
    );

    scan138 scan138 (
        .clk(clk),
        .step(step),
        .counter_val_138(counter_val_138),
        .counter_at_max_138(counter_at_max_138),
        .counter_at_max_112(counter_at_max_112),
        .y_stride_op(y_stride_op),
        .x_stride(x_stride),
        .counter_at_max_109(counter_at_max_109)
    );

    scan140 scan140 (
        .step(step),
        .offset(offset),
        .counter_val_138(counter_val_138),
        .scan_var_140(scan_inter_140)
    );

    always_comb begin
         addr_out = scan_inter_140;
    end
endmodule

module scan109 (
    input logic step,
    output logic [15:0] counter_at_max_109,
    output logic [15:0] counter_val_109,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_109 = counter_val_109 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_109 <= 1'b1 ? (counter_at_max_109 ? 16'b0 : counter_val_109 + 16'd1): counter_val_109; 
        end 
    end
endmodule

module scan112 (
    input logic step,
    output logic [15:0] counter_at_max_112,
    output logic [15:0] counter_val_112,
    input logic [15:0] counter_at_max_109,
    input logic [15:0] y_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_112 = counter_val_112 == y_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_112 <= counter_at_max_109 ? (counter_at_max_112 ? 16'b0 : counter_val_112 + 16'd1): counter_val_112; 
        end 
    end
endmodule

module scan138 (
    input logic step,
    output logic [15:0] counter_at_max_138,
    output logic [15:0] counter_val_138,
    input logic [15:0] counter_at_max_112,
    input logic [15:0] y_stride_op,
    input logic [15:0] x_stride,
    input logic [15:0] counter_at_max_109,
    input logic clk
);
    logic [15:0] x137; 

    always_comb begin 
            x137 = counter_at_max_109 ? y_stride_op : x_stride; 
            counter_at_max_138 = counter_at_max_112 & counter_at_max_109;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_138 <= 1'b1 ? (counter_at_max_138 ? 16'b0 : counter_val_138 + x137): counter_val_138; 
        end 
    end
endmodule

module scan140 (
    input logic step,
    output logic [15:0] scan_var_140, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_138
);
    logic [15:0] x120; 

    always_comb begin 
            x120 = offset + counter_val_138; 
            scan_var_140 = x120; 
    end 
endmodule