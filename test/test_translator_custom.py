from helpers import load_test_data
from translator_test import TranslatorTest
from translator import TranslatorCUSTOM
from abstract_translator import MessageTranslator


class TestTranslatorCustom(TranslatorTest):

    def test_0(self):
        translator = MessageTranslator.get_translator('json', 'json', 'custom')
        assert translator.source_format == 'json'
        assert translator.target_format == 'json'
        assert translator.operation == 'custom'

    def test_apply_script_1(self):
        """
        Tests if the AbstractTranslatorUserDefinedFunctions is able to load a user defined function
        and apply it on a message
        """
        cloud_event = self._get_cloud_event_template(data='this is a plain text message')
        script = load_test_data('test_script_1.py')
        trns = TranslatorCUSTOM()
        trns.set_script(script, 'script')
        result = trns.translate(cloud_event)
        assert 'translated: this is a plain text message' == result.data

    def test_apply_script_2(self):
        """
        Tests if 2 or more user defined functions can invoke each other. test_config_2.json defines the functions
        'script(string)' and foo(string). 'script' invokes 'foo'.
        Also tests if the user can use 'import' or 'from ... import ...' statements.
        """
        cloud_event = self._get_cloud_event_template(data='this is a plain text message')
        script = load_test_data('test_script_2.py')
        trns = TranslatorCUSTOM()
        trns.set_script(script, 'script')
        result = trns.translate(cloud_event)
        assert('translated: This Is A Plain Text Message' == result.data)
