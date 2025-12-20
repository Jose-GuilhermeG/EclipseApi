from abc import ABC, abstractmethod


class IProducer(ABC):

    @abstractmethod
    def sender(self):
        pass
