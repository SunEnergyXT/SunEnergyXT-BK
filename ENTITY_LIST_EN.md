# SunEnergyXT Home Assistant Entity List

This document lists the Home Assistant entities exposed by the official `SunEnergyXT-BK` integration and explains what each entity is used for.

## Scope

- Integration: `SunEnergyXT/SunEnergyXT-BK`
- Entity platforms: `switch`, `number`, `sensor`
- Source mapping: official plugin entity names + local battery API field mapping

## 1. Switch Entities

| HA Entity | API Field | Access | English Description |
| --- | --- | --- | --- |
| `BK Local Mode` | `t598` | RW | Enables or disables the battery's local LAN communication mode. When enabled, Home Assistant or another LAN-side controller can communicate with the battery locally. Cloud-side app strategy control is restricted while this mode is active. |
| `EV3600 Battery Charging Mode` | `t700_1` | RW | Turns the EV3600-related battery charging mode on or off. This mode is used when the system should prioritize charging behavior defined for the battery charging scenario. |
| `EV3600 Car Charging Mode` | `t701_1` | RW | Turns the EV3600 vehicle charging mode on or off. This mode is used when battery energy may be allocated to EV charging behavior. |
| `EV3600 Home Appliance Mode` | `t702_1` | RW | Turns the EV3600 household appliance mode on or off. This mode is used when battery discharge is allocated to household appliance or household load support. |
| `EV3600 Car Grid Charging Active` | `t728` | RW | Allows or blocks grid / AC participation during EV charging mode. When enabled, EV charging mode may fall back to mixed AC supply where supported. |

## 2. Number Entities

| HA Entity | API Field | Access | Unit | English Description |
| --- | --- | --- | --- | --- |
| `BK Discharge Limit` | `t362` | RW | `%` | User-configurable minimum discharge SOC. Once the battery reaches this limit, normal discharge should stop. This is a software configuration limit, not the hardware BMS protection threshold. |
| `BK Charge Limit` | `t363` | RW | `%` | User-configurable maximum charge SOC. Once the battery reaches this limit, normal charging should stop. This is a software configuration limit, not the hardware BMS protection threshold. |
| `EV3600 Discharge Cutoff SOC Setting (Home Appliance Mode)` | `t720` | RW | `%` | Discharge cutoff SOC used specifically for EV3600 home appliance mode. When the battery reaches this SOC, discharge for household appliance loads should stop. |
| `EV3600 Discharge Cutoff SOC Setting (Car Charging Mode)` | `t721` | RW | `%` | Discharge cutoff SOC used specifically for EV3600 car charging mode. When the battery reaches this SOC, discharge for vehicle charging should stop. |
| `EV3600 Charge Cutoff SOC Setting (Battery Charging Mode)` | `t727` | RW | `%` | Charge cutoff SOC used specifically for EV3600 battery charging mode. When this SOC is reached, the dedicated charging mode should stop. |
| `EV3600 System Charging Setting Power` | `t590` | RW | `W` | Configured charging power setpoint for the battery system. This is the target charging power, although actual power may still be limited by hardware conditions, power sources, or active operating logic. |
| `BK Idle Auto-Shutdown Time` | `t596` | RW | `min` | Automatic shutdown timeout used when the system has neither input power nor output power. |
| `BK Low Battery Auto-Shutdown Time` | `t597` | RW | `min` | Automatic shutdown timeout used after the battery reaches the configured low-battery or DOD lower limit. |

## 3. SOC and Battery Protection Sensors

