import logging
from homeassistant.components.sensor import EntityCategory, SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import *
from homeassistant.components.sensor import SensorDeviceClass
from datetime import datetime
from .global_config import *
from .util import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """设置传感器实体."""
    entities = []

    # 创建SOC传感器实体
    sensor_entities = list(ENTITY_SENSOR_TYPES.keys())

    for sensor_id in sensor_entities:
        unit_type, device_type, data_factor = ENTITY_SENSOR_VALUES[sensor_id]

        data_unit = get_data_unit(unit_type)

        device_class = get_device_class(device_type)

        entities.append(
            BatterySensorEntity(
                hass, config_entry, sensor_id, data_unit, device_class, data_factor
            )
        )

    # 创建诊断实体
    diagnostic_entities = list(ENTITY_DIAGNOSTIC_TYPES.keys())

    for sensor_id in diagnostic_entities:
        default_value = ENTITY_DIAGNOSTIC_VALUES[sensor_id]

        entities.append(
            BatteryDiagnosticEntity(hass, config_entry, sensor_id, default_value)
        )

    async_add_entities(entities)


async def async_unload_entry(hass, config_entry) -> bool:
    """卸载传感器实体."""
    message = f"async_unload_entry: {config_entry.options}"

    _LOGGER.info(message)

    return True


class BatterySensorEntity(SensorEntity):
    """soc传感器类."""

    def __init__(
        self, hass, config_entry, sensor_id, data_unit, device_class, data_factor
    ) -> None:
        """初始化函数."""
        self._data_type_id = sensor_id
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_id}"
        # self._attr_name = sensor_name
        # self._state = 0
        self._attributes = {}
        self._attr_native_value = 0
        # self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_device_class = device_class  # 变量类型
        self._attr_native_unit_of_measurement = data_unit  # 单位设置为百分比
        # self._attr_state_class = "measurement"  # 状态类型为测量值
        self._attr_state_class = get_entity_state_class(sensor_id)  # 状态类型为测量值
        self._data_factor = data_factor  # 换算
        self._data_precision = decimal_places_from_string(data_factor)  # 小数位数
        self._attr_suggested_display_precision = self._data_precision  # 显示精度
        self._attr_available = False
        self._attr_has_entity_name = True  # 声明使用实体名翻译模式
        self.translation_key = sensor_id  # 声明使用实体名翻译ID
        # 设备信息
        self._attr_device_info = GLOBAL_EQUIP_INFOS[config_entry.entry_id]

    @property
    def state(self):
        """返回当前状态值."""
        # return self._state
        return self._attr_native_value

    @property
    def unit_of_measurement(self):
        """返回单位."""
        return self._attr_native_unit_of_measurement

    @property
    def device_class(self):
        """设置设备类别."""
        return self._attr_device_class

    @property
    def extra_state_attributes(self):
        """返回额外属性."""
        return self._attributes

    async def async_added_to_hass(self):
        """实体被添加到HA时初始状态函数."""
        # 当实体被添加到HomeAssistant时调用,注册监听数据更新事件
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"data_update_{self._config_entry.entry_id}",
                self._handle_data_update,
            )
        )

    @callback
    def _handle_data_update(self, data):
        # 根据id获得数据类型
        data_type = ENTITY_SENSOR_TYPES[self._data_type_id]

        # 根据属性名称对其赋值,RespondInfo
        respond_info = data

        data_info = respond_info.data

        update_data = getattr(data_info, data_type, None)

        if (update_data is not None) and (update_data != 0xFFFFFFFF):
            # 判断是否可用,如果是加热状态,还需要根据SOC来判断
            available = get_entity_available(data_type, data_info, self._data_factor)

            self._attr_available = available

            if self._attr_available:
                # 根据换算计算值
                update_data = get_data_value(update_data, self._data_factor)
                # self._state = update_data
                self._attr_native_value = update_data

            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._attributes["last_update"] = update_time

            self.async_write_ha_state()  # 通知HA更新状态


class BatteryDiagnosticEntity(SensorEntity):
    """传感器诊断类."""

    def __init__(self, hass, config_entry, sensor_id, default_value) -> None:
        """初始化函数."""
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._data_type_id = sensor_id
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_id}"
        # self._attr_name = sensor_name
        self._attr_device_class = None
        self._attr_options = []  # 空列表表示不限制选项
        self._attr_native_value = default_value
        self._attributes = {}
        self._attr_available = True
        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_id
        self._attr_device_info = GLOBAL_EQUIP_INFOS[config_entry.entry_id]

    @property
    def state(self):
        """返回当前状态值."""
        return self._attr_native_value

    @property
    def device_class(self):
        """设备类别."""
        return self._attr_device_class

    @property
    def extra_state_attributes(self):
        """返回额外属性."""
        return self._attributes

    async def async_added_to_hass(self):
        """添加到HA时设置初始状态函数."""
        # 当实体被添加到HomeAssistant时调用,注册监听数据更新事件
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"diagnostic_update_{self._config_entry.entry_id}",
                self._handle_data_update,
            )
        )

    @callback
    def _handle_data_update(self, data):
        # 根据id获得数据类型
        data_type = ENTITY_DIAGNOSTIC_TYPES[self._data_type_id]

        # 根据属性名称对其赋值
        diagnostics_info = data

        update_data = getattr(diagnostics_info, data_type, None)

        if (update_data is not None) and (update_data != ""):
            self._attr_native_value = update_data

            self._attributes["last_update"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.async_write_ha_state()  # 通知HA更新状态
