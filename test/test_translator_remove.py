from translator.helpers import load_test_data
from translator.translator import TranslatorREMOVE
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


class TestTranslatorREMOVE(TranslatorTest):

    def test_0(self):
        trns = TranslatorREMOVE()
        assert trns.operation == 'remove'
        assert trns.source_format == 'json'
        assert trns.source_format == 'json'

    def test_1(self):
        cloud_event = self._get_cloud_event_template(msg_data_1)
        config = json.loads(load_test_data('test_config_5.json'))
        trns = TranslatorREMOVE().init(dict_element_paths=config['element_paths'])
        result = trns.translate(cloud_event)

        assert 'name' not in result.data['customer']['profile'].keys()
        assert 'id' in result.data['customer']['profile'].keys()


