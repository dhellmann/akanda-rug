import logging
import os
import sys

from oslo.config import cfg

from akanda.rug import main
from akanda.rug import state


class Fake(object):
    def __init__(self, crud):
        self.crud = crud


def delete_callback(self):
    print 'DELETE'


def bandwidth_callback(self, *args, **kwargs):
    print 'BANDWIDTH:', args, kwargs


def debug_one_router(args=sys.argv[1:]):

    main.register_and_load_opts(args)

    # Add our extra option for specifying the router-id to debug
    cfg.CONF.register_cli_opts([
        cfg.StrOpt('router-id',
                   required=True,
                   help='The UUID for the router to debug',
                   ),
    ])
    cfg.CONF(args, project='akanda')

    logging.basicConfig(
        level=logging.DEBUG,
        format=':'.join('%(' + n + ')s'
                        for n in ['processName',
                                  'threadName',
                                  'name',
                                  'levelname',
                                  'message']),
    )

    log = logging.getLogger(__name__)
    log.debug('Proxy settings: %r', os.getenv('no_proxy'))

    a = state.Automaton(
        cfg.CONF.router_id,
        delete_callback,
        bandwidth_callback
    )

    a.send_message(Fake('update'))

    import pdb
    pdb.set_trace()

    a.update()