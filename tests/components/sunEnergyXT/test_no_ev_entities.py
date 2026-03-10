from __future__ import annotations

import pytest

from custom_components.sunEnergyXT.sensor import async_setup_entry as async_setup_sensor_entry
from custom_components.sunEnergyXT.switch import async_setup_entry as async_setup_switch_entry

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
    def __init__(self, coordinator, client, device_info) -> None:
        self.coordinator = coordinator
        self.client = client
        self.device_info = device_info


class DummyClient:
    async def async_set_data(self, *args, **kwargs):
        return True


class DummyEntry:
    def __init__(self, serial_number: str, runtime_data) -> None:
        self.data = {"serial_number": serial_number}
        self.runtime_data = runtime_data
        self._unload_callbacks = []

    def async_on_unload(self, callback):
        self._unload_callbacks.append(callback)


async def test_no_ev_sensor_entities_without_ev_points():
    coordinator = DummyCoordinator(
        data={
            "t211": 100,
            "t590": 3600,
            "t592": 100,
        },
        available_points={"t211", "t590", "t592"},
    )

    entry = DummyEntry(
        serial_number="DCBDCCC00562",
        runtime_data=DummyRuntimeData(
            coordinator=coordinator,
            client=DummyClient(),
            device_info={"identifiers": {("sunEnergyXT", "DCBDCCC00562")}},
        ),
    )

    added_entities = []

    def async_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_sensor_entry(None, entry, async_add_entities)

    created_points = {entity._point for entity in added_entities}

    assert "t211" in created_points
    assert "t590" in created_points
    assert "t592" in created_points

    assert "t701_4" not in created_points  # EV Mode Power
    assert "t711" not in created_points    # AC input power
    assert "t710" not in created_points    # AC charging energy


async def test_no_ev_switch_entities_without_ev_points():
    coordinator = DummyCoordinator(
        data={
            "t598": 1,
        },
        available_points={"t598"},
    )

    entry = DummyEntry(
        serial_number="DCBDCCC00562",
        runtime_data=DummyRuntimeData(
            coordinator=coordinator,
            client=DummyClient(),
            device_info={"identifiers": {("sunEnergyXT", "DCBDCCC00562")}},
        ),
    )

    added_entities = []

    def async_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_switch_entry(None, entry, async_add_entities)

    created_points = {entity._point for entity in added_entities}

    assert "t598" in created_points

    assert "t701_1" not in created_points  # EV mode switch
    assert "t728" not in created_points    # AC mix in EV mode