from .interfeces import IConsumer


class MessageConsumer:
    def __init__(self, consumer: IConsumer):
        self.consumer = consumer

    def listen(self, to, action):
        self.consumer.listen(to, action)
