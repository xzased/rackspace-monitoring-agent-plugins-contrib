#!/usr/bin/env python

## Rackspace Cloud Monitoring Plug-In
## MySQL Scheduled Backup Validation
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
#   return new AlarmStatus(CRITICAL, 'MySQL Scheduled Backup FAILED.');
# }
#
# if (metric['STATE'] == 'FAILED' && metric['ERROR_COUNT'] >= 3) {
#   return new AlarmStatus(CRITICAL, 'MySQL Scheduled Backups FAILED \
#       multiple times.');
# }
#
# if (metric['STATE'] == 'DEGRADED') {
#   return new AlarmStatus(WARNING, 'MySQL Scheduled Backup completed \
#       but the source is not in an ACTIVE state.');
# }
#
# return new AlarmStatus(OK, 'MySQL Scheduled Backup completed successfully');


import json


BACKUP_INFO = '/var/trove/backup.json'


def mysql_backup_check():
    error_count = 0
    try:
        with open(BACKUP_INFO, 'rw') as f:
            data = json.loads(f.read())
            state = data.get('state')
            previous_backups = data.get('previous_backups', [])
            error_state = (b for b in previous_backups if
                            b.state in ['FAILED', 'DEGRADED'])
            error_count = len(error_state)
    except IOError:
        # No scheduled backup available
        state = None
    except:
        # Error loading the backup info
        state = 'ERROR'
    return state, error_count


state, error_count = mysql_backup_check()


if not state:

elif state in ['FAILED', 'DEGRADED']:
    output = ('status ERROR\nmetric STATE string {0}\n'
              'metric ERROR_COUNT int32 {1}')
    print(output.format(state, error_count))
else:
    output = ('status OK\nmetric STATE string {0}\n'
              'metric ERROR_COUNT int32 {1}')
    print(output.format(state, error_count))
