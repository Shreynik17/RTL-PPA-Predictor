#!/usr/bin/env python3
"""
build_dataset.py
Sweeps each parameterized design across multiple bit-widths.
For every (design, width) combo: runs Yosys to get labels
(cell count, logic depth) and extracts RTL features.
Writes the combined table to data/dataset_swept.csv.
"""

import subprocess
import re
import csv
import os

# Parameterized designs: (folder, file, module)
PARAM_DESIGNS = [
    ("adder",      "adder.v",      "adder"),
    ("comparator", "comparator.v", "comparator"),
    ("alu",        "alu.v",        "alu"),
    ("counter",    "counter.v",    "counter"),
    ("shift_reg",  "shift_reg.v",  "shift_reg"),
]

WIDTHS = [2, 4, 8, 16, 32, 64]
PARAM_DIR  = "rtl_param"
OUTPUT_CSV = "data/dataset_swept.csv"


def run_yosys(commands, work_dir):
    result = subprocess.run(
        ["yosys", "-p", commands],
        cwd=work_dir, capture_output=True, text=True
    )
    return result.stdout + result.stderr


def get_cells(output):
    matches = re.findall(r"^\s*(\d+)\s+cells", output, re.MULTILINE)
    return int(matches[-1]) if matches else None   # last 'N cells' line is the final count


def get_depth(output):
    m = re.search(r"length=(\d+)", output)
    return int(m.group(1)) if m else None


def synth_labels(vfile, module, width, work_dir):
    """Synthesize one design at one width, return (cells, depth)."""
    area_cmd  = f"read_verilog {vfile}; chparam -set WIDTH {width} {module}; synth -top {module}; stat"
    depth_cmd = f"read_verilog {vfile}; chparam -set WIDTH {width} {module}; synth -top {module}; abc; ltp"
    cells = get_cells(run_yosys(area_cmd, work_dir))
    depth = get_depth(run_yosys(depth_cmd, work_dir))
    return cells, depth


# --- feature extraction (operates on the RTL text + the chosen width) ---
def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", " ", text)
    return text


def extract_features(vpath, width):
    with open(vpath) as f:
        code = strip_comments(f.read())

    loc       = len([ln for ln in code.splitlines() if ln.strip()])
    n_in      = len(re.findall(r"\binput\b",  code))
    n_out     = len(re.findall(r"\boutput\b", code))
    n_assign  = len(re.findall(r"\bassign\b", code))
    n_always  = len(re.findall(r"\balways\b", code))
    n_case    = len(re.findall(r"\bcase\b",   code))
    is_seq    = 1 if re.search(r"\bposedge\b", code) else 0
    body      = re.sub(r"<=", " ", code)
    n_ops     = len(re.findall(r"<<|>>|==|!=|>=|&&|\|\||[+\-&|\^~<>?]", body))

    return {
        "width": width,
        "loc": loc,
        "n_inputs": n_in,
        "n_outputs": n_out,
        "max_width": width,          # the datapath width = the swept width
        "n_assign": n_assign,
        "n_always": n_always,
        "n_case": n_case,
        "is_sequential": is_seq,
        "n_operators": n_ops,
        "width_x_ops": width * n_ops,   # interaction feature: wide AND op-heavy
    }


def main():
    feature_cols = ["width", "loc", "n_inputs", "n_outputs", "max_width",
                    "n_assign", "n_always", "n_case", "is_sequential",
                    "n_operators", "width_x_ops"]
    fieldnames = ["design"] + feature_cols + ["cell_count", "logic_depth"]

    rows = []
    for folder, vfile, module in PARAM_DESIGNS:
        work_dir = os.path.join(PARAM_DIR, folder)
        vpath    = os.path.join(work_dir, vfile)
        for w in WIDTHS:
            cells, depth = synth_labels(vfile, module, w, work_dir)
            feats = extract_features(vpath, w)
            name = f"{module}{w}"
            rows.append({"design": name, **feats, "cell_count": cells, "logic_depth": depth})
            print(f"{name:14s} width={w:2d} ops={feats['n_operators']:2d} seq={feats['is_sequential']} "
                  f"-> cells={cells:4}, depth={depth}")

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Wrote {len(rows)} rows x {len(fieldnames)} columns to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
