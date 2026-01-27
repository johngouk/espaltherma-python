#!/usr/bin/env python3

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEF_DIR = ROOT / "include" / "def"
OUTPUT_MD = ROOT / "docs" / "model_conversions.md"
OUTPUT_TABLE_MD = ROOT / "docs" / "model_conversions_table.md"
OUTPUT_GROUPS_TABLE_MD = ROOT / "docs" / "model_groups_conversions_table.md"

# Match LabelDef-style lines starting with '{...'
LINE_RE = re.compile(r"^\s*\{(.*)\}\s*,?\s*$")


def parse_int(token: str) -> int:
    token = token.strip()
    if token.lower().startswith("0x"):
        return int(token, 16)
    return int(token)


def normalise_model_label(filename: str) -> str:
    """Short, human-facing model label from header filename.

    - Drop trailing .h
    - Strip any case-insensitive "altherma"
    - Collapse whitespace
    """
    name = filename
    if name.lower().endswith(".h"):
        name = name[:-2]
    lower = name.lower()
    out = []
    i = 0
    while i < len(name):
        if lower.startswith("altherma", i):
            i += len("altherma")
            continue
        out.append(name[i])
        i += 1
    cleaned = "".join(out)
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def collect_model_conversions():
    """Return mapping: model_filename -> sorted list of conv IDs used."""
    per_model: dict[str, set[int]] = {}

    for path in sorted(DEF_DIR.glob("*.h")):
        # Skip generic/protocol definitions
        if path.name in {"DEFAULT.h", "PROTOCOL_S.h", "PROTOCOL_S_ROTEX.h"}:
            continue

        conv_ids: set[int] = per_model.setdefault(path.name, set())

        text = path.read_text(encoding="utf-8", errors="ignore")
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            # Allow commented-out entries starting with //{
            if line.startswith("//"):
                stripped = line[2:].lstrip()
            else:
                stripped = line
            if not stripped.startswith("{"):
                continue
            m = LINE_RE.match(stripped)
            if not m:
                continue
            body = m.group(1)
            parts = [p.strip() for p in body.split(",")]
            if len(parts) < 3:
                continue
            # parts: registry, offset, convId, dataSize, ...
            conv_str = parts[2]
            try:
                conv_id = parse_int(conv_str)
            except ValueError:
                continue
            conv_ids.add(conv_id)

    # Sort converter IDs for each model
    ordered: dict[str, list[int]] = {}
    for fname, ids in per_model.items():
        ordered[fname] = sorted(ids)
    return ordered


def ensure_docs_dir():
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)


def write_markdown(per_model_convs: dict[str, list[int]]):
    ensure_docs_dir()

    model_names = sorted(per_model_convs.keys())

    lines: list[str] = []
    lines.append("# Model Converter Usage")
    lines.append("")
    lines.append("This document lists, for each model-specific header in `include/def`, the set of converter IDs (`convId`) referenced in its `LabelDef` entries (including commented-out ones).")
    lines.append("")

    for fname in model_names:
        convs = per_model_convs[fname]
        if not convs:
            continue
        label = normalise_model_label(fname) or fname
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"*Header file:* `{fname}`")
        lines.append("")
        # Simple ordered list of conv IDs
        lines.append("Converters used (sorted):")
        lines.append("")
        line = ", ".join(str(c) for c in convs)
        lines.append(f"`{line}`")
        lines.append("")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_table_markdown(per_model_convs: dict[str, list[int]]):
    """Write a matrix-style table: rows=models, columns=convIds, cells=X if used."""
    ensure_docs_dir()

    model_names = sorted(per_model_convs.keys())

    # Collect global sorted list of unique convIds
    all_conv_ids: list[int] = sorted({cid for ids in per_model_convs.values() for cid in ids})

    lines: list[str] = []
    lines.append("# Model Converter Usage (Table)")
    lines.append("")
    lines.append("Rows are models, columns are converter IDs (`convId`). `X` indicates that the converter is referenced in that model's header (commented or uncommented).")
    lines.append("")

    # Header row
    header_cells = ["Model"] + [str(cid) for cid in all_conv_ids]
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")

    # Data rows
    for fname in model_names:
        convs = set(per_model_convs[fname])
        label = normalise_model_label(fname) or fname
        row = [label]
        for cid in all_conv_ids:
            row.append("X" if cid in convs else "")
        lines.append("| " + " | ".join(row) + " |")

    OUTPUT_TABLE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_grouped_table_markdown(per_model_convs: dict[str, list[int]]):
    """Write a table grouping models that share the exact same convId set.

    Rows are groups (with list of models); columns are convIds; cells show X if
    that convId is in the group's shared set (by construction, all models in
    a group share the same pattern).
    """
    ensure_docs_dir()

    # Build groups keyed by frozenset of convIds
    groups: dict[frozenset[int], list[str]] = {}
    for fname, ids in per_model_convs.items():
        key = frozenset(ids)
        groups.setdefault(key, []).append(fname)

    # Sort group keys by size then lexicographically
    sorted_keys = sorted(groups.keys(), key=lambda k: (len(k), sorted(k)))

    # Global list of all convIds used anywhere
    all_conv_ids: list[int] = sorted({cid for ids in per_model_convs.values() for cid in ids})

    lines: list[str] = []
    lines.append("# Model Groups by Converter Set (Table)")
    lines.append("")
    lines.append("Each row represents a group of models that use the **exact same set** of converter IDs (`convId`). Columns are convIds; `X` marks membership in the shared set.")
    lines.append("")

    # Header row
    header_cells = ["Group", "Models"] + [str(cid) for cid in all_conv_ids]
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")

    # Data rows
    for idx, key in enumerate(sorted_keys, start=1):
        model_fnames = sorted(groups[key])
        model_labels = [normalise_model_label(f) or f for f in model_fnames]
        group_name = f"G{idx}"
        models_cell = ", ".join(model_labels)
        convs = set(key)
        row = [group_name, models_cell]
        for cid in all_conv_ids:
            row.append("X" if cid in convs else "")
        lines.append("| " + " | ".join(row) + " |")

    OUTPUT_GROUPS_TABLE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    per_model_convs = collect_model_conversions()
    write_markdown(per_model_convs)
    write_table_markdown(per_model_convs)
    write_grouped_table_markdown(per_model_convs)
    print(f"Analysed {len(per_model_convs)} model header files.")
    total_convs = sum(len(v) for v in per_model_convs.values())
    print(f"Total model/conv entries: {total_convs}")
    print(f"Wrote {OUTPUT_MD}, {OUTPUT_TABLE_MD} and {OUTPUT_GROUPS_TABLE_MD}")
