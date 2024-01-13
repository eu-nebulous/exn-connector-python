
import sys

from exn.core.publisher import Publisher
from exn.handler.connector_handler import ConnectorHandler

sys.path.insert(0,'../exn')

import logging

from dotenv import load_dotenv
load_dotenv()

from exn import connector, core

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('exn.connector').setLevel(logging.DEBUG)


class Bootstrap(ConnectorHandler):

    def ready(self, context):
        if context.has_publisher('state'):
            context.publishers['state'].starting()
            context.publishers['state'].started()
            context.publishers['state'].custom('forecasting')
            context.publishers['state'].stopping()
            context.publishers['state'].stopped()

        context.publishers['config'].send({
            'hello': 'world'
        },application="one")

        context.publishers['config'].send({
            'good': 'bye'
        },application="two")

        if context.has_publisher('preferences'):
            context.publishers['preferences'].send()


class MyPublisher(Publisher):

    def __init__(self):
        super().__init__( 'preferences', 'preferences', topic=True)

    def send(self):
        super(MyPublisher, self).send({
            "preferences": {
                "dark_mode": True
            }
        })


connector = connector.EXN('ui', handler=Bootstrap()
                          , publishers=[
        core.publisher.Publisher('config', 'config', True),
        MyPublisher()
    ],
          enable_health=True, enable_state=True
          ,url='localhost'
          ,port=5672
          ,username="admin"
          ,password="admin"
          )

connector.start()
