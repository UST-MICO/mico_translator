from .translators import MessageTranslator
from .messages import CloudEvent
from lxml import etree, builder
from typing import Any


class JsonToXmlTranslator(MessageTranslator, source_format='json', target_format='xml'):

    def test_message(self, message: CloudEvent):
        return isinstance(message.data, dict)

    def translate(self, message: CloudEvent) -> CloudEvent:
        translated = message.create_new_message()
        translated.contenttype = 'application/xml'
        E = builder.ElementMaker()
        ROOT = self.recursive_build(E, 'root', message.data)
        translated.data = etree.tostring(ROOT).decode()
        return translated

    def recursive_build(self, E: builder.ElementMaker, key, data: Any):
        if isinstance(data, dict):
            return self.build_element(E, key, [self.recursive_build(E, k, v) for k, v in data.items()])
        elif isinstance(data, (list, tuple)):
            return self.build_element(E, key, [self.recursive_build(E, key, value) for value in data])
        else:
            return self.build_element(E, key, str(data))

    def build_element(self, E: builder.ElementMaker, key, value):
        element = getattr(E, key)
        if isinstance(value, list):
            return element(*value)
        elif value is not None:
            return element(value)
        return element()
