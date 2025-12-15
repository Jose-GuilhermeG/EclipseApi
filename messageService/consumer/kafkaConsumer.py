from kafka.consumer import KafkaConsumer
from .interfaces import IConsumer, IKafkaConsumer, IValidate
from json import loads
from types import FunctionType


def json_deserializer(json):
    return loads(json.decode("utf-8"))


class kafkaValidateConsumerData(IValidate):
    def __init__(self, deserializer: FunctionType):
        self.deserializer = deserializer

    def process_data(self, data):
        return self.deserializer(data)

    def validade(self, data):
        decode_data = self.process_data(data)
        if not len(decode_data):
            raise Exception("Sem dados")

        return decode_data


class kafkaConsumer(
    kafkaValidateConsumerData,
    IConsumer,
    IKafkaConsumer,
):

    def __init__(self, server: str, deserializer: FunctionType):
        super().__init__(deserializer)
        self.server = server

    def consumer_topic(self, topic: str) -> KafkaConsumer:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.server,
            value_deserializer=self.validade,
            auto_offset_reset="earliest",
        )

        return consumer

    def listen(self, topic: str, action: FunctionType) -> None:
        consumer = self.consumer_topic(topic)
        action(consumer)
