from pathlib import Path

from json import load
from translator.messages import CloudEvent
from translator.translators import MessageTranslator


class TestMessageTranslator:

    def test_cloud_event_1(self):
        cloud_event: CloudEvent
        with Path('./test/test_data/cloud_event_2.json').open() as _file:
            data = load(_file)
            cloud_event = CloudEvent(data)
        translator: MessageTranslator = MessageTranslator.get_translator('json', 'xml')
        assert translator.test_message(cloud_event)
        translated = translator.translate(cloud_event)
        assert translated.contenttype == 'application/xml'
        assert translated.data == '<root><appinfoA>abc</appinfoA><appinfoB>123</appinfoB><appinfoC>True</appinfoC></root>'
