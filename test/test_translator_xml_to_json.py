from translator.translator import TranslatorXMLtoJSON
from translator.helpers import load_test_data
from translator_test import TranslatorTest

import json


class TestTranslatorXMLtoJSON(TranslatorTest):

    def test_translate_1(self):
        """
        Tests if the translator is able to transform a simple XML to JSON
        """
        cloud_event = self._get_cloud_event_template(load_test_data('test_xml_1.xml'))
        translator = TranslatorXMLtoJSON()
        result = translator.translate(cloud_event)
        result_data = json.loads(result.data)
        assert('audience' in result_data.keys())
        assert(result_data['audience']['name'] == 'foo')

    def test_translate_2(self):
        """
        Tests if the translator is able to transform a XML with attributes in the tags
        """
        cloud_event = self._get_cloud_event_template(load_test_data('test_xml_2.xml'))
        translator = TranslatorXMLtoJSON()
        result = translator.translate(cloud_event)
        result_data = json.loads(result.data)
        assert ('audience' in result_data.keys())
        assert (result_data['audience']['name'] == 'foo')
