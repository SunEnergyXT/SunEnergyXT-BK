import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from .tcp_client import *
from .const import DOMAIN
from .discovery import *
from .equip_info import EquipInfo
from .global_config import *
from .discovery import *
from .util import *

PLATFORMS = [Platform.NUMBER, Platform.SWITCH, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """初始化."""

    # 创建存储列表
    if f"{DOMAIN}" not in hass.data:
        hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """实体初始化."""

    # 创建存储列表
    if f"{entry.entry_id}" not in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.entry_id] = {}

    # 创建前端显示设备信息
    await async_create_equip_info(hass, entry)

    # 连接设备
    await async_tcp_connect(hass, entry)

    # 设置传感器平台
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """卸载配置条目."""

    await async_tcp_disconnect(hass, entry)

    await async_remove_device(hass, entry)

    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """重新加载配置条目."""
    await async_unload_entry(hass, entry)

    await async_setup_entry(hass, entry)

    message = "async_reload_entry: %s", entry.data.get("device_name")

    _LOGGER.info(message)


async def async_remove_device(hass: HomeAssistant, entry):
    """删除设备."""

    serial_number = entry.data["serial_number"]

    try:
        # 查找并移除对应的设备
        unique_id = None
        for uid, device in GLOBAL_DEVICES.items():
            if device.serial_number == serial_number:
                unique_id = uid
                break

        if not unique_id:
            return

        del GLOBAL_DEVICES[unique_id]

        message = "removed device: %s", serial_number

        _LOGGER.info(message)

    except Exception as e:
        message = "async_remove_device error: %s", e
        _LOGGER.error(message)


async def async_create_equip_info(hass: HomeAssistant, entry):
    """生成界面显示的设备信息."""
    equip_info = EquipInfo(entry)

    #  设备信息
    device_info = equip_info.get_equip_info()

    # 存储设备信息供实体使用
    GLOBAL_EQUIP_INFOS[entry.entry_id] = device_info


async def async_tcp_disconnect(hass: HomeAssistant, entry):
    """断开原有tcp连接."""

    # 判断之前是否已经存在的tcp连接
    if f"{entry.entry_id}" in GLOBAL_TCP_CLIENTS:
        client = GLOBAL_TCP_CLIENTS[entry.entry_id]

        if client:
            await client.async_stop_client()

    # 释放当前设备存储的数据,保留发现服务
    GLOBAL_TCP_CLIENTS.pop(entry.entry_id, None)


async def async_tcp_connect(hass: HomeAssistant, entry):
    """建立tcp连接."""

    # 断开原先存储的连接
    await async_tcp_disconnect(hass, entry)

    # 创建TCP客户端实例
    client = TcpClient(hass, entry)

    await client.async_connect()

    # 将客户端实例保存在hass数据中，以便其他组件访问
    GLOBAL_TCP_CLIENTS[entry.entry_id] = client
