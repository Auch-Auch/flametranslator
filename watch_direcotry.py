import time
import os
import pytesseract
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import tkinter as tk 
from google_trans_new import google_translator


_text = 'test'

def on_created(event):
    path = event.src_path
    filename, file_extension = os.path.splitext(path)
    if file_extension in [".jpg", ".png", ".jpeg"]:
        text = str(pytesseract.image_to_string(path, lang="eng"))

        global _text
        _text = text.strip()
    os.remove(event.src_path)


if __name__ == "__main__":
    print('work')
    window = tk.Tk()
    window.geometry('200x200')
    # окно поверх остальных
    window.attributes("-topmost",True)
    
    translator = google_translator()
    
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = "/home/alex-auch/Pictures"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    
    text = _text
    msg = None
    
    try:
        while True:
            if _text != text:
                if msg:
                    msg.destroy()
                print(_text)
                trans_text = translator.translate("hello", lang_src='en', lang_tgt='ru')
                msg = tk.Label(text=trans_text)
                msg.pack()
                text = _text
            window.update_idletasks()
            window.update()

            time.sleep(1)
    except KeyboardInterrupt:
        window.destroy()
        my_observer.stop()
        my_observer.join()


hello