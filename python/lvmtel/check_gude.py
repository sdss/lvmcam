#!/usr/bin/env python3

# flake8: noqa

import argparse
import fnmatch
import json
import time

import requests


parser = argparse.ArgumentParser(prog="check_gude")
parser.add_argument("-H", "--host", help="ip address of target host")
parser.add_argument("-s", "--ssl", help="use https connection", action="store_true")
parser.add_argument("--username", help="username for HTTP basic auth credentials")
parser.add_argument("--password", help="password for HTTP basic auth credemtials")
parser.add_argument(
    "-t", "--timeout", help="HTTP timeout value", default=5.0, type=float
)
parser.add_argument("--sensor", help="")
parser.add_argument("--numeric", help="", action="store_true", default=False)
parser.add_argument("--interval", help='"watch"-like interval', default=0.0, type=float)
parser.add_argument("--nagios", help="", action="store_true", default=False)
parser.add_argument(
    "-w", "--warning", help="nagios: threshold to exit as warning level", default=""
)
parser.add_argument(
    "-c", "--critical", help="nagios: threshold to exit as critical level", default=""
)
parser.add_argument(
    "--operator", help="nagios: check warn/crit levels by one of >,<,>=,<=", default=">"
)
parser.add_argument("--label", help="nagios: sensor label", default="sensor")
parser.add_argument("--unit", help="nagios: sensor label", default="")
parser.add_argument(
    "--labelindex",
    help="prepend numeric sensor iteration to nagios label",
    action="store_true",
)
parser.add_argument(
    "--skipsimple",
    help="demo filter to show backward compatiblity",
    action="store_true",
)
parser.add_argument(
    "--skipcomplex",
    help="demo filter to show backward compatiblity",
    action="store_true",
)
parser.add_argument("--verbose", help="", action="store_true", default=False)


args = parser.parse_args()

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_ERROR = 2


