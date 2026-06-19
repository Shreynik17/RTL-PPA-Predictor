module shift_reg #(
  parameter WIDTH = 4
) (
  input  wire             clk,
  input  wire             rst,
  input  wire             serial_in,
  output reg  [WIDTH-1:0] q
);
  always @(posedge clk or posedge rst) begin
    if (rst) q <= {WIDTH{1'b0}};
    else     q <= {q[WIDTH-2:0], serial_in};
  end
endmodule
