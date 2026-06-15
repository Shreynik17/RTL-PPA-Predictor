module seq_detector (
  input  wire clk,
  input  wire rst,
  input  wire in,
  output reg  detected
);
  localparam S0 = 2'b00, S1 = 2'b01, S2 = 2'b10;
  reg [1:0] state, next_state;

  always @(posedge clk or posedge rst) begin
    if (rst) state <= S0;
    else     state <= next_state;
  end

  always @(*) begin
    case (state)
      S0: next_state = in ? S1 : S0;
      S1: next_state = in ? S1 : S2;
      S2: next_state = in ? S1 : S0;
      default: next_state = S0;
    endcase
  end

  always @(*) detected = (state == S2 && in == 1'b1);
endmodule
