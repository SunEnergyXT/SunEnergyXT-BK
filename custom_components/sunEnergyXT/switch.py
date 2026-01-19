import logging
import asyncio
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.restore_state import RestoreEntity
from .const import *
from .tcp_client import *
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback
from datetime import datetime
from .global_config import *


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """设置开关实体."""
    entities = []

    switch_entities = list(ENTITY_SWITCH_TYPES.keys())

    for switch_id in switch_entities:
        enable = ENTITY_SWITCH_VALUES[switch_id]
        entities.append(BatterySwitchEntity(hass, config_entry, switch_id, enable))

    async_add_entities(entities)


async def async_unload_entry(hass, config_entry) -> bool:
    """卸载开关实体."""
    message = f"async_unload_entry: {config_entry.options}"

    _LOGGER.info(message)

    return True


class BatterySwitchEntity(SwitchEntity, RestoreEntity):
    """开关实体类."""

    def __init__(self, hass, config_entry, switch_id, enable) -> None:
        """开关实体类初始化函数."""
        self._data_type_id = switch_id
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_{switch_id}"
        # self._attr_name = switch_name
        self._attr_is_on = False  # 默认关闭
        self._operate = False
        self._attr_available = enable
        self._attributes = {}
        self._attr_has_entity_name = True  # 关键属性1：声明使用实体名翻译模式
        self._attr_translation_key = switch_id

        # 设备信息
        self._attr_device_info = GLOBAL_EQUIP_INFOS[config_entry.entry_id]

        # self._attr_device_info = cast(
        #     DeviceInfo,
        #     {
        #         "identifiers": {(DOMAIN, config_entry.entry_id)},
        #         "name": "BatteryDevice",
        #         "manufacturer": "HighPower",
        #         # "model": "v1.0",
        #         "serial_number": f"{config_entry.entry_id}",
        #         # "connections": [("mac", "a4:c1:38:46:7e:19")],
        #     },
        # )

    async def async_added_to_hass(self):
        """添加到HA时恢复初始状态函数."""
        # # 实体添加到HA时恢复状态
        # await super().async_added_to_hass()

        # if (last_state := await self.async_get_last_state()) is not None:
        #     # 初始值等于最后一次状态值
        #     self._attr_is_on = last_state.state == "on"

        # 注册监听数据更新事件
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"p200_data_update_{self._config_entry.entry_id}",
                self._handle_data_update,
            )
        )

    @callback
    def _handle_data_update(self, data):
        # 设置时不更新数据
        if self._operate:
            return

        # 根据id获得数据类型
        data_type = ENTITY_SWITCH_TYPES[self._data_type_id]

        # 根据属性名称对其赋值,RespondInfo
        respond_info = data

        data_info = respond_info.data

        update_data = getattr(data_info, data_type, None)

        if (update_data is not None) and (update_data != 0xFFFF):
            if update_data == 1:
                self._attr_is_on = True
            else:
                self._attr_is_on = False

            self._attributes["last_update"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            if update_data == -1:
                self._attr_available = False
            else:
                self._attr_available = True

            self.async_write_ha_state()  # 通知HA更新状态

    @property
    def is_on(self) -> bool | None:
        """返回开关状态."""
        return self._attr_is_on

    @callback
    def sync_update_value(self, value):
        """同步更新开关状态函数."""
        # 使用@callback修饰,可以避免异步调用报错
        self._attr_is_on = value

        # 值不同会强制刷新界面信息
        self._attributes["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.async_write_ha_state()  # 通知HA更新状态

    async def async_turn_on(self, **kwargs):
        """开关打开函数."""

        # 操作的时候不给刷新页面值
        if self._operate:
            return

        try:
            self._operate = True

            # 打开开关并通知界面刷新
            self.sync_update_value(True)

            # 根据id获得数据类型
            data_type = ENTITY_SWITCH_TYPES[self._data_type_id]

            # 根据属性名称对其赋值
            data_info = DataInfo()

            setattr(data_info, data_type, 1)

            request_info = RequestInfo(code=0x6056, data=data_info)

            set_data = request_info.request_to_json_remove_FF()

            client = GLOBAL_TCP_CLIENTS[self._config_entry.entry_id]

            result = await client.async_set_data(data_type, 1, set_data)

            if not result:
                await self.hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {"message": f"{self.name} turn on fail", "title": "set_data"},
                )

                # 防止操作太快,界面刷新不过来
                if not client.connected:
                    await asyncio.sleep(2)

                self.sync_update_value(False)
        except Exception as e:
            message = "async_turn_on: %s", e
            _LOGGER.error(message)
        finally:
            # 操作的时候不给刷新页面值
            self._operate = False

    async def async_turn_off(self, **kwargs):
        """开关关闭函数."""
        # 操作的时候不给刷新页面值
        if self._operate:
            return

        try:
            self._operate = True

            # 关闭开关并通知界面刷新
            self.sync_update_value(False)

            # 根据id获得数据类型
            data_type = ENTITY_SWITCH_TYPES[self._data_type_id]

            # 根据属性名称对其赋值
            data_info = DataInfo()

            setattr(data_info, data_type, 0)

            request_info = RequestInfo(code=0x6056, data=data_info)

            set_data = request_info.request_to_json_remove_FF()

            client = GLOBAL_TCP_CLIENTS[self._config_entry.entry_id]

            result = await client.async_set_data(data_type, 0, set_data)

            if not result:
                await self.hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {"message": f"{self.name} turn off fail", "title": "set_data"},
                )

                if not client.connected:
                    await asyncio.sleep(2)

                self.sync_update_value(True)

        except Exception as e:
            message = "async_turn_off: %s", e
            _LOGGER.error(message)
        finally:
            # 操作的时候不给刷新页面值
            self._operate = False
