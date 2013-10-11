"""Populate the workers with the existing routers
"""

import logging
import threading
import time

from oslo.config import cfg
from quantumclient.common import exceptions as q_exceptions

from akanda.rug import event
from akanda.rug.api import quantum

LOG = logging.getLogger(__name__)


def _pre_populate_workers(scheduler):
    """Fetch the existing routers from quantum.

    Wait for quantum to return the list of the existing routers.
    Pause up to max_sleep seconds between each attempt and ignore
    quantum client exceptions.


    """
    nap_time = 1
    max_sleep = 15

    quantum_client = quantum.Quantum(cfg.CONF)

    while True:
        try:
            quantum_routers = quantum_client.get_routers()
            break
        except (q_exceptions.Unauthorized, q_exceptions.Forbidden) as err:
            LOG.warning('PrePopulateWorkers thread failed: %s', err)
            return
        except Exception as err:
            LOG.warning(
                '%s: %s' % ('Could not fetch routers from quantum', err))
            LOG.warning('sleeping %s seconds before retrying' % nap_time)
            time.sleep(nap_time)
            # FIXME(rods): should we get max_sleep from the config file?
            nap_time = min(nap_time * 2, max_sleep)

    LOG.debug('Start pre-populating the workers with %d fetched routers',
              len(quantum_routers))

    for router in quantum_routers:
        message = event.Event(
            tenant_id=router.tenant_id,
            router_id=router.id,
            crud=event.POLL,
            body={}
        )
        scheduler.handle_message(router.tenant_id, message)


def pre_populate_workers(scheduler):
    """Start the pre-populating task
    """

    t = threading.Thread(
        target=_pre_populate_workers,
        args=(scheduler,),
        name='PrePopulateWorkers'
    )

    t.setDaemon(True)
    t.start()
    return t