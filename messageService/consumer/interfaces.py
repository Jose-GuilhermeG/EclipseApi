from abc import ABC, abstractmethod


class IConsumer(ABC):

    @abstractmethod
    def validade(self):
        pass

    @abstractmethod
    def listen(self):
        pass


class IKafkaConsumer(ABC):
    @abstractmethod
    def consumer_topic(self, topic: str):
        pass


class IValidate(ABC):
    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def validate(self):
        pass
