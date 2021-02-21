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

    logic [15:0] counter_val_42;
    logic [15:0] counter_at_max_42;
    logic [15:0] counter_val_45;
    logic [15:0] counter_at_max_45;
    logic [15:0] counter_val_58;
    logic [15:0] counter_at_max_58;
    logic [15:0] counter_val_64;
    logic [15:0] counter_at_max_64;
    logic [15:0] scan_inter_66;

    scan42 scan42 (
        .clk(clk),
        .step(step),
        .counter_val_42(counter_val_42),
        .counter_at_max_42(counter_at_max_42),
        .x_max(x_max)
    );

    scan45 scan45 (
        .clk(clk),
        .step(step),
        .counter_val_45(counter_val_45),
        .counter_at_max_45(counter_at_max_45),
        .y_max(y_max)
    );

    scan58 scan58 (
        .clk(clk),
        .step(step),
        .counter_val_58(counter_val_58),
        .counter_at_max_58(counter_at_max_58),
        .counter_at_max_42(counter_at_max_42),
        .x_stride(x_stride)
    );

    scan64 scan64 (
        .clk(clk),
        .step(step),
        .counter_val_64(counter_val_64),
        .counter_at_max_64(counter_at_max_64),
        .counter_at_max_42(counter_at_max_42),
        .counter_at_max_45(counter_at_max_45),
        .y_stride(y_stride)
    );

    scan66 scan66 (
        .step(step),
        .offset(offset),
        .counter_val_58(counter_val_58),
        .counter_val_64(counter_val_64),
        .scan_var_66(scan_inter_66)
    );

    always_comb begin
         addr_out = scan_inter_66;
    end
endmodule

module scan42 (
    input logic step,
    output logic [15:0] counter_at_max_42,
    output logic [15:0] counter_val_42,
    input logic [15:0] x_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_42 = counter_val_42 == x_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_42 <= 1'b1 ? (counter_at_max_42 ? 16'b0 : counter_val_42 + 16'd1): counter_val_42; 
        end 
    end
endmodule

module scan45 (
    input logic step,
    output logic [15:0] counter_at_max_45,
    output logic [15:0] counter_val_45,
    input logic [15:0] y_max,
    input logic clk
);

    always_comb begin 
            counter_at_max_45 = counter_val_45 == y_max - 16'b1;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_45 <= counter_at_max_45 ? (counter_at_max_45 ? 16'b0 : counter_val_45 + 16'd1): counter_val_45; 
        end 
    end
endmodule

module scan58 (
    input logic step,
    output logic [15:0] counter_at_max_58,
    output logic [15:0] counter_val_58,
    input logic [15:0] counter_at_max_42,
    input logic [15:0] x_stride,
    input logic clk
);

    always_comb begin 
            counter_at_max_58 = counter_at_max_42;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_58 <= 1'b1 ? (counter_at_max_58 ? 16'b0 : counter_val_58 + x_stride): counter_val_58; 
        end 
    end
endmodule

module scan64 (
    input logic step,
    output logic [15:0] counter_at_max_64,
    output logic [15:0] counter_val_64,
    input logic [15:0] counter_at_max_42,
    input logic [15:0] counter_at_max_45,
    input logic [15:0] y_stride,
    input logic clk
);

    always_comb begin 
            counter_at_max_64 = counter_at_max_45;
    end 

    always_ff @(posedge clk) begin
        if (step) begin
            counter_val_64 <= counter_at_max_42 ? (counter_at_max_64 ? 16'b0 : counter_val_64 + y_stride): counter_val_64; 
        end 
    end
endmodule

module scan66 (
    input logic step,
    output logic [15:0] scan_var_66, 
    input logic [15:0] offset,
    input logic [15:0] counter_val_58,
    input logic [15:0] counter_val_64
);
    logic [15:0] x52; 
    logic [15:0] x53; 

    always_comb begin 
            x52 = counter_val_58 + counter_val_64; 
            x53 = offset + x52; 
            scan_var_66 = x53; 
    end 
endmodule