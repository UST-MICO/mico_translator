from translator.translator import TranslatorXMLtoJSON
from translator.helpers import load_test_data
import json

class TestTranslatorXMLtoJSON:

    def test_translate_1(self):
        """
        Tests if the translator is able to transform a simple XML to JSON
        """
        str_xml = load_test_data('test_xml_1.xml')
        translator = TranslatorXMLtoJSON()
        result = json.loads(translator.translate(str_xml))
        assert('audience' in result.keys())
        assert(result['audience']['name'] == 'foo')

    def test_translate_2(self):
        """
        Tests if the translator is able to transform a XML with attributes in the tags
        """
        str_xml = load_test_data('test_xml_2.xml')
        translator = TranslatorXMLtoJSON()
        result = json.loads(translator.translate(str_xml))
        assert ('audience' in result.keys())
        assert (result['audience']['name'] == 'foo')