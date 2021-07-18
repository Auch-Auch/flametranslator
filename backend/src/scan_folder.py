import time
import logging
import os
from PIL import Image

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import pytesseract

from rabbit_client import PikaPublisher
from etc.config import TRANSLATE_QUEUE
from translation_api import translate


class FolderWatcher:
    'Class defining a scan folder'

    def __init__(self, path):
        self.path = path
        self.pika = PikaPublisher()
        self.event_handler = PatternMatchingEventHandler(patterns=["*.jpg", "*.jpeg", "*.png"],
                                    ignore_patterns=[],
                                    ignore_directories=True)
        self.event_handler.on_created = self.on_created
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=False)
        self.observer.start()
    
    def on_created(self, event):
        path = event.src_path
        _, file_extension = os.path.splitext(path)
        if file_extension in [".jpg", ".png", ".jpeg"]:
            text = str(pytesseract.image_to_string(path, lang="eng"))
            translated = translate(text)
            msg = {"text": text, "translated": translated}
            self.pika.publish(msg, TRANSLATE_QUEUE)
        os.remove(event.src_path)

    def on_any_event(self, event):
        pass

    def stop(self):
        self.observer.stop()
        self.observer.join()
