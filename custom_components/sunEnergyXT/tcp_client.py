import asyncio
import logging
import time
from datetime import datetime
from homeassistant.helpers.dispatcher import async_dispatcher_send
from .const import *
from .data_info import *
import queue

_LOGGER = logging.getLogger(__name__)


class TcpClient:
    """tcp客户端连接处理类."""

    def __init__(self, hass, entry) -> None:
        """tcp初始化函数."""
        self.hass = hass
        self.host = entry.data["host"]
        self.port = entry.data["port"]
        self.entry_id = entry.entry_id
        self.serial_number = entry.data["serial_number"]
        self.reader = None
        self.writer = None
        self.listen_data_task = None
        self.check_connect_task = None
        self.connected = False
        self.checked = False
        self.delay = 5
        self.data = queue.Queue()  # 存储从服务器接收的数据
        self.last_time = datetime.now()

    async def async_connect(self):
        """建立TCP连接并启动数据监听任务."""
        try:
            # 如果已有连接，先断开
            await self.async_disconnect()

            # 启动连接检查任务
            self.checked = True

            # 失败后尝试连接不需要重复开启监听
            if self.check_connect_task is None:
                self.check_connect_task = asyncio.create_task(
                    self.async_check_connect(), name="p200_check_connect_task"
                )

            # 建立TCP连接,需要超时机制
            # self.reader, self.writer = await asyncio.open_connection(
            #     self.host, self.port
            # )

            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), timeout=2.0
            )

            self.connected = True

            self.last_time = datetime.now()

            await self.async_update_diagnostics("connected")

            # 启动数据接收任务
            self.listen_data_task = None

            self.listen_data_task = asyncio.create_task(
                self.async_listen_data(), name="p200_listen_data_task"
            )

            message = f"connect to{self.host}:{self.port}"

            _LOGGER.info(message)

        except Exception as e:
            message = f"connect to {self.host} {self.port}" + ":  %s", e
            _LOGGER.error(message)
            await self.async_disconnect()

    async def async_disconnect(self):
        """断开TCP连接."""

        self.connected = False

        await self.async_update_diagnostics("connected")

        # 取消监听任务
        if self.listen_data_task is not None and not self.listen_data_task.done():
            try:
                self.listen_data_task.cancel()

                await asyncio.wait_for(self.listen_data_task, timeout=self.delay)
            except (asyncio.CancelledError, TimeoutError):
                pass  # 需要捕获取消错误,无法转化为异常
            except Exception as e:
                message = "async_disconnect_isten_data_task_error: %s", e
                _LOGGER.error(message)
            finally:
                self.listen_data_task = None

        # 关闭TCP连接
        if self.writer is not None:
            try:
                self.writer.close()

                await asyncio.wait_for(self.writer.wait_closed(), timeout=self.delay)
            except (TimeoutError, Exception) as e:
                message = "async_disconnect_writer_error: %s", e
                _LOGGER.error(message)
            finally:
                self.writer = None
                self.reader = None

    async def async_send_data(self, data: str) -> bool:
        """TCP发送数据函数."""

        if not self.connected or not self.writer:
            message = "not connected, cannot send data"
            _LOGGER.error(message)
            return False

        try:
            ascii_bytes = data.encode("ascii", errors="ignore")

            message = f"{self.serial_number} send_data:{ascii_bytes}"

            _LOGGER.info(message)

            self.writer.write(ascii_bytes)

            await self.writer.drain()
        except Exception as e:
            message = "async_send_data_error: %s", e
            _LOGGER.error(message)
            await self.async_reconnect()
            return False

        return True

    async def async_set_data(
        self, data_type: str, data_value: int, set_data: str
    ) -> bool:
        """TCP数据设置函数."""

        # 清除原先存储的数据
        self.data.queue.clear()

        result = await self.async_send_data(set_data)

        if not result:
            return False

        timeout = 2

        start_time = time.monotonic()

        while True:
            if time.monotonic() - start_time > timeout:
                break

            try:
                while not self.data.empty():
                    respond_info = self.data.get()

                    respond_code = getattr(respond_info, "code", None)

                    respond_data = getattr(respond_info, "data", None)

                    if respond_data is not None:
                        respond_value = getattr(respond_data, data_type, None)

                    if respond_code is not None and respond_value is not None:
                        # 返回值为0为成功
                        if respond_code == 0x6057 and respond_value == 0:
                            return True

            except Exception as e:
                message = "async_set_data_error: %s", e
                _LOGGER.error(message)

            await asyncio.sleep(0.1)

        return False

    async def async_listen_data(self):
        """TCP数据监听函数."""

        # 持续监听来自TCP服务器的数据
        while self.connected:
            try:
                if self.reader is not None:
                    # 根据你的TCP服务器数据格式进行调整,此处会一直等待接收数据
                    data = await self.reader.read(1024)

                if not data:
                    message = f"{self.serial_number} disconnect"
                    _LOGGER.error(message)
                    break  # 连接已关闭

                message = f"{self.serial_number} receive_data:{data}"

                _LOGGER.info(message)

                # 解析数据，这里假设服务器发送JSON格式的SOC信息
                decoded_data = data.decode("ascii", errors="ignore")

                if decoded_data == "":
                    continue

                if "xaa" in decoded_data.lower():
                    continue

                if "code" not in decoded_data.lower():
                    continue

                if not decoded_data.lower().startswith('{"code":'):
                    continue

                count_code = decoded_data.lower().count("code")

                if count_code != 1:
                    continue

                respond_info = RespondInfo.json_to_respond(decoded_data)

                # 设置响应S
                if respond_info.code == 0x6057:
                    self.data.put(respond_info)

                # 数据上报
                if respond_info.code in {0x6052, 0x6055}:
                    await self.async_update_diagnostics("reporttime")
                    await self.async_update_entities(respond_info)

                self.last_time = datetime.now()
            except Exception as e:
                message = "async_listen_data_error: %s", e
                _LOGGER.error(message)
                self.connected = False
                break

        # 连接断开后尝试重连
        await self.async_reconnect()

    async def async_check_connect(self):
        """TCP连接状态检查函数."""
        while self.checked:
            try:
                # 延时
                await asyncio.sleep(self.delay)

                # 判断超时后重新进行连接
                current_time = datetime.now()

                time_diff = abs((current_time - self.last_time).total_seconds())

                if time_diff > 60:
                    await self.async_disconnect()
                    self.last_time = datetime.now()

                await self.async_update_diagnostics("connected")

                if self.connected:
                    continue

                await self.async_connect()

            except Exception as e:
                message = "async_check_connect_error: %s", e
                _LOGGER.error(message)
                self.connected = False

    async def async_update_entities(self, data):
        """传感器实体更新状态函数."""
        # 通过Home Assistant的事件系统触发实体更新
        # 只能被通过 async_dispatcher_connect() 注册的特定监听器接收
        # 当其他地方发送这个信号时，_handle_data_update会被调用
        async_dispatcher_send(
            self.hass,
            f"p200_data_update_{self.entry_id}",
            data,  # 可选的参数
        )

    async def async_update_diagnostics(self, flag):
        """传感器诊断实体更新函数."""

        connect_state = "connected" if self.connected else "disconnected"

        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if flag == "connected":
            diagnostics_info = DiagnosticInfo(connection=connect_state)
        else:
            diagnostics_info = DiagnosticInfo(reporttime=report_time)

        # """通知诊断传感器实体更新状态"""
        async_dispatcher_send(
            self.hass,
            f"p200_diagnostic_update_{self.entry_id}",
            diagnostics_info,  # 可选的参数
        )

    async def async_reconnect(self):
        """TCP断线重连函数."""

        # """实现断线重连逻辑"""
        self.connected = False

        # 如果不是主动断开，尝试重连
        if not self.listen_data_task or self.listen_data_task.cancelled():
            return

        # 延时
        await asyncio.sleep(self.delay)

        if not self.listen_data_task.cancelled():
            await self.async_connect()

    async def async_stop_client(self):
        """TCP客户端停止函数."""

        self.checked = False

        await self.async_disconnect()

        # 取消状态检查任务
        if self.check_connect_task is not None and not self.check_connect_task.done():
            try:
                self.check_connect_task.cancel()

                await asyncio.wait_for(self.check_connect_task, timeout=self.delay)
            except (asyncio.CancelledError, TimeoutError):
                pass  # 需要捕获取消错误,无法转化为异常
            except Exception as e:
                message = "async_stop_client_error: %s", e
                _LOGGER.error(message)
            finally:
                self.check_connect_task = None
