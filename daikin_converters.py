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
    text = convert_raw_value(conv_id, raw)

``text`` will match what the C++ ``Converter::convert()`` writes into
``def->asString`` for the corresponding ``LabelDef``.
"""

from __future__ import annotations


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


def _convert_table300(data: bytes, table_id: int) -> str:
    """Binary flag to ON/OFF (Table 300..307)."""

    bit_index = table_id % 10
    mask = 1 << bit_index
    return "ON" if (data[0] & mask) > 0 else "OFF"


def _convert_table203(data: bytes) -> str:
    v = data[0]
    if v == 0:
        return "Normal"
    if v == 1:
        return "Error"
    if v == 2:
        return "Warning"
    if v == 3:
        return "Caution"
    return "-"


def _convert_table204(data: bytes) -> str:
    array1 = " ACEHFJLPU987654"
    array2 = "0123456789AHCJEF"
    num = (data[0] >> 4) & 0x0F
    num2 = data[0] & 0x0F
    c1 = array1[num] if 0 <= num < len(array1) else " "
    c2 = array2[num2] if 0 <= num2 < len(array2) else " "
    return c1 + c2


def _convert_table312(data: bytes) -> float:
    upper = (data[0] >> 4) & 0x07
    lower = data[0] & 0x0F
    val = (upper + lower) / 16.0
    if data[0] & 0x80:
        val *= -1.0
    return val


def _convert_table315(data: bytes) -> str:
    mode = (data[0] & 0xF0) >> 4
    if mode == 0:
        return "Stop"
    if mode == 1:
        return "Heating"
    if mode == 2:
        return "Cooling"
    if mode == 3:
        return "??"
    if mode == 4:
        return "DHW"
    if mode == 5:
        return "Heating + DHW"
    if mode == 6:
        return "Cooling + DHW"
    return "-"


def _convert_table316(data: bytes) -> str:
    mode = (data[0] & 0xF0) >> 4
    if mode == 0:
        return "H/P only"
    if mode == 1:
        return "Hybrid"
    if mode == 2:
        return "Boiler only"
    return "Unknown"


def _convert_table200(data: bytes) -> str:
    return "OFF" if data[0] == 0 else "ON"


def _convert_table217(data: bytes) -> str:
    r217 = [
        "Fan Only",
        "Heating",
        "Cooling",
        "Auto",
        "Ventilation",
        "Auto Cool",
        "Auto Heat",
        "Dry",
        "Aux.",
        "Cooling Storage",
        "Heating Storage",
        "UseStrdThrm(cl)1",
        "UseStrdThrm(cl)2",
        "UseStrdThrm(cl)3",
        "UseStrdThrm(cl)4",
        "UseStrdThrm(ht)1",
        "UseStrdThrm(ht)2",
        "UseStrdThrm(ht)3",
        "UseStrdThrm(ht)4",
    ]
    idx = data[0]
    if 0 <= idx < len(r217):
        return r217[idx]
    return "-"


def convert_raw_value(conv_id: int, data: bytes) -> str:
    """Convert raw registry bytes to a human-readable string.

    This is a Python port of Converter::convert for a single LabelDef,
    where ``data`` is the slice starting at that label's offset and
    ``len(data) == dataSize``.

    Parameters
    ----------
    conv_id : int
        The converter ID from LabelDef.convid.
    data : bytes
        Raw bytes for this value (already sliced from the registry payload).

    Returns
    -------
    str
        Textual representation matching the C++ implementation.
    """

    dbl = None  # numeric result, if any

    def _return_no_data() -> str:
        return "---"

    # Ensure at least two bytes available for index access
    b = list(data) + [0, 0]
    d0, d1 = b[0], b[1]

    # 100-series: signed conversions
    if conv_id == 100:
        return bytes(data).decode(errors="ignore")
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
        if dbl == -3276.8:
            return _return_no_data()
    elif conv_id == 108:
        dbl = float(get_signed_value(data, 1)) * 0.1
        if dbl == -3276.8:
            return _return_no_data()
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
        if d0 == 0 and d1 == 128:
            return _return_no_data()
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
        if d0 == 0 and d1 == 128:
            return _return_no_data()
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

    # 200/203/204/217/300/312/315/316 tables
    elif conv_id == 200:
        return _convert_table200(data)
    elif conv_id == 203:
        return _convert_table203(data)
    elif conv_id == 204:
        return _convert_table204(data)
    elif conv_id in (201, 217):
        return _convert_table217(data)
    elif conv_id in (300, 301, 302, 303, 304, 305, 306, 307):
        return _convert_table300(data, conv_id)
    elif conv_id == 312:
        dbl = _convert_table312(data)
    elif conv_id == 315:
        return _convert_table315(data)
    elif conv_id == 316:
        return _convert_table316(data)

    # 211: "OFF" or numeric
    elif conv_id == 211:
        if d0 == 0:
            return "OFF"
        else:
            dbl = float(d0)

    # 215/216: split into two nibbles and format as "{0:x}{1:y}"
    elif conv_id in (215, 216):
        num_high = d0 >> 4
        num_low = d0 & 0x0F
        return "{0:%d}{1:%d}" % (num_high, num_low)

    # 401-406: pressure -> temperature
    elif conv_id == 401:
        dbl = float(get_signed_value(data, 0))
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 402:
        dbl = float(get_signed_value(data, 1))
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 403:
        dbl = float(get_signed_value(data, 0)) / 256.0
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 404:
        dbl = float(get_signed_value(data, 1)) / 256.0
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 405:
        dbl = float(get_signed_value(data, 0)) * 0.1
        dbl = convert_press_to_temp(dbl)
    elif conv_id == 406:
        dbl = float(get_signed_value(data, 1)) * 0.1
        dbl = convert_press_to_temp(dbl)

    else:
        return "Conv %d not avail." % conv_id

    if dbl is None:
        return "Conv %d not avail." % conv_id
    return ("%g" % dbl)
