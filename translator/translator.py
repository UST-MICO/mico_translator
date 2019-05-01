from abc import abstractmethod
from importlib import import_module, invalidate_caches
from translator.messages import CloudEvent
import json
import xmltodict
from translator.helpers import element_from_path, set_element_from_path


class AbstractTranslator:
    """
    This class contains basic functionalities, that are required by Transformators.
    """

    def __init__(self, user_functions=None, dependencies=None, main_function_name="script"):
        self._import_modules(dependencies)
        self.dependencies = dependencies
        self.script = user_functions
        self.main_function_name = main_function_name
        self.user_script = self._load_user_defined_functions(user_functions, main_function_name)
        pass

    @staticmethod
    def _load_user_defined_functions(user_functions, main_function_name):
        """
        Loads the user defined functions into the global variable space. Additionally loads the function, which can
        be used as entry point (main function) when a message shall be transformed.
        :param ([dict]) user_functions: A list of dictionaries. Each provides a python function
        :param ([str]) user_functions: The name of the entry point function (main function)

        :return: function object of the entry point function (main function)
        """
        if user_functions is not None:
            for func in user_functions or []:
                exec(func["function"])
                globals()[func["function_name"]] = locals()[func["function_name"]]
            invalidate_caches()
            return globals()[main_function_name]

    @staticmethod
    def _import_modules(modules):
        """
        Imports the modules, that are required in the user defined functions.
        :param ([str]) modules: the names of the modules, that shall be imported
        """
        for module in modules or []:
            globals()[module] = import_module(module)
        invalidate_caches()

    @abstractmethod
    def translate(self, msg):
        """
        :param msg: The message, that shall be transformed
        :return: the result of the message transformation
        """
        pass


class TranslatorCUSTOM(AbstractTranslator):
    """
    This transformer only applies the user defined functions. There are no additional features.
    """
    def __init__(self, user_functions, dependencies=None, main_function_name="script"):
        super().__init__(user_functions, dependencies, main_function_name)

    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        translated.data = self.user_script(msg.data)
        return translated


class TranslatorXMLtoJSON(AbstractTranslator):
    """
    This transformer converts an XML to JSON
    """
    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        translated.data = json.dumps(xmltodict.parse(msg.data))
        return translated


class TranslatorEDIT(AbstractTranslator):
    def __init__(self, user_functions, dict_element_paths, dependencies=None, main_function_name="script"):
        super().__init__(user_functions, dependencies, main_function_name)
        self.dict_element_paths = self._prepare_dict_element_paths(dict_element_paths)

    @staticmethod
    def _prepare_dict_element_paths(dict_element_paths):
        return [{'key': d['key'], 'path':d['path'].split('.')} for d in dict_element_paths]

    def _extract_elements_from_dict(self, dict_msg):
        d = dict()
        for dict_path in self.dict_element_paths:
            d[dict_path['key']] = element_from_path(dict_msg, dict_path['path'])
        return d

    def translate(self, msg: CloudEvent):
        translated = msg.create_new_message()
        dict_elements = self._extract_elements_from_dict(msg.data)
        translated_elements = self.user_script(dict_elements)
        for d in self.dict_element_paths:
            translated.data = set_element_from_path(translated.data, d['path'], translated_elements[d['key']])
        return translated


class TranslatorREMOVE(AbstractTranslator):
    def translate(self, msg):
        raise NotImplementedError


class TranslatorADD(AbstractTranslator):
    """
    This translator adds one or more elements to a message message
    """
    def translate(self, a):
        raise NotImplementedError



