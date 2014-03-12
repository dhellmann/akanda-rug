import Queue
import threading

import unittest2 as unittest

from akanda.rug import uniquequeue


class TestUniqueQueue(unittest.TestCase):

    def test_single_thread(self):
        class T(object):
            pass

        q = uniquequeue.UniqueQueue()
        a = T()
        q.put(a)
        q.put(a)
        self.assertEqual(1, q.qsize())

    def test_add_after_get(self):
        class T(object):
            pass

        q = uniquequeue.UniqueQueue()
        a = T()
        q.put(a)
        self.assertEqual(1, q.qsize())
        q.get()
        self.assertEqual(0, q.qsize())
        q.put(a)
        q.put(a)
        self.assertEqual(1, q.qsize())

    def test_multiple_threads(self):
        class T(object):
            pass

        q = uniquequeue.UniqueQueue()
        a = T()
        threads = [
            threading.Thread(target=q.put, args=(a,))
            for i in range(2)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(1, q.qsize())

    def test_empty(self):
        q = uniquequeue.UniqueQueue()
        self.assertRaises(Queue.Empty, q.get, False, 0)
        self.assertRaises(Queue.Empty, q.get, True, 0)
        
