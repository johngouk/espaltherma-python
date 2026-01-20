"""Micropython driver for Daikin Altherma serial (I/S) protocol.

This is a Python translation of the core serial communication logic
from ESPAltherma's `include/comm.h` and the protocol description in
`doc/Daikin I protocol.md` and `doc/Daikin S protocol.md`.

It is intended to run on an ESP32 using MicroPython and a UART
connected to the Daikin Altherma heat pump service port.

The driver focuses on:

* Building request frames for I and S protocols
* Reading replies with timeout
* Handling dynamic reply length for I protocol
* Detecting common error replies (0x15 0xEA)
* Verifying the Sum-and-Invert CRC
* Normalising replies so that callers always get protocol-independent
  registry payload bytes

Example (ESP32 / MicroPython):

    from machine import UART, Pin
    from daikin_serial import DaikinSerial

    # Adjust uart_id / pins to your board wiring
    uart = UART(1, baudrate=9600, bits=8, parity=UART.EVEN, stop=1,
                tx=Pin(17), rx=Pin(16))

    # Configure protocol once for this heat pump ("I" or "S")
    daikin = DaikinSerial(uart, protocol="I")

    # Read registry 0x60 using the configured protocol
    payload = daikin.query_registry(0x60)
    # `payload` contains only the registry content bytes (no header/CRC).

"""

from __future__ import annotations

try:
    import utime as _time  # MicroPython
except ImportError:  # CPython fallback for testing
    import time as _time


class DaikinSerialError(Exception):
    """Base exception for Daikin serial driver errors."""


class DaikinTimeoutError(DaikinSerialError):
    """Raised when no or incomplete reply is received within the timeout."""


class DaikinCRCError(DaikinSerialError):
    """Raised when a reply has an invalid CRC."""


class DaikinProtocolError(DaikinSerialError):
    """Raised for protocol-level errors returned by the heat pump."""


def _ticks_ms():
    """Return milliseconds since boot (MicroPython-compatible)."""

    # MicroPython "utime" exposes ticks_ms; CPython does not.
    if hasattr(_time, "ticks_ms"):
        return _time.ticks_ms()  # type: ignore[attr-defined]
    # Fallback for normal Python (for local testing)
    return int(_time.time() * 1000)


def _ticks_diff(later, earlier):
    """Return later - earlier in ms, handling wraparound if using ticks_ms."""

    if hasattr(_time, "ticks_diff"):
        return _time.ticks_diff(later, earlier)  # type: ignore[attr-defined]
    return later - earlier


def sum_and_invert(data):
    """Compute Daikin "SumAndInvert" checksum (same as getCRC in comm.h).

    This is: (~sum(data)) & 0xFF.
    """

    total = 0
    for b in data:
        total = (total + b) & 0xFF
    return (~total) & 0xFF


