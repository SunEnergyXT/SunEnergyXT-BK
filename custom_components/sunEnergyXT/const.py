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
    WIFI_CNFG_DISC_SOC_MIN: (1, 20, 1, "%", True),
    WIFI_CNFG_CHG_SOC_MAX: (70, 100, 1, "%", True),
    WIFI_CP_HA_DOD_MIN_SOC: (5, 20, 1, "%", False),
    WIFI_CP_EV_DOD_MIN_SOC: (5, 40, 1, "%", False),
    WIFI_CP_CHG_DOD_MAX_SOC: (80, 100, 1, "%", False),
    WIFI_SYS_CHG_SET_POWER: (0, 3600, 1, "W", False),
    WIFI_NO_INPUT_OUTPUT_TIMEOUT: (15, 1440, 1, "min", True),
    WIFI_INTO_DOD_TIMEOUT: (5, 1440, 1, "min", True),
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
# 总输入功率 t33
WIFI_INPUTPOWER_TOTAL = "wifi_inputpower_total"
# 总输出功率 t34
WIFI_OUTPUTPOWER_TOTAL = "wifi_outputpower_total"
# 日累计发电量 t49
WIFI_EEPC_DAY = "wifi_eepc_day"
# 日输出电量 t66
WIFI_OUTPUTENERGY_DAY = "wifi_outputenergy_day"
# 日市电充电电量 t710
WIFI_CP_AC_CHG_ENERGY_DAY = "wifi_cp_ac_chg_energy_day"
# 市电输入功率 t711
WIFI_CP_AC_INPUTPOWER = "wifi_cp_ac_inputpower"
# 车充模式功率 t701_4
WIFI_CAR_CHG_MODE_POWER = "wifi_car_chg_mode_power"
# 家电模式功率 t702_4
WIFI_HOME_MODE_POWER = "wifi_home_mode_power"
# 主机PV1输入功率 t50
WIFI_INPUTPOWER_PV1 = "wifi_inputpower_pv1"
# 主机PV2输入功率 t62
WIFI_INPUTPOWER_PV2 = "wifi_inputpower_pv2"
# 从机1PV输入功率 t63
WIFI_INPUTPOWER_PV3 = "wifi_inputpower_pv3"
# 从机2PV输入功率 t64
WIFI_INPUTPOWER_PV4 = "wifi_inputpower_pv4"
# 从机3PV输入功率 t65
WIFI_INPUTPOWER_PV5 = "wifi_inputpower_pv5"
# 从机4PV输入功率 t812
WIFI_INPUTPOWER_PV6 = "wifi_inputpower_pv6"
# 从机5PV输入功率 t813
WIFI_INPUTPOWER_PV7 = "wifi_inputpower_pv7"
# 从机6PV输入功率 t814
WIFI_INPUTPOWER_PV8 = "wifi_inputpower_pv8"
# 从机7PV输入功率 t815
WIFI_INPUTPOWER_PV9 = "wifi_inputpower_pv9"
# 主机电芯最低温度 t220
WIFI_B_CELLTEMP = "wifi_b_celltemp"
# 从机1电芯最低温度 t233
WIFI_B1_CELLTEMP = "wifi_b1_celltemp"
# 从机2电芯最低温度 t246
WIFI_B2_CELLTEMP = "wifi_b2_celltemp"
# 从机3电芯最低温度 t259
WIFI_B3_CELLTEMP = "wifi_b3_celltemp"
# 从机4电芯最低温度 t836
WIFI_B4_CELLTEMP = "wifi_b4_celltemp"
# 从机5电芯最低温度 t849
WIFI_B5_CELLTEMP = "wifi_b5_celltemp"
# 从机6电芯最低温度 t862
WIFI_B6_CELLTEMP = "wifi_b6_celltemp"
# 从机7电芯最低温度 t875
WIFI_B7_CELLTEMP = "wifi_b7_celltemp"
# 主机加热状态 t586
WIFI_B_HEATER_WORKING_STATUS = "wifi_b_heater_working_status"
# 从机1加热状态 t586
WIFI_B1_HEATER_WORKING_STATUS = "wifi_b1_heater_working_status"
# 从机2加热状态 t586
WIFI_B2_HEATER_WORKING_STATUS = "wifi_b2_heater_working_status"
# 从机3加热状态 t586
WIFI_B3_HEATER_WORKING_STATUS = "wifi_b3_heater_working_status"
# 从机4加热状态 t586
WIFI_B4_HEATER_WORKING_STATUS = "wifi_b4_heater_working_status"
# 从机5加热状态 t586
WIFI_B5_HEATER_WORKING_STATUS = "wifi_b5_heater_working_status"
# 从机6加热状态 t586
WIFI_B6_HEATER_WORKING_STATUS = "wifi_b6_heater_working_status"
# 从机7加热状态 t586
WIFI_B7_HEATER_WORKING_STATUS = "wifi_b7_heater_working_status"
# 主机MPPT1输入电流 t537
WIFI_MBMS_MPPT1_IN_I = "wifi_mbms_mppt1_in_i"
# 主机MPPT1输入电压 t536
WIFI_MBMS_MPPT1_IN_V = "wifi_mbms_mppt1_in_v"
# 主机MPPT2输入电流 t545
WIFI_MBMS_MPPT2_IN_I = "wifi_mbms_mppt2_in_i"
# 主机MPPT2输入电压 t544
WIFI_MBMS_MPPT2_IN_V = "wifi_mbms_mppt2_in_v"
# 从机1MPPT输入电流 t553
WIFI_SBMS1_MPPT_IN_I = "wifi_sbms1_mppt_in_i"
# 从机1MPPT输入电压 t552
WIFI_SBMS1_MPPT_IN_V = "wifi_sbms1_mppt_in_v"
# 从机2MPPT输入电流 t561
WIFI_SBMS2_MPPT_IN_I = "wifi_sbms2_mppt_in_i"
# 从机2MPPT输入电压 t560
WIFI_SBMS2_MPPT_IN_V = "wifi_sbms2_mppt_in_v"
# 从机3MPPT输入电流 t569
WIFI_SBMS3_MPPT_IN_I = "wifi_sbms3_mppt_in_i"
# 从机3MPPT输入电压 t568
WIFI_SBMS3_MPPT_IN_V = "wifi_sbms3_mppt_in_v"
# 从机4MPPT输入电流 t970
WIFI_SBMS4_MPPT_IN_I = "wifi_sbms4_mppt_in_i"
# 从机4MPPT输入电压 t969
WIFI_SBMS4_MPPT_IN_V = "wifi_sbms4_mppt_in_v"
# 从机5MPPT输入电流 t978
WIFI_SBMS5_MPPT_IN_I = "wifi_sbms5_mppt_in_i"
# 从机5MPPT输入电压 t977
WIFI_SBMS5_MPPT_IN_V = "wifi_sbms5_mppt_in_v"
# 从机6MPPT输入电流 t986
WIFI_SBMS6_MPPT_IN_I = "wifi_sbms6_mppt_in_i"
# 从机6MPPT输入电压 t985
WIFI_SBMS6_MPPT_IN_V = "wifi_sbms6_mppt_in_v"
# 从机7MPPT输入电流 t994
WIFI_SBMS7_MPPT_IN_I = "wifi_sbms7_mppt_in_i"
# 从机7MPPT输入电压 t993
WIFI_SBMS7_MPPT_IN_V = "wifi_sbms7_mppt_in_v"


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
    WIFI_INPUTPOWER_TOTAL: "t33",
    WIFI_OUTPUTPOWER_TOTAL: "t34",
    WIFI_EEPC_DAY: "t49",
    WIFI_OUTPUTENERGY_DAY: "t66",
    WIFI_CP_AC_CHG_ENERGY_DAY: "t710",
    WIFI_CP_AC_INPUTPOWER: "t711",
    WIFI_CAR_CHG_MODE_POWER: "t701_4",
    WIFI_HOME_MODE_POWER: "t702_4",
    WIFI_INPUTPOWER_PV1: "t50",
    WIFI_INPUTPOWER_PV2: "t62",
    WIFI_INPUTPOWER_PV3: "t63",
    WIFI_INPUTPOWER_PV4: "t64",
    WIFI_INPUTPOWER_PV5: "t65",
    WIFI_INPUTPOWER_PV6: "t812",
    WIFI_INPUTPOWER_PV7: "t813",
    WIFI_INPUTPOWER_PV8: "t814",
    WIFI_INPUTPOWER_PV9: "t815",
    WIFI_B_CELLTEMP: "t220",
    WIFI_B1_CELLTEMP: "t233",
    WIFI_B2_CELLTEMP: "t246",
    WIFI_B3_CELLTEMP: "t259",
    WIFI_B4_CELLTEMP: "t836",
    WIFI_B5_CELLTEMP: "t849",
    WIFI_B6_CELLTEMP: "t862",
    WIFI_B7_CELLTEMP: "t875",
    WIFI_B_HEATER_WORKING_STATUS: "t586",
    WIFI_B1_HEATER_WORKING_STATUS: "t586",
    WIFI_B2_HEATER_WORKING_STATUS: "t586",
    WIFI_B3_HEATER_WORKING_STATUS: "t586",
    WIFI_B4_HEATER_WORKING_STATUS: "t586",
    WIFI_B5_HEATER_WORKING_STATUS: "t586",
    WIFI_B6_HEATER_WORKING_STATUS: "t586",
    WIFI_B7_HEATER_WORKING_STATUS: "t586",
    WIFI_MBMS_MPPT1_IN_I: "t537",
    WIFI_MBMS_MPPT1_IN_V: "t536",
    WIFI_MBMS_MPPT2_IN_I: "t545",
    WIFI_MBMS_MPPT2_IN_V: "t544",
    WIFI_SBMS1_MPPT_IN_I: "t553",
    WIFI_SBMS1_MPPT_IN_V: "t552",
    WIFI_SBMS2_MPPT_IN_I: "t561",
    WIFI_SBMS2_MPPT_IN_V: "t560",
    WIFI_SBMS3_MPPT_IN_I: "t569",
    WIFI_SBMS3_MPPT_IN_V: "t568",
    WIFI_SBMS4_MPPT_IN_I: "t970",
    WIFI_SBMS4_MPPT_IN_V: "t969",
    WIFI_SBMS5_MPPT_IN_I: "t978",
    WIFI_SBMS5_MPPT_IN_V: "t977",
    WIFI_SBMS6_MPPT_IN_I: "t986",
    WIFI_SBMS6_MPPT_IN_V: "t985",
    WIFI_SBMS7_MPPT_IN_I: "t994",
    WIFI_SBMS7_MPPT_IN_V: "t993",
}

