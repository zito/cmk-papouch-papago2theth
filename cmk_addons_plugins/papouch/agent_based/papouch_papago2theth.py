#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:sta:si:sw=4:sts=4:et:

# Check has been developed using:
# Papago 2TH ETH - Thermo / Humidity / Dew point meter with eth if
# Device Firmware Version   1.7/15
# http://www.papouch.com/en/shop/product/papago-2th-eth-temperature-and-humidity-meter-with-ethernet/
# Václav Ovsík <vaclav.ovsik@gmail.com>

# papago_temp_V02-MIB::deviceName.0 = STRING: "termo-srv"
# papago_temp_V02-MIB::psAlarmString.0 = ""
# papago_temp_V02-MIB::inChType.1 = INTEGER: 1
# papago_temp_V02-MIB::inChType.2 = INTEGER: 2
# papago_temp_V02-MIB::inChType.3 = INTEGER: 3
# papago_temp_V02-MIB::inChType.4 = INTEGER: 0
# papago_temp_V02-MIB::inChType.5 = INTEGER: 0
# papago_temp_V02-MIB::inChType.6 = INTEGER: 0
# papago_temp_V02-MIB::inChStatus.1 = INTEGER: 0
# papago_temp_V02-MIB::inChStatus.2 = INTEGER: 0
# papago_temp_V02-MIB::inChStatus.3 = INTEGER: 0
# papago_temp_V02-MIB::inChStatus.4 = INTEGER: 4
# papago_temp_V02-MIB::inChStatus.5 = INTEGER: 4
# papago_temp_V02-MIB::inChStatus.6 = INTEGER: 4
# papago_temp_V02-MIB::inChValue.1 = INTEGER: 231
# papago_temp_V02-MIB::inChValue.2 = INTEGER: 266
# papago_temp_V02-MIB::inChValue.3 = INTEGER: 28
# papago_temp_V02-MIB::inChValue.4 = INTEGER: 0
# papago_temp_V02-MIB::inChValue.5 = INTEGER: 0
# papago_temp_V02-MIB::inChValue.6 = INTEGER: 0
# papago_temp_V02-MIB::inChUnits.1 = INTEGER: 0
# papago_temp_V02-MIB::inChUnits.2 = INTEGER: 0
# papago_temp_V02-MIB::inChUnits.3 = INTEGER: 0
# papago_temp_V02-MIB::inChUnits.4 = INTEGER: 0
# papago_temp_V02-MIB::inChUnits.5 = INTEGER: 0
# papago_temp_V02-MIB::inChUnits.6 = INTEGER: 0
# papago_temp_V02-MIB::channelEntry.5.1 = NULL

# .1.3.6.1.4.1.18248.31.1.1.1.0 = STRING: "termo-srv"
# .1.3.6.1.4.1.18248.31.1.1.2.0 = ""
# .1.3.6.1.4.1.18248.31.1.2.1.1.1.1 = INTEGER: 1
# .1.3.6.1.4.1.18248.31.1.2.1.1.1.2 = INTEGER: 2
# .1.3.6.1.4.1.18248.31.1.2.1.1.1.3 = INTEGER: 3
# .1.3.6.1.4.1.18248.31.1.2.1.1.1.4 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.1.5 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.1.6 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.2.1 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.2.2 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.2.3 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.2.4 = INTEGER: 4
# .1.3.6.1.4.1.18248.31.1.2.1.1.2.5 = INTEGER: 4
# .1.3.6.1.4.1.18248.31.1.2.1.1.2.6 = INTEGER: 4
# .1.3.6.1.4.1.18248.31.1.2.1.1.3.1 = INTEGER: 231
# .1.3.6.1.4.1.18248.31.1.2.1.1.3.2 = INTEGER: 265
# .1.3.6.1.4.1.18248.31.1.2.1.1.3.3 = INTEGER: 28
# .1.3.6.1.4.1.18248.31.1.2.1.1.3.4 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.3.5 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.3.6 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.4.1 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.4.2 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.4.3 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.4.4 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.4.5 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.4.6 = INTEGER: 0
# .1.3.6.1.4.1.18248.31.1.2.1.1.5.1 = NULL


import enum
import pydantic

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    OIDEnd,
    Result,
    SNMPTree,
    Service,
    SimpleSNMPSection,
    State,
    StringTable,
    all_of,
    contains,
    get_value_store,
    startswith,
)

from cmk.plugins.lib.humidity import check_humidity, CheckParams
from cmk.plugins.lib.temperature import check_temperature, TempParamType


class SensorType(enum.IntEnum):
    NA          = 0
    TEMP        = 1
    HUMIDITY    = 2
    DEWPOINT    = 3

    def label(self) -> str:
        match self.value:
            case SensorType.NA: return "NA"
            case SensorType.TEMP: return "Temperature"
            case SensorType.HUMIDITY: return "Humidity"
            case SensorType.DEWPOINT: return "Dew point"

class SensorName(enum.IntEnum):
    A = 0
    B = 1

class SensorState(enum.IntEnum):
    OK              = 0
    NOT_AVAILABLE   = 1
    OVERFLOW        = 2
    UNDERFLOW       = 3
    ERROR           = 4
    
    def cmk_state(self) -> State:
        match self.value:
            case SensorState.OK: return State.OK
            case SensorState.NOT_AVAILABLE: return State.UKNOWN
            case SensorState.OVERFLOW: return State.WARN
            case SensorState.UNDERFLOW: return State.WARN
            case SensorState.ERROR: return State.CRIT


