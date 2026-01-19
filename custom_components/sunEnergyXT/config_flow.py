from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN
from .tcp_client import *
from .discovery import *
from .global_config import *
from .util import *


class BkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理集成配置流程."""

    VERSION = 1

    async def async_mdns_start(self):
        """启动msdn发现服务."""
        data_key = "msdn_discovery"

        # 判断之前是否已经存在连接
        if data_key in GLOBAL_MDNS_CLIENTS:
            manager = GLOBAL_MDNS_CLIENTS[data_key]

            if manager:
                await manager.async_stop_discovery()

        # 释放当前设备存储的数据,保留发现服务
        GLOBAL_MDNS_CLIENTS.pop(data_key, None)

        # 创建设备发现管理器
        mdns_manager = MdnsManager(self.hass)

        # 开始监听服务
        await mdns_manager.async_start_discovery()

        # 将客户端实例保存在hass数据中，以便其他组件访问
        GLOBAL_MDNS_CLIENTS[data_key] = mdns_manager

    async def async_get_devices(self) -> dict[str, Any]:
        """处理搜索到的设备,排查已添加的."""
        await self.async_mdns_start()

        await asyncio.sleep(2)

        devices = GLOBAL_DEVICES.copy()

        # 剔除已经存在的设备
        entries = self._async_current_entries()
        if entries:
            for entry in entries:
                # del devices[device_id]
                serial_number = entry.unique_id
                devices.pop(serial_number, None)

        return devices

    async def async_step_user(self, user_input=None):
        """处理用户初始步骤."""
        errors = {}

        # # 用户输入信息后,走的这一步
        if user_input is not None:
            try:
                # 检查该设备是否已被配置
                unique_id = user_input["serial_number"]

                await self.async_set_unique_id(unique_id)

                self._abort_if_unique_id_configured()

                device_info = get_device_info_form_serial_number(unique_id)

                return self.async_create_entry(
                    title=user_input["device_name"], data=device_info
                )
            except Exception as e:
                message = e.args[0] if e.args else str(e)
                errors["base"] = get_error_message(message)

        # 搜索设备信息
        devices = await self.async_get_devices()

        # 使用not可以判断是否包含成员
        if not devices:
            # 跳转到 device_not_found 步骤
            return await self.async_step_device_not_found()

        # 搜索到设备信息生成模板
        schema = get_discover_schema(devices)

        # 显示配置表单,第一次登录时还没有输入信息，走的这一步
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_device_not_found(self, user_input=None):
        """处理未找到设备的情况."""
        errors = {}

        if user_input is not None:
            if user_input["manual_config"] == "yes":
                # 用户选择继续，进行手动配置
                return await self.async_step_manual()

            # 用户选择不继续，中止流程
            return self.async_abort(reason="no_devices_found")

        # 显示选择表单
        schema = get_manual_select_schema()

        return self.async_show_form(
            step_id="device_not_found",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_manual(self, user_input=None):
        """实现手动配置逻辑."""
        errors = {}

        # # 用户输入信息后,走的这一步
        if user_input is not None:
            # 验证用户输入
            try:
                # 检查网络连接性,连接失败则弹出错误提示
                host = user_input["host"]

                port = user_input["port"]

                validate_connection(host, port)

                # 检查该设备是否已被配置
                unique_id = user_input["serial_number"]

                await self.async_set_unique_id(unique_id)

                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input["device_name"], data=user_input
                )
            except Exception as e:
                message = e.args[0] if e.args else str(e)
                errors["base"] = get_error_message(message)

        # 显示配置表单,第一次登录时还没有输入信息，走的这一步
        schema = get_manual_schema()

        return self.async_show_form(step_id="manual", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """处理界面修改参数配置流程."""
        return BkOptionsFlow(config_entry)


class BkOptionsFlow(config_entries.OptionsFlow):
    """处理配置界面参数修改."""

    def __init__(self, config_entry) -> None:
        """初始化函数."""
        self.entry = config_entry

    def check_serial_number_change(self, user_input):
        """检查序列号是否已经改变."""
        intput_number = user_input["serial_number"]

        entity_number = self.entry.data["serial_number"]

        if intput_number != entity_number:
            raise ValueError("serial_number_cannot_change")

        return False

    async def async_step_init(self, user_input=None):
        """处理参数配置更改."""
        errors = {}

        if user_input is not None:
            try:
                self.check_serial_number_change(user_input)

                # if not state:
                #     return self.async_abort(
                #         reason="serial_number_cannot_change",
                #     )

                updated_data = {**self.entry.data, **user_input}

                # 检查网络连接性,连接失败则弹出错误提示
                host = user_input["host"]

                port = user_input["port"]

                validate_connection(host, port)

                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data=updated_data,
                    title=user_input.get("device_name", self.entry.title),
                )

                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self.entry.entry_id)
                )

                # 必需步骤 - 完成配置流程
                return self.async_create_entry(
                    title=user_input["device_name"], data=updated_data
                )
            except Exception as e:
                message = e.args[0] if e.args else str(e)
                errors["base"] = get_error_message(message)

        # 加载配置参数方案
        schmea = get_config_schema(self.entry)

        return self.async_show_form(step_id="init", data_schema=schmea, errors=errors)
