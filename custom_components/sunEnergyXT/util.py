import socket
import voluptuous as vol
from .global_config import *
from typing import Any
from homeassistant.helpers import selector


def get_discover_schema(devices) -> vol.Schema:
    """生成发现设备选择模板."""
    options_list: list[selector.SelectOptionDict] = [
        {"value": serial_number, "label": serial_number} for serial_number in devices
    ]

    default_info = ""

    if options_list:
        default_info = options_list[0]["value"]

    return vol.Schema(
        {
            vol.Required("device_name", default="BK215"): str,  # 集成实例名称
            vol.Required(
                "serial_number", default=default_info
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=options_list,
                )
            ),
        }
    )


def get_config_schema(entry) -> vol.Schema:
    """生成配置模板."""
    return vol.Schema(
        {
            vol.Required(
                "device_name", default=entry.title
            ): str,  # 集成实例名称,实际为条目名称
            vol.Required(
                "serial_number", default=entry.data["serial_number"]
            ): str,  # 集成实例名称
            vol.Required("host", default=entry.data["host"]): str,  # 服务器IP地址
            vol.Required("port", default=int(entry.data["port"])): int,  # 端口
            vol.Required(
                "sw_version", default=entry.data["sw_version"]
            ): str,  # 软件版本
            vol.Required(
                "hw_version", default=entry.data["hw_version"]
            ): str,  # 硬件版本
        }
    )


def get_manual_schema() -> vol.Schema:
    """生成默认模板."""
    return vol.Schema(
        {
            vol.Required("device_name", default="BK215"): str,  # 集成实例名称
            vol.Required("serial_number", default="BK2150000001"): str,  # 集成实例名称
            vol.Required("host", default="172.26.80.1"): str,  # 服务器IP地址
            vol.Required("port", default=8000): int,  # 端口
            vol.Required("sw_version", default="sw_v1.0"): str,  # 软件版本
            vol.Required("hw_version", default="hw_v1.0"): str,  # 硬件版本
        }
    )


def get_manual_select_schema() -> vol.Schema:
    """生成手动配置选择模板."""
    return vol.Schema(
        {
            vol.Required("manual_config", default="yes"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=["yes", "no"],
                    translation_key="manual_config_options",  # 关键：指向翻译键
                    # 在翻译文件中，“是/否”的定义方式需要调整
                )
            )
        }
    )


def get_device_info_form_serial_number(serial_number) -> dict[str, Any]:
    """通过序列号生成设备信息."""
    if not GLOBAL_DEVICES:
        return {}

    device = GLOBAL_DEVICES[f"{serial_number}"]

    if not device:
        return {}

    user_input = {}
    user_input["serial_number"] = serial_number
    user_input["host"] = device.host
    user_input["port"] = device.port
    user_input["sw_version"] = device.sw_version
    user_input["hw_version"] = device.hw_version

    return user_input


def get_device_info_form_device(device) -> dict[str, Any]:
    """通过发现设备生成设备信息."""
    if not device:
        return {}

    user_input = {}
    user_input["serial_number"] = device.serial_number
    user_input["host"] = device.host
    user_input["port"] = device.port
    user_input["sw_version"] = device.sw_version
    user_input["hw_version"] = device.hw_version

    return user_input


def validate_connection(host, port):
    """验证连接的辅助函数."""
    if not check_tcp_connection(host, port):
        raise ConnectionError("cannot_connect")

    return True


def check_tcp_connection(host, port) -> bool:
    """测试TCP连接是否成功."""

    result = False

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(2)

    try:
        # 尝试建立连接
        sock.connect((host, port))

        result = True
    except Exception:
        result = False
    finally:
        sock.close()

    return result


def get_error_message(messages: str) -> str:
    """整理错误类型."""
    if "cannot_connect" in messages:
        return "cannot_connect"

    if "invalid_host" in messages:
        return "invalid_host"

    if "timeout_connect" in messages:
        return "timeout_connect"

    if "already_configured" in messages:
        return "already_configured"

    if "already_configured_device" in messages:
        return "already_configured_device"

    if "already_in_progress" in messages:
        return "already_in_progress"

    if "unknown" in messages:
        return "unknown"

    return messages
