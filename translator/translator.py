import json
import xmltodict
from translator.abstract_translator import *
from .messages import CloudEvent
from lxml import etree, builder
from typing import Any



class TranslatorCUSTOM(
        MessageTranslatorUserDefinedFunctions,
        source_format='json', target_format='json', operation='custom'):
    """
    This transformer only applies the user defined functions. There are no additional features.
    """

    def init(self, user_functions=None, dependencies=None, main_function_name="script"):
        """
        TODO: Should be a normal constructor. But this is not possible right now as MessageTranslator
        requires a default constructor without arguments.
        """
        return super().init(user_functions, dependencies, main_function_name)

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError

    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        translated.data = self.user_script(msg.data)
        return translated


class TranslatorEDIT(
        MessageTranslatorUserDefinedFunctions, MessageTranslatorPathManipulation,
        source_format='json', target_format='json', operation='edit'):

    dict_element_paths = None

    def init(self, user_functions, dict_element_paths, dependencies=None, main_function_name="script", **kwargs):
        """
        TODO: Should be a normal constructor. But this is not possible right now as MessageTranslator
        requires a default constructor without arguments.
        """
        MessageTranslatorUserDefinedFunctions.init(self, user_functions, dependencies, main_function_name)
        MessageTranslatorPathManipulation.init(self, dict_element_paths)
        return self

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError

    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        dict_elements = self._extract_elements_from_dict(msg.data)
        translated_elements = self.user_script(dict_elements)
        for d in self.dict_element_paths:
            translated.data = self._set_element_from_path(translated.data, d['path'], translated_elements[d['key']])
        return translated


class TranslatorADD(MessageTranslatorUserDefinedFunctions):
    """
    This translator adds one or more elements to a message message
    """
    def translate(self, a):
        raise NotImplementedError


class TranslatorJSONtoXML(MessageTranslator, source_format='json', target_format='xml', operation='format_translation'):

    def test_message(self, message: CloudEvent):
        return isinstance(message.data, dict)

    def translate(self, message: CloudEvent) -> CloudEvent:
        translated = message.create_new_message()
        translated.contenttype = 'application/xml'
        E = builder.ElementMaker()
        ROOT = self.recursive_build(E, 'root', message.data)
        translated.data = etree.tostring(ROOT).decode()
        return translated

    def recursive_build(self, E: builder.ElementMaker, key, data: Any):
        if isinstance(data, dict):
            return self.build_element(E, key, [self.recursive_build(E, k, v) for k, v in data.items()])
        elif isinstance(data, (list, tuple)):
            return self.build_element(E, key, [self.recursive_build(E, key, value) for value in data])
        else:
            return self.build_element(E, key, str(data))

    def build_element(self, E: builder.ElementMaker, key, value):
        element = getattr(E, key)
        if isinstance(value, list):
            return element(*value)
        elif value is not None:
            return element(value)
        return element()


class TranslatorXMLtoJSON(
        MessageTranslator,
        source_format='xml', target_format='json', operation='format_translation'):
    """
    This transformer converts an XML to JSON
    """

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError

    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        translated.data = json.dumps(xmltodict.parse(msg.data))
        return translated

