#!/usr/bin/env python

## Rackspace Cloud Monitoring Plug-In
## MySQL Backup Validation
#
# (C)2016 Ruben Quinones <ruben.quinones@rackspace.com>
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Usage:
# Place plug-in in /usr/lib/rackspace-monitoring-agent/plugins
#
# The following is an example 'criteria' for a Rackspace Monitoring Alarm:
#
# if (metric['STATE'] == 'FAILED') {
#   return new AlarmStatus(CRITICAL, 'MySQL Backup FAILED.');
# }
#
# if (metric['STATE'] == 'FAILED' && metric['LAST_BACKUP_STATE'] == 'FAILED') {
#   return new AlarmStatus(CRITICAL, 'MySQL Backups FAILED.');
# }
#
# if (metric['STATE'] == 'DEGRADED') {
#   return new AlarmStatus(WARNING, 'MySQL Backup completed \
#       but the source is not in an ACTIVE state.');
# }
#
# return new AlarmStatus(OK, 'MySQL Scheduled Backup completed successfully');


import json


BACKUP_FILE = '/var/lib/trove/backup.json'

MESSAGE = """
status {check_status}
metric STATE string {state}
metric LAST_BACKUP_STATE string {last_backup_state}
metric LAST_BACKUP_SIZE float {last_backup_size} GB
metric TIME_TO_NEXT_SCHEDULED_BACKUP int32 \
{time_to_next_scheduled_backup} minutes
metric TIME_SINCE_LAST_SUCCESSFUL_BACKUP int32 \
{time_since_last_successful_backup} minutes
"""

DEFAULT_DATA = {
    'check_status': 'ERROR',
    'state': 'NOT_AVAILABLE',
    'last_backup_state': 'NOT_AVAILABLE',
    'last_backup_size': 0,
    'time_to_next_scheduled_backup': 0,
    'time_since_last_successful_backup': 0,
}

def get_mysql_backup_data():
    try:
        with open(BACKUP_FILE, 'r') as f:
            backup_data = json.loads(f.read())
            if backup_data.get('state') in ['FAILED', 'DEGRADED']:
                backup_data['check_status'] = 'ERROR'
            else:
                backup_data['check_status'] = 'OK'
            return backup_data
    except IOError:
        # No backup data available
        return DEFAULT_DATA


backup_data = get_mysql_backup_data()

try:
    formatted_message = MESSAGE.format(**backup_data)
except KeyError:
    # We are missing some data
    backup_data['check_status'] = 'ERROR'
    for key, value in DEFAULT_DATA.items():
        if key not in backup_data:
            backup_data[key] = value
    formatted_message = MESSAGE.format(**backup_data)

print(formatted_message)
