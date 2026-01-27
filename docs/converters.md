# ESPAltherma Converter IDs (`include/converters.h`)

This document describes how each converter ID (`convId`) in `include/converters.h` interprets the raw bytes from a Daikin registry and turns them into a human‑readable value (`def->asString`).

Unless otherwise noted:

- `data` is the raw byte slice for the field.
- `num` is `def->dataSize` (number of bytes).
- `getSignedValue(data, num, cnvflg)` reads a 1–2 byte **signed** integer (cnvflg controls endianness).
- `getUnsignedValue(data, num, cnvflg)` reads a 1–2 byte **unsigned** integer.

At the end of `convert()`, if `dblData` is set, it is formatted with `sprintf(def->asString, "%g", dblData)`.

---

## 100 – Raw ASCII text

- Behavior:
  - Appends the raw bytes directly to `asString`:
    - `strlcat(def->asString, (char*)data, num);`
- Intended for simple ASCII strings or identifiers.

---

## 101–119: Signed numeric scalings

All of these start from a signed integer via `getSignedValue(data, num, cnvflg)` and then apply a scale.

### 101 – Signed integer (LSB-first)

- `dblData = getSignedValue(data, num, 0);`
- No scaling, little-endian for 2‑byte values.

### 102 – Signed integer (MSB-first)

- `dblData = getSignedValue(data, num, 1);`
- No scaling, big-endian for 2‑byte values.

### 103 – Signed / 256.0 (LSB-first)

- `dblData = getSignedValue(data, num, 0) / 256.0;`
- Typically fixed‑point with 1/256 resolution.

### 104 – Signed / 256.0 (MSB-first)

- `dblData = getSignedValue(data, num, 1) / 256.0;`

### 105 – Signed × 0.1 (LSB-first)

- `dblData = getSignedValue(data, num, 0) * 0.1;`
- Used frequently for temperatures/pressures with 0.1 units.

### 106 – Signed × 0.1 (MSB-first)

- `dblData = getSignedValue(data, num, 1) * 0.1;`

### 107 – Signed × 0.1, with "---" sentinel (LSB-first)

- `dblData = getSignedValue(data, num, 0) * 0.1;`
- If `dblData == -3276.8`, output `"---"` and return.
- Special "invalid / not available" sentinel.

### 108 – Signed × 0.1, with "---" sentinel (MSB-first)

- Same as 107 but big-endian: `getSignedValue(..., 1)`.

### 109 – Signed / 256 × 2.0 (LSB-first)

- `dblData = getSignedValue(data, num, 0) / 256.0 * 2.0;`

### 110 – Signed / 256 × 2.0 (MSB-first)

- `dblData = getSignedValue(data, num, 1) / 256.0 * 2.0;`

### 111 – Signed × 0.5 (MSB-first)

- `dblData = getSignedValue(data, num, 1) * 0.5;`

### 112 – (Signed − 64) × 0.5 (MSB-first)

- `dblData = (getSignedValue(data, num, 1) - 64) * 0.5;`
- Offset + scale; often a centered quantity.

### 113 – Signed × 0.25 (MSB-first)

- `dblData = getSignedValue(data, num, 1) * 0.25;`

### 114 – Custom 2‑byte signed fixed‑point with sentinel

- Special handling for a 2‑byte signed value with fractional part:
  - If `data[0] == 0` and `data[1] == 128`, output `"---"` and return.
  - Construct a signed 16‑bit `num2` from `[data[1], data[0]]` (big‑endian).
  - If sign bit set, compute two’s complement.
  - Integer part from high 8 bits; fraction from low 8 bits / 256.
  - `dblData = value * 10.0`.
- Used for high‑resolution temperatures.

### 115 – Signed / 2560.0 (LSB-first)

- `dblData = getSignedValue(data, num, 0) / 2560.0;`

### 116 – Signed / 2560.0 (MSB-first)

- `dblData = getSignedValue(data, num, 1) / 2560.0;`

