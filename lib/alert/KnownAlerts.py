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

from typing import List
from lib.alert.Alert import Alert


class KnownAlerts:
    def __init__(self):
        self.__known = {}

    def insert_if_new(self, alert: Alert) -> bool:
        '''
        Insert an alert into the collection if it's not known. Returns True, if the alert was not known before.

        :param alert: Alert to insert
        :return: True, if alert was not known before. False otherwise.
        '''
        key = self.__get_key(alert)
        if key in self.__known and self.__known[key] == alert:  # sub attributes might have been updated
            return False
        self.__known[key] = alert
        return True

    def delete_all_except(self, alerts: List[Alert]) -> List[Alert]:
        '''
        Considers all inserted alerts to be outdated, with the exception of the alerts provided here.

        :param alerts: Alerts not to consider outdated.
        :return: List of all alerts that were deleted, because they were not in the list provided.
        '''
        if len(self.__known) == 0:
            return []
        keep_keys = []
        for alert in alerts:
            keep_keys.append(self.__get_key(alert))

        deleted = []
        delete_keys = []
        for key, value in self.__known.items():
            if key not in keep_keys:
                delete_keys.append(key)
                deleted.append(value)

        for key in delete_keys:
            del self.__known[key]

        return deleted

    @staticmethod
    def __get_key(alert: Alert) -> str:
        '''
        Internal method to provide a unique key for an alert

        :param alert: Alert that needs a unique key
        :return: The unique key
        '''
        # Cell ID, event, start time and altitude identify a warning. DWD provides no id in JSON format
        return alert.warnCellId + '_' + alert.event + '_' + alert.start + '_' + str(alert.altitudeStart) + '_' + str(
            alert.altitudeEnd)
