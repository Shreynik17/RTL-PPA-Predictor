module comparator4 (
  input  wire [3:0] a,
  input  wire [3:0] b,
  output wire       gt,
  output wire       eq,
  output wire       lt
);
  assign gt = (a > b);
  assign eq = (a == b);
  assign lt = (a < b);
endmodule
