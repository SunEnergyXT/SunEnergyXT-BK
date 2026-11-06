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
                return {k: remove_ffff(v) for k, v in d.items() if v != 0xFFFFFFFF}

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
                return {k: remove_ffff(v) for k, v in d.items() if v != 0xFFFFFFFF}

            if isinstance(d, list):
                return [remove_ffff(item) for item in d]

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
    t700_1: int = 0xFFFFFFFF
    t701_1: int = 0xFFFFFFFF
    t702_1: int = 0xFFFFFFFF
    t728: int = 0xFFFFFFFF
    t598: int = 0xFFFFFFFF

    # numbers
    t362: int = 0xFFFFFFFF
    t363: int = 0xFFFFFFFF
    t720: int = 0xFFFFFFFF
    t721: int = 0xFFFFFFFF
    t727: int = 0xFFFFFFFF
    t590: int = 0xFFFFFFFF
    t596: int = 0xFFFFFFFF
    t597: int = 0xFFFFFFFF

    # sensor
    t211: int = 0xFFFFFFFF
    t592: int = 0xFFFFFFFF
    t593: int = 0xFFFFFFFF
    t594: int = 0xFFFFFFFF
    t595: int = 0xFFFFFFFF
    t1001: int = 0xFFFFFFFF
    t1002: int = 0xFFFFFFFF
    t1003: int = 0xFFFFFFFF
    t1004: int = 0xFFFFFFFF

    t507: int = 0xFFFFFFFF
    t508: int = 0xFFFFFFFF
    t509: int = 0xFFFFFFFF
    t510: int = 0xFFFFFFFF
    t511: int = 0xFFFFFFFF
    t512: int = 0xFFFFFFFF
    t513: int = 0xFFFFFFFF
    t514: int = 0xFFFFFFFF

    t948: int = 0xFFFFFFFF
    t949: int = 0xFFFFFFFF
    t950: int = 0xFFFFFFFF
    t951: int = 0xFFFFFFFF
    t952: int = 0xFFFFFFFF
    t953: int = 0xFFFFFFFF
    t954: int = 0xFFFFFFFF
    t955: int = 0xFFFFFFFF

    t33: int = 0xFFFFFFFF
    t34: int = 0xFFFFFFFF
    t49: int = 0xFFFFFFFF
    t66: int = 0xFFFFFFFF
    t710: int = 0xFFFFFFFF
    t711: int = 0xFFFFFFFF
    t701_4: int = 0xFFFFFFFF
    t702_4: int = 0xFFFFFFFF
    t50: int = 0xFFFFFFFF
    t62: int = 0xFFFFFFFF
    t63: int = 0xFFFFFFFF
    t64: int = 0xFFFFFFFF
    t65: int = 0xFFFFFFFF
    t812: int = 0xFFFFFFFF
    t813: int = 0xFFFFFFFF
    t814: int = 0xFFFFFFFF
    t815: int = 0xFFFFFFFF

    t220: int = 0xFFFFFFFF
    t233: int = 0xFFFFFFFF
    t246: int = 0xFFFFFFFF
    t259: int = 0xFFFFFFFF
    t836: int = 0xFFFFFFFF
    t849: int = 0xFFFFFFFF
    t862: int = 0xFFFFFFFF
    t875: int = 0xFFFFFFFF
    t586: int = 0xFFFFFFFF
    t537: int = 0xFFFFFFFF
    t536: int = 0xFFFFFFFF
    t545: int = 0xFFFFFFFF
    t544: int = 0xFFFFFFFF
    t553: int = 0xFFFFFFFF
    t552: int = 0xFFFFFFFF
    t561: int = 0xFFFFFFFF
    t560: int = 0xFFFFFFFF
    t569: int = 0xFFFFFFFF
    t568: int = 0xFFFFFFFF
    t970: int = 0xFFFFFFFF
    t969: int = 0xFFFFFFFF
    t978: int = 0xFFFFFFFF
    t977: int = 0xFFFFFFFF
    t986: int = 0xFFFFFFFF
    t985: int = 0xFFFFFFFF
    t994: int = 0xFFFFFFFF
    t993: int = 0xFFFFFFFF
    t475: int = 0xFFFFFFFF

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

    # 网络连接状态
    connection: str = ""
    # 数据更新时间
    reporttime: str = ""
    # 网络信号强度
    networkrssi: str = ""

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
