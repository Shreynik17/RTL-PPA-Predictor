module comparator4_tb;
  reg [3:0] a, b;
  wire gt, eq, lt;
  comparator4 uut (.a(a), .b(b), .gt(gt), .eq(eq), .lt(lt));
  initial begin
    $display("Testing 4-bit Comparator");
    $display(" a   b  | gt eq lt");
    a=4'd5; b=4'd3; #10; $display("%2d  %2d |  %b  %b  %b", a, b, gt, eq, lt);
    a=4'd7; b=4'd7; #10; $display("%2d  %2d |  %b  %b  %b", a, b, gt, eq, lt);
    a=4'd2; b=4'd9; #10; $display("%2d  %2d |  %b  %b  %b", a, b, gt, eq, lt);
    $display("Test complete"); $finish;
  end
endmodule
