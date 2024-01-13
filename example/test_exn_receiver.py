import sys
sys.path.insert(0,'../exn')


import logging

from dotenv import load_dotenv
load_dotenv()

from proton import Message
from exn.connector import EXN
from exn.core.consumer import Consumer
from exn.core.context import Context
from exn.core.handler import Handler
from exn.handler.connector_handler import ConnectorHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('exn.connector').setLevel(logging.DEBUG)


class MyGeneralHandler(Handler):
    def on_message(self, key, address, body, message: Message, context=None):
        logging.info(f"[MyGeneralHandler] Received {key} => {address}: {body}")


class Bootstrap(ConnectorHandler):
    context = None

    def ready(self, context: Context):
        self.context = context
        # do work here

        self.context.register_consumers(
            Consumer('ui_health', 'health', handler=my_general_handler, topic=True)
        )


class MyConfigHandler(Handler):
    def on_message(self, key, address, body, message: Message, context=None):
        logging.info(f"[MyConfigHandler{self}] Received {key} => {address}: {body}")


my_general_handler = MyGeneralHandler()

connector = EXN('ui', handler=Bootstrap(),
                          consumers=[
                              Consumer('ui_all', 'eu.nebulouscloud.ui.preferences.>',
                                                     handler=my_general_handler,
                                                     topic=True,
                                                     fqdn=True),
                              Consumer('config_two', 'config',
                                                     handler=MyConfigHandler(),
                                                     application="two",
                                                     topic=True,
                                                     ),
                              Consumer('config_one', 'config',
                                                     handler=MyConfigHandler(),
                                                     application="one",
                                                     topic=True,
                                                     ),

                          ])

connector.start()