class SensorItem(pydantic.BaseModel):
    stype: SensorType
    sname: SensorName
    state: SensorState
    reading: float

    def label(self) -> str:
        return "Sensor " + self.sname.name + " " + self.stype.label()

Section = list[SensorItem]


def parse_papouch_papago2theth(string_table: StringTable) -> Section:
    section: NewSection = []
    for oidend, typeid, state, reading_str in string_table:
        i = int(oidend) -1
        section.append(SensorItem(stype=typeid,
                                 sname = i // 3,
                                 state = state,
                                 reading = float(reading_str) / 10))
    return section


snmp_section_papouch_papago2theth = SimpleSNMPSection(
    name="papouch_papago2theth",
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".0.10.43.6.1.4.1"),
        contains(".1.3.6.1.2.1.1.1.0", "Papago_2TH_ETH"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.18248.31.1.2.1.1",
        oids=[
            OIDEnd(),
            "1",        # papago_temp_V02-MIB::inChType
            "2",        # papago_temp_V02-MIB::inChStatus
            "3",        # papago_temp_V02-MIB::inChValue
        ],
    ),
    parse_function=parse_papouch_papago2theth,
)


def inventory_papouch_papago2theth(section: Section, what: SensorType) -> DiscoveryResult:
    for item in section:
        if item.stype == what:
            yield Service(item=item.label())

def check_papouch_papago2theth_temp(
    item: str,
    params: TempParamType,
    section: Section,
    what: SensorType,
) -> CheckResult:
    for s in section:
        if s.label() == item:
            yield from check_temperature(reading=s.reading,
                                     params=params,
                                     unique_name=f"papouch_papago2theth_{item}",
                                     value_store = get_value_store(),
                                     dev_unit='c',
                                     dev_status=s.state.cmk_state(),
                                     dev_status_name=s.state.name)


#   .--temperature---------------------------------------------------------.
#   |      _                                      _                        |
#   |     | |_ ___ _ __ ___  _ __   ___ _ __ __ _| |_ _   _ _ __ ___       |
#   |     | __/ _ \ '_ ` _ \| '_ \ / _ \ '__/ _` | __| | | | '__/ _ \      |
#   |     | ||  __/ | | | | | |_) |  __/ | | (_| | |_| |_| | | |  __/      |
#   |      \__\___|_| |_| |_| .__/ \___|_|  \__,_|\__|\__,_|_|  \___|      |
#   |                       |_|                                            |
#   +----------------------------------------------------------------------+
#   |                               main check                             |
#   '----------------------------------------------------------------------'

check_plugin_papouch_papago2theth_temp = CheckPlugin(
    name="papouch_papago2theth",
    sections=["papouch_papago2theth"],
    service_name="%s",
    discovery_function=lambda section: \
        (yield from inventory_papouch_papago2theth(section, SensorType.TEMP)),
    check_function=lambda item, params, section: \
        (yield from check_papouch_papago2theth_temp(item, params, section, SensorType.TEMP)),
    check_ruleset_name="temperature",
    check_default_parameters={},
)


#.
#   .--dew point-----------------------------------------------------------.
#   |                _                             _       _               |
#   |             __| | _____      __  _ __   ___ (_)_ __ | |_             |
#   |            / _` |/ _ \ \ /\ / / | '_ \ / _ \| | '_ \| __|            |
#   |           | (_| |  __/\ V  V /  | |_) | (_) | | | | | |_             |
#   |            \__,_|\___| \_/\_/   | .__/ \___/|_|_| |_|\__|            |
#   |                                 |_|                                  |
#   '----------------------------------------------------------------------'

check_plugin_papouch_papago2theth_dewpoint = CheckPlugin(
    name="papouch_papago2theth_dewpoint",
    sections=["papouch_papago2theth"],
    service_name="%s",
    discovery_function=lambda section: \
        (yield from inventory_papouch_papago2theth(section, SensorType.DEWPOINT)),
    check_function=lambda item, params, section: \
        (yield from check_papouch_papago2theth_temp(item, params, section, SensorType.DEWPOINT)),
    check_ruleset_name="temperature",
    check_default_parameters={},
)


#.
#   .--humidity------------------------------------------------------------.
#   |              _                     _     _ _ _                       |
#   |             | |__  _   _ _ __ ___ (_) __| (_) |_ _   _               |
#   |             | '_ \| | | | '_ ` _ \| |/ _` | | __| | | |              |
#   |             | | | | |_| | | | | | | | (_| | | |_| |_| |              |
#   |             |_| |_|\__,_|_| |_| |_|_|\__,_|_|\__|\__, |              |
#   |                                                  |___/               |
#   '----------------------------------------------------------------------'


PAPOUCH_PAPAGO2THETH_HUMIDITY_DEFAULT_PARAMETERS = {
    "levels": (60, 80),
    "levels_lower": (30, 20),
}

def check_papouch_papago2theth_humidity(
    item: str,
    params: CheckParams,
    section: Section,
) -> CheckResult:

    for s in section:
        if s.label() == item:
            yield Result(state=s.state.cmk_state(), summary=f"Status: {s.state.name}")
            yield from check_humidity(humidity=s.reading, params=params)


check_plugin_papouch_papago2theth_humidity = CheckPlugin(
    name="papouch_papago2theth_humidity",
    sections=["papouch_papago2theth"],
    service_name="%s",
    discovery_function=lambda section: \
        (yield from inventory_papouch_papago2theth(section, SensorType.HUMIDITY)),
    check_function=check_papouch_papago2theth_humidity,
    check_default_parameters=PAPOUCH_PAPAGO2THETH_HUMIDITY_DEFAULT_PARAMETERS,
    check_ruleset_name="humidity",
)
