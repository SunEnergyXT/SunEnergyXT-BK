"""全局常量."""

DOMAIN = "sunEnergyXT"

# 配置项键名(switch)
# 电池系统切换本地模式开关 t598
WIFI_SYSTEM_LOCAL_COMM_ENABLE = "wifi_system_local_comm_enable"
# 充电模式开关 t700
WIFI_CHG_MODE_HM = "wifi_chg_mode_hm"
# 车充模式开关 t701
WIFI_CAR_CHG_MODE_HM = "wifi_car_chg_mode_hm"
# 家电模式开关 t702
WIFI_HOME_MODE_HM = "wifi_home_mode_hm"
# 车充盒车充模式下允许混合切换市电供电 t728
WIFI_CP_EV_AC_ACTIVE_SET = "wifi_cp_ev_ac_active_set"

# SwitchType显示类型映射
ENTITY_SWITCH_TYPES = {
    WIFI_SYSTEM_LOCAL_COMM_ENABLE: "t598",
    WIFI_CHG_MODE_HM: "t700_1",
    WIFI_CAR_CHG_MODE_HM: "t701_1",
    WIFI_HOME_MODE_HM: "t702_1",
    WIFI_CP_EV_AC_ACTIVE_SET: "t728",
}

# SwitchValue初始化值
ENTITY_SWITCH_VALUES = {
    WIFI_SYSTEM_LOCAL_COMM_ENABLE: (True),
    WIFI_CHG_MODE_HM: (False),
    WIFI_CAR_CHG_MODE_HM: (False),
    WIFI_HOME_MODE_HM: (False),
    WIFI_CP_EV_AC_ACTIVE_SET: (False),
}

# 配置项键名(number)
# 允许放电最低SOC t362
WIFI_CNFG_DISC_SOC_MIN = "wifi_cnfg_disc_soc_min"
# 允许充电最高SOCt 363
WIFI_CNFG_CHG_SOC_MAX = "wifi_cnfg_chg_soc_max"
# 车充盒家电模式下的放电截止SOC设置 t720
WIFI_CP_HA_DOD_MIN_SOC = "wifi_cp_ha_dod_min_soc"
# 车充盒车充模式下的放电截止SOC设置 t721
WIFI_CP_EV_DOD_MIN_SOC = "wifi_cp_ev_dod_min_soc"
# 车充盒充电模式下的充电截止SOC设置 t727
WIFI_CP_CHG_DOD_MAX_SOC = "wifi_cp_chg_dod_max_soc"
# 电池系统设定充电功率 t590
WIFI_SYS_CHG_SET_POWER = "wifi_sys_chg_set_power"
# 电池系统无输入输出自动关机超时时间 t596
WIFI_NO_INPUT_OUTPUT_TIMEOUT = "wifi_no_input_output_timeout"
# 电池系统到达DOD下限自动关机超时时间 t597
WIFI_INTO_DOD_TIMEOUT = "wifi_into_dod_timeout"

# NumberType显示类型映射
ENTITY_NUMBER_TYPES = {
    WIFI_CNFG_DISC_SOC_MIN: "t362",
    WIFI_CNFG_CHG_SOC_MAX: "t363",
    WIFI_CP_HA_DOD_MIN_SOC: "t720",
    WIFI_CP_EV_DOD_MIN_SOC: "t721",
    WIFI_CP_CHG_DOD_MAX_SOC: "t727",
    WIFI_SYS_CHG_SET_POWER: "t590",
    WIFI_NO_INPUT_OUTPUT_TIMEOUT: "t596",
    WIFI_INTO_DOD_TIMEOUT: "t597",
}

# NumberValue初始化值
ENTITY_NUMBER_VALUES = {
    WIFI_CNFG_DISC_SOC_MIN: (1, 20, 1, True),
    WIFI_CNFG_CHG_SOC_MAX: (70, 100, 1, True),
    WIFI_CP_HA_DOD_MIN_SOC: (5, 20, 1, False),
    WIFI_CP_EV_DOD_MIN_SOC: (5, 40, 1, False),
    WIFI_CP_CHG_DOD_MAX_SOC: (80, 100, 1, False),
    WIFI_SYS_CHG_SET_POWER: (0, 3600, 1, True),
    WIFI_NO_INPUT_OUTPUT_TIMEOUT: (15, 1440, 1, True),
    WIFI_INTO_DOD_TIMEOUT: (5, 1440, 1, True),
}

