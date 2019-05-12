from helpers import load_test_data
from translator import TranslatorEDIT
from translator_test import TranslatorTest
from abstract_translator import MessageTranslator
import json

msg_data_1 = {
    "customer": {
        "profile": {
            "id": 1,
            "name": "John Doe"
        }
    }
}


class TestTranslatorEDIT(TranslatorTest):

    def test_0(self):
        translator = MessageTranslator.get_translator('json', 'json', 'edit')
        assert translator.target_format == 'json'
        assert translator.source_format == 'json'
        assert translator.operation == 'edit'

    def test_1(self):
        script = load_test_data('test_script_4.py')
        element_paths = json.loads(load_test_data('test_paths_4.json'))
        cloud_event = self._get_cloud_event_template(msg_data_1)
        trns = TranslatorEDIT()
        trns.set_script(script, 'script')
        trns.set_element_paths(element_paths)
        result = trns.translate(cloud_event)

        assert(result.data['customer']['profile']['id'] == 101)
        assert (result.data['customer']['profile']['name'] == 'john doe')
