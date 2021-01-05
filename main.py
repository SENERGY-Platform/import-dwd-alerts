# Copyright 2020 InfAI (CC SES)
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

import time

import schedule
from import_lib.import_lib import ImportLib, get_logger

from lib.alert.AlertImport import AlertImport

if __name__ == '__main__':
    lib = ImportLib()
    logger = get_logger(__name__)
    alertImport = AlertImport(lib)

    alertImport.import_most_recent()

    logger.info("Setting schedule to run every 10 minutes")
    schedule.every(10).minutes.do(alertImport.import_most_recent)

    while True:
        schedule.run_pending()
        time.sleep(1)
