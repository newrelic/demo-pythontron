from abc import ABC, abstractmethod


class IDatabaseConnection(ABC):

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def close(self, **kwargs):
        pass
