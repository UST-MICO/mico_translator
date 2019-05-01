from translator.helpers import load_test_data
from translator.translator import TranslatorEDIT
from translator_test import TranslatorTest
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

    def test_1(self):
        cloud_event = self._get_cloud_event_template(msg_data_1)
        config = json.loads(load_test_data('test_config_4.json'))
        trns = TranslatorEDIT(user_functions=config['function_scripts'], dict_element_paths=config['element_paths'])
        result = trns.translate(cloud_event)

        assert(result.data['customer']['profile']['id'] == 101)
        assert (result.data['customer']['profile']['name'] == 'john doe')
