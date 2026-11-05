# SunEnergyXT-BK

SunEnergyXT-BK is a Home Assistant custom integration for SunEnergyXT BK battery
local monitoring and control.

## Installation

Install this repository as a custom Home Assistant integration, for example with
HACS as a custom repository.

The integration files must be available under:

```text
custom_components/sunEnergyXT/
```

Restart Home Assistant after installation, then add the integration from:

```text
Settings > Devices & services > Add integration > SunEnergyXT-BK
```

## Installing or updating on Home Assistant 2026.11 and later

Home Assistant 2026.11 replaces HACS with its built-in marketplace, which does
not accept the `sunEnergyXT` domain of this integration. The integration can
therefore not be installed or updated there, copy it manually instead:

1. Download `Source code (zip)` of the latest release from
   https://github.com/SunEnergyXT/SunEnergyXT-BK/releases
2. Copy the `custom_components/sunEnergyXT/` folder from the zip to
   `/config/custom_components/sunEnergyXT/`, replacing the existing folder, for
   example through the Samba share, the File editor / Studio Code Server
   add-on, or SSH.
3. Restart Home Assistant.

When updating, configured devices, entities, and history are kept, there is no
need to remove and add the integration again. On Home Assistant versions before
2026.11, HACS keeps installing and updating it as before.

## Prerequisites

- The battery must be reachable from Home Assistant on the local network.
- Local communication must already be available on the device.
- If automatic discovery does not find the device, use manual configuration with
  the device host, port, serial number, software version, and hardware version.

## Entities

The integration creates sensor, switch, number, and diagnostic entities for the
BK device.

See [ENTITY_LIST_EN.md](ENTITY_LIST_EN.md) for the full English entity list and
API field mapping.

Some diagnostic entities are intended for troubleshooting only. In particular,
`wifi_update_time` can update very frequently and is disabled by default for new
installations to avoid unnecessary Home Assistant recorder and logbook entries.
It can still be enabled manually from the entity registry when needed.

## Known Limitations

- Switching from cloud mode to local mode cannot be completed through this local
  TCP integration when the device is not already reachable locally.
- The integration exposes the entities defined by the current local protocol.
  Device variants and extension modules may report unsupported values as
  unavailable.
- The current integration domain is `sunEnergyXT`. Renaming the domain would be
  a breaking change for existing installations. Because of this domain, the
  Home Assistant 2026.11 marketplace cannot install or update the integration,
  see "Installing or updating on Home Assistant 2026.11 and later".

## Issues

Report bugs or feature requests on GitHub:

https://github.com/SunEnergyXT/SunEnergyXT-BK/issues
