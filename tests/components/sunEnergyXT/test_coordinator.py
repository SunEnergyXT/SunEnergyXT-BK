from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from custom_components.sunEnergyXT.coordinator import SunEnergyXTCoordinator

pytestmark = pytest.mark.asyncio


class DummyClient:
    def __init__(self) -> None:
        self.async_send_json = AsyncMock()
        self.read_messages = AsyncMock()


async def test_coordinator_marks_point_available_only_after_two_valid_hits(hass):
    client = DummyClient()
    coordinator = SunEnergyXTCoordinator(hass, client)

    # Erster Poll: valide Werte zum ersten Mal gesehen
    client.read_messages.side_effect = [
        [{"code": 0x6052, "data": {"t211": 100, "t590": 3600}}],
        [],
        [],
        # Zweiter Poll: dieselben Werte erneut valide
        [{"code": 0x6052, "data": {"t211": 99, "t590": 3600}}],
        [],
        [],
    ]

    first_data = await coordinator._async_update_data()
    assert first_data["t211"] == 100
    assert first_data["t590"] == 3600

    assert "t211" not in coordinator.available_points
    assert "t590" not in coordinator.available_points

    second_data = await coordinator._async_update_data()
    assert second_data["t211"] == 99
    assert second_data["t590"] == 3600

    assert "t211" in coordinator.available_points
    assert "t590" in coordinator.available_points


async def test_coordinator_ignores_invalid_values(hass):
    client = DummyClient()
    coordinator = SunEnergyXTCoordinator(hass, client)

    client.read_messages.side_effect = [
        [{"code": 0x6052, "data": {"t211": -1, "t475": None, "t592": 100}}],
        [],
        [],
        [{"code": 0x6052, "data": {"t211": -1, "t475": "", "t592": 100}}],
        [],
        [],
    ]

    await coordinator._async_update_data()
    await coordinator._async_update_data()

    assert "t211" not in coordinator.available_points
    assert "t475" not in coordinator.available_points
    assert "t592" in coordinator.available_points


async def test_coordinator_calls_listener_for_new_points(hass):
    client = DummyClient()
    coordinator = SunEnergyXTCoordinator(hass, client)

    listener = AsyncMock()

    called = {"count": 0}

    def sync_listener() -> None:
        called["count"] += 1

    remove_listener = coordinator.register_new_point_listener(sync_listener)

    client.read_messages.side_effect = [
        [{"code": 0x6052, "data": {"t211": 100}}],
        [],
        [],
        [{"code": 0x6052, "data": {"t211": 99}}],
        [],
        [],
    ]

    # Erster Poll: noch kein available point
    await coordinator._async_update_data()
    assert called["count"] == 0

    # Zweiter Poll: t211 wird verfügbar -> Listener wird aufgerufen
    await coordinator._async_update_data()
    assert called["count"] == 1

    remove_listener()