import logging

from exn import connector, core

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('exn.connector').setLevel(logging.DEBUG)


class Bootstrap(connector.ConnectorHandler):

    def on_message(self, key, address, body, context, **kwargs):
        logging.info(f"Received {key} => {address}")
        if key == 'ui_health':
            logging.info(f"I am healthy => {body}")

        if key == 'ui_all':
            logging.info(f"These are my preferences => {body}")


connector = connector.EXN('ui', handler=Bootstrap(),
                          consumers=[
                              core.consumer.Consumer('ui_health', 'health', topic=True),
                              core.consumer.Consumer('ui_all', 'eu.nebulouscloud.ui.preferences.>', topic=True,
                                                     fqdn=True)
                          ])

connector.start()
