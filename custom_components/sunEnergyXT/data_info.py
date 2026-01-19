from typing import Any
from dataclasses import dataclass, asdict
import json
from typing import Any, Dict
from dataclasses import dataclass


@dataclass
class RequestInfo:
    """请求信息类."""

    code: int
    data: "DataInfo"

    def request_to_json(self) -> str:
        """请求信息类转jason字符串函数."""
        return json.dumps(asdict(self), separators=(",", ":"))

    def request_to_json_remove_FF(self) -> str:
        """请求信息类转jason字符串函数,剔除初始化值为FFFF的变量."""

        def remove_ffff(d):
            # """递归删除值为0xFFFF的字段"""
            if isinstance(d, dict):
                return {k: remove_ffff(v) for k, v in d.items() if v != 0xFFFF}

            if isinstance(d, list):
                return [remove_ffff(item) for item in d]

            return d

        data_dict = asdict(self)
        filtered_dict = remove_ffff(data_dict)
        return json.dumps(filtered_dict, separators=(",", ":"))

    @classmethod
    def json_to_request(cls, json_str: str):
        """jason字符串转请求信息类函数."""

        # 从 JSON 字符串创建对象
        data = json.loads(json_str)

        if "data" in data and isinstance(data["data"], dict):
            # 需要给DataInfo的字段赋初始值
            data["data"] = DataInfo.dict_to_data(data["data"])

        return cls(**data)


@dataclass
class RespondInfo:
    """响应信息类."""

    code: int
    data: "DataInfo"

    def respond_to_json(self) -> str:
        """响应信息类转jason字符串函数."""
        return json.dumps(asdict(self), separators=(",", ":"))

    def request_to_json_remove_FF(self) -> str:
        """响应信息类转jason字符串函数,剔除初始化值为FFFF的变量."""

        def remove_ffff(d):
            # """递归删除值为0xFFFF的字段"""
            if isinstance(d, dict):
                return {k: remove_ffff(v) for k, v in d.items() if v != 0xFFFF}
            elif isinstance(d, list):
                return [remove_ffff(item) for item in d]
            else:
                return d

        data_dict = asdict(self)
        filtered_dict = remove_ffff(data_dict)
        return json.dumps(filtered_dict, separators=(",", ":"))

    @classmethod
    def json_to_respond(cls, json_str: str):
        """jason字符串转响应信息类函数."""

        # 从 JSON 字符串创建对象
        data = json.loads(json_str)

        if "data" in data and isinstance(data["data"], dict):
            # 需要给DataInfo的字段赋初始值
            data["data"] = DataInfo.dict_to_data(data["data"])

        return cls(**data)


@dataclass
class DataInfo:
    """数据信息类."""

    # switch
    t700_1: int = 0xFFFF
    t701_1: int = 0xFFFF
    t702_1: int = 0xFFFF
    t728: int = 0xFFFF
    t598: int = 0xFFFF

    # numbers
    t362: int = 0xFFFF
    t363: int = 0xFFFF
    t720: int = 0xFFFF
    t721: int = 0xFFFF
    t727: int = 0xFFFF
    t590: int = 0xFFFF
    t596: int = 0xFFFF
    t597: int = 0xFFFF

    # sensor
    t211: int = 0xFFFF
    t592: int = 0xFFFF
    t593: int = 0xFFFF
    t594: int = 0xFFFF
    t595: int = 0xFFFF
    t1001: int = 0xFFFF
    t1002: int = 0xFFFF
    t1003: int = 0xFFFF
    t1004: int = 0xFFFF

    t507: int = 0xFFFF
    t508: int = 0xFFFF
    t509: int = 0xFFFF
    t510: int = 0xFFFF
    t511: int = 0xFFFF
    t512: int = 0xFFFF
    t513: int = 0xFFFF
    t514: int = 0xFFFF

    t948: int = 0xFFFF
    t949: int = 0xFFFF
    t950: int = 0xFFFF
    t951: int = 0xFFFF
    t952: int = 0xFFFF
    t953: int = 0xFFFF
    t954: int = 0xFFFF
    t955: int = 0xFFFF

    def data_to_json(self) -> str:
        """数据信息类转jason字符串函数."""
        return json.dumps(asdict(self), separators=(",", ":"))

    @classmethod
    def json_to_data(cls, json_str: str):
        """jason字符串转数据信息类函数."""
        data = json.loads(json_str)
        return cls(**data)

    @classmethod
    def dict_to_data(cls, data_dict: Dict[str, Any]) -> "DataInfo":
        """dict字典转数据信息类函数."""
        return cls(**data_dict)


@dataclass
class DiagnosticInfo:
    """诊断数据信息类."""

    connection: str = ""
    reporttime: str = ""

    def diagnostic_to_json(self) -> str:
        """诊断数据类转jason字符串函数."""
        return json.dumps(asdict(self), separators=(",", ":"))

    @classmethod
    def json_to_diagnostic(cls, json_str: str):
        """jason字符串转诊断数据类函数."""
        data = json.loads(json_str)

        return cls(**data)


@dataclass
class MdnsDeiveInfo:
    """mdns发现设备信息类."""

    service_type: str = ""
    service_name: str = ""
    serial_number: str = ""
    host: str = ""
    port: int = 0
    sw_version: str = ""
    hw_version: str = ""

    def respond_to_json(self) -> str:
        """设备信息类转jason字符串函数."""
        return json.dumps(asdict(self), separators=(",", ":"))

    @classmethod
    def json_to_respond(cls, json_str: str):
        """jason字符串转设备信息类函数."""
        data = json.loads(json_str)

        return cls(**data)
