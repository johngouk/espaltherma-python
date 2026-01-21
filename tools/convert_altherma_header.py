"""Convert Daikin Altherma C++ labelDefs header to a Python tuple module.

This script parses `include/def/Altherma(EBLA-EDLA D series 9-16kW Monobloc).h`
(labelDefs array) and emits a Python file with a `LABEL_DEFS` list of tuples:

    (registry_id, offset, conv_id, data_size, data_type, label)

Commented-out rows in the C++ header are **included** as well; the leading
`//` is ignored, and labels are taken verbatim.

The output is written to a *temporary* filename so as not to overwrite the
existing `altherma_ebla_edla_d_9_16_monobloc.py` file.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "include" / "def" / "Altherma(EBLA-EDLA D series 9-16kW Monobloc).h"
OUT_PY = ROOT / "altherma_ebla_edla_d_9_16_monobloc_generated.py"

# C++ row pattern, e.g.:
#   {0x20,0,105,2,1,"Outdoor air temp.(R1T)"},
# or commented:
#   //{0x00,0,802,0,-1,"*Refrigerant type"},
ROW_RE = re.compile(
    r"^\s*//?\{\s*"  # optional leading // then '{'
    r"([^}]*)"         # inner comma-separated fields
    r"\}\s*,?"        # closing '}' and optional comma
)


def parse_row(line: str):
    """Parse a single labelDefs row line into its components.

    Returns (registry_id, offset, conv_id, data_size, data_type, label) or
    None if the line does not look like a row.
    """

    m = ROW_RE.match(line)
    if not m:
        return None

    inner = m.group(1)
    # Split top-level by commas; there are exactly 6 fields
    parts = [p.strip() for p in inner.split(",")]
    if len(parts) != 6:
        return None

    reg_str, off_str, conv_str, size_str, dtype_str, label_str = parts

    def parse_int(s: str) -> int:
        s = s.strip()
        # Handles hex (0xNN) and decimal
        try:
            return int(s, 0)
        except ValueError:
            return 0

    registry_id = parse_int(reg_str)
    offset = parse_int(off_str)
    conv_id = parse_int(conv_str)
    data_size = parse_int(size_str)
    data_type = parse_int(dtype_str)

    # label_str is a C string literal, e.g. "Outdoor air temp.(R1T)"
    # Strip surrounding quotes and unescape simple sequences.
    label = label_str.strip()
    if label.startswith('"') and label.endswith('"'):
        label = label[1:-1]
    label = label.replace('\\"', '"')

    return registry_id, offset, conv_id, data_size, data_type, label


def convert_header_to_python(header: Path, out_path: Path) -> None:
    rows = []
    for line in header.read_text(encoding="utf-8").splitlines():
        parsed = parse_row(line)
        if parsed is None:
            continue
        rows.append(parsed)

    lines = []
    lines.append("# Auto-generated from %s" % header.name)
    lines.append("# DO NOT EDIT BY HAND" )
    lines.append("")
    lines.append("LABEL_DEFS = [")
    for reg, off, conv, size, dtype, label in rows:
        # Represent registry_id and offset as integers (no hex) for simplicity.
        lines.append(
            "    (%d, %d, %d, %d, %d, %r)," % (reg, off, conv, size, dtype, label)
        )
    lines.append("]")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not HEADER.exists():
        raise SystemExit(f"Header not found: {HEADER}")

    if OUT_PY.exists():
        print(f"NOTE: {OUT_PY.name} already exists and will be overwritten.")

    convert_header_to_python(HEADER, OUT_PY)
    print(f"Wrote {OUT_PY}")


if __name__ == "__main__":
    main()
