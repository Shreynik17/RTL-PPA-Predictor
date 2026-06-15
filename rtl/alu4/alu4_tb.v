module alu4_tb;
  reg [3:0] a, b;
  reg [2:0] op;
  wire [3:0] result;
  wire zero;
  alu4 uut (.a(a), .b(b), .op(op), .result(result), .zero(zero));
  initial begin
    $display("Testing 4-bit ALU  (a=6, b=3)");
    a = 4'd6; b = 4'd3;
    op=3'b000; #10; $display("ADD : %2d", result);
    op=3'b001; #10; $display("SUB : %2d", result);
    op=3'b010; #10; $display("AND : %2d", result);
    op=3'b011; #10; $display("OR  : %2d", result);
    op=3'b100; #10; $display("XOR : %2d", result);
    op=3'b101; #10; $display("NOT : %2d", result);
    op=3'b110; #10; $display("SHL : %2d", result);
    op=3'b111; #10; $display("SHR : %2d", result);
    $display("Test complete"); $finish;
  end
endmodule
