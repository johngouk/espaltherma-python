# WARP Project Guide: espaltherma-python

This repository contains Python tooling to interface with Daikin Altherma heat pumps, mirroring the original ESPAltherma C/C++ implementation. It is used both on MicroPython (ESP32) and on a host PC for development/testing.

## Core Components

### `daikin_serial.py`
- MicroPython-friendly driver for the Daikin Altherma service port.
- Wraps the proprietary Daikin serial protocols ("I" and "S").
- Public contract:
  - `DaikinSerial.query_registry(reg_id: int) -> bytes` returns **payload-only** bytes for the specified registry, independent of protocol variant:
    - Frame headers, protocol markers, and CRC are removed.
    - Returned data is a raw payload buffer that matches the layout assumed by the C++ label/converter tables.

### `daikin_converters.py`
- Python port of `include/converters.h` from ESPAltherma.
- Two main exports:
  - `convert_raw_value(conv_id: int, data: bytes) -> list[int]`
  - `DaikinConverter`

#### `convert_raw_value`
- Input:
  - `conv_id`: the Daikin converter ID from the label definitions.
  - `data`: the raw bytes for a single field (already sliced out of the payload).
- Output:
  - A list of **16‑bit integers** (Modbus holding register values, big-endian words).
- Behaviour:
  - **Numeric converters** (`conv_id` in `101–119, 151–158, 161–165, 312, 401–406`):
    - Compute the same physical value as C++ (`float`), then pack it into **32‑bit IEEE‑754** and return **two registers**: high word, then low word.
  - **Boolean / ON–OFF converters**:
    - `200`, and 300-series bit flags (300–307), plus the OFF case of `211`:
      - Return a single register: `0x0001` for ON/True, `0x0000` for OFF/False.
  - **String-mapped converters** (status/enum-like):
    - For IDs that were text in C++ (e.g. `203`, `204`, `217`, `315`, `316`, `100`), the Python version does **not** return strings.
    - Instead, it returns the underlying raw code(s) encoded into 16‑bit registers, typically one register per source byte.
  - **Special nibble codes `215`/`216`:**
    - C++ concatenates high/low nibbles and formats them as text.
    - Python combines them into a single 16‑bit value: `(high_nibble << 8) | low_nibble` and returns one register.
  - **Unknown/unsupported `conv_id`:**
    - Falls back to packing raw bytes into 16‑bit big-endian registers (last odd byte becomes `0x00XX`).

#### `DaikinConverter`
- Purpose: bridge from the JSON label definition to `convert_raw_value`.
- Construction:
  - `DaikinConverter.from_json_file(path)` loads a JSON file such as `altherma_ebla_edla_d_9_16_monobloc.json`.
  - Internally builds a mapping: `(registry_id, offset) -> (conv_id, data_size)`.
  - Entries with `data_size <= 0` (markers like `NextDataGrid`, `*Refrigerant type`) are ignored.
- Main method:
  - `convert_field(registry_id: int, offset: int, payload: bytes) -> list[int]`:
    - Looks up metadata for `(registry_id, offset)`.
    - Slices the `payload` accordingly (respecting `data_size`, clipping if necessary).
    - Calls `convert_raw_value(conv_id, raw_slice)` and returns its register list.
    - If the field is unknown or out-of-range, returns an empty list; callers typically treat that as `0`.

### `altherma_ebla_edla_d_9_16_monobloc.json`
- JSON translation of the original C++ label definitions for **Altherma EBLA/EDLA D 9–16kW Monobloc**.
- Each entry contains:
  - `registry_id` (0–255)
  - `offset` (byte offset within that registry payload)
  - `conv_id` (converter ID)
  - `data_size` (number of payload bytes for this field)
  - `data_type` (original C++ hint; not critical for Modbus mapping)
  - `label` (human-readable description)

### `altherma_ebla_edla_d_9_16_monobloc_registers.md`
- Pre-generated Modbus map for this specific model.
- For each JSON label row with `data_size > 0` it defines:
  - **Register Address**: `(registry_id << 8) | offset`, shown in hex.
  - **Number of Registers**:
    - `2` if the converter returns a 32‑bit float (same rule as above).
    - `1` otherwise.
  - **Description**: the `label` from JSON.
- This is a convenience document for SCADA/Modbus client configuration.

## Modbus TCP Bridge

