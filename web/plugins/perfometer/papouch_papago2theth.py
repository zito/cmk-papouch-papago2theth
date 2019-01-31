#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim:sta:si:sw=4:sts=4:et:
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2015             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# The Check_MK official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Check has been developed using:
# Papago 2TH ETH - Thermo / Humidity / Dew point meter with eth if
# Device Firmware Version   1.4/6
# http://www.papouch.com/en/shop/product/papago-2th-eth-temperature-and-humidity-meter-with-ethernet/
#
# +------------------------------------------------------------------+
# | This file has been contributed by:                               |
# |                                                                  |
# | Václav Ovsík <vaclav.ovsik@gmail.com>             Copyright 2015 |
# +------------------------------------------------------------------+


def perfometer_logistic(value, color, value_half, value99):
    K = (value99 - value_half) / 4.6                 # log(1/99) = -4.6
    pos = int(100.0 / ( 1.0 + math.exp( - (value - value_half) / K)) + 0.5)
    return render_perfometer([(pos, color), (100 - pos, "white")])

def perfometer_check_mk_papouch_papago2theth(row, check_command, perf_data):
    state = row["service_state"]
    info = row["service_plugin_output"]
    text = info.split(' - ', 1)[1]
    (measure, rest) = text.split(': ', 1)
    valunit = rest.split(' ', 1)[0]
    unit = valunit.lstrip('-0123456789.')
    val = float(valunit[0:-len(unit)])
    color = '#00ff00'
    if state == 1:
        color = '#ffff00'
    elif state == 2:
        color = '#ff0000'
    if measure == 'Humidity':
        return valunit, perfometer_linear(val, color)
    if measure == 'Dew point':
        return valunit, perfometer_logistic(val, color, 9, 30)
    return valunit, perfometer_logistic(val, color, 20, 40)

perfometers['check_mk-papouch_papago2theth'] = perfometer_check_mk_papouch_papago2theth