class DaikinSerial:
    """Low-level Daikin Altherma serial protocol driver.

    Parameters
    ----------
    uart:
        A configured UART-like object with ``read``, ``write`` and ``any``
        methods (e.g. ``machine.UART`` on MicroPython).
    protocol:
        Either ``"I"`` (default) or ``"S"``. The heat pump supports only
        one of these; configure it here once.
    timeout_ms:
        Maximum time to wait for a complete reply (default: 300 ms,
        matching ``SER_TIMEOUT`` in the C++ code).
    logger:
        Optional callable taking a single string for debug logging.
        Defaults to ``print``. Pass ``False`` to disable logging.
    """

    def __init__(self, uart, protocol="I", timeout_ms=300, logger=None):
        protocol = (protocol or "I").upper()
        if protocol not in ("I", "S"):
            raise ValueError("protocol must be 'I' or 'S'")

        self.uart = uart
        self.protocol = protocol
        self.timeout_ms = int(timeout_ms)

        if logger is None:
            self._log = print
        elif logger is False:
            # Small convenience: logger=False disables logging entirely
            self._log = lambda *args, **kwargs: None
        else:
            self._log = logger

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def query_registry(self, reg_id):
        """Query a single registry and return its *payload bytes*.

        This wraps the low-level I/S protocols and always returns only the
        registry payload, independent of the protocol variant used by the
        heat pump.

        For both protocol I and S, the returned value is the sequence of bytes
        that represent the registry content, with the protocol-specific
        header and trailing CRC removed.

        Parameters
        ----------
        reg_id:
            Registry identifier (0-255).

        Returns
        -------
        bytes
            Registry payload bytes, without header/CRC, same layout for
            both protocol I and S.

        Raises
        ------
        DaikinTimeoutError
            If no or incomplete reply is received within the timeout.
        DaikinProtocolError
            If the heat pump returns an explicit error frame (0x15 0xEA).
        DaikinCRCError
            If the CRC of the reply is invalid.
        DaikinSerialError
            If the decoded registry ID in the response does not match the
            requested one.
        """

        cmd = self._build_command(reg_id)
        self._log("Querying register 0x%02X..." % reg_id)

        # Flush any pending data from UART RX buffer (equivalent to
        # MySerial.flush(SERIAL_FLUSH_TX_ONLY) + discard input).
        try:
            if hasattr(self.uart, "read"):
                # Read and discard whatever is waiting
                any_fn = getattr(self.uart, "any", None)
                if any_fn is not None:
                    while any_fn():
                        # Limit each read to avoid blocking too long
                        self.uart.read(32)
            # Some UART drivers have flush; if present, call it.
            if hasattr(self.uart, "flush"):
                self.uart.flush()
        except Exception:
            # Be robust to UART implementations that don't support all ops
            pass

        # Send command
        self.uart.write(cmd)

        # Read reply
        expected_len = self._initial_reply_len(reg_id)
        deadline = _ticks_ms() + self.timeout_ms

        buf = bytearray()
        error_checked = False

        any_fn = getattr(self.uart, "any", None)

        while len(buf) < expected_len and _ticks_diff(deadline, _ticks_ms()) > 0:
            if any_fn is None or not any_fn():
                # Small sleep to avoid tight loop on some ports
                continue

            chunk = self.uart.read(1)
            if not chunk:
                continue
            buf.extend(chunk)

            # Dynamic length handling for I protocol once 3 bytes read
            if self.protocol == "I" and len(buf) == 3:
                # Length field is at index 2 and does not include
                # the initial 3 bytes (see Daikin I protocol doc).
                length_field = buf[2]
                expected_len = length_field + 2

            # Common error reply for both protocols: 0x15 0xEA
            if not error_checked and len(buf) >= 2:
                if buf[0] == 0x15 and buf[1] == 0xEA:
                    self._log("Error 0x15 0xEA returned from HP")
                    raise DaikinProtocolError("HP returned error 0x15 0xEA")
                error_checked = True

        # Timeout / incomplete reply
        if len(buf) == 0:
            self._log("Time out! Check connection")
            raise DaikinTimeoutError("No reply from heat pump")
        if len(buf) < expected_len:
            self._log(
                "ERR: Time out on register 0x%02X! got %d/%d bytes" %
                (reg_id, len(buf), expected_len)
            )
            self._log(self._format_buffer(buf))
            raise DaikinTimeoutError(
                "Incomplete reply: got %d of %d bytes" % (len(buf), expected_len)
            )

        self._log(self._format_buffer(buf))

        # CRC check: last byte is CRC over all previous bytes
        calc_crc = sum_and_invert(buf[:-1])
        if calc_crc != buf[-1]:
            self._log(
                "ERROR: Wrong CRC on register 0x%02X. Calculated 0x%02X but got 0x%02X" %
                (reg_id, calc_crc, buf[-1])
            )
            self._log("Buffer: " + self._format_buffer(buf))
            raise DaikinCRCError(
                "CRC mismatch: calc=0x%02X, recv=0x%02X" % (calc_crc, buf[-1])
            )

        # At this point we have a valid frame; normalize it to payload only.
        proto = self.protocol
        if proto == "I":
            # I-protocol frame:
            #   [0] = 0x40
            #   [1] = reg_id
            #   [2] = payload length (number of bytes after this one, up to CRC)
            #   [3..N-2] = payload
            #   [N-1] = CRC
            if buf[1] != (reg_id & 0xFF):
                raise DaikinSerialError(
                    "Registry ID mismatch in I frame: expected 0x%02X, got 0x%02X"
                    % (reg_id, buf[1])
                )
            payload = buf[3:-1]
        else:  # "S"
            # S-protocol frame:
            #   [0] = reg_id
            #   [1..N-2] = payload
            #   [N-1] = CRC
            if buf[0] != (reg_id & 0xFF):
                raise DaikinSerialError(
                    "Registry ID mismatch in S frame: expected 0x%02X, got 0x%02X"
                    % (reg_id, buf[0])
                )
            payload = buf[1:-1]

        self._log(".. CRC OK! Payload length=%d" % len(payload))
        return bytes(payload)

    # ------------------------------------------------------------------
    # Helpers mirroring the C++ implementation
    # ------------------------------------------------------------------

    def _initial_reply_len(self, reg_id):
        """Return initial reply length guess.

        For I protocol this is a conservative minimum (12 bytes), and the
        actual length is overridden when the 3rd byte is received.

        For S protocol this mirrors the hard-coded lengths in the C++ code
        (see ``get_reply_len`` in ``include/comm.h`` and
        ``doc/Daikin S protocol.md``).
        """

        if self.protocol == "I":
            return 12

        # Protocol S: hard-coded by registry
        if reg_id == 0x50:
            return 6
        if reg_id == 0x56:
            return 4
        # All other known S registries (0x53, 0x54, 0x55) use 18 bytes
        return 18

    @staticmethod
    def _format_buffer(buf):
        """Return a hex-formatted string similar to logBuffer in C++."""

        return " ".join("0x%02X" % b for b in buf)

    def _build_command(self, reg_id):
        """Build command frame for a given registry and configured protocol.

        Mirrors the logic in ``queryRegistry`` in ``include/comm.h``.
        """

        reg_id &= 0xFF
        if self.protocol == "I":
            # 03 40 REG CRC
            cmd = bytearray(4)
            cmd[0] = 0x03
            cmd[1] = 0x40
            cmd[2] = reg_id
            cmd[3] = sum_and_invert(cmd[:3])
            return bytes(cmd)
        else:  # "S"
            # 02 REG CRC
            cmd = bytearray(3)
            cmd[0] = 0x02
            cmd[1] = reg_id
            cmd[2] = sum_and_invert(cmd[:2])
            return bytes(cmd)
