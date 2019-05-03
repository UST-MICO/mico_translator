from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import KafkaAdminClient
from kafka import TopicPartition
from kafka.admin import NewTopic
from translator.messages import CloudEvent
from translator.helpers import load_test_data
from json import loads, dumps
from pathlib import Path

bootstrap_servers = ['localhost:9092']


class TestTranslationWithKafka:

    def test_cloud_event_1(self):
        event = load_test_data('cloud_event_1.json')
        sender = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: v.encode('utf-8'))
        sender.send('test', value=event)
        consumer = KafkaConsumer('neu', bootstrap_servers=bootstrap_servers)
        consumer.seek_to_beginning()
        for msg in consumer:
            print(msg)
