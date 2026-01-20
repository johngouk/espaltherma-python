"""Modbus TCP bridge for Daikin Altherma using DaikinSerial.

This module implements a minimal Modbus TCP *slave/server* on MicroPython
which forwards Modbus read requests to a Daikin Altherma heat pump via the
proprietary serial protocol handled by :class:`DaikinSerial`.

Design
======

- The ESP32 runs this server and exposes a Modbus TCP slave (default unit ID 1).
- A Modbus master connects over TCP (port 502 by default) and sends requests.
- We currently support **function code 3 (Read Holding Registers)**.
- The Modbus starting register address is interpreted directly as the Daikin
  ``reg_id`` (0-255).
- For each request we read that Daikin registry once via
  ``DaikinSerial.query_registry(reg_id)`` and map up to the requested
  number of Modbus registers (2 * quantity bytes) from the returned
  payload, padding with zeros if the payload is shorter than requested.

This is intentionally minimal and meant as a starting point. It can be
extended later to:

- Support reading multiple Daikin values per registry and mapping them into
  consecutive Modbus registers.
- Support additional Modbus function codes (e.g. FC4 for input registers).
- Implement caching or rate limiting for Daikin serial traffic.

Example usage on ESP32 / MicroPython::

    import network
    from machine import UART, Pin

    from daikin_serial import DaikinSerial
    from daikin_modbus_tcp_bridge import DaikinModbusTCPBridge
    from daikin_converters import DaikinConverter

    # Bring up Wi-Fi and get local IP (not shown here)
    # ...

    # Configure UART connected to Daikin service port
    uart = UART(1, baudrate=9600, bits=8, parity=UART.EVEN, stop=1,
                tx=Pin(17), rx=Pin(16))

    # Configure Daikin protocol once for this heat pump ("I" or "S")
    daikin = DaikinSerial(uart, protocol="I")

    # Load model-specific label definitions
    converter = DaikinConverter.from_json_file(
        "altherma_ebla_edla_d_9_16_monobloc.json"
    )

    # Start Modbus TCP bridge on all interfaces, port 502, unit ID 1
    bridge = DaikinModbusTCPBridge(
        daikin,
        converter=converter,
        unit_id=1,
        host="0.0.0.0",
        port=502,
    )
    bridge.serve_forever()

"""

from __future__ import annotations

try:
    import usocket as socket  # MicroPython
except ImportError:  # pragma: no cover - CPython fallback for local testing
    import socket  # type: ignore[assignment]

from daikin_serial import DaikinSerial, DaikinSerialError
from daikin_converters import DaikinConverter


class ModbusServerError(Exception):
    """Base exception for bridge/server errors."""


