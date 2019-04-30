import os
from pathlib import Path
from json import load
from .translation_manager import TranslationManager
from .translators import MessageTranslator
from .messages import CloudEvent

if __name__ == "__main__":
    translator = MessageTranslator.get_translator('json', 'xml')
    """
    with Path('./test/test_data/cloud_event_2.json').open() as _file:
        data = load(_file)
        cloud_event = CloudEvent(data)
        if translator.test_message(cloud_event):
            translated = translator.translate(cloud_event)
            print(translated.serialize_message())
    """
    manager = TranslationManager(['localhost:9092'], 'test', 'neu', translator)
    try:
        manager.start_consuming()
    except KeyboardInterrupt:
        print('exiting program')
