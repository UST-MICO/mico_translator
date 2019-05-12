from os import environ
from translation_manager import TranslationManager
from abstract_translator import \
    MessageTranslator, MessageTranslatorUserDefinedFunctions, MessageTranslatorPathManipulation
from json import load

if __name__ == "__main__":
    SOURCE_FORMAT = environ.get('SOURCE_FORMAT', 'json')
    TARGET_FORMAT = environ.get('TARGET_FORMAT', 'xml')
    OPERATION = environ.get('OPERATION', 'format_translation')
    SCRIPT_FILE = environ.get('SCRIPT_FILE', '')
    FUNCTION_NAME = environ.get('FUNCTION_NAME', '')
    PATHS_FILE = environ.get('PATHS_FILE', '')

    SOURCE_TOPIC = environ.get('SOURCE_TOPIC', 'test')
    TARGET_TOPIC = environ.get('TARGET_TOPIC', 'neu')
    KAFKA_BROKER = environ.get('KAFKA_BROKER', 'localhost:9092')

    print(f'Starting translation from "{SOURCE_FORMAT}" to "{TARGET_FORMAT}".')
    print(f'Subscribing to kafka broker "{KAFKA_BROKER}" topic "{SOURCE_TOPIC}".')
    print(f'Publishing translated messages on topic "{TARGET_TOPIC}"')

    translator = MessageTranslator.get_translator(SOURCE_FORMAT, TARGET_FORMAT, OPERATION)
    if isinstance(translator, MessageTranslatorUserDefinedFunctions) and SCRIPT_FILE != '':
        with open(SCRIPT_FILE, 'r') as file:
            script = file.read()
        translator.set_script(script, FUNCTION_NAME)
    if isinstance(translator, MessageTranslatorPathManipulation) and PATHS_FILE != '':
        with open(PATHS_FILE, 'r') as file:
            paths = load(file)
            translator.set_element_paths(paths)

    manager = TranslationManager([KAFKA_BROKER], SOURCE_TOPIC, TARGET_TOPIC, translator)
    try:
        manager.start_consuming()
    except KeyboardInterrupt:
        print('exiting program')
