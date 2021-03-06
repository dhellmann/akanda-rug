# Copyright 2014 DreamHost, LLC
#
# Author: DreamHost, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""Periodic health check code.
"""

import logging
import threading
import time

from akanda.rug import event

LOG = logging.getLogger(__name__)


def _health_inspector(period, scheduler):
    """Runs in the thread.
    """
    while True:
        time.sleep(period)
        LOG.debug('waking up')
        e = event.Event(
            tenant_id='*',
            router_id='*',
            crud=event.POLL,
            body={},
        )
        scheduler.handle_message('*', e)


def start_inspector(period, scheduler):
    """Start a health check thread.
    """
    t = threading.Thread(
        target=_health_inspector,
        args=(period, scheduler,),
        name='HealthInspector',
    )
    t.setDaemon(True)
    t.start()
    return t
