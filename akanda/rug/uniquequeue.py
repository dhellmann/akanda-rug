"""A Queue subclass that only supports one instance of any given item.
"""

import logging
import Queue
import threading

LOG = logging.getLogger(__name__)

# alias
Empty = Queue.Empty


class UniqueQueue(object):

    def __init__(self):
        self._u_lock = threading.Lock()
        self._u_set = set()
        self._q = Queue.Queue()

    def put(self, item, block=True, timeout=None):
        with self._u_lock:
            if item not in self._u_set:
                LOG.debug('adding %r', item)
                self._u_set.add(item)
                return self._q.put(item, block, timeout)
            else:
                LOG.debug('%r is already in the work queue', item)

    def get(self, block=True, timeout=None):
        with self._u_lock:
            item = self._q.get(block, timeout)
            self._u_set.remove(item)
            return item

    def task_done(self):
        with self._u_lock:
            self._q.task_done()

    def qsize(self):
        with self._u_lock:
            return self._q.qsize()
