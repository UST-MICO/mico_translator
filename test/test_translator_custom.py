from translator.helpers import load_test_data
from translator.translator import TranslatorCUSTOM
from translator_test import TranslatorTest
import json


class TestTranslatorCustom(TranslatorTest):

    def test_apply_script_1(self):
        """
        Tests if the AbstractTranslator is able to load a user defined function and apply it on a message
        """
        cloud_event = self._get_cloud_event_template(data='this is a plain text message')
        config = json.loads(load_test_data('test_config_1.json'))
        trns = TranslatorCUSTOM(user_functions=config['function_scripts'])
        result = trns.translate(cloud_event)
        assert('translated: ' + cloud_event.data == result.data)

    def test_apply_script_2(self):
        """
        Tests if 2 or more user defined functions can invoke each other. test_config_2.json defines the functions
        'script(string)' and foo(string). 'skript' invokes 'foo'.
        """
        cloud_event = self._get_cloud_event_template('this is a plain text message')
        config = json.loads(load_test_data('test_config_2.json'))
        trns = TranslatorCUSTOM(user_functions=config['function_scripts'])
        result = trns.translate(cloud_event)

        assert('translated: ' + cloud_event.data == result.data)

    def test_import_dependencies(self):
        """
        Tests if the translator is able to import dependencies, such that they can be applied in a user defined
        function. test_config_3.json contains a user defined function that has the 'json' library as dependency.
        The translator has to import the library before the user defined function is invoked. The test is successful,
        when the translator appends the key value pair ('test', 'test_data')
        """
        cloud_event = self._get_cloud_event_template('{"name": "this is a json"}')
        config = json.loads(load_test_data('test_config_3.json'))
        trns = TranslatorCUSTOM(user_functions=config['function_scripts'], dependencies=config['dependencies'])
        result = trns.translate(cloud_event)
        assert(('test', 'test_data') in result.data.items())
