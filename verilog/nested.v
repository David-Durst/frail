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

    logic [15:0] counter_val_15;
    logic [15:0] counter_at_max_15;
    logic [15:0] counter_val_18;
    logic [15:0] counter_at_max_18;
    logic [15:0] counter_val_37;
    logic [15:0] counter_at_max_37;
    logic [15:0] counter_val_56;
    logic [15:0] counter_at_max_56;
    logic [15:0] scan_inter_58;

    scan15 scan15 (
        .clk(clk),
        .step(step),
        .counter_val_15(counter_val_15),
        .counter_at_max_15(counter_at_max_15),
        .x_max(x_max)
    );

    scan18 scan18 (
        .clk(clk),
        .step(step),
        .counter_val_18(counter_val_18),
        .counter_at_max_18(counter_at_max_18),
        .counter_at_max_15(counter_at_max_15),
        .y_max(y_max)
    );

    scan37 scan37 (
        .clk(clk),
        .step(step),
        .counter_val_37(counter_val_37),
        .counter_at_max_37(counter_at_max_37),
        .counter_at_max_15(counter_at_max_15),
        .x_stride(x_stride)
    );

    scan56 scan56 (
        .clk(clk),
        .step(step),
        .counter_val_56(counter_val_56),
        .counter_at_max_56(counter_at_max_56),
        .counter_at_max_18(counter_at_max_18),
        .y_stride_op(y_stride_op),
        .x_stride(x_stride),
        .counter_at_max_15(counter_at_max_15)
    );

    scan58 scan58 (
        .step(step),
        .offset(offset),
        .counter_val_37(counter_val_37),
        .counter_val_56(counter_val_56),
        .scan_var_58(scan_inter_58)
    );

    always_comb begin
         addr_out = scan_inter_58;
    end
endmodule

module scan15 (
    input logic step,
    output logic [15:0] counter_at_max_15,
    output logic [15:0] counter_val_15,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_15 = counter_val_15 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_15 <= 1'b1 ? (counter_at_max_15 ? 16'b0 : counter_val_15 + 16'd1): counter_val_15; 
        end 
    end
endmodule

module scan18 (
    input logic step,
    output logic [15:0] counter_at_max_18,
    output logic [15:0] counter_val_18,
    input logic [15:0] counter_at_max_15,
    input logic [15:0] y_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_18 = counter_val_18 == y_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_18 <= counter_at_max_15 ? (counter_at_max_18 ? 16'b0 : counter_val_18 + 16'd1): counter_val_18; 
        end 
    end
endmodule

module scan37 (
    input logic step,
    output logic [15:0] counter_at_max_37,
    output logic [15:0] counter_val_37,
    input logic [15:0] counter_at_max_15,
    input logic [15:0] x_stride,
    input logic clk
);

    always_comb begin 
            counter_at_max_37 = counter_at_max_15;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_37 <= 1'b1 ? (counter_at_max_37 ? 16'b0 : counter_val_37 + x_stride): counter_val_37; 
        end 
    end
endmodule

module scan56 (
    input logic step,
    output logic [15:0] counter_at_max_56,
    output logic [15:0] counter_val_56,
    input logic [15:0] counter_at_max_18,
    input logic [15:0] y_stride_op,
    input logic [15:0] x_stride,
    input logic [15:0] counter_at_max_15,
    input logic clk
);
    logic [15:0] x55; 

    always_comb begin 
            x55 = counter_at_max_15 ? y_stride_op : x_stride; 
            counter_at_max_56 = counter_at_max_18 & counter_at_max_15;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_56 <= 1'b1 ? (counter_at_max_56 ? 16'b0 : counter_val_56 + x55): counter_val_56; 
        end 
    end
endmodule

module scan58 (
    input logic step,
    output logic [15:0] scan_var_58, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_37,
    input logic [15:0] counter_val_56
);
    logic [15:0] x31; 
    logic [15:0] x32; 

    always_comb begin 
            x31 = counter_val_37 + counter_val_56; 
            x32 = offset + x31; 
            scan_var_58 = x32; 
    end 
endmodule