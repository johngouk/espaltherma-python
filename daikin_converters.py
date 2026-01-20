"""Daikin registry value converters (Python port of include/converters.h).

Usage
=====

Given:
- ``payload``: bytes from ``DaikinSerial.query_registry(reg_id)``
- ``offset``: byte offset of this value inside the payload
- ``data_size``: number of bytes for this value (LabelDef.dataSize)
- ``conv_id``: LabelDef.convid

Call::

    raw = payload[offset:offset + data_size]
    regs = convert_raw_value(conv_id, raw)

``regs`` is a list of 16-bit big-endian integers suitable to be used as
Modbus holding registers.

Numeric values are still scaled using the same logic as
``include/converters.h`` (e.g. temperature scaling, pressure-to-temperature
mapping). Converters which originally mapped values to literal strings now
return the underlying raw value encoded into registers, except for ON/OFF
cases, which are represented as ``0x0001`` (ON) and ``0x0000`` (OFF).
"""

from __future__ import annotations

import struct

try:  # MicroPython compatibility
    import ujson as json  # type: ignore[import]
except ImportError:  # pragma: no cover - CPython fallback
    import json  # type: ignore[assignment]


def convert_press_to_temp(data: float) -> float:
    """Polynomial pressure->temperature conversion for R32.

    Direct port of Converter::convertPress2Temp.
    """

    num = -2.6989493795556e-07 * data ** 6
    num2 = 4.26383417104661e-05 * data ** 5
    num3 = -2.62978346547749e-03 * data ** 4
    num4 = 8.05858127503585e-02 * data ** 3
    num5 = -1.31924457284073e00 * data ** 2
    num6 = 1.34157368435437e01 * data
    num7 = -5.11813342993155e01
    return num + num2 + num3 + num4 + num5 + num6 + num7


def get_unsigned_value(data: bytes, cnvflg: int) -> int:
    """Port of Converter::getUnsignedValue (for up to 2 bytes)."""

    data_size = len(data)
    if data_size == 0:
        return 0
    if data_size == 1:
        return data[0]
    # data_size >= 2
    b0, b1 = data[0], data[1]
    if cnvflg == 0:
        # little-endian: low, high
        return (b1 << 8) | b0
    else:
        # big-endian: high, low
        return (b0 << 8) | b1


def get_signed_value(data: bytes, cnvflg: int) -> int:
    """Port of Converter::getSignedValue (two's-complement)."""

    num = get_unsigned_value(data, cnvflg)
    if num & 0x8000:
        num = (~num & 0xFFFF) + 1
        return -num
    return num


def _convert_table300_flag(data: bytes, table_id: int) -> bool:
    """Return True/False for ON/OFF (Table 300..307)."""

    bit_index = table_id % 10
    mask = 1 << bit_index
    return (data[0] & mask) > 0


def _convert_table203(data: bytes) -> int:
    """Return the raw status code for table 203.

    The original C++ mapped 0..3 to strings (Normal/Error/Warning/Caution).
    For Modbus purposes we keep the underlying numeric code.
    """

    return data[0] & 0xFF


def _convert_table204(data: bytes) -> int:
    """Return the raw packed code used by table 204.

    The C++ version mapped this to a two-character code. Here we simply
    keep the packed byte value for Modbus transport.
    """

    return data[0] & 0xFF


def _convert_table312(data: bytes) -> float:
    upper = (data[0] >> 4) & 0x07
    lower = data[0] & 0x0F
    val = (upper + lower) / 16.0
    if data[0] & 0x80:
        val *= -1.0
    return val


def _convert_table315(data: bytes) -> int:
    """Return the raw mode code (upper nibble) for table 315."""

    return (data[0] & 0xF0) >> 4


def _convert_table316(data: bytes) -> int:
    """Return the raw mode code (upper nibble) for table 316."""

    return (data[0] & 0xF0) >> 4


def _convert_table200_flag(data: bytes) -> bool:
    """Return True/False for ON/OFF (table 200)."""

    return data[0] != 0


def _convert_table217(data: bytes) -> int:
    """Return the raw operating mode code for table 217."""

    return data[0] & 0xFF


def _bytes_to_registers(data: bytes) -> list[int]:
    """Map raw bytes to 16-bit big-endian register values.

    - Every pair of bytes becomes one register: (hi << 8) | lo.
    - A trailing single byte becomes one register 0x00XX.
    """

    regs: list[int] = []
    length = len(data)
    i = 0
    while i + 1 < length:
        hi = data[i]
        lo = data[i + 1]
        regs.append((hi << 8) | lo)
        i += 2
    if i < length:
        regs.append(data[i] & 0xFF)
    return regs