# SensorValue显示初始状态
ENTITY_SENSOR_VALUES = {
    WIFI_SOC: ("%", "BATTERY", "1"),
    WIFI_B_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B1_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B2_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B3_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B4_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B5_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B6_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_B7_ACTUAL_SOC: ("%", "BATTERY", "1"),
    WIFI_MBMS_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_MBMS_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS1_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS1_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS2_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS2_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS3_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS3_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS4_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS4_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS5_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS5_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS6_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS6_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_SBMS7_HW_LIMITED_DISC_SOC_MIN: ("%", "BATTERY", "1"),
    WIFI_SBMS7_HW_LIMITED_CHG_SOC_MAX: ("%", "BATTERY", "1"),
    WIFI_INPUTPOWER_TOTAL: ("W", "POWER", "1"),
    WIFI_OUTPUTPOWER_TOTAL: ("W", "POWER", "1"),
    WIFI_EEPC_DAY: ("kWh", "ENERGY", "0.001"),
    WIFI_OUTPUTENERGY_DAY: ("kWh", "ENERGY", "0.001"),
    WIFI_CP_AC_CHG_ENERGY_DAY: ("kWh", "ENERGY", "0.001"),
    WIFI_CP_AC_INPUTPOWER: ("W", "POWER", "1"),
    WIFI_CAR_CHG_MODE_POWER: ("W", "POWER", "1"),
    WIFI_HOME_MODE_POWER: ("W", "POWER", "1"),
    WIFI_INPUTPOWER_PV1: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV2: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV3: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV4: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV5: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV6: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV7: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV8: ("W", "POWER", "0.01"),
    WIFI_INPUTPOWER_PV9: ("W", "POWER", "0.01"),
    WIFI_B_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B1_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B2_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B3_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B4_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B5_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B6_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B7_CELLTEMP: ("°C", "TEMPERATURE", "TEMP273"),
    WIFI_B_HEATER_WORKING_STATUS: ("", "ENUM", "BIT0"),
    WIFI_B1_HEATER_WORKING_STATUS: ("", "ENUM", "BIT1"),
    WIFI_B2_HEATER_WORKING_STATUS: ("", "ENUM", "BIT2"),
    WIFI_B3_HEATER_WORKING_STATUS: ("", "ENUM", "BIT3"),
    WIFI_B4_HEATER_WORKING_STATUS: ("", "ENUM", "BIT4"),
    WIFI_B5_HEATER_WORKING_STATUS: ("", "ENUM", "BIT5"),
    WIFI_B6_HEATER_WORKING_STATUS: ("", "ENUM", "BIT6"),
    WIFI_B7_HEATER_WORKING_STATUS: ("", "ENUM", "BIT7"),
    WIFI_MBMS_MPPT1_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_MBMS_MPPT1_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_MBMS_MPPT2_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_MBMS_MPPT2_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS1_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS1_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS2_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS2_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS3_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS3_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS4_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS4_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS5_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS5_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS6_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS6_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
    WIFI_SBMS7_MPPT_IN_I: ("A", "CURRENT", "0.1"),
    WIFI_SBMS7_MPPT_IN_V: ("V", "VOLTAGE", "0.1"),
}

# 只读项键名(sensor)
# 连接状态
WIFI_CONNECTION = "wifi_connection"
# 上一次刷新时间
WIFI_REPORT_TIME = "wifi_update_time"
# 网络信号强度 t475
WIFI_WIRELESS_NETWORK_RSSI = "wifi_wireless_network_rssi"

# DiagnosticType显示类型映
ENTITY_DIAGNOSTIC_TYPES = {
    WIFI_CONNECTION: "connection",
    WIFI_REPORT_TIME: "reporttime",
    WIFI_WIRELESS_NETWORK_RSSI: "networkrssi",
}

# DiagnosticValue初始化值
ENTITY_DIAGNOSTIC_VALUES = {
    WIFI_CONNECTION: ("disconnected"),
    WIFI_REPORT_TIME: ("2000.01.01 00:00:00"),
    WIFI_WIRELESS_NETWORK_RSSI: ("0 dB"),
}
