from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka import ConsumerRebalanceListener
from translator.messages import CloudEvent
from time import sleep, time
from random import choice

bootstrap_servers = ['localhost:9092']
message_keys = [str(i+1).encode() for i in range(10)]
topic = 'compact'
client_id = 'compacted-topic-client-12'
client_group_id = 'compacted-topic-client-group-11'


class Rebalance_Listener(ConsumerRebalanceListener):

    def on_partitions_revoked(self, revoked):
        print('revoked', revoked)

    def on_partitions_assigned(self, assigned):
        print('assigned', assigned)


def send_messages():
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: v.encode('utf-8'),
        batch_size=0,
        client_id=client_id
    )
    for i in range(4):
        key = choice(message_keys)
        message = str(time())
        print(f'Sending message {message} with key {key}')
        producer.send(topic, value=message, key=key)
    producer.close()


def read_messages():
    consumer = KafkaConsumer(topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        consumer_timeout_ms=3000,
        fetch_max_wait_ms=1000,
        client_id=client_id
        #group_id=client_group_id
    )
    print(consumer.topics(), consumer.subscription(), consumer.partitions_for_topic(topic))
    #partition = [p for p in consumer.partitions_for_topic(topic)][0]
    #topic_partition = TopicPartition(topic, partition)
    #consumer.assign([topic_partition])
    try:
        while not consumer.assignment():
            print('subscribe...')
            consumer.subscribe(topics=[topic], listener=Rebalance_Listener())
            sleep(1)
        print('Subscription:', consumer.subscription())
        print('Assignment:', consumer.assignment())
        print('Paused topics:', consumer.paused())
        for tp in consumer.assignment():
            print(tp, consumer.position(tp))
        #consumer.seek_to_beginning(topic_partition)
        consumer.seek_to_beginning()
        #print('Position in log:', consumer.position(topic_partition))
        for m in consumer:
            print(m)
        #messages = consumer.poll(timeout_ms=0)
        #print(messages)
    finally:
        consumer.unsubscribe()
        consumer.close()


def simple_consume():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    consumer = KafkaConsumer(topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        consumer_timeout_ms=3000,
        fetch_max_wait_ms=1000,
        client_id=client_id
        #group_id=client_group_id
    )
    for message in consumer:
        print(message)


if __name__ == "__main__":
    send_messages()
    read_messages()
    #simple_consume()