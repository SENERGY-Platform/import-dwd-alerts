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
from typing import Optional, Union
import rfc3339
import json


class Alert(object):
    '''
    Class to store DWD alert
    '''
    def __init__(self, warnCellId: str, regionName: str, end: Optional[Union[datetime, str]],
                 start: Union[datetime, str], type: int,
                 state: str, level: int,
                 description: str, event: str, headline: str, instruction: str, stateShort: str,
                 altitudeStart: Optional[int],
                 altitudeEnd: Optional[int], urgency: str):
        self.warnCellId = warnCellId
        self.regionName = regionName
        self.__end = end
        if end is not None and isinstance(end, datetime):
            self.__end = rfc3339.format(end, utc=True)
        if isinstance(start, datetime):
            self.__start = rfc3339.format(start, utc=True)
        else:
            self.__start = start
        self.type = type
        self.state = state
        self.level = level
        self.description = description
        self.event = event
        self.headline = headline
        self.instruction = instruction
        self.stateShort = stateShort
        self.altitudeStart = altitudeStart
        self.altitudeEnd = altitudeEnd
        self.urgency = urgency

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, end: Optional[datetime]):
        self.__end = end
        if end is not None:
            self.__end = rfc3339.format(end, utc=True)

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start: datetime):
        self.__start = rfc3339.format(start, utc=True)

    def __str__(self):
        return json.dumps(self.dict(), ensure_ascii=False)

    def __eq__(self, other):
        return self.dict() == other.dict()

    def dict(self) -> dict:
        '''
        Get this alert as dict . Datetimes are already converted to rfc3339 strings

        :return: dict representation of alert
        '''
        d = self.__dict__.copy()
        d['end'] = d['_Alert__end']
        del d['_Alert__end']
        d['start'] = d['_Alert__start']
        del d['_Alert__start']
        return d

    def end_dt(self) -> datetime:
        '''
        Get the end property as datetime

        :return: end property as datetime
        '''
        return datetime.strptime(self.__end, "%Y-%m-%dT%H:%M:%SZ").astimezone(timezone.utc)


def from_dict(d: dict) -> Alert:
    '''
    Create an Alert from a dict

    :param d: Alert in dict representation
    :return: Alert
    :except ValueError: If the dict is missing one or more values
    '''
    if not 'regionName' in d or \
            not 'warnCellId' in d or \
            not 'urgency' in d or \
            not 'end' in d or \
            not 'start' in d or \
            not 'type' in d or \
            not 'level' in d or \
            not 'state' in d or \
            not 'description' in d or \
            not 'event' in d or \
            not 'headline' in d or \
            not 'instruction' in d or \
            not 'stateShort' in d or \
            not 'altitudeStart' in d or \
            not 'altitudeEnd' in d:
        raise ValueError('dict malformed!')
    return Alert(warnCellId=d['warnCellId'], urgency=d['urgency'], regionName=d['regionName'], end=d['end'],
                 start=d['start'], type=d['type'], level=d['level'],
                 description=d['description'],
                 event=d['event'], headline=d['headline'], instruction=d['instruction'],
                 state=d['state'], stateShort=d['stateShort'], altitudeStart=d['altitudeStart'],
                 altitudeEnd=d['altitudeEnd'])
