from helpers import load_test_data
from abstract_translator import MessageTranslator
from translation_manager import TranslationManager
from translator_test import TranslatorTest
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from time import sleep
import threading
from queue import Queue
import json

bootstrap_servers = ['localhost:9092']


def _consume_manager(manager):
    manager.start_consuming()


def _consume_response(consumer, queue):
    for consumed_record in consumer:
        d = json.loads(consumed_record.value.decode())
        queue.put(d['data'])
        break


class TestTranslationManager(TranslatorTest):

    @staticmethod
    def _set_topics(topic_names):
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        available_topics = consumer.topics()
        topics = [NewTopic(name, num_partitions=1, replication_factor=1)
                  for name in topic_names if name not in available_topics]
        if len(topics) > 0:
            admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            admin.create_topics(topics)
            admin.create_topics('manager_test_out')
        _ = KafkaConsumer().topics()
        for topic in available_topics:
            assert topic in _


    def test_0(self):
        """
        This test creates a translation manager, sends a message to it and checks if the
        message was correctly translated.
        """
        # set up a queue and some test topics
        queue = Queue()
        topic_names = ['manager_test_in', 'manager_test_out']
        self._set_topics(topic_names)

        # create the translator and provide it to the manager
        trns = MessageTranslator.get_translator('json', 'json', 'edit')
        trns.set_script(load_test_data('test_script_4.py'), 'script')
        trns.set_element_paths(json.loads(load_test_data('test_paths_4.json')))
        manager = TranslationManager(bootstrap_servers, topic_names[0], topic_names[1],
                                     trns)

        # run the manager
        thread_manager = threading.Thread(
            target=_consume_manager,
            args=[manager])
        thread_manager.start()

        # set up a consumer for receiving the response of the manager.
        consumer_response = KafkaConsumer(topic_names[1], bootstrap_servers=bootstrap_servers)
        thread_consumer = threading.Thread(
            target=_consume_response,
            args=[consumer_response, queue]
        )

        # run the consumer
        thread_consumer.start()

        sleep(2)

        # create a message and a producer
        msg = json.dumps(
            self._get_cloud_event_template({"customer": {"profile": {"id": 1, "name": "John Doe"}}}).message)
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

        # send the message with the producer
        producer.send('manager_test_in', bytes(msg, 'utf-8'))

        # wait until the manager response was consumed
        while True:
            if not queue.empty():
                break

        result = queue.get()

        # test if the message was translated correctly
        assert (result['customer']['profile']['id'] == 101)
        assert (result['customer']['profile']['name'] == 'john doe')
