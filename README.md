# mico_translator

### Use Cases
- The user can define a manipulation that is applied on the elements of an incoming message.
    - There are various manipulation types, that can be used: ADD, DELETE, REPLACE, COPY, CUSTOM
- The user can send messages to the translator to apply the defined data manipulation
- The user can define a consumer, to which each manipulated message is forwarded to


## Kafka commands:

```bash
# test producer
kafka-console-producer.sh --broker-list localhost:9092 --topic test

# test consumer
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic neu --partition 0
```

```bash
# create compact topic (adapt command to your installation where neccessary)
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --config cleanup.policy=compact --topic compact
```
