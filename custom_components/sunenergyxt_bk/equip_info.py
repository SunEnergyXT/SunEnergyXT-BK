from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from typing import cast


class EquipInfo:
    """前端界面显示的设备信息类."""

    def __init__(self, entry: ConfigEntry) -> None:
        """初始化函数."""
        self.entry = entry

    def get_equip_info(self) -> DeviceInfo | None:
        """前端设备信息获取函数."""
        serial_umber = self.entry.data["serial_number"]
        sw_version = self.entry.data["sw_version"]
        hw_version = self.entry.data["hw_version"]

        # 设备信息
        return cast(
            DeviceInfo,
            {
                # 唯一标识,序列号,mac地址不能一样，否则无法区分设备
                "identifiers": {(DOMAIN, self.entry.entry_id)},
                "name": f"{serial_umber}",
                "manufacturer": "SunEnergyXT",  # 制造商
                "sw_version": f"{sw_version}",  # 软件版本
                "hw_version": f"{hw_version}",  # 硬件版本
                "serial_number": f"{serial_umber}",  # 序列号
                # "model": "设备型号:BK215",
                # "connections": [("mac", "a4:c1:38:46:7e:19")],
            },
        )