### 117 – Signed × 0.01 (LSB-first)

- `dblData = getSignedValue(data, num, 0) * 0.01;`

### 118 – Signed × 0.01 (MSB-first)

- `dblData = getSignedValue(data, num, 1) * 0.01;`

### 119 – Special 2‑byte signed fixed‑point without sentinel

- If `data[0] == 0` and `data[1] == 128`, output `"---"` and return.
- Construct `num3` from `[data[1], data[0] & 0x7F]`:
  - High 8 bits = integer part, low 8 bits / 256 = fraction.
- `dblData` is that combined value (no extra ×10, unlike 114).

---

## 151–158: Unsigned numeric scalings

Same pattern as 101–118, but using `getUnsignedValue`.

### 151 – Unsigned int (LSB-first)

- `dblData = getUnsignedValue(data, num, 0);`

### 152 – Unsigned int (MSB-first)

- `dblData = getUnsignedValue(data, num, 1);`

### 153 – Unsigned / 256.0 (LSB-first)

- `dblData = getUnsignedValue(data, num, 0) / 256.0;`

### 154 – Unsigned / 256.0 (MSB-first)

- `dblData = getUnsignedValue(data, num, 1) / 256.0;`

### 155 – Unsigned × 0.1 (LSB-first)

- `dblData = getUnsignedValue(data, num, 0) * 0.1;`

### 156 – Unsigned × 0.1 (MSB-first)

- `dblData = getUnsignedValue(data, num, 1) * 0.1;`

### 157 – Unsigned / 256 × 2.0 (LSB-first)

- `dblData = getUnsignedValue(data, num, 0) / 256.0 * 2.0;`

### 158 – Unsigned / 256 × 2.0 (MSB-first)

- `dblData = getUnsignedValue(data, num, 1) / 256.0 * 2.0;`

---

## 161–165: Additional unsigned helpers

### 161 – Unsigned × 0.5 (MSB-first)

- `dblData = getUnsignedValue(data, num, 1) * 0.5;`

### 162 – (Unsigned − 64) × 0.5 (MSB-first)

- `dblData = (getUnsignedValue(data, num, 1) - 64) * 0.5;`

### 163 – Unsigned × 0.25 (MSB-first)

- `dblData = getUnsignedValue(data, num, 1) * 0.25;`

### 164 – Unsigned × 5 (MSB-first)

- `dblData = getUnsignedValue(data, num, 1) * 5;`

### 165 – Unsigned & 0x3FFF (mask)

- `dblData = (getUnsignedValue(data, num, 0) & 0x3FFF);`
- Masks off the top two bits.

---

## 200 – Simple ON/OFF (byte)

- Uses `convertTable200(data, asString)`:
  - `data[0] == 0` → `"OFF"`
  - `data[0] != 0` → `"ON"`

---

## 201 & 217 – Mode string table

- `201` falls through into the `217` handler.
- Both call `convertTable217(data, asString)`:
  - Looks up `data[0]` in a fixed table of strings (e.g. `"Fan Only"`, `"Heating"`, `"Cooling"`, `"Auto"`, `"DHW"`, `"Cooling Storage"`, `"UseStrdThrm(ht)4"`, etc.).
  - Writes the selected mode name into `asString`.

---

## 203 – Error type: Normal/Error/Warning/Caution

- Uses `convertTable203(data, asString)`:
  - `0` → `"Normal"`
  - `1` → `"Error"`
  - `2` → `"Warning"`
  - `3` → `"Caution"`
  - Other → `"-"`.

---

## 204 – Error code (two-character code)

- Uses `convertTable204(data, asString)`:
  - Interprets high and low nibbles of `data[0]`.
  - Maps via two lookup arrays to generate a 2‑character code:
    - `ret[0]` from `" ACEHFJLPU987654"` (high nibble)
    - `ret[1]` from `"0123456789AHCJEF"` (low nibble)
  - `ret[2] = 0` (null terminator).

---

