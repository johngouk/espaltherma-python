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
    pairs: set[tuple[int, int]] = set()
    model_files = []

    for path in sorted(DEF_DIR.glob("*.h")):
        # Treat the clearly generic/protocol files as non-model-specific.
        if path.name in {"DEFAULT.h", "PROTOCOL_S.h", "PROTOCOL_S_ROTEX.h"}:
            continue
        model_files.append(path)

        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            m = LINE_RE.match(line)
            if not m:
                continue
            reg_str, off_str = m.groups()
            try:
                reg = parse_int(reg_str)
                off = parse_int(off_str)
            except ValueError:
                continue
            pairs.add((reg, off))

    return sorted(pairs, key=lambda ro: (ro[0], ro[1])), model_files


def ensure_docs_dir():
    docs_dir = OUTPUT_MD.parent
    docs_dir.mkdir(parents=True, exist_ok=True)


def write_markdown(pairs):
    ensure_docs_dir()

    lines = []
    lines.append("# Combined Register/Offset Index")
    lines.append("")
    lines.append("This file lists all **unique** `(registry_id, offset)` pairs found across all model-specific `include/def/*.h` files (excluding `DEFAULT.h` and protocol headers), sorted by registry then offset.")
    lines.append("")
    lines.append("| Registry (hex) | Offset (hex) | Registry (dec) | Offset (dec) | Packed Address (hex) |")
    lines.append("| -------------- | ----------- | -------------- | ----------- | -------------------- |")

    for reg, off in pairs:
        reg_hex = f"0x{reg:02X}"
        off_hex = f"0x{off:02X}"
        packed = (reg << 8) | off
        packed_hex = f"0x{packed:04X}"
        lines.append(f"| {reg_hex} | {off_hex} | {reg} | {off} | {packed_hex} |")

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    pairs, model_files = collect_register_offsets()
    write_markdown(pairs)
    print(f"Parsed {len(model_files)} model-specific headers.")
    print(f"Found {len(pairs)} unique (registry, offset) pairs.")
    print(f"Wrote {OUTPUT_MD}")