### `daikin_modbus_tcp_bridge.py`
- Provides a simple **Modbus TCP slave** that proxies reads to `DaikinSerial`.
- Key class: `DaikinModbusTCPBridge(daikin: DaikinSerial, converter: DaikinConverter, unit_id=1, host="0.0.0.0", port=502, logger=...)`.
- Only **Function Code 3 (Read Holding Registers)** is implemented.

#### Addressing Scheme
- The bridge **requires** a `DaikinConverter`.
- Every Modbus holding register address is treated as a *packed* Daikin selector:
  - `registry_id = (address >> 8) & 0xFF`
  - `offset      = address & 0xFF`
- For a single FC3 request:
  - `start_addr` and `quantity` are decoded from the Modbus PDU.
  - For each `i` in `0 .. quantity-1`:
    - `addr        = (start_addr + i) & 0xFFFF`
    - `registry_id = addr >> 8`
    - `offset      = addr & 0xFF`
- The bridge groups all requested registers by `registry_id`:
  - For each distinct `registry_id` in the request:
    - Calls `DaikinSerial.query_registry(registry_id)` **once** and caches the payload.
  - For each `(registry_id, offset)` pair:
    - Calls `converter.convert_field(registry_id, offset, payload)`.
    - Takes the **first** 16‑bit value if any are returned.
    - If conversion fails or returns an empty list, it returns `0` for that Modbus register.

#### Error Handling
- If `DaikinSerial` reports an error or times out for a registry:
  - Bridge returns Modbus **ILLEGAL DATA ADDRESS (0x02)** for that FC3 request.
- Unexpected internal errors map to **SLAVE DEVICE FAILURE (0x04)**.
- Malformed or out-of-range Modbus requests (e.g. quantity > 125) map to **ILLEGAL DATA VALUE (0x03)**.

## Quick Start for Warp Agents

1. **Need to understand how Modbus addresses map to Daikin data?**  
   - Read `altherma_ebla_edla_d_9_16_monobloc_registers.md` for the packed `(registry_id << 8) | offset` register list.  
   - Use `registry_id = addr >> 8`, `offset = addr & 0xFF` to find the corresponding JSON label row.
2. **Need to see how raw bytes are converted?**  
   - Open `daikin_converters.py` and look at `convert_raw_value` for scaling rules, and `DaikinConverter.convert_field` for how label metadata is applied.
3. **Need to follow the data path end‑to‑end?**  
   - Start in `daikin_modbus_tcp_bridge.py` → `_handle_read_holding_registers` (Modbus request) → `_read_daikin_payload` (serial query) → `DaikinConverter.convert_field` (payload → registers).
4. **Adding support for a new Daikin model?**  
   - Generate a new `*_model.json` label file, then use `DaikinConverter.from_json_file` and a new `*_registers.md` generated with the same rules as the existing one.

## Typical Usage Pattern

### On ESP32 / MicroPython

1. **Create the serial driver**:
   - Configure UART connected to Daikin service port.
   - Instantiate `DaikinSerial(uart, protocol="I" or "S")`.
2. **Load model definition and converter**:
   - `converter = DaikinConverter.from_json_file("altherma_ebla_edla_d_9_16_monobloc.json")`.
3. **Start the Modbus TCP bridge**:
   - `bridge = DaikinModbusTCPBridge(daikin, converter=converter, unit_id=1, host="0.0.0.0", port=502)`.
   - `bridge.serve_forever()`.
4. **Configure the Modbus master** using addresses from `altherma_ebla_edla_d_9_16_monobloc_registers.md`.

## Extending to Other Models

To support a different Daikin model:

1. Generate a new JSON label definition from its C++ header (similar to `altherma_...json`).
2. Place it alongside the existing JSON.
3. Instantiate a new `DaikinConverter` with that file.
4. Use the same `(registry_id << 8) | offset` addressing scheme.
5. Optionally, generate a new `*_registers.md` for that model following the same rules.

## Warp-Specific Notes

- When modifying the bridge:
  - Preserve the packed addressing scheme and the `DaikinConverter` requirement.
  - Do **not** reintroduce legacy passthrough behaviour (raw payload as sequential registers).
- When adding new converters:
  - Keep all outputs as **lists of 16‑bit register values**.
  - Ensure ON/OFF-style fields always map to `0x0001` (ON) and `0x0000` (OFF).
  - For new string/enum fields, prefer returning **numeric codes**, not strings.
- Documentation:
  - Model-specific Modbus maps belong in `*_registers.md` files.
  - Core behaviour and rules for this repo should be kept up to date in this `WARP.md`.
