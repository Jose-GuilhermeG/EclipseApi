from kafka.consumer import KafkaConsumer
from .interfeces import IConsumer, IKafkaConsumer, IValidate
from json import loads
from types import FunctionType


def json_deserializer(json):
    return loads(json.decode("utf-8"))


def kafak_consumer_factory(
    topic: str,
    bootstrap_servers: list[str],
    value_deserializer: FunctionType,
    auto_offset_reset: str,
):
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=value_deserializer,
        auto_offset_reset=auto_offset_reset,
    )


class kafkaValidateConsumerData(IValidate):
    def __init__(self, deserializer: FunctionType):
        self.deserializer = deserializer

    def process_data(self, data):
        return self.deserializer(data)

    def validate(self, data):
        decode_data = self.process_data(data)
        if not len(decode_data):
            raise Exception("Sem dados")

        return decode_data


class kafkaMessageConsumer(
    kafkaValidateConsumerData,
    IConsumer,
    IKafkaConsumer,
):

    def __init__(
        self,
        server: str,
        deserializer: FunctionType,
        kafka_consumer_factory: FunctionType = kafak_consumer_factory,
        auto_offset_reset: str = "latest",
    ):
        super().__init__(deserializer)
        self.server = server
        self.factory = kafak_consumer_factory
        self.auto_offset_reset = auto_offset_reset

    def consumer_topic(self, topic: str) -> KafkaConsumer:
        consumer = self.factory(
            topic=topic,
            bootstrap_servers=self.server,
            value_deserializer=self.validate,
            auto_offset_reset=self.auto_offset_reset,
        )
        return consumer

    def listen(self, topic: str, action: FunctionType) -> None:
        consumer = self.consumer_topic(topic)
        action(consumer)
