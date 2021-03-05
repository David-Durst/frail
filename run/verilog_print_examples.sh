#python -c 'import frail; print("design b:"); frail.print_verilog(frail.design_b); print("design a:"); frail.print_verilog(frail.design_a)'
#python -c 'import frail; print("design b:"); frail.print_frail(frail.design_b); frail.print_verilog(frail.design_b);'
#python -c 'import frail; print("design a:"); frail.print_frail(frail.design_a); frail.print_verilog(frail.design_a);'
#python -c 'import frail; frail.print_verilog(frail.design_a, top_name="design_a");'
#python -c 'import frail; frail.print_verilog(frail.counter_design, top_name="counter_design");'
python -c 'import frail; frail.print_verilog(frail.rewrite, top_name="rewrite", lake_state=frail.rewrite_lake_state);'
#python -c 'import frail; frail.print_verilog(frail.op_design, top_name="op_design");'
#python -c 'import frail; frail.print_verilog(frail.design_b, top_name="design_b");'
#python -c 'import frail;'
