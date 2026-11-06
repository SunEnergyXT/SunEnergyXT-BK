# SunEnergyXT-BK

SunEnergyXT-BK is a Home Assistant custom integration for SunEnergyXT BK battery
local monitoring and control.

## Installation

### Home Assistant 2026.11 and later

1. Open the marketplace of Home Assistant and add
   `https://github.com/SunEnergyXT/SunEnergyXT-BK` as a custom repository of the
   type Integration.
2. Install SunEnergyXT-BK from the marketplace and restart Home Assistant.

Updates are offered in the marketplace afterwards.

### Home Assistant before 2026.11

1. In HACS, add `https://github.com/SunEnergyXT/SunEnergyXT-BK` as a custom
   repository of the type Integration.
2. Download SunEnergyXT-BK in HACS and restart Home Assistant.

### Add the device

After the restart, add the integration from:

```text
Settings > Devices & services > Add integration > SunEnergyXT-BK
```

## Upgrading from 1.0.3 or earlier

Version 1.0.4 changes the integration domain from `sunEnergyXT` to
`sunenergyxt_bk`, so that the built-in marketplace of Home Assistant 2026.11
can install and update it. Earlier versions can not be updated to 1.0.4 in place,
upgrade once as follows:

1. Go to `Settings > Devices & services > SunEnergyXT-BK` and delete every
   configured device of the integration.
2. Remove the old version:
   - Home Assistant 2026.11 and later: uninstall SunEnergyXT-BK in the
     marketplace.
   - Before 2026.11 with HACS: remove SunEnergyXT-BK in HACS. If the folder
     `/config/custom_components/sunEnergyXT/` still exists afterwards, delete
     it.
   - Installed by copying files: delete the folder
     `/config/custom_components/sunEnergyXT/`.
3. Install the new version as described under "Installation" and restart Home
   Assistant.
4. Add the devices again with the same serial numbers.

The entities get the same entity IDs as before, so automations, dashboards, and
history keep working. Delete the old devices before adding them again,
otherwise Home Assistant appends `_2` to the new entity IDs.

From 1.0.4 on, updates are installed through the marketplace or HACS as usual.

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

## Issues

Report bugs or feature requests on GitHub:

https://github.com/SunEnergyXT/SunEnergyXT-BK/issues
