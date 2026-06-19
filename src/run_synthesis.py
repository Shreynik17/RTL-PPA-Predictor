#!/usr/bin/env python3
"""
run_synthesis.py
Loops over all RTL designs, runs Yosys on each to extract
ML target labels (cell count = area, logic depth = timing),
and writes everything to data/dataset.csv.
"""

import subprocess   # lets Python run terminal commands (like Yosys)
import re           # "regular expressions" — for finding numbers in text
import csv          # for writing the CSV file
import os           # for working with file paths

# --- 1. List of designs to process ---
# Each entry is (folder_name, verilog_file, top_module_name)
DESIGNS = [
    ("mux2to1",      "mux2to1.v",      "mux2to1"),
    ("adder4",       "adder4.v",       "adder4"),
    ("comparator4",  "comparator4.v",  "comparator4"),
    ("alu4",         "alu4.v",         "alu4"),
    ("counter4",     "counter4.v",     "counter4"),
    ("shift_reg4",   "shift_reg4.v",   "shift_reg4"),
    ("seq_detector", "seq_detector.v", "seq_detector"),
]

RTL_DIR = "rtl"
OUTPUT_CSV = "data/dataset.csv"


def run_yosys(commands, work_dir):
    """Run Yosys with a script of commands inside work_dir, return its text output."""
    result = subprocess.run(
        ["yosys", "-p", commands],
        cwd=work_dir,                # run inside the design's folder
        capture_output=True,         # grab the output instead of printing it
        text=True                    # return output as a string, not bytes
    )
    return result.stdout + result.stderr


def get_cell_count(output):
    """Find the 'N cells' line in Yosys output and return N as an integer."""
    # look for a line like "    20 cells"
    match = re.search(r"^\s*(\d+)\s+cells", output, re.MULTILINE)
    return int(match.group(1)) if match else None


def get_logic_depth(output):
    """Find the 'length=N' from the longest topological path."""
    # look for "Longest topological path in <name> (length=9):"
    match = re.search(r"length=(\d+)", output)
    return int(match.group(1)) if match else None


def main():
    rows = []

    for folder, vfile, top in DESIGNS:
        design_path = os.path.join(RTL_DIR, folder)
        print(f"Processing {top} ...")

        # --- area: run synth + stat ---
        area_out = run_yosys(f"read_verilog {vfile}; synth -top {top}; stat", design_path)
        cells = get_cell_count(area_out)

        # --- timing: run synth + abc + ltp ---
        depth_out = run_yosys(f"read_verilog {vfile}; synth -top {top}; abc; ltp", design_path)
        depth = get_logic_depth(depth_out)

        print(f"   cells = {cells},  logic_depth = {depth}")
        rows.append({"design": top, "cell_count": cells, "logic_depth": depth})

    # --- write everything to CSV ---
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["design", "cell_count", "logic_depth"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
