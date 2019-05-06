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
    The user provides a set of user defined functions to the init function.
    The functions are then instantiated. Everytime when a message comes in
    Translator.CUSTOM.translate, the user defined functions are applied on
    this message. It is required, that the user provides the name of the initial
    function (main_function_name), to which the message shall be provided (the
    other functions may then invoked by this function)
    When the user defined functions apply some dependencies, these can as well
    be provided in the init_function

    Example:
    =======

        The user defines the functions, that are applied on the each message and
        passes them to the translator:
        > functions = [{
                        'function_name': 'script',
                        'function': 'def script(string):\n    return "translated: " + string'
                      }]
        > trns = TranslatorCUSTOM().init(user_functions=functions)

        Now let's simulate an incoming message
        > cloud_event = self._get_cloud_event_template('this is a plain text message')
        > result = trns.translate(cloud_event)

        As defined in the user defined function 'script' the string 'translated: '
        was prepended to the message data
        > print(result)
        >> 'translated: this is a plain text message'
    """
    def init(self, user_functions=None, dependencies=None, main_function_name="script"):
        """
        TODO: Should be a normal constructor. But this is not possible right now as MessageTranslator requires a default constructor without arguments.
        """
        return super().init(user_functions, dependencies, main_function_name)

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError

    def translate(self, message: CloudEvent):
        translated = message.create_new_message()
        translated.data = self.user_script(message.data)
        return translated


class TranslatorEDIT(
        MessageTranslatorUserDefinedFunctions, MessageTranslatorPathManipulation,
        source_format='json', target_format='json', operation='edit'):
    """
    This translator is intended to edit a user defined set of elements in the message.
    When the translator is created, the user defines the path to each element, that he/she
    wants to edit. To every path, he defines a key.
    The user defined function then gets a dictionary with all the elements and the corresponding
    keys. The user defined function then manipulates each element. The new values are then
    automatically injected into the message.

    Example:
    =======

        The user defines key and path for each element, that shall be edited
        > element_paths = [
            {
                'key': 'path_1',
                'path': 'customer.profile.id'
            },
            {
                'key': 'path_2',
                'path': 'customer.profile.name'
            }]

        The user defines the function, that shall be applied on the elements
        > user_functions = [{
                            'function_name': 'script',
                            'function': "def script(dict_elements):
                                            dict_elements['path_1'] = dict_elements['path_1'] + 100
                                            dict_elements['path_2'] = dict_elements['path_2'].lower()
                                            return dict_elements\n"}]


        Let's create the translator with the corresponding paths and functions
        > trns = TranslatorEDIT().init(
                            user_functions= user_functions,
                            dict_element_paths=element_paths)

        Now let's simulate an incoming message
        > cloud_event = self._get_cloud_event_template({'customer': {'profile': {'id': 1, 'name': 'John Doe'}}})
        > result = trns.translate(cloud_event)

        As defined by the user defined function the elements in the following paths were manipulated:
            - customer.profile.id: Add 100 to the original value
            - customer.profile.name: convert to lower case

        > print(result.data)
        >> {'customer': {'profile': {'id': 101, 'name': 'john doe'}}}
    """

    dict_element_paths = None

    def init(self, user_functions, dict_element_paths, dependencies=None, main_function_name="script", **kwargs):
        """
        TODO: Should be a normal constructor. But this is not possible right now as MessageTranslator requires a default constructor without arguments.
        """
        MessageTranslatorUserDefinedFunctions.init(self, user_functions, dependencies, main_function_name)
        MessageTranslatorPathManipulation.init(self, dict_element_paths)
        return self

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError

    def translate(self, message: CloudEvent):
        translated = message.create_new_message()
        dict_elements = self._extract_elements_from_dict(message.data)
        translated_elements = self.user_script(dict_elements)
        for d in self.dict_element_paths:
            translated.data = self._set_element_from_path(translated.data, d['path'], translated_elements[d['key']])
        return translated


class TranslatorREMOVE(MessageTranslatorPathManipulation, source_format='json', target_format='json', operation='remove'):

    def init(self, dict_element_paths=None):
        """
        TODO: Should be a normal constructor. But this is not possible right now as MessageTranslator requires a default constructor without arguments.
        """
        return super().init(dict_element_paths)

    def translate(self, message: CloudEvent) -> CloudEvent:
        translated = message.create_new_message()
        for p in self.dict_element_paths:
            translated.data = self._delete_element_from_path(translated.data, p['path'])
        return translated

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError


class TranslatorADD(MessageTranslatorUserDefinedFunctions):
    """
    TODO
    This translator adds some data to each message that arrives. Therefore, the user
    provides a key-value pair for every element that shall be added. The key must
    represent the path, at which the value is then added to the message.
    """
    def translate(self, a):
        raise NotImplementedError


class TranslatorJSONtoXML(MessageTranslator, source_format='json', target_format='xml', operation='format_translation'):
    """
    A simple translator for converting messages from the JSON format to XML.
    Example:
    =======

        Create the translator:
        > translator = TranslatorJSONtoXML()

        Let's simulate an incoming message:
        > cloud_event = CloudEvent(loads(load_test_data('cloud_event_2.json')))
        > result = translator.translate(cloud_event)

        The XML was translated to JSON:
        > print(result.data)
        >> '<root><appinfoA>abc</appinfoA><appinfoB>123</appinfoB><appinfoC>True</appinfoC></root>'
    """

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
    A simple translator that converts from XML to JSON.

    Example:
    =======

        Create the translator:
        > translator = TranslatorXMLtoJSON()

        Let's simulate an incoming message:
        > cloud_event = self._get_cloud_event_template(load_test_data('test_xml_1.xml')))
        > result = translator.translate(cloud_event)

        The XML was converted to JSON
        > print(result.data)
        >>{"audience": {"id": "123", "name": "foo"}}
    """

    def test_message(self, message: CloudEvent) -> bool:
        raise NotImplementedError

    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        translated.data = json.dumps(xmltodict.parse(msg.data))
        return translated

