from .messages import CloudEvent
from kafka import KafkaProducer
from typing import List, Dict, Union


def route_message(sender: KafkaProducer, message: CloudEvent, default_topic: str = None):
    """Route the message according to routing slip or to default topic if no routing slip is present.

    Arguments:
        sender {KafkaProducer} -- The sender to send the message to
        message {CloudEvent} -- The message to route

    Keyword Arguments:
        default_topic {str} -- Fallback if no routing slip is present (default: {None})
    """
    topic = default_topic
    if 'routingSlip' not in message or len(message.routingSlip) <= 0:
        if default_topic is None:
            raise AttributeError('Default topic was None and message had no routingSlip!')
    else:
        dest: Union[str|Dict] = message.routingSlip.pop()
        if isinstance(dest, str):
            topic = dest
        else:
            topic = dest['topic']
    if 'route' not in message:
        message['route'] = []
    message.route.append(topic)
    sender.send(topic, message)
