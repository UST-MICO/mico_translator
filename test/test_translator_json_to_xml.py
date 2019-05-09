from translator import TranslatorJSONtoXML
from helpers import load_test_data
from translator_test import TranslatorTest
from translator.messages import CloudEvent
from json import loads
from lxml import etree


class TestTranslatorJSONtoXML(TranslatorTest):

    def test_translate_1(self):
        """
        Tests if the translator is able to transform a simple JSON to XML
        """
        cloud_event = CloudEvent(loads(load_test_data('cloud_event_2.json')))
        translator = TranslatorJSONtoXML()
        result = translator.translate(cloud_event)

        tree_xml = etree.fromstring(result.data)
        l_elements = tree_xml.getchildren()
        assert l_elements[0].tag == 'appinfoA'
        assert l_elements[1].text == '123'
        assert l_elements[2].text == 'True'



