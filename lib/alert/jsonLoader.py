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
import json
from datetime import datetime, timezone
from typing import List, Tuple

import requests
from import_lib.import_lib import get_logger

from lib.alert.Alert import Alert, from_dict
from lib.util.strings import remove_suffix, remove_prefix

logger = get_logger(__name__)

DWD_URL = "https://www.dwd.de/DWD/warnungen/warnapp/json/warnings.json"
headers = {'user-agent': 'https://github.com/SENERGY-Platform/import-dwd-alerts'}  # required by dwd


def get_most_recent() -> Tuple[datetime, List[Alert]]:
    '''
    Download latest alert file and transform alerts into Objects

    :return: Timestamp of last update and list of all alerts
    '''
    try:
        r = requests.get(DWD_URL, timeout=10, headers=headers)
    except requests.Timeout:
        logger.error("Error fetching latest alerts! Timeout")
        return datetime.now(), []
    if not r.ok:
        logger.error("Error fetching latest alerts! Code:" + str(r.status_code))
        return datetime.now(), []
    s = r.content.decode()
    s = remove_prefix(s, 'warnWetter.loadWarnings(')
    s = remove_suffix(s, ');')
    j = json.loads(s)
    l = []

    if 'warnings' not in j or 'time' not in j or 'vorabInformation'  not in j:
        logger.error('Error fetching latest alerts! Malformed reply')
        return datetime.now(), []

    for warnCellid in j['warnings']:
        for rawAlert in j['warnings'][warnCellid]:
            l.append(__transform_alert(warnCellid, 'Warnung', rawAlert))

    for warnCellid in j['vorabInformation']:
        for rawAlert in j['vorabInformation'][warnCellid]:
            l.append(__transform_alert(warnCellid, 'Vorabinformation', rawAlert))

    t_s = j['time'] / 1000
    return datetime.fromtimestamp(t_s, timezone.utc), l


def __transform_alert(warnCellId: str, urgency: str, raw_alert: dict) -> Alert:
    if 'end' not in raw_alert or 'start' not in raw_alert:
        raise ValueError('rawAlert malformed!')
    raw_alert['start'] = datetime.fromtimestamp(raw_alert['start'] / 1000, timezone.utc)
    if raw_alert['end'] is not None:
        raw_alert['end'] = datetime.fromtimestamp(raw_alert['end'] / 1000, timezone.utc)
    raw_alert['warnCellId'] = warnCellId
    raw_alert['urgency'] = urgency
    return from_dict(raw_alert)
