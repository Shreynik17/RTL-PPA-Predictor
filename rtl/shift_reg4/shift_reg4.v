module shift_reg4 (
  input  wire       clk,
  input  wire       rst,
  input  wire       serial_in,
  output reg  [3:0] q
);
  always @(posedge clk or posedge rst) begin
    if (rst) q <= 4'd0;
    else     q <= {q[2:0], serial_in};
  end
endmodule
