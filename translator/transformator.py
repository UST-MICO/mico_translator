from abc import abstractmethod
from importlib import import_module, invalidate_caches


class AbstractTransformator:
    """
    This class contains basic functionalities, that are required by Transformators.
    """

    def __init__(self, user_functions, dependencies=None, main_function_name="script"):
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
        :param (str) function_name: The name of the entry point function (main function)

        :return: function object of the entry point function (main function)
        """
        for func in user_functions or []:
            exec(func["function"])
            globals()[func["function_name"]] = locals()[func["function_name"]]
        # exec(user_script)
        # locals()[function_name]
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
    def transform(self, msg):
        """
        :param msg: The message, that shall be transformed
        :return: the result of the message transformation
        """
        pass


class TransformatorCustom(AbstractTransformator):
    """
    This transformer only applies the user defined functions. There are no additional features.
    """
    def __init__(self, user_functions, dependencies=None, main_function_name="script"):
        super().__init__(user_functions, dependencies, main_function_name)

    def transform(self, msg):
        return self.user_script(msg)