| HA Entity | API Field | Access | Unit | English Description |
| --- | --- | --- | --- | --- |
| `BK Battery Level` | `t211` | R | `%` | Aggregated battery SOC shown for the overall system. This is the main battery level value typically used for the full system view. |
| `Head storage` | `t592` | R | `%` | Actual remaining SOC of the head unit or main battery pack. In parallel systems, this is the real SOC of the main pack rather than the aggregated system SOC. |
| `Expansion 1 storage` | `t593` | R | `%` | Actual remaining SOC of expansion battery 1. |
| `Expansion 2 storage` | `t594` | R | `%` | Actual remaining SOC of expansion battery 2. |
| `Expansion 3 storage` | `t595` | R | `%` | Actual remaining SOC of expansion battery 3. |
| `Expansion 4 storage` | `t1001` | R | `%` | Actual remaining SOC of expansion battery 4. |
| `Expansion 5 storage` | `t1002` | R | `%` | Actual remaining SOC of expansion battery 5. |
| `Expansion 6 storage` | `t1003` | R | `%` | Actual remaining SOC of expansion battery 6. |
| `Expansion 7 storage` | `t1004` | R | `%` | Actual remaining SOC of expansion battery 7. |
| `Head HW discharge limit` | `t507` | R | `%` | Hardware-enforced minimum discharge SOC of the head unit. This is the BMS protection lower limit and is read-only. |
| `Head HW charge limit` | `t508` | R | `%` | Hardware-enforced maximum charge SOC of the head unit. This is the BMS protection upper limit and is read-only. |
| `Expansion 1 HW discharge limit` | `t509` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 1. |
| `Expansion 1 HW charge limit` | `t510` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 1. |
| `Expansion 2 HW discharge limit` | `t511` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 2. |
| `Expansion 2 HW charge limit` | `t512` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 2. |
| `Expansion 3 HW discharge limit` | `t513` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 3. |
| `Expansion 3 HW charge limit` | `t514` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 3. |
| `Expansion 4 HW discharge limit` | `t948` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 4. |
| `Expansion 4 HW charge limit` | `t949` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 4. |
| `Expansion 5 HW discharge limit` | `t950` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 5. |
| `Expansion 5 HW charge limit` | `t951` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 5. |
| `Expansion 6 HW discharge limit` | `t952` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 6. |
| `Expansion 6 HW charge limit` | `t953` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 6. |
| `Expansion 7 HW discharge limit` | `t954` | R | `%` | Hardware-enforced minimum discharge SOC of expansion battery 7. |
| `Expansion 7 HW charge limit` | `t955` | R | `%` | Hardware-enforced maximum charge SOC of expansion battery 7. |

## 4. Power and Energy Sensors

| HA Entity | API Field | Access | Unit | English Description |
| --- | --- | --- | --- | --- |
| `BK Total Input Power` | `t33` | R | `W` | Total instantaneous input power of the battery system. According to the local API notes, this corresponds to total MPPT input power. |
| `BK Total Output Power` | `t34` | R | `W` | Total instantaneous output power of the battery system. According to the local API notes, this corresponds to total inverter-side output power. |
| `BK Daily Yield` | `t49` | R | `kWh` | Daily PV generation energy. The plugin converts the raw `Wh` field into `kWh` using a `0.001` factor. |
| `BK Daily Output Energy` | `t66` | R | `kWh` | Daily output energy delivered by the battery system. The plugin converts the raw `Wh` field into `kWh`. |
| `EV3600 Daily Grid Charge` | `t710` | R | `kWh` | Daily energy charged from the grid in the EV3600-related charging scenario. |
| `EV3600 Grid Input Power` | `t711` | R | `W` | Instantaneous power currently drawn from the grid. Useful to see whether the system is currently charging from AC power. |
| `EV3600 Car Charging Power` | `t701_4` | R | `W` | Instantaneous power used by vehicle charging mode. |
| `EV3600 Home Load Power` | `t702_4` | R | `W` | Instantaneous power used by household appliance / home load mode. |
| `Head PV1 Power` | `t50` | R | `W` | PV input power measured on MPPT channel 1 of the head unit. The plugin applies a `0.01` scaling factor. |
| `Head PV2 Power` | `t62` | R | `W` | PV input power measured on MPPT channel 2 of the head unit. The plugin applies a `0.01` scaling factor. |
| `Expansion 1 MPPT Power` | `t63` | R | `W` | PV input power of expansion battery 1. |
| `Expansion 2 MPPT Power` | `t64` | R | `W` | PV input power of expansion battery 2. |
| `Expansion 3 MPPT Power` | `t65` | R | `W` | PV input power of expansion battery 3. |
| `Expansion 4 MPPT Power` | `t812` | R | `W` | PV input power of expansion battery 4. |
| `Expansion 5 MPPT Power` | `t813` | R | `W` | PV input power of expansion battery 5. |
| `Expansion 6 MPPT Power` | `t814` | R | `W` | PV input power of expansion battery 6. |
| `Expansion 7 MPPT Power` | `t815` | R | `W` | PV input power of expansion battery 7. |

## 5. Temperature and Heater Sensors

