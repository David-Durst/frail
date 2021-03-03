module nested (

    input logic clk,
    input logic step,
    input logic [15:0] config_68_74_op,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    input logic [15:0] y_max,
    output logic [15:0] addr_out
);

    logic [15:0] counter_val_52;
    logic [15:0] counter_at_max_52;
    logic [15:0] counter_val_55;
    logic [15:0] counter_at_max_55;
    logic [15:0] counter_val_81;
    logic [15:0] counter_at_max_81;
    logic [15:0] scan_inter_83;

    scan52 scan52 (
        .clk(clk),
        .step(step),
        .counter_val_52(counter_val_52),
        .counter_at_max_52(counter_at_max_52),
        .x_max(x_max)
    );

    scan55 scan55 (
        .clk(clk),
        .step(step),
        .counter_val_55(counter_val_55),
        .counter_at_max_55(counter_at_max_55),
        .counter_at_max_52(counter_at_max_52),
        .y_max(y_max)
    );

    scan81 scan81 (
        .clk(clk),
        .step(step),
        .counter_val_81(counter_val_81),
        .counter_at_max_81(counter_at_max_81),
        .counter_at_max_55(counter_at_max_55),
        .counter_at_max_52(counter_at_max_52),
        .config_68_74_op(config_68_74_op),
        .x_stride(x_stride)
    );

    scan83 scan83 (
        .step(step),
        .offset(offset),
        .counter_val_81(counter_val_81),
        .scan_var_83(scan_inter_83)
    );

    always_comb begin
         addr_out = scan_inter_83;
    end
endmodule

module scan52 (
    input logic step,
    output logic [15:0] counter_at_max_52,
    output logic [15:0] counter_val_52,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_52 = counter_val_52 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_52 <= 1'b1 ? (counter_at_max_52 ? 16'b0 : counter_val_52 + 16'd1): counter_val_52; 
        end 
    end
endmodule

module scan55 (
    input logic step,
    output logic [15:0] counter_at_max_55,
    output logic [15:0] counter_val_55,
    input logic [15:0] counter_at_max_52,
    input logic [15:0] y_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_55 = counter_val_55 == y_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_55 <= counter_at_max_52 ? (counter_at_max_55 ? 16'b0 : counter_val_55 + 16'd1): counter_val_55; 
        end 
    end
endmodule

module scan81 (
    input logic step,
    output logic [15:0] counter_at_max_81,
    output logic [15:0] counter_val_81,
    input logic [15:0] counter_at_max_55,
    input logic [15:0] counter_at_max_52,
    input logic [15:0] config_68_74_op,
    input logic [15:0] x_stride,
    input logic clk
);
    logic [15:0] x80; 

    always_comb begin 
            counter_at_max_81 = counter_at_max_55;
            x80 = counter_at_max_52 ? config_68_74_op : x_stride; 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_81 <= 1'b1 ? (counter_at_max_81 ? 16'b0 : counter_val_81 + x80): counter_val_81; 
        end 
    end
endmodule

module scan83 (
    input logic step,
    output logic [15:0] scan_var_83, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_81
);
    logic [15:0] x63; 

    always_comb begin 
            x63 = offset + counter_val_81; 
            scan_var_83 = x63; 
    end 
endmodule