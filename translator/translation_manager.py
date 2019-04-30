from typing import List
from kafka import KafkaConsumer, KafkaProducer
from .translators import MessageTranslator
from .messages import CloudEvent
from json import loads, dumps
from json.decoder import JSONDecodeError


class TranslationManager():
    """
    Manages on the fly translation of messages between source_topic and target_topic.
    """

    def __init__(self, bootstrap_servers: List[str], source_topic: str, target_topic: str, translator):
        self.bootstrap_servers = bootstrap_servers
        self.source_topic = source_topic
        self.target_topic = target_topic
        self.consumer = KafkaConsumer(self.source_topic, bootstrap_servers=bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: v.serialize_message().encode('utf-8'))
        self.translator = translator

    def start_consuming(self):
        """
        Start consuming messages from the source_topic, translate them and send them to target_topic.
        """
        for consumerRecord in self.consumer:
            try:
                message = CloudEvent(loads(consumerRecord.value.decode()))
            except JSONDecodeError:
                print(f'Could not deserialize message "{consumerRecord.value.decode()}", skipping message!')
                continue
            except KeyError:
                print(f'Message "{consumerRecord.value.decode()}" is not a valid cloud event, skipping message!')
                continue
            if not self.translator.test_message(message):
                continue # skip messages the translator can't handle
            print(f'Translating message "{message.serialize_message()}"')
            translated = self.translate_message(message)
            print(f'Translated message "{translated.serialize_message()}"')
            self.producer.send(self.target_topic, translated)

    def translate_message(message: CloudEvent) -> CloudEvent:
        """
        Wrap translator.translate.
        """
        return self.translator.translate(message)