# 只读项键名(sensor)
# 剩余容量SOCt t211
WIFI_SOC = "wifi_soc"
# 主机真实剩余容量SOC t592
WIFI_B_ACTUAL_SOC = "wifi_b_actual_soc"
# 从机1真实剩余容量SOC t593
WIFI_B1_ACTUAL_SOC = "wifi_b1_actual_soc"
# 从机2真实剩余容量SOC t594
WIFI_B2_ACTUAL_SOC = "wifi_b2_actual_soc"
# 从机3真实剩余容量SOC t595
WIFI_B3_ACTUAL_SOC = "wifi_b3_actual_soc"
# 从机4真实剩余容量SOC t1001
WIFI_B4_ACTUAL_SOC = "wifi_b4_actual_soc"
# 从机5真实剩余容量SOC t1002
WIFI_B5_ACTUAL_SOC = "wifi_b5_actual_soc"
# 从机6真实剩余容量SOC t1005
WIFI_B6_ACTUAL_SOC = "wifi_b6_actual_soc"
# 从机7真实剩余容量SOC t1006
WIFI_B7_ACTUAL_SOC = "wifi_b7_actual_soc"
# 主机BMS硬件限制放电最低SOC t507
WIFI_MBMS_HW_LIMITED_DISC_SOC_MIN = "wifi_mbms_hw_limited_disc_soc_min"
# 主机BMS硬件限制充电最高SOC t508
WIFI_MBMS_HW_LIMITED_CHG_SOC_MAX = "wifi_mbms_hw_limited_chg_soc_max"
# 从机1BMS硬件限制放电最低SOC t509
WIFI_SBMS1_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms1_hw_limited_disc_soc_min"
# 从机1BMS硬件限制充电最高SOC t510
WIFI_SBMS1_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms1_hw_limited_chg_soc_max"
# 从机2BMS硬件限制放电最低SOC t511
WIFI_SBMS2_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms2_hw_limited_disc_soc_min"
# 从机2BMS硬件限制充电最高SOC t512
WIFI_SBMS2_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms2_hw_limited_chg_soc_max"
# 从机3BMS硬件限制放电最低SOC t513
WIFI_SBMS3_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms3_hw_limited_disc_soc_min"
# 从机3BMS硬件限制充电最高SOC t514
WIFI_SBMS3_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms3_hw_limited_chg_soc_max"
# 从机4BMS硬件限制放电最低SOC t948
WIFI_SBMS4_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms4_hw_limited_disc_soc_min"
# 从机4BMS硬件限制充电最高SOC t949
WIFI_SBMS4_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms4_hw_limited_chg_soc_max"
# 从机5BMS硬件限制放电最低SOC t950
WIFI_SBMS5_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms5_hw_limited_disc_soc_min"
# 从机5BMS硬件限制放电最低SOC t951
WIFI_SBMS5_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms5_hw_limited_chg_soc_max"
# 从机6BMS硬件限制放电最低SOC t952
WIFI_SBMS6_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms6_hw_limited_disc_soc_min"
# 从机6BMS硬件限制充电最高SOC t953
WIFI_SBMS6_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms6_hw_limited_chg_soc_max"
# 从机7BMS硬件限制放电最低SOC t954
WIFI_SBMS7_HW_LIMITED_DISC_SOC_MIN = "wifi_sbms7_hw_limited_disc_soc_min"
# 从机7BMS硬件限制充电最高SOC t955
WIFI_SBMS7_HW_LIMITED_CHG_SOC_MAX = "wifi_sbms7_hw_limited_chg_soc_max"

# SensorType显示类型映射
ENTITY_SENSOR_TYPES = {
    WIFI_SOC: "t211",
    WIFI_B_ACTUAL_SOC: "t592",
    WIFI_B1_ACTUAL_SOC: "t593",
    WIFI_B2_ACTUAL_SOC: "t594",
    WIFI_B3_ACTUAL_SOC: "t595",
    WIFI_B4_ACTUAL_SOC: "t1001",
    WIFI_B5_ACTUAL_SOC: "t1002",
    WIFI_B6_ACTUAL_SOC: "t1003",
    WIFI_B7_ACTUAL_SOC: "t1004",
    WIFI_MBMS_HW_LIMITED_DISC_SOC_MIN: "t507",
    WIFI_MBMS_HW_LIMITED_CHG_SOC_MAX: "t508",
    WIFI_SBMS1_HW_LIMITED_DISC_SOC_MIN: "t509",
    WIFI_SBMS1_HW_LIMITED_CHG_SOC_MAX: "t510",
    WIFI_SBMS2_HW_LIMITED_DISC_SOC_MIN: "t511",
    WIFI_SBMS2_HW_LIMITED_CHG_SOC_MAX: "t512",
    WIFI_SBMS3_HW_LIMITED_DISC_SOC_MIN: "t513",
    WIFI_SBMS3_HW_LIMITED_CHG_SOC_MAX: "t514",
    WIFI_SBMS4_HW_LIMITED_DISC_SOC_MIN: "t948",
    WIFI_SBMS4_HW_LIMITED_CHG_SOC_MAX: "t949",
    WIFI_SBMS5_HW_LIMITED_DISC_SOC_MIN: "t950",
    WIFI_SBMS5_HW_LIMITED_CHG_SOC_MAX: "t951",
    WIFI_SBMS6_HW_LIMITED_DISC_SOC_MIN: "t952",
    WIFI_SBMS6_HW_LIMITED_CHG_SOC_MAX: "t953",
    WIFI_SBMS7_HW_LIMITED_DISC_SOC_MIN: "t954",
    WIFI_SBMS7_HW_LIMITED_CHG_SOC_MAX: "t955",
}

# 只读项键名(sensor)
# 连接状态
WIFI_CONNECTION = "wifi_connection"
# 上一次刷新时间
WIFI_REPORT_TIME = "wifi_update_time"

# diagnosticType显示类型映
ENTITY_DIAGNOSTIC_TYPES = {
    WIFI_CONNECTION: "connection",
    WIFI_REPORT_TIME: "reporttime",
}
