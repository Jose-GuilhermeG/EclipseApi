from core.interfeces import IProducer
from kafka.producer import KafkaProducer
from django.conf import settings
from core.utils import json_serializer
from types import FunctionType


def kafkaProducerFactory(servers, serializer):
    return KafkaProducer(bootstrap_servers=servers, value_serializer=serializer)


class KafkaMessageProducer(IProducer):
    def __init__(
        self,
        servers: list[str] = settings.KAFKA_SERVER,
        serializer: FunctionType = json_serializer,
        kafkaFactory: FunctionType = kafkaProducerFactory,
    ):
        self.servers: list[str] = servers
        self.serializer: FunctionType = serializer
        self.factory: FunctionType = kafkaFactory
        self.producer = self.factory(self.servers, self.serializer)

    def sender(self, topic, value, on_success, on_fail):
        self.producer.send(topic, value).add_callback(on_success).add_errback(on_fail)


class messageProducer:
    def __init__(self, producer: IProducer):
        self.producer = producer

    def sender(
        self,
        to: str,
        value: dict,
        on_success: FunctionType = lambda success: print(success),
        on_fail: FunctionType = lambda fail: print(fail),
    ):
        self.producer.sender(to, value, on_success, on_fail)
