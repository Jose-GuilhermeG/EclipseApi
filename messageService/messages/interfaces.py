# imports
from abc import ABC, abstractmethod


class IEmailSender(ABC):

    @abstractmethod
    def get_email_manager(self):
        pass

    @abstractmethod
    def send_email(self):
        pass

    @abstractmethod
    def get_smtp_server(self) -> str:
        pass


class IEmailBuilder(ABC):
    @abstractmethod
    def get_message(self):
        pass


class ISmtpClient(ABC):
    @abstractmethod
    def as_string(self):
        pass

    @abstractmethod
    def attach(self):
        pass


class IMessage(ABC):
    @abstractmethod
    def send_message(self):
        pass
