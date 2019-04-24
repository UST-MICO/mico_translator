from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import TopicPartition


topic = 'wat'
bootstrap_servers = ['localhost:9092']
topic_partition = TopicPartition(topic=topic, partition=0)
msg = b'this is a message'


# The test can be executed using pytest
class TestKafka:

    def test_produce_and_consume(self):

        # publish 10 events to the topic 'wat'
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        for _ in range(10):
            producer.send(topic, msg)

        # consume all previous events, that where published to the topic 'wat'
        consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')
        events = consumer.poll(1000)[topic_partition]
        n_events = len(events)

        # the events is a list of events that must not be empty
        assert(n_events > 0)

        # the last event must (most likely) have the value 'this is a message'
        assert(events[n_events-1].value == msg)
