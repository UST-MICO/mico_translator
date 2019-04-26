from .translators import MessageTranslator


class JsonToXmlTranslator(MessageTranslator, source_format='json', target_format='xml'):

    def translate(self, message: dict) -> dict:
        return message
