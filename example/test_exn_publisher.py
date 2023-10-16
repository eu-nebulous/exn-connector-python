import logging
import time

from exn import connector, core

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('exn.connector').setLevel(logging.DEBUG)


class MyHandler(connector.ConnectorHandler):

    def ready(self, context):
        if context.has_publisher('state'):
            context.publishers['state'].starting()
            context.publishers['state'].started()
            context.publishers['state'].custom('forecasting')
            context.publishers['state'].stopping()
            context.publishers['state'].stopped()

        context.publishers['config'].send({
            'hello': 'world'
        })
        context.publishers['preferences'].send()


class MyPublisher(core.publisher.Publisher):
    def __init__(self):
        super().__init__('preferences', 'preferences.changed', True)

    def send(self, body={}):
        body.update({
            "preferences": {
                "dark_mode": True
            }
        })
        super(MyPublisher, self).send(body)


connector = connector.EXN('ui', handler=MyHandler()
                          , publishers=[
        core.publisher.Publisher('config', 'config', True),
        MyPublisher(),
    ],
                          enable_health=True, enable_state=False
                          ,url='localhost'
                          ,port=5672
                          ,username="admin"
                          ,password="adming"
                          )

connector.start()
