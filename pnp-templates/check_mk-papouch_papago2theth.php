<?php

# Template:	check_mk-papouch_papago2theth.php
# Author:	vaclav.ovsik@gmail.com

# DS
#   1 tempc

$_WARNRULE = '#FFFF00';
$_CRITRULE = '#FF0000';


if ($NAME[1] == 'dewp') {
    $ds_name[1] = "Dew point";
    $my_units = $my_units2 = '°C';
} elseif ($NAME[1] == 'hum') {
    $ds_name[1] = "Humidity";
    $my_units = '%';
    $my_units2 = '%%';
} elseif ($NAME[1] == 'tempc') {
    $ds_name[1] = "Temperature";
    $my_units = $my_units2 = '°C';
}

$opt[1] = "--vertical-label '$my_units' --title \"$hostname / $servicedesc\" ";
$def[1] = rrd::def("tempc", $RRDFILE[1], $DS[1], "AVERAGE");
$def[1] .= rrd::line1("tempc", "#050", $ds_name[1]);
$def[1] .= rrd::gprint("tempc", array("LAST", "MIN", "MAX", "AVERAGE"), "%3.1lf$my_units2");

$lc = $CRIT_MIN[1];
$hc = $CRIT_MAX[1];
$lw = $WARN_MIN[1];
$hw = $WARN_MAX[1];
if ( $hc == null ) { $hc = $CRIT[1]; }
if ( $hw == null ) { $hw = $WARN[1]; }

$adef = array();
$nl = "\\n";
$nlevel = 0;
if ($hc != null) {
    array_push($adef, rrd::hrule($hc, $_CRITRULE, sprintf("Critical above %.1f$my_units2$nl", $hc)));
    $nl = "";
    $nlevel++;
}
if ($lc != null) {
    array_push($adef, rrd::hrule($lc, $_CRITRULE, sprintf("Critical below %.1f$my_units2$nl", $lc)));
    $nl = "";
    $nlevel++;
}
if ($nlevel > 1) {
    $nl = "\\n";
}
if ($hw != null) {
    array_push($adef, rrd::hrule($hw, $_WARNRULE, sprintf("Warning above %.1f$my_units2$nl", $hw)));
    $nl = "";
}
if ($lw != null) {
    array_push($adef, rrd::hrule($lw, $_WARNRULE, sprintf("Warning below %.1f$my_units2$nl", $lw)));
    $nl = "";
}
$def[1] .= join("", array_reverse($adef));

?>
