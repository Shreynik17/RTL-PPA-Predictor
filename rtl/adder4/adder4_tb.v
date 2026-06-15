module adder4_tb;
  reg  [3:0] a, b;
  reg        cin;
  wire [3:0] sum;
  wire       cout;

  adder4 uut (
    .a(a),
    .b(b),
    .cin(cin),
    .sum(sum),
    .cout(cout)
  );

  initial begin
    $display("Testing 4-bit Adder");
    $display("  a  +   b  + cin = cout sum  (decimal)");

    a = 4'd3;  b = 4'd5;  cin = 0; #10;
    $display("%4d + %4d + %b   =  %b   %4d  (%0d)", a, b, cin, cout, sum, {cout,sum});

    a = 4'd8;  b = 4'd7;  cin = 0; #10;
    $display("%4d + %4d + %b   =  %b   %4d  (%0d)", a, b, cin, cout, sum, {cout,sum});

    a = 4'd15; b = 4'd1;  cin = 0; #10;
    $display("%4d + %4d + %b   =  %b   %4d  (%0d)", a, b, cin, cout, sum, {cout,sum});

    a = 4'd15; b = 4'd15; cin = 1; #10;
    $display("%4d + %4d + %b   =  %b   %4d  (%0d)", a, b, cin, cout, sum, {cout,sum});

    $display("Test complete");
    $finish;
  end

endmodule