| HA Entity | API Field | Access | Unit | English Description |
| --- | --- | --- | --- | --- |
| `Head Battery Temp` | `t220` | R | `°C` | Lowest cell temperature of the head unit. The raw API value is Kelvin and the plugin converts it using `TEMP273`. |
| `Expansion 1 Temp` | `t233` | R | `°C` | Lowest cell temperature of expansion battery 1. |
| `Expansion 2 Temp` | `t246` | R | `°C` | Lowest cell temperature of expansion battery 2. |
| `Expansion 3 Temp` | `t259` | R | `°C` | Lowest cell temperature of expansion battery 3. |
| `Expansion 4 Temp` | `t836` | R | `°C` | Lowest cell temperature of expansion battery 4. |
| `Expansion 5 Temp` | `t849` | R | `°C` | Lowest cell temperature of expansion battery 5. |
| `Expansion 6 Temp` | `t862` | R | `°C` | Lowest cell temperature of expansion battery 6. |
| `Expansion 7 Temp` | `t875` | R | `°C` | Lowest cell temperature of expansion battery 7. |
| `Head Heater State` | `t586` | R | enum | Heater state bit for the head unit. The plugin interprets the heater status through `BIT0` and exposes `on` / `off`. |
| `Expansion 1 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 1, interpreted through `BIT1`. |
| `Expansion 2 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 2, interpreted through `BIT2`. |
| `Expansion 3 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 3, interpreted through `BIT3`. |
| `Expansion 4 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 4, interpreted through `BIT4`. |
| `Expansion 5 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 5, interpreted through `BIT5`. |
| `Expansion 6 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 6, interpreted through `BIT6`. |
| `Expansion 7 Heater State` | `t586` | R | enum | Heater state bit for expansion battery 7, interpreted through `BIT7`. |

## 6. MPPT Current and Voltage Sensors

| HA Entity | API Field | Access | Unit | English Description |
| --- | --- | --- | --- | --- |
| `Head MPPT1 Current` | `t537` | R | `A` | Input current on MPPT channel 1 of the head unit. The plugin converts the raw value using a `0.1` factor. |
| `Head MPPT1 Voltage` | `t536` | R | `V` | Input voltage on MPPT channel 1 of the head unit. The plugin converts the raw value using a `0.1` factor. |
| `Head MPPT2 Current` | `t545` | R | `A` | Input current on MPPT channel 2 of the head unit. |
| `Head MPPT2 Voltage` | `t544` | R | `V` | Input voltage on MPPT channel 2 of the head unit. |
| `Expansion 1 MPPT Current` | `t553` | R | `A` | MPPT input current of expansion battery 1. |
| `Expansion 1 MPPT Voltage` | `t552` | R | `V` | MPPT input voltage of expansion battery 1. |
| `Expansion 2 MPPT Current` | `t561` | R | `A` | MPPT input current of expansion battery 2. |
| `Expansion 2 MPPT Voltage` | `t560` | R | `V` | MPPT input voltage of expansion battery 2. |
| `Expansion 3 MPPT Current` | `t569` | R | `A` | MPPT input current of expansion battery 3. |
| `Expansion 3 MPPT Voltage` | `t568` | R | `V` | MPPT input voltage of expansion battery 3. |
| `Expansion 4 MPPT Current` | `t970` | R | `A` | MPPT input current of expansion battery 4. |
| `Expansion 4 MPPT Voltage` | `t969` | R | `V` | MPPT input voltage of expansion battery 4. |
| `Expansion 5 MPPT Current` | `t978` | R | `A` | MPPT input current of expansion battery 5. |
| `Expansion 5 MPPT Voltage` | `t977` | R | `V` | MPPT input voltage of expansion battery 5. |
| `Expansion 6 MPPT Current` | `t986` | R | `A` | MPPT input current of expansion battery 6. |
| `Expansion 6 MPPT Voltage` | `t985` | R | `V` | MPPT input voltage of expansion battery 6. |
| `Expansion 7 MPPT Current` | `t994` | R | `A` | MPPT input current of expansion battery 7. |
| `Expansion 7 MPPT Voltage` | `t993` | R | `V` | MPPT input voltage of expansion battery 7. |

## 7. Diagnostic Sensors

| HA Entity | API Field | Access | Unit | English Description |
| --- | --- | --- | --- | --- |
| `Connection State` | internal | R | enum | Integration-level diagnostic entity that shows whether the Home Assistant integration is currently connected to the device. This is not a direct battery API field; it is derived from the integration runtime state. |
| `Last Update Time` | internal | R | timestamp | Integration-level diagnostic entity showing the last successful data refresh time. This is generated by the integration, not directly reported by the battery protocol. |
| `Wi-Fi Signal Strength` | `t475` | R | `dB` | Wi-Fi RSSI value reported by the battery. The local API sends the raw value as positive, and the integration presents it as a signal-strength diagnostic sensor. |

## Notes

- `R` means read-only.
- `RW` means readable and writable.
- Some EV3600-related entities may be unavailable when the current topology or firmware does not support the corresponding mode.
- If the local API reports `-1` for a field, the plugin may mark the entity as unavailable.
