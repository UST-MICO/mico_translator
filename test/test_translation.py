from json import load
from messages import CloudEvent
from abstract_translator import MessageTranslator
from helpers import get_project_root


class TestMessageTranslator:

    def test_cloud_event_1(self):
        cloud_event: CloudEvent
        with (get_project_root() / 'test' / 'test_data' / 'cloud_event_2.json').open() as _file:
            data = load(_file)
            cloud_event = CloudEvent(data)
        translator: MessageTranslator = MessageTranslator.get_translator('json', 'xml', 'format_translation')
        assert translator.test_message(cloud_event)
        translated = translator.translate(cloud_event)
        assert translated.contenttype == 'application/xml'
        assert translated.data == '<root><appinfoA>abc</appinfoA><appinfoB>123</appinfoB><appinfoC>True</appinfoC></root>'
