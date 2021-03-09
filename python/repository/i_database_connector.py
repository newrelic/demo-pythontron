from abc import ABC, abstractmethod


class IDatabaseConnector(ABC):

    @abstractmethod
    def connect(self, **kwargs):
        raise NotImplementedError()
