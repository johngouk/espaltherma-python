# Converter Functions Used by `altherma_ebla_edla_d_9_16_monobloc.json`

This document lists each distinct `conv_id` value referenced in `altherma_ebla_edla_d_9_16_monobloc.json` and summarises what the original C++ `Converter::convert` logic in `include/converters.h` does for that ID.

| conv_id | Description (from `include/converters.h`) |
| --- | --- |
| 101 | Interprets the field as a signed value via `getSignedValue(data, size, 0)` (little‑endian if 2 bytes), no additional scaling. |
| 105 | Signed value via `getSignedValue(data, size, 0)` multiplied by `0.1` (typically a temperature or similar in 0.1‑unit resolution). |
| 114 | Two‑byte signed special: decodes sign and 1/256 fractional part, multiplies by `10.0`; `0x00 0x80` is treated as “no data” and displayed as `---`. |
| 118 | Signed value via `getSignedValue(data, size, 1)` (big‑endian if 2 bytes) multiplied by `0.01` (centi‑unit resolution). |
| 119 | Two‑byte special: masks off the sign bit, then combines integer and 1/256 fractional part into a floating value; `0x00 0x80` is treated as “no data” (`---`). |
| 151 | Unsigned value via `getUnsignedValue(data, size, 0)` (little‑endian if 2 bytes), no scaling. |
| 152 | Unsigned value via `getUnsignedValue(data, size, 1)` (big‑endian if 2 bytes), no scaling. |
| 161 | Unsigned value via `getUnsignedValue(data, size, 1)` multiplied by `0.5` (half‑unit steps). |
| 203 | Uses `convertTable203`: maps a status byte `0..3` to text `Normal / Error / Warning / Caution` (anything else to `-`). |
| 204 | Uses `convertTable204`: splits a packed byte into two nibbles and maps them through lookup tables to form a 2‑character code (e.g. error/detail code). |
| 211 | If the first byte is `0`, writes `"OFF"`; otherwise treats the byte as a numeric value (no scaling) and formats it as a number. |
| 214 | No explicit case in `Converter::convert`; falls through to the default handler and reports `"Conv 214 not avail."`. |
| 215 | Nibble code: takes high and low nibbles of the byte and formats them as two decimal digits via `sprintf`, representing parts of an EEPROM/model code. |
| 217 | Uses `convertTable217`: interprets the byte as an index into a mode string table (e.g. `Fan Only`, `Heating`, `Cooling`, `Auto`, `DHW`, etc.). |
| 219 | No explicit case in `Converter::convert`; falls through to the default handler and reports `"Conv 219 not avail."`. |
| 300 | Uses `convertTable300`: inspects a specific bit (based on table ID) in the status byte and outputs `"ON"` if set, `"OFF"` if clear. |
| 301 | Same as 300, using `convertTable300` with a different bit position determined by the table ID. |
| 302 | Same as 300, using `convertTable300` with its own bit position. |
| 303 | Same as 300, using `convertTable300` with its own bit position. |
| 304 | Same as 300, using `convertTable300` with its own bit position. |
| 305 | Same as 300, using `convertTable300` with its own bit position. |
| 306 | Same as 300, using `convertTable300` with its own bit position. |
| 307 | Same as 300, using `convertTable300` with its own bit position. |
| 310 | No explicit case in `Converter::convert`; falls through to the default handler and reports `"Conv 310 not avail."`. |
| 311 | No explicit case in `Converter::convert`; falls through to the default handler and reports `"Conv 311 not avail."`. |
| 315 | Uses `convertTable315`: decodes the upper nibble of the byte as an operating mode (`Stop`, `Heating`, `Cooling`, `DHW`, `Heating + DHW`, `Cooling + DHW`, or `-`). |
| 316 | Uses `convertTable316`: decodes the upper nibble as a hybrid mode (`H/P only`, `Hybrid`, `Boiler only`, or `Unknown`). |
| 405 | Pressure‑to‑temperature: interprets the field via `getSignedValue(data, size, 0)` (or `1` for related IDs), applies a scale (here `* 0.1`), then passes the result to `convertPress2Temp` (R32 pressure→temperature polynomial). |
| 802 | No explicit case in `Converter::convert`; used as a marker (e.g. refrigerant type) and reported as `"Conv 802 not avail."` by the default handler. |
| 995 | No explicit case in `Converter::convert`; used as a structural marker like `NextDataGrid`, reported as `"Conv 995 not avail."`. |
| 998 | No explicit case in `Converter::convert`; used as a structural marker like `In-Out separator`, reported as `"Conv 998 not avail."`. |
