module alu4 (
  input  wire [3:0] a,
  input  wire [3:0] b,
  input  wire [2:0] op,
  output reg  [3:0] result,
  output wire       zero
);
  always @(*) begin
    case (op)
      3'b000: result = a + b;
      3'b001: result = a - b;
      3'b010: result = a & b;
      3'b011: result = a | b;
      3'b100: result = a ^ b;
      3'b101: result = ~a;
      3'b110: result = a << 1;
      3'b111: result = a >> 1;
      default: result = 4'd0;
    endcase
  end
  assign zero = (result == 4'd0);
endmodule