class DaikinModbusTCPBridge:
    """Bridge Modbus TCP requests to a DaikinSerial instance.

    Parameters
    ----------
    daikin:
        An initialized :class:`DaikinSerial` instance, configured with the
        correct UART and protocol ("I" or "S").
    unit_id:
        Modbus unit identifier (slave ID). Most masters use 1 by default.
    host:
        Local IP address to bind to (default ``"0.0.0.0"``).
    port:
        TCP port to listen on (default 502).
    converter:
        A :class:`DaikinConverter` instance constructed with the appropriate
        model JSON definition. This bridge *requires* a converter and will
        raise if one is not supplied.
    logger:
        Optional callable taking a single string for debug logging.
        Defaults to ``print``. Pass ``False`` to disable logging.

    Limitations
    -----------
    - Only Modbus function code 3 (Read Holding Registers) is supported.
    - Each Modbus holding register address encodes a Daikin
      ``(registry_id, offset)`` pair as ``(registry_id << 8) | offset``.
      The bridge reads each referenced Daikin registry once per request and
      uses :class:`DaikinConverter` to extract and scale the value.
    - No write functions are implemented; unsupported functions return a
      Modbus exception response (ILLEGAL FUNCTION).
    """

    def __init__(self, daikin: DaikinSerial, converter: DaikinConverter,
                 unit_id: int = 1, host: str = "0.0.0.0", port: int = 502,
                 logger=None) -> None:
        self.daikin = daikin
        self.converter = converter
        self.unit_id = int(unit_id) & 0xFF
        self.host = host
        self.port = int(port)

        if logger is None:
            self._log = print
        elif logger is False:
            self._log = lambda *args, **kwargs: None
        else:
            self._log = logger

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def serve_forever(self) -> None:
        """Block and serve Modbus TCP requests indefinitely."""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except Exception:
                # Not all MicroPython ports support all socket options
                pass

            s.bind((self.host, self.port))
            s.listen(1)
            self._log(
                "Daikin Modbus TCP bridge listening on %s:%d (unit_id=%d)"
                % (self.host, self.port, self.unit_id)
            )

            while True:
                conn, addr = s.accept()
                self._log("Accepted connection from %s:%d" % addr)
                try:
                    self._handle_client(conn)
                except Exception as exc:  # pragma: no cover - defensive
                    self._log("Client handler error: %r" % exc)
                finally:
                    try:
                        conn.close()
                    except Exception:
                        pass
                    self._log("Connection closed from %s:%d" % addr)
        finally:  # pragma: no cover - best-effort cleanup
            try:
                s.close()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _handle_client(self, conn) -> None:
        """Handle all requests from a single TCP client connection."""

        # Simple loop: read one Modbus TCP ADU at a time
        while True:
            req = conn.recv(260)
            if not req:
                break  # client closed connection

            if len(req) < 8:
                # Not even a full MBAP header; ignore
                continue

            # Parse MBAP header
            trans_id = (req[0] << 8) | req[1]
            proto_id = (req[2] << 8) | req[3]
            length = (req[4] << 8) | req[5]
            unit_id = req[6]

            if proto_id != 0:
                # Not Modbus protocol; ignore
                continue

            # Length includes Unit ID + PDU bytes; must be >= 2
            if length < 2:
                continue

            # Ensure we have the full PDU
            pdu_len = length - 1
            if len(req) < 7 + pdu_len:
                # Incomplete frame; ignore or break
                continue

            pdu = req[7:7 + pdu_len]
            func_code = pdu[0]

            if unit_id != self.unit_id:
                # Not addressed to us; ignore silently
                continue

            if func_code == 3:  # Read Holding Registers
                resp_pdu = self._handle_read_holding_registers(pdu)
            else:
                # Illegal function
                resp_pdu = bytes([func_code | 0x80, 0x01])  # ILLEGAL FUNCTION

            # Build response MBAP header
            resp_length = len(resp_pdu) + 1  # unit_id + PDU
            resp_mbap = bytes([
                (trans_id >> 8) & 0xFF,
                trans_id & 0xFF,
                0x00, 0x00,  # protocol id = 0
                (resp_length >> 8) & 0xFF,
                resp_length & 0xFF,
                self.unit_id,
            ])

            try:
                conn.send(resp_mbap + resp_pdu)
            except Exception as exc:
                self._log("Send error: %r" % exc)
                break

    def _handle_read_holding_registers(self, pdu: bytes) -> bytes:
        """Handle Modbus function 3 (Read Holding Registers).

        Request PDU format::

            byte 0: function code (0x03)
            byte 1-2: starting address (big-endian)
            byte 3-4: quantity of registers to read (big-endian)

        Response PDU format::

            byte 0: function code (0x03)
            byte 1: byte count (N * 2)
            byte 2..: N registers, each 2 bytes big-endian

        Mapping strategy
        ----------------
        - Each Modbus holding register address is treated as a packed
          ``(registry_id << 8) | offset`` value.
        - For all addresses in the requested range we group by ``registry_id``,
          read each referenced Daikin registry once via
          :meth:`DaikinSerial.query_registry`, and then call
          :meth:`DaikinConverter.convert_field` with ``(registry_id, offset, payload)``.
        - The first 16-bit register returned by the converter for each
          ``(registry_id, offset)`` is used as the Modbus holding register
          value; if the field is unknown or out of range, 0 is returned.
        """

        if len(pdu) < 5:
            # Malformed -> exception: ILLEGAL DATA VALUE
            return bytes([0x83, 0x03])

        start_addr = (pdu[1] << 8) | pdu[2]
        quantity = (pdu[3] << 8) | pdu[4]

        if quantity <= 0 or quantity > 125:
            # Modbus spec limit for FC3
            return bytes([0x83, 0x03])  # ILLEGAL DATA VALUE

        # Packed (registry_id << 8) | offset addressing using DaikinConverter
        regs = []  # type: list[int]
        payload_cache = {}  # type: dict[int, bytes]
        for i in range(quantity):
            addr = (start_addr + i) & 0xFFFF
            registry_id = (addr >> 8) & 0xFF
            offset = addr & 0xFF

            if registry_id not in payload_cache:
                try:
                    payload_cache[registry_id] = self._read_daikin_payload(registry_id)
                except DaikinSerialError as exc:
                    self._log("Daikin error on reg 0x%02X: %r" % (registry_id, exc))
                    # Map to Modbus ILLEGAL DATA ADDRESS
                    return bytes([0x83, 0x02])
                except Exception as exc:  # pragma: no cover - defensive
                    self._log("Unexpected error on reg 0x%02X: %r" % (registry_id, exc))
                    return bytes([0x83, 0x04])  # SLAVE DEVICE FAILURE

            payload = payload_cache[registry_id]

            try:
                field_regs = self.converter.convert_field(  # type: ignore[attr-defined]
                    registry_id, offset, payload
                )
            except Exception as exc:  # pragma: no cover - defensive
                self._log(
                    "Converter error for reg 0x%02X offset 0x%02X: %r"
                    % (registry_id, offset, exc)
                )
                regs.append(0)
                continue

            if not field_regs:
                regs.append(0)
            else:
                regs.append(int(field_regs[0]) & 0xFFFF)

        # Build response PDU
        byte_count = len(regs) * 2
        resp = bytearray(2 + byte_count)
        resp[0] = 0x03
        resp[1] = byte_count

        idx = 2
        for value in regs:
            resp[idx] = (value >> 8) & 0xFF
            resp[idx + 1] = value & 0xFF
            idx += 2

        return bytes(resp)

    # ------------------------------------------------------------------
    # Daikin mapping helpers
    # ------------------------------------------------------------------

    def _read_daikin_payload(self, reg_id: int) -> bytes:
        """Query Daikin registry and return its payload bytes.

        This delegates to :meth:`DaikinSerial.query_registry`, which returns
        protocol-independent payload bytes (header and CRC already stripped).
        """

        payload = self.daikin.query_registry(reg_id)

        if payload is None:
            raise DaikinSerialError("No payload returned for reg 0x%02X" % reg_id)

        return bytes(payload)
