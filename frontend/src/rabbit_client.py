import asyncio
import sys
import json
import logging

import pika
from PyQt5.QtWidgets import QWidget

from etc.config import TRANSLATE_QUEUE
from ui import TranslationInfo


class PikaConsumer():
    def __init__(self, window:QWidget, url:str = "localhost", queue:str = TRANSLATE_QUEUE):
        self.url = url
        self.connected= False
        self.queue = queue
        self.window = window
        self.logger = logging.getLogger(__name__)


    def consume(self) -> None:
        try:
            self.conn = pika.BlockingConnection(pika.ConnectionParameters(self.url))
            channel = self.conn.channel()
            channel.queue_declare(queue=self.queue)
            channel.basic_consume(
                queue=self.queue, 
                on_message_callback=self.on_message_callback, 
                auto_ack=True)
            self.logger.info("Consumer started, waiting for messages..")
            channel.start_consuming()
        except Exception as e:
            self.logger.exception(f"Error while consuming, reason: {e}")
            sys.exit(0)


    def on_message_callback(self, ch, method, properties, body):
        data = json.loads(body)
        self.window.show_text(data["translated"])
