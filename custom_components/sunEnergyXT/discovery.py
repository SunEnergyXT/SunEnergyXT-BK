import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import zeroconf
from zeroconf import ServiceListener, ServiceStateChange
from zeroconf.asyncio import AsyncServiceInfo
from zeroconf.asyncio import AsyncServiceBrowser
import asyncio
from homeassistant.helpers.dispatcher import async_dispatcher_send
from .const import *
from .data_info import MdnsDeiveInfo
from .global_config import GLOBAL_DEVICES
from .util import *

_LOGGER = logging.getLogger(__name__)


class MdnsManager:
    """管理mDNS服务发现."""

    def __init__(self, hass: HomeAssistant) -> None:
        """初始化函数."""
        self.hass = hass
        self.aiozc = None
        self.browser = None
        self.listener = None

    async def async_start_discovery(self):
        """mdns启动发现监听函数."""

        # 获取AsyncZeroconf对象[citation:1]
        self.aiozc = await zeroconf.async_get_async_instance(self.hass)

        # 定义要监听的服务类型
        # service_types = ["_http._tcp.local.", "_hp-bk215._http._tcp.local."]
        service_type = "_http._tcp.local."  # 正确收到mdns广播的服务类型

        # 创建服务监听器
        self.listener = MdnsServiceListener(self.hass, self)

        # 启动服务浏览器
        self.browser = AsyncServiceBrowser(
            self.aiozc.zeroconf, service_type, self.listener
        )

        message = f"started mdns discovery for service types: {service_type}"

        _LOGGER.info(message)

    async def async_stop_discovery(self):
        """mdns停止发现服务."""
        if self.browser:
            await self.browser.async_cancel()
            self.browser = None

    async def async_handle_parse_info(self, info) -> MdnsDeiveInfo | None:
        """mdns发现数据处理函数."""
        try:
            service_type = info.type
            service_name = info.name
            addresses = info.parsed_addresses()

            message = f"add mdns discovery for service types:{service_type} name: {service_name}"

            _LOGGER.info(message)

            if "hp-bk215" not in service_name:
                return None

            if not addresses:
                message = "service %s has no valid addresses", service_name

                _LOGGER.info(message)

                return None

            # 使用第一个可用的地址
            host = addresses[0]

            if not info.properties:
                return None

            # 提取设备信息
            properties = {}
            for key, value in info.properties.items():
                # 解码bytes为string
                properties[key.decode()] = (
                    value.decode() if isinstance(value, bytes) else value
                )

            if not properties:
                return None

            # 创建设备唯一ID
            serial_number = properties["id"]  # 序列号唯一
            port = properties["port"]
            sw_version = properties["fw_ver"]
            hw_version = properties["model"]

            message = f"mdns discovery info serial_number:{serial_number} ip:{host} port:{port}"

            _LOGGER.info(message)

            return MdnsDeiveInfo(
                service_type,
                service_name,
                serial_number,
                host,
                port,
                sw_version,
                hw_version,
            )

        except Exception as e:
            message = "error handling parse info: %s", e
            _LOGGER.error(message)

        return None

    async def async_handle_service_add(self, info):
        """mdns新增设备函数."""
        try:
            add_info = await self.async_handle_parse_info(info)

            if not add_info:
                return

            serial_number = add_info.serial_number

            host = add_info.host

            if not serial_number:
                return

            GLOBAL_DEVICES[serial_number] = add_info

            # 发送更新函数
            await self.async_update_devices(add_info)

            message = f"add mdns discovery sn:{serial_number} host:{host}"

            _LOGGER.info(message)

        # keys_list = list(self.hass.data[DOMAIN].keys())

        # # 通知Home Assistant有新设备
        # self.hass.async_create_task(
        #     self.hass.config_entries.async_reload(keys_list[1])
        # )

        # # 触发Home Assistant的配置流
        # await self.hass.config_entries.flow.async_init(
        #     "p200",  # 你的集成域名
        #     context={"source": config_entries.SOURCE_ZEROCONF},
        #     data=device_info,
        # )

        except Exception as e:
            message = "error handling service add: %s", e
            _LOGGER.error(message)

    async def async_handle_service_update(self, info):
        """mdns发现更新函数."""
        try:
            update_info = await self.async_handle_parse_info(info)

            if not update_info:
                return

            serial_number = update_info.serial_number

            host = update_info.host

            if not serial_number:
                return

            GLOBAL_DEVICES[serial_number] = update_info

            # 发送更新函数
            await self.async_update_devices(update_info)

            message = f"update mdns discovery sn:{serial_number} host:{host}"

            _LOGGER.info(message)

            # keys_list = list(self.hass.data[DOMAIN].keys())

            # # 通知Home Assistant有新设备
            # self.hass.async_create_task(
            #     self.hass.config_entries.async_reload(keys_list[1])
            # )

            # # 触发Home Assistant的配置流
            # await self.hass.config_entries.flow.async_init(
            #     "p200",  # 你的集成域名
            #     context={"source": config_entries.SOURCE_ZEROCONF},
            #     data=device_info,
            # )

        except Exception as e:
            message = "error handling service update: %s", e
            _LOGGER.error(message)

    async def async_handle_judge_change(self, entry_info, device_info) -> bool:
        """mdns判断配置是否更新函数."""
        return any(entry_info.get(key) != device_info.get(key) for key in entry_info)

    async def async_update_devices(self, device_info: MdnsDeiveInfo):
        """mdns配置更新函数."""
        serial_number = device_info.serial_number

        entries = self.hass.config_entries.async_entries(DOMAIN)

        current_entry = None

        for entry in entries:
            if entry.data.get("serial_number") == serial_number:
                current_entry = entry
                break

        if not current_entry:
            return

        device_data = get_device_info_form_device(device_info)

        entry_data = current_entry.data

        # 配置信息没有更改,则返回
        if not await self.async_handle_judge_change(entry_data, device_data):
            return

        updated_data = {**current_entry.data, **device_data}

        self.hass.config_entries.async_update_entry(
            current_entry,
            data=updated_data,
            title=device_data.get("device_name", current_entry.title),
        )

        self.hass.async_create_task(
            self.hass.config_entries.async_reload(current_entry.entry_id)
        )

        # await self.hass.config_entries.async_reload(current_entry.entry_id)

        # async_dispatcher_send(
        #     self.hass,
        #     f"p200_options_update_{serial_number}",
        #     self.hass,
        #     device_info,  # 正确传递参数
        # )

    async def async_handle_service_remove(self, service_name):
        """mdns设备删除函数."""
        try:
            # 查找并移除对应的设备
            unique_id = None

            for uid, device in GLOBAL_DEVICES.items():
                if device.service_name == service_name:
                    unique_id = uid
                    break

            if not unique_id:
                return

            del GLOBAL_DEVICES[unique_id]

            message = "removed device sn: %s", unique_id

            _LOGGER.info(message)

            # keys_list = list(self.hass.data[DOMAIN].keys())
            # # 通知Home Assistant设备已移除
            # self.hass.async_create_task(
            #     self.hass.config_entries.async_reload(keys_list[1])
            # )
        except Exception as e:
            message = "error handling service remove: %s", e
            _LOGGER.error(message)