def convert_raw_value(conv_id: int, data: bytes) -> list[int]:
    """Convert raw registry bytes to *register values*.

    This function keeps the scaling and mapping rules from
    ``include/converters.h`` but expresses the result as 16-bit
    big-endian integers suitable for Modbus holding registers.

    Behaviour overview
    ------------------
    - Numeric converters (most 100/150/400-series IDs, plus 312) compute the
      same physical value as the C++ code and then pack it into a 32-bit
      IEEE-754 float, returned as two 16-bit registers (high word first).
    - Converters which originally mapped values to strings (e.g. 203, 204,
      217, 215, 216, 315, 316, 100) now return the underlying raw codes,
      encoded into 16-bit registers via :func:`_bytes_to_registers`.
    - ON/OFF style converters (200 and 300..307, plus the OFF case of 211)
      return a single register: 0x0001 for ON and 0x0000 for OFF.

    Parameters
    ----------
    conv_id : int
        The converter ID from LabelDef.convid.
    data : bytes
        Raw bytes for this value (already sliced from the registry payload).

    Returns
    -------
    list[int]
        One or more 16-bit big-endian register values.
    """

    # Ensure at least two bytes available for index access
    b = list(data) + [0, 0]
    d0, d1 = b[0], b[1]

    # ------------------------------------------------------------------
    # Boolean / string-like converters
    # ------------------------------------------------------------------

    # convId 200: simple ON/OFF
    if conv_id == 200:
        return [0x0001] if _convert_table200_flag(data) else [0x0000]

    # convId 300-307: bit flags -> ON/OFF
    if conv_id in (300, 301, 302, 303, 304, 305, 306, 307):
        on = _convert_table300_flag(data, conv_id)
        return [0x0001] if on else [0x0000]

    # convId 211: OFF or numeric byte
    if conv_id == 211:
        if d0 == 0:
            return [0x0000]
        # non-zero -> treat as underlying numeric code
        return _bytes_to_registers(bytes([d0]))

    # Pure string mappings: keep underlying raw codes
    if conv_id in (203, 204, 217, 315, 316, 100):
        # 203/204/217/315/316/100 were originally mapped to text; we now
        # just expose their raw codes/bytes.
        if conv_id == 203:
            return _bytes_to_registers(bytes([_convert_table203(data)]))
        if conv_id == 204:
            return _bytes_to_registers(bytes([_convert_table204(data)]))
        if conv_id == 217:
            return _bytes_to_registers(bytes([_convert_table217(data)]))
        if conv_id == 315:
            return _bytes_to_registers(bytes([_convert_table315(data)]))
        if conv_id == 316:
            return _bytes_to_registers(bytes([_convert_table316(data)]))
        # conv_id == 100: raw character bytes
        return _bytes_to_registers(data)

    # convId 215/216: combine upper and lower nibbles into 16 bits
    # high nibble -> high 8 bits, low nibble -> low 8 bits.
    if conv_id in (215, 216):
        high_nibble = (d0 >> 4) & 0x0F
        low_nibble = d0 & 0x0F
        value = (high_nibble << 8) | low_nibble
        return [value]

    # ------------------------------------------------------------------
    # Numeric converters (use original scaling, then pack as float32)
    # ------------------------------------------------------------------

    dbl = None  # numeric result, if any

    # 100-series: signed conversions (except 100 which was handled above)
    if conv_id == 101:
        dbl = float(get_signed_value(data, 0))
    elif conv_id == 102:
        dbl = float(get_signed_value(data, 1))
    elif conv_id == 103:
        dbl = float(get_signed_value(data, 0)) / 256.0
    elif conv_id == 104:
        dbl = float(get_signed_value(data, 1)) / 256.0
    elif conv_id == 105:
        dbl = float(get_signed_value(data, 0)) * 0.1
    elif conv_id == 106:
        dbl = float(get_signed_value(data, 1)) * 0.1
    elif conv_id == 107:
        dbl = float(get_signed_value(data, 0)) * 0.1
    elif conv_id == 108:
        dbl = float(get_signed_value(data, 1)) * 0.1
    elif conv_id == 109:
        dbl = float(get_signed_value(data, 0)) / 256.0 * 2.0
    elif conv_id == 110:
        dbl = float(get_signed_value(data, 1)) / 256.0 * 2.0
    elif conv_id == 111:
        dbl = float(get_signed_value(data, 1)) * 0.5
    elif conv_id == 112:
        dbl = float(get_signed_value(data, 1) - 64) * 0.5
    elif conv_id == 113:
        dbl = float(get_signed_value(data, 1)) * 0.25
    elif conv_id == 114:
        num2 = (d1 << 8) | d0
        if d1 & 0x80:
            num2 = (~(num2 - 1)) & 0xFFFF
        dbl = ((num2 & 0xFF00) >> 8) + (num2 & 0xFF) / 256.0
        dbl *= 10.0
        if d1 & 0x80:
            dbl *= -1.0
    elif conv_id == 115:
        dbl = float(get_signed_value(data, 0)) / 2560.0
    elif conv_id == 116:
        dbl = float(get_signed_value(data, 1)) / 2560.0
    elif conv_id == 117:
        dbl = float(get_signed_value(data, 0)) * 0.01
    elif conv_id == 118:
        dbl = float(get_signed_value(data, 1)) * 0.01
    elif conv_id == 119:
        num3 = (d1 << 8) | (d0 & 0x7F)
        dbl = ((num3 & 0xFF00) >> 8) + (num3 & 0xFF) / 256.0

    # 150-series: unsigned conversions
    elif conv_id == 151:
        dbl = float(get_unsigned_value(data, 0))
    elif conv_id == 152:
        dbl = float(get_unsigned_value(data, 1))
    elif conv_id == 153:
        dbl = float(get_unsigned_value(data, 0)) / 256.0
    elif conv_id == 154:
        dbl = float(get_unsigned_value(data, 1)) / 256.0
    elif conv_id == 155:
        dbl = float(get_unsigned_value(data, 0)) * 0.1
    elif conv_id == 156:
        dbl = float(get_unsigned_value(data, 1)) * 0.1
    elif conv_id == 157:
        dbl = float(get_unsigned_value(data, 0)) / 256.0 * 2.0
    elif conv_id == 158:
        dbl = float(get_unsigned_value(data, 1)) / 256.0 * 2.0
    elif conv_id == 161:
        dbl = float(get_unsigned_value(data, 1)) * 0.5
    elif conv_id == 162:
        dbl = float(get_unsigned_value(data, 1) - 64) * 0.5
    elif conv_id == 163:
        dbl = float(get_unsigned_value(data, 1)) * 0.25
    elif conv_id == 164:
        dbl = float(get_unsigned_value(data, 1)) * 5.0
    elif conv_id == 165:
        dbl = float(get_unsigned_value(data, 0) & 0x3FFF)

    # 312: special numeric mapping
    elif conv_id == 312:
        dbl = _convert_table312(data)

    # 401-406: pressure -> temperature
    elif conv_id == 401:
        dbl = float(get_signed_value(data, 0))
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 402:
        dbl = float(get_signed_value(data, 1))
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 403:
        dbl = float(get_signedValue(data, 0)) / 256.0
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 404:
        dbl = float(get_signedValue(data, 1)) / 256.0
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 405:
        dbl = float(get_signed_value(data, 0)) * 0.1
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 406:
        dbl = float(get_signed_value(data, 1)) * 0.1
        dbl = convert_press_to_temp(dbl)

    else:
        # Unknown or unsupported convId: fall back to raw bytes
        return _bytes_to_registers(data)

    if dbl is None:
        # Should not happen, but fall back to raw bytes defensively
        return _bytes_to_registers(data)

    # Pack the numeric value as an IEEE-754 32-bit float and return
    # it as two 16-bit big-endian registers.
    hi, lo = struct.unpack("!HH", struct.pack("!f", float(dbl)))
    return [hi, lo]


