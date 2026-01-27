#!/usr/bin/env python3

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEF_DIR = ROOT / "include" / "def"
OUTPUT_MD = ROOT / "docs" / "all_registers.md"

# Match lines like: {0x20,2,105,2,1,"Label"}
LINE_RE = re.compile(r"^\s*\{\s*(0x[0-9A-Fa-f]+|\d+)\s*,\s*(0x[0-9A-Fa-f]+|\d+)\s*,")


def parse_int(token: str) -> int:
    token = token.strip()
    if token.lower().startswith("0x"):
        return int(token, 16)
    return int(token)


def collect_register_offsets():
    # (registry, offset) -> set of model file basenames
    index: dict[tuple[int, int], set[str]] = {}
    model_files: list[Path] = []

    for path in sorted(DEF_DIR.glob("*.h")):
        # Treat the clearly generic/protocol files as non-model-specific.
        if path.name in {"DEFAULT.h", "PROTOCOL_S.h", "PROTOCOL_S_ROTEX.h"}:
            continue
        model_files.append(path)
        model_name = path.name

        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            # Allow commented-out LabelDef entries (lines starting with "//{...")
            if line.startswith("//"):
                stripped = line[2:].lstrip()
            else:
                stripped = line
            m = LINE_RE.match(stripped)
            if not m:
                continue
            reg_str, off_str = m.groups()
            try:
                reg = parse_int(reg_str)
                off = parse_int(off_str)
            except ValueError:
                continue
            key = (reg, off)
            index.setdefault(key, set()).add(model_name)

    # Sort keys by registry then offset, and also sort model lists for stability.
    sorted_pairs = []
    for (reg, off) in sorted(index.keys(), key=lambda ro: (ro[0], ro[1])):
        models = sorted(index[(reg, off)])
        sorted_pairs.append(((reg, off), models))

    return sorted_pairs, model_files


def ensure_docs_dir():
    docs_dir = OUTPUT_MD.parent
    docs_dir.mkdir(parents=True, exist_ok=True)


def _normalise_model_label(filename: str) -> str:
    """Return a short model label from a header filename.

    - Drop the trailing .h
    - Remove any case-insensitive "altherma" tokens
    - Collapse internal whitespace.
    """
    name = filename
    if name.lower().endswith(".h"):
        name = name[:-2]
    # Remove "altherma" (any case) wherever it appears
    lower = name.lower()
    out_chars = []
    i = 0
    while i < len(name):
        if lower.startswith("altherma", i):
            i += len("altherma")
            continue
        out_chars.append(name[i])
        i += 1
    cleaned = "".join(out_chars)
    # Normalise whitespace
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def write_markdown(pairs_with_models, ordered_model_filenames):
    """Write a matrix of (registry, offset) vs models.

    pairs_with_models: [((reg, off), [model_filename, ...]), ...]
    ordered_model_filenames: [model_filename, ...] giving column order.
    """
    ensure_docs_dir()

    # Build header with one column per model (normalised label).
    model_labels = [_normalise_model_label(fn) for fn in ordered_model_filenames]

    lines = []
    lines.append("# Combined Register/Offset Index")
    lines.append("")
    lines.append("This file lists all **unique** `(registry_id, offset)` pairs found across all model-specific `include/def/*.h` files (excluding `DEFAULT.h` and protocol headers), sorted by registry then offset.")
    lines.append("")

    header_cells = ["Registry (hex)", "Offset (hex)"] + model_labels
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")

    for (reg, off), models in pairs_with_models:
        reg_hex = f"0x{reg:02X}"
        off_hex = f"0x{off:02X}"
        present = set(models)
        row = [reg_hex, off_hex]
        for fn in ordered_model_filenames:
            row.append("X" if fn in present else "")
        lines.append("| " + " | ".join(row) + " |")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    pairs_with_models, model_files = collect_register_offsets()
    # Stable column order: sort by filename.
    ordered_model_filenames = sorted({p.name for p in model_files})
    write_markdown(pairs_with_models, ordered_model_filenames)
    print(f"Parsed {len(model_files)} model-specific headers.")
    print(f"Found {len(pairs_with_models)} unique (registry, offset) pairs.")
    print(f"Wrote {OUTPUT_MD}")
