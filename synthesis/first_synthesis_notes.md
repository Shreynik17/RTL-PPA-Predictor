# First Synthesis Run — adder4

Manually synthesized the 4-bit adder with Yosys to understand
where the ML target labels come from.

## Results
| Design  | Cells (area proxy) | Logic depth (timing proxy) |
|---------|--------------------|----------------------------|
| adder4  | 20                 | 9                          |

## Commands used
- Area:  `yosys -p "read_verilog adder4.v; synth; stat"`
- Depth: `yosys -p "read_verilog adder4.v; synth; abc; ltp"`

## Key observations
- 20 cells = 12 NAND + 8 XOR after ABC optimization.
- Longest path (depth 9) ends at `cout` — the carry chain,
  which is the classic timing bottleneck in adders.
- Cells (area) and depth (timing) are separate targets:
  wide-shallow vs narrow-deep circuits differ, which is why
  the literature predicts both independently.
