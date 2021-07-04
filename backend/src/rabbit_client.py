import asyncio
import json
import pika
import logging


class PikaPublisher():
    def __init__(self, url:str = "localhost"):
        self.loop = asyncio.get_event_loop()
        self.url = url
        self.connected= False
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(self.url))
        self.logger = logging.getLogger(__name__)


    def publish(self, msg:dict, queue:str):
        if self.conn:
            try:
                channel = self.conn.channel()
                channel.queue_declare(queue=queue)
                channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=json.dumps(msg))
                self.logger.info(f"msg: {msg} sent to queue: {queue}")
            except Exception as e:
                self.logger.exception(f"Error while sending {msg}, reason {e}")
        else:
            self.logger.warning(f"Connection to host {self.url} is not established")
