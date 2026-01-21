# Altherma EBLA/EDLA D 9–16kW Monobloc – Modbus Register Map

This document defines a Modbus register mapping derived from `altherma_ebla_edla_d_9_16_monobloc.json`.

- **Register Address** = `(registry_id << 8) | offset` shown in hex (`0xRRRR`).
- **Number of Registers**:
  - 2 for numeric converters that output a 32‑bit float:  
    `conv_id` in `{101–119, 151–158, 161–165, 312, 401–406}`
  - 1 for all other entries (flags, codes, raw bytes, 215/216 nibble codes, etc.).

Entries with `data_size = 0` (such as `"*Refrigerant type"`) are omitted.

## Modbus Register Map

| Register Address | Number of Registers | Description |
| --- | --- | --- |
| 0x0000 | 2 | Sensor Data Qty |
| 0x0000 | 1 | NextDataGrid |
| 0x0000 | 1 | NextDataGrid |
| 0x0000 | 1 | In-Out separator |
| 0x0001 | 2 | INV compressor Qty |
| 0x0002 | 2 | STD compressor Qty |
| 0x0003 | 2 | Fan Data Qty |
| 0x0004 | 2 | Expansion Valve Data Qty |
| 0x0005 | 2 | 4 Way Valve Data Qty |
| 0x0006 | 2 | Crank Case Heater Qty |
| 0x0007 | 2 | Solenoid valve Qty |
| 0x0008 | 2 | Max. connectable indoor units |
| 0x0009 | 2 | Connected Indoor Unit Qty |
| 0x000A | 2 | O/U MPU ID (xx) |
| 0x000B | 2 | O/U MPU ID (yy) |
| 0x000C | 2 | O/U capacity (kW) |
| 0x1000 | 1 | Operation Mode |
| 0x1001 | 1 | Thermostat ON/OFF |
| 0x1001 | 1 | Restart standby |
| 0x1001 | 1 | Startup Control |
| 0x1001 | 1 | Defrost Operation |
| 0x1001 | 1 | Oil Return Operation |
| 0x1001 | 1 | Pressure equalizing operation |
| 0x1001 | 1 | Demand Signal |
| 0x1001 | 1 | Low noise control |
| 0x1004 | 1 | Error type |
| 0x1005 | 1 | Error Code |
| 0x1006 | 2 | Target Evap. Temp. |
| 0x1008 | 2 | Target Cond. Temp. |
| 0x100A | 1 | Discharge Temp. Drop |
| 0x100A | 1 | Discharge Temp. Protection Retry Qty |
| 0x100A | 1 | Comp. INV Current Drop |
| 0x100A | 1 | Comp. INV Current Protection Retry Qty |
| 0x100B | 1 | HP Drop Control |
| 0x100B | 1 | HP Protection Retry Qty |
| 0x100B | 1 | LP Drop Control |
| 0x100B | 1 | LP Protection Retry Qty |
| 0x100C | 1 | Fin Temp. Drop Control |
| 0x100C | 1 | Fin Temp. Protection Retry Qty |
| 0x100C | 1 | Other Drop Control |
| 0x100C | 1 | Not in use |
| 0x1100 | 1 | O/U EEPROM (1st digit) |
| 0x1101 | 1 | O/U EEPROM (3rd 4th digit) |
| 0x1102 | 1 | O/U EEPROM (5th 6th digit) |
| 0x1103 | 1 | O/U EEPROM (7th 8th digit) |
| 0x1104 | 1 | O/U EEPROM (10th digit) |
| 0x1105 | 1 | O/U EEPROM (11th digit) |
| 0x2000 | 2 | R1T-Outdoor air temp. |
| 0x2002 | 2 | O/U Heat Exch. Temp.(R4T) |
| 0x2004 | 2 | Discharge pipe temp.(R2T) |
| 0x2006 | 2 | Suction pipe temp.(R3T) |
| 0x2008 | 2 | Heat exchanger mid-temp.(R5T) |
| 0x200A | 2 | Liquid pipe temp.(R6T) |
| 0x200C | 2 | High Pressure |
| 0x200C | 2 | High Pressure(T) |
| 0x200E | 2 | Low Pressure |
| 0x200E | 2 | Low Pressure(T) |
| 0x2100 | 2 | INV primary current (A) |
| 0x2102 | 2 | INV secondary current (A) |
| 0x2104 | 2 | INV fin temp. |
| 0x2106 | 2 | Fan1 Fin temp. |
| 0x2108 | 2 | Fan2 Fin temp. |
| 0x210A | 2 | Compressor outlet temperature |
| 0x3000 | 2 | INV frequency (rps) |
| 0x3001 | 1 | Fan 1 (step) |
| 0x3002 | 1 | Fan 2 (step) |
| 0x3003 | 2 | Expansion valve 1 (pls) |
| 0x3005 | 2 | Expansion valve 2 (pls) |
| 0x3007 | 2 | Expansion valve 3 (pls) |
| 0x3009 | 2 | Expansion valve 4 (pls) |
| 0x300B | 1 | 4 Way Valve |
| 0x300C | 1 | Crank case heater |
| 0x300D | 1 | Hot gas bypass valve (Y3S) |
| 0x300D | 1 | LP bypass valve (Y2S) |
| 0x300D | 1 | Y3S |
| 0x6000 | 1 | Data Enable/Disable |
| 0x6001 | 2 | Indoor Unit Address |
| 0x6002 | 1 | I/U operation mode |
| 0x6002 | 1 | Ext. Thermostat ON/OFF |
| 0x6002 | 1 | Freeze Protection |
| 0x6002 | 1 | Silent Mode |
| 0x6002 | 1 | Freeze Protection for water piping |
| 0x6003 | 1 | Error Code |
| 0x6004 | 2 | Error detailed code |
| 0x6005 | 1 | Error type |
| 0x6006 | 1 | I/U capacity code |
| 0x6007 | 2 | DHW setpoint |
| 0x6009 | 2 | LW setpoint (main) |
| 0x600B | 1 | Water flow switch |
| 0x600B | 1 | Thermal protector (Q1L) BUH |
| 0x600B | 1 | Thermal protector BSH |
| 0x600B | 1 | Benefit kWh rate power supply |
| 0x600B | 1 | Solar input |
| 0x600B | 1 | SmartGridContact2 |
| 0x600B | 1 | SmartGridContact1 |
| 0x600B | 1 | Bivalent Operation |
| 0x600C | 1 | 2way valve(On:Heat_Off:Cool) |
| 0x600C | 1 | 3way valve(On:DHW_Off:Space) |
| 0x600C | 1 | BSH |
| 0x600C | 1 | BUH Step1 |
| 0x600C | 1 | BUH Step2 |
| 0x600C | 1 | Floor loop shut off valve |
| 0x600C | 1 | Water pump operation |
| 0x600C | 1 | Solar pump operation |
| 0x600D | 2 | Indoor Option Code |
| 0x600E | 1 | I/U Software ID (yy) |
| 0x600F | 1 | I/U Software ID (xx) |
| 0x6010 | 2 | I/U EEPROM Ver. |
| 0x6100 | 1 | Data Enable/Disable |
| 0x6101 | 2 | Indoor Unit Address |
| 0x6102 | 2 | Leaving water temp. before BUH (R1T) |
| 0x6104 | 2 | Leaving water temp. after BUH (R2T) |
| 0x6106 | 2 | Refrig. Temp. liquid side (R3T) |
| 0x6108 | 2 | Inlet water temp.(R4T) |
| 0x610A | 2 | DHW tank temp. (R5T) |
| 0x610C | 2 | Indoor ambient temp. (R1T) |
| 0x610E | 2 | Ext. indoor ambient sensor (R6T) |
| 0x6200 | 1 | Data Enable/Disable |
| 0x6201 | 2 | Indoor Unit Address |
| 0x6202 | 1 | Reheat ON/OFF |
| 0x6202 | 1 | Storage ECO ON/OFF |
| 0x6202 | 1 | Storage comfort ON/OFF |
| 0x6202 | 1 | Powerful DHW Operation. ON/OFF |
| 0x6202 | 1 | Space heating Operation ON/OFF |
| 0x6202 | 1 | System OFF (ON:System off) |
| 0x6202 | 1 | Not in use |
| 0x6202 | 1 | Emergency (indoor) active/not active |
| 0x6203 | 2 | LW setpoint (add) |
| 0x6205 | 2 | RT setpoint |
| 0x6207 | 1 | Add. Ext. RT Input Cool. |
| 0x6207 | 1 | Add. Ext. RT Input Heat. |
| 0x6207 | 1 | Main RT Cooling |
| 0x6207 | 1 | Main RT Heating |
| 0x6207 | 1 | Pwr consumption limit 4 |
| 0x6207 | 1 | Pwr consumption limit 3 |
| 0x6207 | 1 | Pwr consumption limit 2 |
| 0x6207 | 1 | Pwr consumption limit 1 |
| 0x6208 | 1 | None |
| 0x6208 | 1 | Not in use |
| 0x6208 | 1 | Not in use |
| 0x6208 | 1 | PHE Heater |
| 0x6208 | 1 | Tank preheat ON/OFF |
| 0x6208 | 1 | Circulation pump operation |
| 0x6208 | 1 | Alarm output |
| 0x6208 | 1 | Space H Operation output |
| 0x6209 | 2 | Flow sensor (l/min) |
| 0x620B | 2 | Water pressure |
| 0x620C | 2 | Water pump signal (0:max-100:stop) |
| 0x620D | 2 | [Future] 3 way Valve Mixing 1 |
| 0x620E | 2 | [Future] 3 way Valve Mixing 2 |
| 0x620F | 2 | Refrigerant pressure sensor |
| 0x6300 | 1 | Data Enable/Disable |
| 0x6301 | 2 | Indoor Unit Address |
| 0x6302 | 1 | I/U EEPROM (3rd digit) |
| 0x6303 | 1 | I/U EEPROM (4th 5th digit) |
| 0x6304 | 1 | I/U EEPROM (6th 7th digit) |
| 0x6305 | 1 | I/U EEPROM (8th 9th digit) |
| 0x6306 | 1 | I/U EEPROM (11th digit) |
| 0x6307 | 1 | I/U EEPROM (12th digit)(rev.) |
| 0x6308 | 1 | Not in use |
| 0x6309 | 1 | Not in use |
| 0x630A | 1 | Not in use |
| 0x630B | 1 | Not in use |
| 0x630C | 1 | Not in use |
| 0x630D | 1 | BUH output capacity |
| 0x630E | 2 | Current measured by CT sensor of L1 |
| 0x630F | 2 | Current measured by CT sensor of L2 |
| 0x6310 | 1 | HP Forced FG |
| 0x6310 | 2 | Current measured by CT sensor of L3 |
| 0x6400 | 1 | Data Enable/Disable |
| 0x6401 | 2 | Indoor Unit Address |
| 0x6402 | 1 | Hybrid Op. Mode |
| 0x6402 | 1 | Boiler Operation Demand |
| 0x6402 | 1 | Boiler DHW Demand |
| 0x6402 | 1 | Bypass Valve Output |
| 0x6403 | 2 | BE_COP |
| 0x6405 | 2 | Hybrid Heating Target Temp. |
| 0x6407 | 2 | Boiler Heating Target Temp. |
| 0x6409 | 1 | Add pump |
| 0x6409 | 1 | Main pump |
| 0x640A | 2 | Mixed water temp. |
| 0x640C | 2 | 2nd Domestic hot water temperature |
| 0x640E | 2 | Target delta T heating |
| 0x640F | 2 | Target delta T cooling |
| 0x6500 | 1 | Data Enable/Disable |
| 0x6501 | 2 | Indoor Unit Address |
| 0x6502 | 2 | Outlet water heat exchanger temp (hydro split model) DLWB2 |
| 0x6504 | 2 | [EKMIK] Bizone kit mixed leaving water temperature R1T |
| 0x6506 | 1 | [EKMIK] Bizone kit mix valve position M1S |
| 0xA000 | 2 | Suction temp |
| 0xA002 | 2 | Outdoor heat exchanger temp. |
| 0xA004 | 2 | Liquid pipe temp. |
| 0xA006 | 2 | Pressure |
| 0xA008 | 2 | Expansion valve 3 (pls) |
| 0xA00A | 2 | O/U MPU ID |
| 0xA00B | 2 | O/U MPU ID |
| 0xA00C | 1 | HPS operation |
| 0xA00C | 1 | Safeguard operation |
| 0xA00C | 1 | Crank case heater |
| 0xA00C | 1 | Solenoid Valve 3 |
| 0xA00C | 1 | Solenoid Valve 2 |
| 0xA00C | 1 | Solenoid Valve 1 |
| 0xA00C | 1 | 4 way valve (Y1S) |
| 0xA00C | 1 | 52C Output |
| 0xA00D | 1 | Discharge Temp. Drop |
| 0xA00D | 1 | During emergency operation |
| 0xA00D | 1 | Indoor unit blowout 50 C flag |
| 0xA00D | 1 | Powerful bit (MT setting bit) |
| 0xA00E | 2 | Compressor port temperature |
| 0xA100 | 2 | (Raw data)Water heat exchanger inlet temp. |
| 0xA102 | 2 | (Raw data)Water heat exchanger outlet temp. |
| 0xA104 | 1 | Liquid INJ solenoid valve (Y4S) |
| 0xA104 | 1 | Bottom Plate Heater |
| 0xA104 | 1 | PHE Heater |
| 0xA105 | 2 | Target Discharge Temp. |
| 0xA107 | 2 | Target port temperature |
| 0xA109 | 1 | Monobloc setting |
| 0xA109 | 1 | Minichiller setting |
| 0xA109 | 1 | MT setting |
| 0xA109 | 1 | GSHP setting |
| 0xA109 | 1 | Hydro split setting |
| 0xA109 | 1 | Alterma LT setting |
