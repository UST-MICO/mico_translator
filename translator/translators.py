from .messages import CloudEvent
from abc import abstractmethod
from typing import Dict, Tuple


class MessageTranslator():
    """
    Abstract message translator class.
    """

    translators: Dict[Tuple[str, str], 'MessageTranslator'] = {}

    def __init_subclass__(cls, source_format='', target_format='', **kwargs):
        """
        Registration hook for subclasses.

        All MessageTranslators need to provide source and target format.
        """
        MessageTranslator.translators[(source_format, target_format)] = cls()
        cls.source_format = source_format
        cls.target_format = target_format

    @staticmethod
    def get_translator(source_format: str, target_format: str):
        """
        Get the translator translating from source to target format.
        """
        return MessageTranslator.translators.get((source_format, target_format))

    @abstractmethod
    def test_message(self, message: CloudEvent) -> bool:
        """
        Test wether the translator can handle the message.
        """
        raise NotImplementedError()

    @abstractmethod
    def translate(self, message: CloudEvent) -> CloudEvent:
        """
        Actual translation method of the translator.
        """
        raise NotImplementedError()
