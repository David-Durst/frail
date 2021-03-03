module nested (

    input logic clk,
    input logic step,
    input logic [15:0] config_66_72_op,
    input logic [15:0] offset,
    input logic [15:0] x_max,
    input logic [15:0] x_stride,
    output logic [15:0] addr_out
);

    logic [15:0] counter_val_50;
    logic [15:0] counter_at_max_50;
    logic [15:0] counter_val_78;
    logic [15:0] counter_at_max_78;
    logic [15:0] scan_inter_80;

    scan50 scan50 (
        .clk(clk),
        .step(step),
        .counter_val_50(counter_val_50),
        .counter_at_max_50(counter_at_max_50),
        .x_max(x_max)
    );

    scan78 scan78 (
        .clk(clk),
        .step(step),
        .counter_val_78(counter_val_78),
        .counter_at_max_78(counter_at_max_78),
        .counter_at_max_50(counter_at_max_50),
        .config_66_72_op(config_66_72_op),
        .x_stride(x_stride)
    );

    scan80 scan80 (
        .step(step),
        .offset(offset),
        .counter_val_78(counter_val_78),
        .scan_var_80(scan_inter_80)
    );

    always_comb begin
         addr_out = scan_inter_80;
    end
endmodule

module scan50 (
    input logic step,
    output logic [15:0] counter_at_max_50,
    output logic [15:0] counter_val_50,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_50 = counter_val_50 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_50 <= 1'b1 ? (counter_at_max_50 ? 16'b0 : counter_val_50 + 16'd1): counter_val_50; 
        end 
    end
endmodule

module scan78 (
    input logic step,
    output logic [15:0] counter_at_max_78,
    output logic [15:0] counter_val_78,
    input logic [15:0] counter_at_max_50,
    input logic [15:0] config_66_72_op,
    input logic [15:0] x_stride,
    input logic clk
);
    logic [15:0] x77; 

    always_comb begin 
            counter_at_max_78 = counter_at_max_53;
            x77 = counter_at_max_50 ? config_66_72_op : x_stride; 
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_78 <= 1'b1 ? (counter_at_max_78 ? 16'b0 : counter_val_78 + x78): counter_val_78; 
        end 
    end
endmodule

module scan80 (
    input logic step,
    output logic [15:0] scan_var_80, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_78
);
    logic [15:0] x61; 

    always_comb begin 
            x61 = offset + counter_val_78; 
            scan_var_80 = x61; 
    end 
endmodule