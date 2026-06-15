module counter4_tb;
  reg clk, rst;
  wire [3:0] count;
  counter4 uut (.clk(clk), .rst(rst), .count(count));
  initial clk = 0;
  always #5 clk = ~clk;
  initial begin
    $display("Testing 4-bit Counter");
    rst = 1; #12; rst = 0;
    repeat (18) begin #10 $display("count = %2d", count); end
    $display("Test complete"); $finish;
  end
endmodule
