from kafka import KafkaProducer
from kafka import KafkaConsumer
from helpers import load_test_data
from time import sleep

bootstrap_servers = ['localhost:9092']


class TestTranslationWithKafka:

    def test_cloud_event_1(self):
        event = load_test_data('cloud_event_2.json')
        sender = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: v.encode('utf-8'))
        consumer = KafkaConsumer('neu', bootstrap_servers=bootstrap_servers)
        consumer.subscribe(topics=['neu'])
        for i in range(20):
            if consumer.assignment():
                break
            sleep(1)
        else:
            raise IOError('Could not subscribe to target topic!')
        consumer.seek_to_end()
        sender.send('test', value=event)
        for msg in consumer:
            print(msg)
