from messages import CloudEvent
from typing import Dict, Tuple
from abc import abstractmethod
from importlib import import_module, invalidate_caches
from copy import deepcopy


class MessageTranslator():
    """
    Abstract message translator class.
    """

    translators: Dict[Tuple[str, str, str], 'MessageTranslator'] = {}

    def __init_subclass__(cls, source_format='', target_format='', operation='', **kwargs):
        """
        Registration hook for subclasses.

        All MessageTranslators need to provide source and target format.
        """
        MessageTranslator.translators[(source_format, target_format, operation)] = cls()
        cls.source_format = source_format
        cls.target_format = target_format
        cls.operation = operation

    @staticmethod
    def get_translator(source_format: str, target_format: str, operation: str) -> 'MessageTranslator':
        """
        Get the translator translating from source to target format.
        """
        return MessageTranslator.translators.get((source_format, target_format, operation))

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


class MessageTranslatorUserDefinedFunctions(MessageTranslator, operation='abstract_class_user_defined_functions'):
    """
    This class contains basic functionalities, that are required by Transformators.
    """
    dependencies = None
    script = None
    main_function_name = None
    user_script = None

    def init(self, user_functions=None, dependencies=None, main_function_name="script", **kwargs):
        """
        TODO: Should be a normal constructor. But this is not possible right now as MessageTranslator
        requires a default constructor without arguments.
        """
        self._import_modules(dependencies)
        self.dependencies = dependencies
        self.script = user_functions
        self.main_function_name = main_function_name
        self.user_script = self._load_user_defined_functions(user_functions, main_function_name)
        return self

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
    def test_message(self, message: CloudEvent) -> bool:
        """
        Documentation see MessageTranslator
        """
        raise NotImplementedError


class MessageTranslatorPathManipulation(MessageTranslator, operation='abstract_class_path_manipulation'):

    dict_element_paths = None

    def init(self, dict_element_paths=None):
        self.dict_element_paths = self._prepare_dict_element_paths(dict_element_paths)
        return self

    def _element_from_path(self, dictionary, list_path):
        l = deepcopy(list_path)
        key = l.pop(0)
        if len(l) > 0:
            return self._element_from_path(dictionary[key], l)
        else:
            return dictionary[key]

    @staticmethod
    def _set_element_from_path(dictionary, list_path, value):
        def recursion(d, l):
            key = l.pop(0)
            if len(l) > 0:
                return recursion(d[key], l)
            else:
                d[key] = value

        l_aux = deepcopy(list_path)
        d_aux = deepcopy(dictionary)
        recursion(d_aux, l_aux)
        return d_aux

    @staticmethod
    def _delete_element_from_path(dictionary, list_path):
        def recursion(d, l):
            key = l.pop(0)
            if len(l) > 0:
                return recursion(d[key], l)
            else:
                del d[key]
        l_aux = deepcopy(list_path)
        d_aux = deepcopy(dictionary)
        recursion(d_aux, l_aux)
        return d_aux


    @staticmethod
    def _prepare_dict_element_paths(dict_element_paths):
        return [{'key': d['key'], 'path': d['path'].split('.')} for d in dict_element_paths]

    def _extract_elements_from_dict(self, dict_msg):
        d = dict()
        for dict_path in self.dict_element_paths:
            d[dict_path['key']] = self._element_from_path(dict_msg, dict_path['path'])
        return d

    @abstractmethod
    def test_message(self, message: CloudEvent) -> bool:
        """
        Documentation see MessageTranslator
        """
        raise NotImplementedError

