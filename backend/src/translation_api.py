import google_trans_new


def translate(text:str) -> str:
    translator = google_trans_new.google_translator()
    translated = translator.translate(text, lang_src="en", lang_tgt="ru")
    return translated
