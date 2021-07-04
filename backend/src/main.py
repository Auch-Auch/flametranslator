import time
import logging
import os
from PIL import Image

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import pytesseract

from rabbit_client import PikaPublisher
from scan_folder import FolderWatcher
from etc.config import DIRECTORY_TO_WATCH


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()


def main():
    folder_watcher = None
    try:
        folder_watcher = FolderWatcher(DIRECTORY_TO_WATCH)
        logger.info(f"Daemon started, watching {DIRECTORY_TO_WATCH}")
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info(f"Daemon stopped")
        if folder_watcher:
            folder_watcher.stop()


if __name__ == "__main__":
    main()
