# RTL PPA Predictor

This is a project I built to learn how machine learning can be applied to chip design (an area usually called ML-for-EDA). The goal is to predict the **area** and **timing** of a digital circuit directly from its Verilog code, without actually running the full synthesis step.

I'm an electronics engineering student and I'm interested in VLSI and design verification, so I wanted a project that sits between hardware and ML rather than being purely one or the other.

## The idea

Normally, to find out how big a circuit is or how fast it can run, you have to synthesize it with an EDA tool, which can be slow. Some recent research (MasterRTL, RTL-Timer) looks at whether you can instead *predict* these numbers straight from the RTL code using machine learning. This project is my own small, from-scratch version of that idea, built entirely with open-source tools.

## How it works

The pipeline goes through these steps:

1. Write a set of small Verilog circuits (adder, comparator, ALU, counter, shift register, etc.).
2. Synthesize each one with Yosys to get the true numbers:
   - cell count (a proxy for area)
   - logic depth (a proxy for timing)
3. Extract features from the RTL source code (bit-width, number of operators, whether it's sequential, etc.).
4. Make a bigger dataset by re-generating each design at different bit-widths (2 to 64).
5. Train ML models (linear regression and random forest) to predict the area and timing from the features.

## Results

With 30 samples (5 designs swept across 6 bit-widths):

| Target | Best model | R² |
|--------|-----------|-----|
| Cell count (area) | Linear Regression | 0.98 |
| Logic depth (timing) | Linear Regression | 0.71 |

A couple of things I found interesting while doing this:

- Linear regression actually did **better** than random forest on cell count. This is because the random forest can't predict values larger than what it saw in training, and some of my designs (like the 64-bit ALU) are much bigger than the rest. Linear regression can extrapolate, so it handled them better.
- The most useful feature by far was `width * operators` (bit-width multiplied by operator count), which I added as a combined feature. It explained about 93% of the variation in area on its own.

The prediction plots are in the `results/` folder.

## Repository layout

```
rtl/         original fixed-width Verilog designs + testbenches
rtl_param/   parameterized designs (any bit-width)
synthesis/   synthesis notes
src/         python scripts (synthesis automation, feature extraction, training)
data/        generated datasets (csv)
results/     prediction plots
```

## How to run it

You'll need Python 3, Yosys, and Icarus Verilog installed.

Install the Python packages:
```
pip install -r requirements.txt
```

Generate the dataset (runs Yosys across all designs and widths):
```
python3 src/build_dataset.py
```

Train the models and produce the plots:
```
python3 src/train_model.py
```

## Limitations

I want to be honest about where this stands:

- The dataset is small (30 samples). It's enough to show the approach works, but not enough to draw strong conclusions. Adding more design types and widths would make the results more reliable.
- Timing (logic depth) is harder to predict than area, and my current features don't capture it well. Things like carry-chain length would probably help.
- The designs are simple building blocks, not large real-world modules.

## What I'd do next

- Add more designs (multiplier, divider, FIFO, etc.) and more widths to grow the dataset to 100+ samples.
- Add structural features to improve the timing prediction.
- Try the same idea on a couple of larger open-source RTL designs.

## Tools used

Verilog, Icarus Verilog (simulation), Yosys (synthesis), Python, pandas, scikit-learn, matplotlib.
