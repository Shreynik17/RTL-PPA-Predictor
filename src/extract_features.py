#!/usr/bin/env python3
"""
extract_features.py
Reads each RTL design, extracts numeric features describing the
source code, joins them with the synthesis labels from dataset.csv,
and writes the combined table to data/dataset_full.csv.
"""

import re
import csv
import os

DESIGNS = [
    ("mux2to1",      "mux2to1.v",      "mux2to1"),
    ("adder4",       "adder4.v",       "adder4"),
    ("comparator4",  "comparator4.v",  "comparator4"),
    ("alu4",         "alu4.v",         "alu4"),
    ("counter4",     "counter4.v",     "counter4"),
    ("shift_reg4",   "shift_reg4.v",   "shift_reg4"),
    ("seq_detector", "seq_detector.v", "seq_detector"),
]

RTL_DIR    = "rtl"
LABELS_CSV = "data/dataset.csv"
OUTPUT_CSV = "data/dataset_full.csv"


def strip_comments(text):
    """Remove /* block */ and // line comments so they don't pollute parsing."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", " ", text)
    return text


def count_ports(text, keyword):
    """Count ports of a direction (input/output), total bits, and widest bus."""
    n_ports = 0
    n_bits  = 0
    max_w   = 0
    for line in text.splitlines():
        line = line.strip().rstrip(",").rstrip(";").strip()
        m = re.match(rf"{keyword}\b\s*(?:wire|reg)?\s*(?:\[(\d+):(\d+)\])?\s*(.+)", line)
        if m:
            width = 1
            if m.group(1) is not None:
                hi, lo = int(m.group(1)), int(m.group(2))
                width = abs(hi - lo) + 1
            names = [x for x in m.group(3).split(",") if x.strip()]
            n_ports += len(names)
            n_bits  += width * len(names)
            max_w    = max(max_w, width)
    return n_ports, n_bits, max_w


def extract_features(vpath):
    with open(vpath) as f:
        code = strip_comments(f.read())

    loc = len([ln for ln in code.splitlines() if ln.strip()])

    n_in,  in_bits,  in_maxw  = count_ports(code, "input")
    n_out, out_bits, out_maxw = count_ports(code, "output")
    max_width = max(in_maxw, out_maxw, 1)

    n_assign = len(re.findall(r"\bassign\b", code))
    n_always = len(re.findall(r"\balways\b", code))
    n_case   = len(re.findall(r"\bcase\b",   code))
    is_seq   = 1 if re.search(r"\bposedge\b", code) else 0

    body = re.sub(r"<=", " ", code)   # drop non-blocking arrows before counting ops
    operators = re.findall(r"<<|>>|==|!=|>=|&&|\|\||[+\-&|\^~<>?]", body)
    n_operators = len(operators)

    return {
        "loc": loc,
        "n_inputs": n_in,
        "n_outputs": n_out,
        "total_input_bits": in_bits,
        "total_output_bits": out_bits,
        "max_width": max_width,
        "n_assign": n_assign,
        "n_always": n_always,
        "n_case": n_case,
        "is_sequential": is_seq,
        "n_operators": n_operators,
    }


def load_labels():
    labels = {}
    with open(LABELS_CSV) as f:
        for row in csv.DictReader(f):
            labels[row["design"]] = (row["cell_count"], row["logic_depth"])
    return labels


def main():
    labels = load_labels()
    feature_names = ["loc", "n_inputs", "n_outputs", "total_input_bits",
                     "total_output_bits", "max_width", "n_assign", "n_always",
                     "n_case", "is_sequential", "n_operators"]
    fieldnames = ["design"] + feature_names + ["cell_count", "logic_depth"]

    rows = []
    for folder, vfile, top in DESIGNS:
        vpath = os.path.join(RTL_DIR, folder, vfile)
        feats = extract_features(vpath)
        cells, depth = labels.get(top, ("", ""))
        rows.append({"design": top, **feats, "cell_count": cells, "logic_depth": depth})
        print(f"{top:14s} loc={feats['loc']:2d} in={feats['n_inputs']} out={feats['n_outputs']} "
              f"bits={feats['total_input_bits']:2d} ops={feats['n_operators']:2d} "
              f"seq={feats['is_sequential']} always={feats['n_always']}  ->  cells={cells}, depth={depth}")

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Wrote {len(rows)} rows x {len(fieldnames)} columns to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
