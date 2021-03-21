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
    logic [15:0] counter_val_44;
    logic [15:0] counter_at_max_44;
    logic [15:0] scan_inter_46;

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

    scan44 scan44 (
        .clk(clk),
        .step(step),
        .counter_val_44(counter_val_44),
        .counter_at_max_44(counter_at_max_44),
        .counter_at_max_18(counter_at_max_18),
        .y_stride_op(y_stride_op),
        .x_stride(x_stride),
        .counter_at_max_15(counter_at_max_15)
    );

    scan46 scan46 (
        .step(step),
        .offset(offset),
        .counter_val_44(counter_val_44),
        .scan_var_46(scan_inter_46)
    );

    always_comb begin
         addr_out = scan_inter_46;
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

module scan44 (
    input logic step,
    output logic [15:0] counter_at_max_44,
    output logic [15:0] counter_val_44,
    input logic [15:0] counter_at_max_18,
    input logic [15:0] y_stride_op,
    input logic [15:0] x_stride,
    input logic [15:0] counter_at_max_15,
    input logic clk
);
    logic [15:0] x43; 

    always_comb begin 
            x43 = counter_at_max_15 ? y_stride_op : x_stride; 
            counter_at_max_44 = counter_at_max_18 & counter_at_max_15;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_44 <= 1'b1 ? (counter_at_max_44 ? 16'b0 : counter_val_44 + x43): counter_val_44; 
        end 
    end
endmodule

module scan46 (
    input logic step,
    output logic [15:0] scan_var_46, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_44
);
    logic [15:0] x26; 

    always_comb begin 
            x26 = offset + counter_val_44; 
            scan_var_46 = x26; 
    end 
endmodule