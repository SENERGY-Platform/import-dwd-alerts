#  Copyright 2020 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime, timezone
from typing import List, Iterator

from import_lib.import_lib import ImportLib, get_logger

import lib.alert.jsonLoader
from lib.alert.Alert import Alert, from_dict
from lib.alert.KnownAlerts import KnownAlerts

logger = get_logger(__name__)


class AlertImport:
    def __init__(self, lib: ImportLib):
        self.__lib = lib

        self.__filterRegionNames = self.__lib.get_config("FilterRegionNames", [])
        if not isinstance(self.__filterRegionNames, List):
            logger.error("Invalid config for FilterRegionNames will not be used")
            self.__filterRegionNames = []

        self.__filterWarnCellIds = self.__lib.get_config("FilterWarnCellIds", [])
        if not isinstance(self.__filterWarnCellIds, List):
            logger.error("Invalid config for FilterWarnCellIds will not be used")
            self.__filterWarnCellIds = []

        self.__filterStateShorts = self.__lib.get_config("FilterStateShorts", [])
        if not isinstance(self.__filterStateShorts, List):
            logger.error("Invalid config for FilterStateShorts will not be used")
            self.__filterStateShorts = []

        self.__use_filter = len(self.__filterRegionNames) > 0 or len(self.__filterWarnCellIds) > 0 or len(
            self.__filterStateShorts) > 0

        self.__last_dt = datetime.fromtimestamp(0, timezone.utc)

        self.__known = KnownAlerts()

        previous_alerts = self.__lib.get_last_n_messages(10000)  # this is probably too much, but this only runs once
        if previous_alerts is not None:
            previous_alerts = previous_alerts[::-1]  # reverse list, newest msgs have lowest index
            if len(previous_alerts) > 0:
                self.__last_dt = previous_alerts[0][0].astimezone(timezone.utc)
            for dtAlertTuple in previous_alerts:
                if dtAlertTuple[0].astimezone(timezone.utc) < self.__last_dt:
                    break  # all remaining msgs are too old
                if not self.__known.insert_if_new(from_dict(dtAlertTuple[1])):
                    logger.error("Import previously published alert failed: Already exists (double import)!")

        logger.debug("Init completed")

    def import_most_recent(self):
        '''
        Import the most recent alerts. Only new imports will be published. If an alert prematurely expires,
        an additional message will be published.
        '''
        dt, l = lib.alert.jsonLoader.get_most_recent()
        if dt <= self.__last_dt:
            logger.warning("Already imported these alerts. Scheduled too often? Ignore at startup")
            return
        self.__last_dt = dt
        logger.info("Got " + str(len(l)) + " alerts")
        if self.__use_filter:
            l = self.__filter_alerts(l)

        previously_known_but_now_missing = self.__known.delete_all_except(l)
        premature_counter = 0
        for alert in previously_known_but_now_missing:
            if alert.end is None or alert.end_dt() > dt:
                alert.end = dt
                self.__lib.put(dt, alert.dict())
                premature_counter += 1
        logger.info(str(premature_counter) + " alerts ended prematurely (message sent)")

        counter = 0
        total = 0
        for alert in l:
            total += 1
            if self.__known.insert_if_new(alert):
                self.__lib.put(dt, alert.dict())
                counter += 1
        logger.info(str(counter) + " new alerts imported (of " + str(total) + " after filtering)")

    def __filter_alerts(self, alerts: List[Alert]) -> Iterator[Alert]:
        return filter(lambda alert:
                      alert.warnCellId in self.__filterWarnCellIds or
                      alert.regionName in self.__filterRegionNames or
                      alert.stateShort in self.__filterStateShorts,
                      alerts)
