# Combined Register/Offset Index

This file lists all **unique** `(registry_id, offset)` pairs found across all model-specific `include/def/*.h` files (excluding `DEFAULT.h` and protocol headers), sorted by registry then offset.

| Registry (hex) | Offset (hex) | Size | (EBLA-EDLA EWAA-EWYA D SERIES 9-16KW) | (HYBRID) | (LT_CA_CB_04-08KW) | (LT_CA_CB_11-16KW) | (LT_MULTI_DHWHP) | (LT_MULTI_HYBRID) | (EBLA-EDLA D series 4-8kW Monobloc) | (EBLA-EDLA D series 9-16kW Monobloc) | (EGSAH-X-EWSAH-X-D series 6-10kW GEO3) | (EGSQH-A series 10kW GEO2) | (EPGA D EAB-EAV-EAVZ D(J) series 11-16kW) | (EPRA D ETSH-X 16P30-50 D series 14-16kW-ECH2O) | (EPRA D ETV16-ETB16-ETVZ16 D series 14-16kW) | (EPRA D_D7 ETSH-X 16P30-50 E_E7 series 14-18kW-ECH2O) | (EPRA D_D7 ETV16-ETB16-ETVZ16 E_E7 series 14-18kW) | (EPRA E ETSH-X 16P30-50 E series 8-12kW-ECH2O) | (EPRA E ETV16-ETB16-ETVZ16 E_EJ series 8-12kW) | (ERGA D EHSH-X P30-50 D series 04-08kW-ECH2O) | (ERGA D EHV-EHB-EHVZ DA series 04-08kW) | (ERGA D EHV-EHB-EHVZ DJ series 04-08 kW) | (ERGA E EHSH-X P30-50 E_EF series 04-08kW-ECH2O) | (ERGA E EHV-EHB-EHVZ E_EJ series 04-08kW) | (ERLA D EBSH-X 16P30-50 D SERIES 11-16kW-ECH2O) | (ERLA D EBV-EBB-EBVZ D SERIES 11-16kW) | (ERLA03 D EHFH-EHFZ DJ series 3kW) | (LT_CB_04-08kW Bizone) | (LT_CB_11-16kW Bizone) | (LT_EBLQ-EBLQ-CA series 5-7kW Monobloc) | (LT_EBLQ-EDLQ-CA series 11-16kW Monobloc) | Daikin Mini chiller(EWAA-EWYA D series 4-8kW) | Daikin Mini chiller(EWAA-EWYA D series 9-16kW) | Daikin Mini chiller(EWAQ-EWYQ B series 4-8kW) | EKHWET-BAV3(MULTI DHW TANK) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0x00 | 0x00 | 0,1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x02 | 0,1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x03 | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x04 | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x05 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x06 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x07 | 1,3 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x08 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x09 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x0A | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x0B | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x00 | 0x0C | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x00 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x04 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x05 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x06 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x08 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x0A | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x0B | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x10 | 0x0C | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x11 | 0x00 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x11 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x11 | 0x02 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x11 | 0x03 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x11 | 0x04 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x11 | 0x05 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x00 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x02 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x04 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x06 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x08 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x0A | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x0C | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x0E | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x20 | 0x10 | 2 |  | X |  | X |  |  |  |  |  | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X |  | X |  | X |  |  |
| 0x20 | 0x12 | 2 |  | X |  | X |  |  |  |  |  | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X |  | X |  | X |  |  |
| 0x21 | 0x00 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x21 | 0x02 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x21 | 0x04 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x21 | 0x06 | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x21 | 0x07 | 2 |  | X | X | X | X | X |  |  |  | X |  |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x08 | 2 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  | X |  | X |  | X | X |
| 0x21 | 0x09 | 2 |  | X | X | X | X | X |  |  |  | X |  |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x0A | 2 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  | X |  | X |  | X | X |
| 0x21 | 0x0B | 2 |  | X | X | X | X | X |  |  |  | X |  |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x0C | 2 |  |  |  |  |  |  |  |  |  |  | X |  |  |  |  | X | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 0x21 | 0x0D | 2 |  | X | X | X | X | X |  |  |  | X |  |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x0F | 1 |  | X | X | X | X | X |  |  |  | X | X |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x10 | 1 |  | X | X | X | X | X |  |  |  | X | X |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x11 | 1 |  | X | X | X | X | X |  |  |  | X | X |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x21 | 0x12 | 1 |  | X | X | X | X | X |  |  |  | X | X |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X |  | X |  | X |  |  |
| 0x30 | 0x00 | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x30 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x30 | 0x02 | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x30 | 0x03 | 2 | X |  |  | X |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  | X | X |  |  | X |
| 0x30 | 0x04 | 2 |  | X | X |  | X | X |  |  |  | X |  |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X | X |  |  | X | X |  |
| 0x30 | 0x05 | 2 | X |  |  | X |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  | X | X |  |  | X |
| 0x30 | 0x06 | 2 |  | X | X |  | X | X |  |  |  | X |  |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X | X |  |  | X | X |  |
| 0x30 | 0x07 | 1,2 | X |  |  | X |  |  | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  |  |  | X | X |  |  | X |
| 0x30 | 0x08 | 1,2 |  | X | X | X | X | X |  |  |  | X | X |  |  |  |  |  |  | X | X |  |  |  |  |  | X | X | X | X | X |  | X | X |  |
| 0x30 | 0x09 | 1,2 | X |  |  | X |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  | X | X |  |  | X |
| 0x30 | 0x0A | 1 |  |  |  |  |  |  |  |  |  |  | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 0x30 | 0x0B | 1 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x30 | 0x0C | 1 | X |  |  |  |  |  | X | X | X |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x30 | 0x0D | 1 | X |  |  |  |  |  | X | X | X |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x60 | 0x00 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x02 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x03 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x04 | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x05 | 1 | X |  | X |  |  |  | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  |  |  | X |  |  | X |
| 0x60 | 0x06 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x07 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x09 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x0B | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x0C | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x0D | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x0E | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x0F | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x60 | 0x10 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x00 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x02 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x04 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x06 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x08 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x0A | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x0C | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x61 | 0x0D | 2 |  |  |  |  |  |  |  |  | X | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 0x61 | 0x0E | 2 | X | X | X | X | X | X | X | X |  |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  | X | X | X |  | X |
| 0x62 | 0x00 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x02 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x03 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x05 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x07 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x08 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x09 | 2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x0B | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x0C | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x0D | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x0E | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x0F | 1,2 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x62 | 0x10 | 1 |  | X | X | X | X | X |  |  |  | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X |  | X | X |  |
| 0x63 | 0x00 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x01 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x02 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x03 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x04 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x05 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x06 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x07 | 1 | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x63 | 0x08 | 1,2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x09 | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X |  |  |  |  |  |  | X |  | X |  |  |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x0A | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x0B | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X |  | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x0C | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x0D | 1 | X |  |  |  |  |  | X | X | X |  |  | X | X | X | X | X | X |  |  | X |  | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x0E | 1 | X |  |  |  |  |  | X | X | X |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x0F | 1 | X |  |  |  |  |  | X | X | X |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x63 | 0x10 | 1 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0x64 | 0x00 | 1 | X | X | X | X | X | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x64 | 0x01 | 1 | X | X | X | X | X | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x64 | 0x02 | 1 | X | X | X | X | X | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x64 | 0x03 | 2 | X | X | X | X | X | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x64 | 0x05 | 2 | X | X | X | X | X | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x64 | 0x07 | 2 | X | X | X | X | X | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |
| 0x64 | 0x09 | 1 | X |  | X | X | X | X | X | X |  |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  | X | X | X |  | X |
| 0x64 | 0x0A | 2 | X |  | X | X | X | X | X | X |  |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  | X | X | X |  | X |
| 0x64 | 0x0C | 2 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  |  |  |  | X |  |  | X |
| 0x64 | 0x0E | 1 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  |  |  |  | X |  |  | X |
| 0x64 | 0x0F | 1 | X |  |  |  |  |  | X | X | X |  | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |  |  |  |  | X |  |  | X |
| 0x65 | 0x00 | 1 |  |  |  |  |  |  |  | X |  |  |  |  |  | X | X | X | X |  |  |  | X |  | X | X |  |  |  |  |  |  |  |  |  |
| 0x65 | 0x01 | 1,2 |  |  |  |  |  |  |  | X |  |  |  |  |  |  |  |  |  |  |  |  | X |  | X | X |  |  |  |  |  |  |  |  |  |
| 0x65 | 0x02 | 2 |  |  |  |  |  |  |  | X |  |  |  |  |  | X | X | X | X |  |  |  | X |  | X | X |  |  |  |  |  |  |  |  |  |
| 0x65 | 0x04 | 2 |  |  |  |  |  |  |  | X |  |  |  |  |  | X | X | X | X |  |  |  | X |  | X | X |  |  |  |  |  |  |  |  |  |
| 0x65 | 0x06 | 1 |  |  |  |  |  |  |  | X |  |  |  |  |  | X | X | X | X |  |  |  | X |  | X | X |  |  |  |  |  |  |  |  |  |
| 0xA0 | 0x00 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x02 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x04 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x06 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x08 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x0A | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x0B | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x0C | 1 | X |  |  |  |  |  | X | X |  |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x0D | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA0 | 0x0E | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA1 | 0x00 | 2 | X |  |  |  |  |  | X | X |  |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA1 | 0x02 | 2 | X |  |  |  |  |  | X | X |  |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA1 | 0x04 | 1 | X |  |  |  |  |  | X | X |  |  | X | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA1 | 0x05 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA1 | 0x07 | 2 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
| 0xA1 | 0x09 | 1 | X |  |  |  |  |  | X | X |  |  |  | X | X | X | X | X | X |  |  | X | X | X | X | X |  |  |  |  |  | X |  |  | X |
