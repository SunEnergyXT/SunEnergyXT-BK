from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from custom_components.sunEnergyXT.sensor import SunEnergyXTSensor, async_setup_entry

pytestmark = pytest.mark.asyncio


class DummyCoordinator:
    def __init__(self, data: dict, available_points: set[str]) -> None:
        self.data = data
        self.available_points = available_points
        self._listeners: list = []

    def register_new_point_listener(self, listener):
        self._listeners.append(listener)

        def _remove():
            if listener in self._listeners:
                self._listeners.remove(listener)

        return _remove


class DummyRuntimeData:
    def __init__(self, coordinator, device_info) -> None:
        self.coordinator = coordinator
        self.device_info = device_info


class DummyEntry:
    def __init__(self, serial_number: str, runtime_data) -> None:
        self.data = {"serial_number": serial_number}
        self.runtime_data = runtime_data
        self._unload_callbacks = []

    def async_on_unload(self, callback):
        self._unload_callbacks.append(callback)


async def test_sensor_setup_creates_only_available_entities():
    coordinator = DummyCoordinator(
        data={
            "t211": 100,
            "t590": 3600,
            "t701_4": 1200,
            "t475": 55,
        },
        available_points={"t211", "t590"},
    )

    entry = DummyEntry(
        serial_number="DCBDCCC00562",
        runtime_data=DummyRuntimeData(
            coordinator=coordinator,
            device_info={"identifiers": {("sunEnergyXT", "DCBDCCC00562")}},
        ),
    )

    added_entities: list[SunEnergyXTSensor] = []

    def async_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_entry(None, entry, async_add_entities)

    created_points = {entity._point for entity in added_entities}

    assert "t211" in created_points
    assert "t590" in created_points

    assert "t701_4" not in created_points
    assert "t475" not in created_points


async def test_sensor_setup_adds_new_entities_when_new_points_become_available():
    coordinator = DummyCoordinator(
        data={
            "t211": 100,
            "t590": 3600,
            "t701_4": 1200,
        },
        available_points={"t211"},
    )

    entry = DummyEntry(
        serial_number="DCBDCCC00562",
        runtime_data=DummyRuntimeData(
            coordinator=coordinator,
            device_info={"identifiers": {("sunEnergyXT", "DCBDCCC00562")}},
        ),
    )

    added_entities: list[SunEnergyXTSensor] = []

    def async_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_entry(None, entry, async_add_entities)

    created_points = {entity._point for entity in added_entities}
    assert created_points == {"t211"}

    coordinator.available_points.update({"t590", "t701_4"})

    for listener in coordinator._listeners:
        listener()

    created_points = {entity._point for entity in added_entities}
    assert "t211" in created_points
    assert "t590" in created_points
    assert "t701_4" in created_points


async def test_sensor_native_value_applies_multiplier_and_precision():
    coordinator = DummyCoordinator(
        data={"t475": 55},
        available_points={"t475"},
    )

    entity = SunEnergyXTSensor(
        coordinator=coordinator,
        serial_number="DCBDCCC00562",
        device_info={"identifiers": {("sunEnergyXT", "DCBDCCC00562")}},
        description=MagicMock(
            key="t475",
            name="Network RSSI",
            native_unit_of_measurement="dB",
            device_class=None,
            state_class=None,
            entity_category=None,
            suggested_display_precision=0,
            multiplier=-1,
            offset=0.0,
        ),
    )

    assert entity.native_value == -55
    assert entity.available is True