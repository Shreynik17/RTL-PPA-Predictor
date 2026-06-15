module seq_detector_tb;
  reg clk, rst, in;
  wire detected;
  integer i;
  reg [0:9] stream = 10'b1011010100;
  seq_detector uut (.clk(clk), .rst(rst), .in(in), .detected(detected));
  initial clk = 0;
  always #5 clk = ~clk;
  initial begin
    $display("Testing 101 Sequence Detector");
    rst = 1; in = 0; #12; rst = 0;
    for (i = 0; i < 10; i = i + 1) begin
      in = stream[i]; #10;
      $display("in=%b  detected=%b", in, detected);
    end
    $display("Test complete"); $finish;
  end
endmodule
