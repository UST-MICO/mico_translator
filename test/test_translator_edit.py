from translator.helpers import load_test_data
from translator.translator import TranslatorEDIT
import json

msg_data_1 = {
    "customer": {
        "profile": {
            "id": 1,
            "name": "John Doe"
        }
    }
}


class TestTranslatorEDIT:
    def test_1(self):
        config = json.loads(load_test_data('test_config_4.json'))
        trns = TranslatorEDIT(user_functions=config['function_scripts'], dict_element_paths=config['element_paths'])
        result = trns.translate(msg_data_1)

        assert(result['customer']['profile']['id'] == 101)
        assert (result['customer']['profile']['name'] == 'john doe')