class GudeSensor:
    values = {}

    #
    # get sensor_descr / sensor_values as JSON objects
    #
    def getSensorsJson(self, host, ssl, timeout, username=None, password=None):
        if ssl:
            url = "https://"
        else:
            url = "http://"

        url += host + "/" + "status.json"

        auth = None
        if username:
            auth = requests.auth.HTTPBasicAuth(username, password)

        DESCR = 0x10000
        VALUES = 0x4000
        EXTEND = (
            0x800000  # enables complex sensors-groups, such as Sensor 101, 20, etc...
        )
        SENSORS = DESCR + VALUES

        if args.skipcomplex:
            cgi = {
                "components": SENSORS
            }  # simple-sensors only (fully backward compatible)
        elif args.skipsimple:
            cgi = {
                "components": SENSORS + EXTEND,
                "types": "C",
            }  # complex sensors-groups only
        else:
            cgi = {
                "components": SENSORS + EXTEND
            }  # simple-sensors + complex sensors-groups in one merged view

        r = requests.get(url, params=cgi, verify=False, auth=auth, timeout=timeout)

        if r.status_code == 200:
            if args.verbose:
                print(f"HTTP GET:\n\t{r.url}")
                print(f"HTTP RESPONSE:\n\t{r.text}\n\n")

            return json.loads(r.text)
        else:
            raise ValueError("http request error {0}".format(r.status))

    #
    # walk and merge sensor_descr / sensor_value
    #
    def collectSensorData(self):
        jsonIndex = -1
        for sensorType in self.sensorJson["sensor_descr"]:
            jsonIndex += 1
            sensorValues = self.sensorJson["sensor_values"][jsonIndex]["values"]
            st = sensorType["type"]

            for si, sensorProp in enumerate(sensorType["properties"]):
                self.printSensorIdStr(sensorProp)
                id = sensorProp.get("real_id", si)

                # simple sensor
                if "fields" in sensorType:
                    for sf, fieldProp in enumerate(sensorType["fields"]):
                        field = self.store(
                            "{0}.{1}.{2}".format(st, id, sf),
                            sensorValues[si][sf]["v"],
                            fieldProp,
                            "\t",
                        )

                # sensor groups
                if "groups" in sensorType:
                    for gi, sensorGroup in enumerate(sensorProp["groups"]):
                        for grm, groupMember in enumerate(sensorGroup):
                            self.printSensorIdStr(groupMember, "\t")
                            for sf, fieldProp in enumerate(
                                sensorType["groups"][gi]["fields"]
                            ):
                                field = self.store(
                                    "{0}.{1}.{2}.{3}.{4}".format(st, id, gi, grm, sf),
                                    sensorValues[si][gi][grm][sf]["v"],
                                    fieldProp,
                                    "\t\t",
                                )

    #
    # store sensor-field as dict identified by locatorStr (vector)
    #
    def store(self, locatorStr, value, fieldProp, prefix=""):
        field = {"value": value, "unit": fieldProp["unit"], "name": fieldProp["name"]}
        self.values[locatorStr] = field
        if not self.filter:
            print(
                "{0}{1} {2} {3} {4}".format(
                    prefix,
                    locatorStr,
                    field["value"],
                    fieldProp["unit"],
                    fieldProp["name"],
                )
            )
        return field

    #
    # nagios : check sensor value limits
    #
    def checkThreshExceeded(self, value, thresh, operator):
        if not len(str(thresh)):
            return False

        range = str(thresh).split(":")
        if len(range) == 2:
            if range[0] and (float(value) < float(range[0])):
                return True
            if range[1] and (float(value) > float(range[1])):
                return True

        if len(range) == 1:
            if operator == "<" and (float(value) < float(thresh)):
                return True
            if operator == ">" and (float(value) > float(thresh)):
                return True
            if operator == "<=" and (float(value) <= float(thresh)):
                return True
            if operator == ">=" and (float(value) >= float(thresh)):
                return True

        return False

    #
    # nagios : print status text (performance data)
    #
    def nagiosText(self, level, value, labelindex):
        return "{0}: {1}={2}{3} (w: {4}, c: {5}, op:{6})".format(
            level,
            self.label + labelindex,
            value,
            self.unit,
            self.warning,
            self.critical,
            self.operator,
        )

    #
    # nagios : set exit code to most critical item
    #
    def setExitCode(self, exitcode, level):
        if level > exitcode:
            exitcode = level

    #
    # print sensor id / name
    #
    def printSensorIdStr(self, sensorProp, prefix=""):
        if not self.filter:
            print(
                "{0}{1} {2}".format(
                    prefix, sensorProp.get("id", ""), sensorProp.get("name", "")
                )
            )

    #
    # print all requested sensors
    #
    def printSensorInfo(
        self, label, unit, numeric, nagios, critical, warning, operator
    ):
        maxexitcode = 0
        labelindex = 0
        self.label = label
        self.unit = unit
        self.warning = warning
        self.critical = critical
        self.operator = operator

        nagiosPerfomanceText = ""
        if self.filter:
            for sensor in gudeSensors.values:
                if fnmatch.fnmatch(sensor, self.filter):
                    if nagios:
                        exitcode = 0
                        if args.labelindex:
                            labelindex += 1
                        else:
                            labelindex = ""

                        if not exitcode and self.checkThreshExceeded(
                            self.values[sensor]["value"], critical, operator
                        ):
                            print(
                                self.nagiosText(
                                    "CRITICAL",
                                    self.values[sensor]["value"],
                                    str(labelindex),
                                )
                            )
                            exitcode = 2

                        if not exitcode and self.checkThreshExceeded(
                            self.values[sensor]["value"], warning, operator
                        ):
                            print(
                                self.nagiosText(
                                    "WARNING",
                                    self.values[sensor]["value"],
                                    str(labelindex),
                                )
                            )
                            exitcode = 1

                        if not exitcode:
                            print(
                                self.nagiosText(
                                    "OK", self.values[sensor]["value"], str(labelindex)
                                )
                            )

                        if maxexitcode < exitcode:
                            maxexitcode = exitcode

                        nagiosPerfomanceText += " {0}{1}={2}{3};{4};{5}".format(
                            label,
                            labelindex,
                            self.values[sensor]["value"],
                            unit,
                            warning,
                            critical,
                        )
                    else:
                        if not numeric:
                            print(
                                "{0} {1} {2} {3}".format(
                                    sensor,
                                    self.values[sensor]["name"],
                                    self.values[sensor]["value"],
                                    self.values[sensor]["unit"],
                                )
                            )
                        else:
                            print("{0}".format(self.values[sensor]["value"]))

        if nagios and nagiosPerfomanceText:
            print("{0} |{1}".format(self.host, nagiosPerfomanceText))

        self.exitcode = maxexitcode

    def __init__(self, host, filter, ssl, timeout, username, password):
        self.filter = filter
        self.host = host
        self.sensorJson = self.getSensorsJson(host, ssl, timeout, username, password)
        print(f"{host} {ssl} {timeout} {username}")
        print(self.sensorJson)
        self.collectSensorData()


while True:
    try:
        gudeSensors = GudeSensor(
            str(args.host),
            args.sensor,
            args.ssl,
            args.timeout,
            args.username,
            args.password,
        )
    except:
        print("ERROR getting sensor json")
        exit(EXIT_ERROR)

    gudeSensors.printSensorInfo(
        args.label,
        args.unit,
        args.numeric,
        args.nagios,
        args.critical,
        args.warning,
        args.operator,
    )

    if args.interval:
        time.sleep(args.interval)
    else:
        break

exit(gudeSensors.exitcode)
