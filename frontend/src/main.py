import sys
import logging
from threading import Thread
import threading

from PyQt5.QtWidgets import QApplication
import pika

from rabbit_client import PikaConsumer
from ui import TranslationInfo

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()


def main():
    try:
        app = QApplication(sys.argv)
        window = TranslationInfo()
        rabbit_client = PikaConsumer(window)
        pika_thread = Thread(target=rabbit_client.consume)
        logger.info("QT service started")
        pika_thread.start()
        sys.exit(app.exec())
    except Exception as e:
        logger.exception(e)
        if pika_thread:
            pika_thread.join()
        sys.exit(0)

if __name__ == "__main__":
    main()