class MdnsServiceListener(ServiceListener):
    """mdns设备侦听类."""

    def __init__(self, hass, mdns_manager) -> None:
        """初始化函数."""
        self.hass = hass
        self.mdns_manager = mdns_manager
        self.add_task = None
        self.remove_task = None
        self.update_task = None

    def add_service(self, zc, type_, name):
        """mdns服务添加回调函数."""
        self.add_task = asyncio.create_task(
            self.async_handle_service_add(zc, type_, name)
        )

    def remove_service(self, zc, type_, name):
        """mdns服务移除回调函数."""
        self.remove_task = asyncio.create_task(
            self.async_handle_service_remove(zc, type_, name)
        )

    def update_service(self, zc, type_, name):
        """mdns服务更新回调函数."""
        self.update_task = asyncio.create_task(
            self.async_handle_service_update(zc, type_, name)
        )

    async def async_handle_service_add(self, aiozc_zero, service_type, service_name):
        """mdns异步处理服务添加函数."""
        try:
            # info = AsyncServiceInfo(type_, name)
            # if await info.async_request(self.discovery_manager.aiozc.zeroconf, 3000):
            #     if change_type in {"added", "updated"}:
            #         await self.discovery_manager.async_handle_service_discovery(info)
            #     elif change_type == "removed":
            #         # 处理设备移除
            #         await self.async_handle_service_removal(name)

            info = AsyncServiceInfo(service_type, service_name)

            if not await info.async_request(aiozc_zero, 3000):
                return

            await self.mdns_manager.async_handle_service_add(info)

        except Exception as e:
            message = ("error handling service add: %s", e)
            _LOGGER.error(message)

    async def async_handle_service_remove(self, aiozc_zero, service_type, service_name):
        """mdns异步处理服务删除函数."""
        try:
            await self.mdns_manager.async_handle_service_remove(service_name)

        except Exception as e:
            message = ("error handling service remove: %s", e)
            _LOGGER.error(message)

    async def async_handle_service_update(self, aiozc_zero, service_type, service_name):
        """mdns异步处理服务更新函数."""
        try:
            info = AsyncServiceInfo(service_type, service_name)

            if not await info.async_request(aiozc_zero, 3000):
                return

            await self.mdns_manager.async_handle_service_update(info)

        except Exception as e:
            message = ("error handling service update: %s", e)
            _LOGGER.error(message)
