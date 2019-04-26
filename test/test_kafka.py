from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import KafkaAdminClient
from kafka import TopicPartition
from kafka.admin import NewTopic


bootstrap_servers = ['localhost:9092']

# The test can be executed using pytest
class TestKafka:

    def test_delete_topics(self):
        # get all topics...
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        topics = consumer.topics()

        # ...and delete them
        client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        client.delete_topics(topics)

        # ...now check if they were all deleted
        topics = consumer.topics()
        assert(len(topics) == 0)

    def test_create_topics(self):
        # create topics ...
        topic_names = ['test_1', 'test2', 'test_3']

        # submit the request
        client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        client.create_topics([NewTopic(name, num_partitions=1, replication_factor=1) for name in topic_names])

        # request all registered topics
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        topics = consumer.topics()

        # check if the requested topics were created
        for topic in topic_names:
            assert(topic in topics)

    def test_produce_and_consume(self):
        topic = 'test_4'
        topic_partition = TopicPartition(topic='test_4', partition=0)
        msg = b'this is a message'
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
