from typing import List
from kafka import KafkaConsumer, KafkaProducer
from .translators import MessageTranslator
from json import loads, dumps
from json.decoder import JSONDecodeError


class TranslationManager():

    def __init__(self, bootstrap_servers: List[str], source_topic: str, target_topic: str, translator):
        self.bootstrap_servers = bootstrap_servers
        self.source_topic = source_topic
        self.target_topic = target_topic
        self.consumer = KafkaConsumer(self.source_topic, bootstrap_servers=bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: dumps(v).encode('utf-8'))
        self.translator = translator

    def start_consuming(self):
        for consumerRecord in self.consumer:
            try:
                message = loads(consumerRecord.value.decode())
            except JSONDecodeError:
                print(f'Could not deserialize message "{consumerRecord.value.decode()}", skipping message!')
                continue
            print(f'Translating message "{message}"')
            translated = self.translator.translate(message)
            print(f'Translated message "{translated}"')
            self.producer.send(self.target_topic, translated)

