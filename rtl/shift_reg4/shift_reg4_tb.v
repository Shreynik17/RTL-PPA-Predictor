module shift_reg4_tb;
  reg clk, rst, serial_in;
  wire [3:0] q;
  shift_reg4 uut (.clk(clk), .rst(rst), .serial_in(serial_in), .q(q));
  initial clk = 0;
  always #5 clk = ~clk;
  initial begin
    $display("Testing 4-bit Shift Register");
    rst = 1; serial_in = 0; #12; rst = 0;
    serial_in = 1; #10; $display("q = %b", q);
    serial_in = 0; #10; $display("q = %b", q);
    serial_in = 1; #10; $display("q = %b", q);
    serial_in = 1; #10; $display("q = %b", q);
    serial_in = 0; #10; $display("q = %b", q);
    $display("Test complete"); $finish;
  end
endmodule
