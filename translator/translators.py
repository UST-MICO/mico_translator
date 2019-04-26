from typing import Dict, Tuple


class MessageTranslator():

    translators: Dict[Tuple[str, str], 'MessageTranslator'] = {}

    def __init_subclass__(cls, source_format='', target_format='', **kwargs):
        MessageTranslator.translators[(source_format, target_format)] = cls()

    @staticmethod
    def get_translator(source_format: str, target_format: str):
        return MessageTranslator.translators.get((source_format, target_format))

    def translate(self, message: dict) -> dict:
        raise NotImplementedError()
