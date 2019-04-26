import os
from .translation_manager import TranslationManager
from .translators import MessageTranslator

if __name__ == "__main__":
    translator = MessageTranslator.get_translator('json', 'xml')
    manager = TranslationManager(['localhost:9092'], 'test', 'neu', translator)
    try:
        manager.start_consuming()
    except KeyboardInterrupt:
        print('exiting program')
