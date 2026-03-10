from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sunEnergyXT.const import DOMAIN
from custom_components.sunEnergyXT.tcp_client import TcpClient

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


async def test_extract_json_messages_handles_multiple_frames(hass):
    entry = _create_entry()
    client = TcpClient(hass, entry)

    chunk = (
        '{"code":24658,"data":{"t211":100}}'
        '{"code":24661,"data":{"t592":100}}'
    )

    messages = client._extract_json_messages(chunk)

    assert len(messages) == 2
    assert messages[0] == '{"code":24658,"data":{"t211":100}}'
    assert messages[1] == '{"code":24661,"data":{"t592":100}}'
    assert client._buffer == ""


async def test_extract_json_messages_keeps_incomplete_frame_in_buffer(hass):
    entry = _create_entry()
    client = TcpClient(hass, entry)

    chunk = (
        '{"code":24658,"data":{"t211":100}}'
        '{"code":24661,"data":{"t592":100}'
    )

    messages = client._extract_json_messages(chunk)

    assert len(messages) == 1
    assert messages[0] == '{"code":24658,"data":{"t211":100}}'
    assert client._buffer == '{"code":24661,"data":{"t592":100}'


async def test_extract_json_messages_completes_buffered_frame_on_next_chunk(hass):
    entry = _create_entry()
    client = TcpClient(hass, entry)

    first_chunk = (
        '{"code":24658,"data":{"t211":100}}'
        '{"code":24661,"data":{"t592":100}'
    )
    second_chunk = "}"

    first_messages = client._extract_json_messages(first_chunk)
    second_messages = client._extract_json_messages(second_chunk)

    assert len(first_messages) == 1
    assert len(second_messages) == 1
    assert second_messages[0] == '{"code":24661,"data":{"t592":100}}'
    assert client._buffer == ""


async def test_parse_json_message_handles_malformed_unk_code_key(hass):
    entry = _create_entry()
    client = TcpClient(hass, entry)

    raw_message = '{"code":-3,"data":{""unk code":24656}}'

    parsed = client._parse_json_message(raw_message)

    assert parsed is not None
    assert parsed["code"] == -3
    assert parsed["data"] == {"unk code": 24656}