## 211 – Special thermostat/integer

- If `data == 0` (pointer check in the code, but intended logic is likely `data[0] == 0`):
  - Output `"OFF"`.
- Else:
  - `dblData = (uint)data[0];`
  - Numeric 0–255 value.

---

## 215 & 216 – Packed nibbles as hex string

- Both handled identically:
  - `num = data[0] >> 4` (high nibble).
  - `num2 = data[0] & 0x0F` (low nibble).
  - `sprintf(def->asString, "{0:X}{1:X}", num, num2);`
- Intention: encode two 4‑bit codes as a 2‑digit hex‑style text (though the actual `sprintf` format is a bit odd in the C++ shown).

---

## 300–307 – Bit flags (ON/OFF)

- Group of converters that all go via `convertTable300(data, convId, asString)`.
- `convertTable300`:
  - Computes a bit mask based on the table ID (`convId`), using `tableID % 10`.
  - Tests `data[0] & mask`:
    - If non‑zero → `"ON"`.
    - Else → `"OFF"`.
- These are designed for individual bits packed into a single status byte.

---

## 312 – Signed nibble‑based fractional value

- Uses `convertTable312(data)`:
  - `dblData = ((7 & data[0] >> 4) + (15U & data[0])) / 16.0;`
  - If bit 7 set (`0x80`), `dblData *= -1.0;`
- Returns a small signed fractional value (resolution 1/16).

---

## 315 – Indoor operation mode (coarse)

- Uses `convertTable315(data, asString)`:
  - Extracts upper nibble of `data[0]`:
    - `0` → `"Stop"`
    - `1` → `"Heating"`
    - `2` → `"Cooling"`
    - `3` → `"??"`
    - `4` → `"DHW"`
    - `5` → `"Heating + DHW"`
    - `6` → `"Cooling + DHW"`
    - default → `"-"`.

---

## 316 – System type (H/P vs Hybrid vs Boiler)

- Uses `convertTable316(data, asString)`:
  - Upper nibble of `data[0]`:
    - `0` → `"H/P only"`
    - `1` → `"Hybrid"`
    - `2` → `"Boiler only"`
    - default → `"Unknown"`.

---

## 401–406 – Pressure to temperature (R32) conversions

These are all intended to take a pressure in various numeric formats, then convert that pressure to a temperature using `convertPress2Temp()`.

`convertPress2Temp(double data)` applies a 6th‑order polynomial (for R32 refrigerant):

```c
T = a6*p^6 + a5*p^5 + a4*p^4 + a3*p^3 + a2*p^2 + a1*p + a0
```

Where `p` is the pressure in some engineering units (depends on conv).

For each ID:

- **401**  
  - `dblData = getSignedValue(data, num, 0);`  
  - `dblData = convertPress2Temp(dblData);`

- **402**  
  - `dblData = getSignedValue(data, num, 1);`  
  - `dblData = convertPress2Temp(dblData);`

- **403**  
  - `dblData = getSignedValue(data, num, 0) / 256.0;`  
  - `dblData = convertPress2Temp(dblData);`

- **404**  
  - `dblData = getSignedValue(data, num, 1) / 256.0;`  
  - `dblData = convertPress2Temp(dblData);`

- **405**  
  - `dblData = getSignedValue(data, num, 0) * 0.1;`  
  - `dblData = convertPress2Temp(dblData);`

- **406**  
  - `dblData = getSignedValue(data, num, 1) * 0.1;`  
  - `dblData = convertPress2Temp(dblData);`

(Implementation detail: the C++ `switch` is missing `break;`s between these cases, so in the raw code they technically fall through; conceptually, each ID is “pressure in X numeric format → temperature via polynomial.”)

---

## Default / Unknown converters

- If none of the `case` labels match `convId`, or after the 401–406 fall‑through, the `default` case runs:
  - `sprintf(def->asString, "Conv %d not avail.", convId);`
- This indicates an unsupported or unimplemented converter ID.
