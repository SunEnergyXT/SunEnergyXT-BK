from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sunEnergyXT.const import DOMAIN

pytestmark = pytest.mark.asyncio


def _create_entry() -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            "serial_number": "DCBDCCC00562",
            "host": "10.6.50.106",
            "port": 8000,
            "device_name": "SunEnergyXT BK",
            "hw_version": "BK215",
            "sw_version": "V1.5.7",
        },
        title="SunEnergyXT BK",
    )


async def test_setup_entry(hass, enable_custom_integrations):
    entry = _create_entry()
    entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.sunEnergyXT.tcp_client.TcpClient.async_connect",
            new=AsyncMock(),
        ),
        patch(
            "custom_components.sunEnergyXT.tcp_client.TcpClient.async_stop_client",
            new=AsyncMock(),
        ),
        patch(
            "custom_components.sunEnergyXT.coordinator.SunEnergyXTCoordinator.async_config_entry_first_refresh",
            new=AsyncMock(),
        ),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED


async def test_setup_entry_sets_runtime_data(hass, enable_custom_integrations):
    entry = _create_entry()
    entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.sunEnergyXT.tcp_client.TcpClient.async_connect",
            new=AsyncMock(),
        ),
        patch(
            "custom_components.sunEnergyXT.tcp_client.TcpClient.async_stop_client",
            new=AsyncMock(),
        ),
        patch(
            "custom_components.sunEnergyXT.coordinator.SunEnergyXTCoordinator.async_config_entry_first_refresh",
            new=AsyncMock(),
        ),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    runtime_data = entry.runtime_data
    assert runtime_data is not None
    assert runtime_data.client is not None
    assert runtime_data.coordinator is not None
    assert runtime_data.device_info is not None

    assert runtime_data.device_info["serial_number"] == "DCBDCCC00562"
    assert runtime_data.device_info["name"] == "SunEnergyXT BK"

    assert entry.entry_id in hass.data[DOMAIN]


async def test_unload_entry(hass, enable_custom_integrations):
    entry = _create_entry()
    entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.sunEnergyXT.tcp_client.TcpClient.async_connect",
            new=AsyncMock(),
        ),
        patch(
            "custom_components.sunEnergyXT.coordinator.SunEnergyXTCoordinator.async_config_entry_first_refresh",
            new=AsyncMock(),
        ),
        patch(
            "custom_components.sunEnergyXT.tcp_client.TcpClient.async_stop_client",
            new=AsyncMock(),
        ) as mock_stop_client,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state is ConfigEntryState.LOADED
        assert entry.entry_id in hass.data[DOMAIN]

        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()

    mock_stop_client.assert_awaited_once()
    assert entry.entry_id not in hass.data[DOMAIN]
    assert entry.state is ConfigEntryState.NOT_LOADED