class DaikinConverter:
    """Lookup and convert Daikin values by ``(registry_id, offset)``.

    This class is a thin helper around :func:`convert_raw_value` which
    understands the JSON label definition format generated from the original
    C++ ``LabelDef`` tables.

    Typical usage
    -------------
    >>> converter = DaikinConverter.from_json_file("altherma_ebla_edla_d_9_16_monobloc.json")
    >>> payload = daikin.query_registry(reg_id)
    >>> regs = converter.convert_field(reg_id, offset, payload)
    """

    def __init__(self, label_defs) -> None:
        """Construct from an iterable of label definition mappings.

        ``label_defs`` is usually the result of ``json.load(...)`` on the
        model JSON file. Only entries with a positive ``data_size`` are
        registered; entries like "NextDataGrid" (``data_size == 0``) are
        ignored.
        """

        mapping = {}
        for entry in label_defs or []:
            try:
                reg_id = int(entry["registry_id"]) & 0xFF
                offset = int(entry["offset"]) & 0xFF
                conv_id = int(entry["conv_id"])
                data_size = int(entry.get("data_size", 0))
            except (KeyError, TypeError, ValueError):
                continue

            if data_size <= 0:
                # Skip markers / non-data rows
                continue

            mapping[(reg_id, offset)] = (conv_id, data_size)

        self._mapping = mapping

    @classmethod
    def from_json_file(cls, path: str) -> "DaikinConverter":
        """Load label definitions from a JSON file and build a converter."""

        with open(path, "r") as f:
            label_defs = json.load(f)
        return cls(label_defs)

    def has_field(self, registry_id: int, offset: int) -> bool:
        """Return True if we have metadata for this (registry, offset)."""

        key = (int(registry_id) & 0xFF, int(offset) & 0xFF)
        return key in self._mapping

    def convert_field(self, registry_id: int, offset: int, payload: bytes) -> list[int]:
        """Convert the value at ``(registry_id, offset)`` in *payload*.

        If no matching label definition exists, we fall back to exposing a
        single raw byte at ``offset`` (if available) as a 16-bit register.
        """

        reg_id = int(registry_id) & 0xFF
        off = int(offset) & 0xFF
        key = (reg_id, off)

        meta = self._mapping.get(key)

        if meta is None:
            # Unknown field: expose a single raw byte (if present)
            if off >= len(payload):
                return []
            raw = payload[off:off + 1]
            # conv_id 0 is not special; convert_raw_value will fall back
            # to _bytes_to_registers(data) and return 0x00XX.
            return convert_raw_value(0, raw)

        conv_id, data_size = meta
        end = off + data_size

        if end > len(payload):
            if off >= len(payload):
                return []
            raw = payload[off:]
        else:
            raw = payload[off:end]

        return convert_raw_value(conv_id, raw)
