import logging
import asyncio
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfPower, UnitOfTime, PERCENTAGE
from homeassistant.helpers.restore_state import RestoreEntity
from .const import *
from .tcp_client import *
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback
from datetime import datetime
from .global_config import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """设置number实体."""
    entities = []

    number_entities = list(ENTITY_NUMBER_TYPES.keys())

    # SOC 相关数值实体 (百分比 0-100)
    soc_entities = [
        entity for entity in number_entities if "soc" in str(entity).lower()
    ]

    for number_id in soc_entities:
        min_val, max_val, step, enable = ENTITY_NUMBER_VALUES[number_id]
        entities.append(
            BatteryNumberEntity(
                hass,
                config_entry,
                number_id,
                PERCENTAGE,
                min_val,
                max_val,
                step,
                enable,
            )
        )

    # 功率实体
    power_entities = [
        entity for entity in number_entities if "power" in str(entity).lower()
    ]

    for number_id in power_entities:
        min_val, max_val, step, enable = ENTITY_NUMBER_VALUES[number_id]
        entities.append(
            BatteryNumberEntity(
                hass,
                config_entry,
                number_id,
                UnitOfPower.WATT,
                min_val,
                max_val,  # 假设最大功率 10kW
                step,
                enable,
            )
        )

    # 时间实体 (秒)
    timeout_entities = [
        entity for entity in number_entities if "time" in str(entity).lower()
    ]

    for number_id in timeout_entities:
        min_val, max_val, step, enable = ENTITY_NUMBER_VALUES[number_id]
        entities.append(
            BatteryNumberEntity(
                hass,
                config_entry,
                number_id,
                UnitOfTime.MINUTES,
                min_val,
                max_val,  # 最大1440
                step,  # 步长1min
                enable,
            )
        )

    async_add_entities(entities)


async def async_unload_entry(hass, config_entry) -> bool:
    """卸载number实体."""
    message = f"async_unload_entry: {config_entry.options}"

    _LOGGER.info(message)

    return True


class BatteryNumberEntity(NumberEntity, RestoreEntity):
    """number实体类."""

    def __init__(
        self,
        hass,
        config_entry,
        number_id,
        unit,
        min_value,
        max_value,
        step,
        enable,
    ) -> None:
        """初始化函数."""
        self._data_type_id = number_id
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_{number_id}"
        # self._attr_name = number_name
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_available = enable  # 初始化时是否可用
        self._operate = False
        self._attributes = {}
        self._attr_native_value = min_value  # 默认值
        self._attr_has_entity_name = True  # 关键属性1：声明使用实体名翻译模式
        self._attr_translation_key = number_id
        # 设备信息
        self._attr_device_info = GLOBAL_EQUIP_INFOS[config_entry.entry_id]

    async def async_added_to_hass(self):
        """添加到HA时恢复上一次状态."""
        # # 实体添加到HA时恢复状态
        # await super().async_added_to_hass()

        # # 恢复之前的状态
        # if (last_state := await self.async_get_last_state()) is not None:
        #     try:
        #         self._attr_native_value = float(last_state.state)
        #     except (ValueError, TypeError):
        #         self._attr_native_value = 0.0

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
        # 设置时不更新上报数据
        if self._operate:
            return

        # 根据id获得数据类型
        data_type = ENTITY_NUMBER_TYPES[self._data_type_id]

        # 根据属性名称对其赋值,RespondInfo
        respond_info = data

        data_info = respond_info.data

        update_data = getattr(data_info, data_type, None)

        if (update_data is not None) and (update_data != 0xFFFF):
            self._attr_native_value = update_data

            self._attributes["last_update"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            if update_data == -1:
                self._attr_available = False
            else:
                self._attr_available = True

            self.async_write_ha_state()  # 通知HA更新状态

    @property
    def native_value(self) -> float | None:
        """返回当前值."""
        return self._attr_native_value

    @callback
    def sync_update_value(self, value):
        """数据同步更新函数."""
        # 使用@callback修饰,可以避免异步调用报错
        self._attr_native_value = value

        # 值不同会强制刷新界面信息
        self._attributes["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.async_write_ha_state()  # 通知HA更新状态

    async def async_set_native_value(self, value: float):
        """数据更新函数."""

        # 操作的时候不给刷新页面值
        if self._operate:
            return

        try:
            self._operate = True

            # 设置之前的状态值
            last_value = self.native_value

            # 刷新到设置的值
            self.sync_update_value(value)

            # 根据id获得数据类型
            data_type = ENTITY_NUMBER_TYPES[self._data_type_id]

            # 根据属性名称对其赋值
            data_info = DataInfo()

            setattr(data_info, data_type, value)

            request_info = RequestInfo(code=0x6056, data=data_info)

            set_data = request_info.request_to_json_remove_FF()

            client = GLOBAL_TCP_CLIENTS[self._config_entry.entry_id]

            result = await client.async_set_data(data_type, value, set_data)

            if not result:
                await self.hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "message": f"{self.name} set value {value} fail",
                        "title": "set_data",
                    },
                )

                # TCP没有连接会立即返回错误
                if not client.connected:
                    await asyncio.sleep(2)

                self.sync_update_value(last_value)

        except Exception as e:
            message = "async_set_native_value: %s", e
            _LOGGER.error(message)
        finally:
            # 操作的时候不给刷新页面值
            self._operate = False
