from abc import ABC, abstractmethod


class Store(ABC):

    @abstractmethod
    def get_suburl(self):
        pass

    @abstractmethod
    def set_suburl(self):
        pass

    @abstractmethod
    def get_proxy(self):
        pass

    @abstractmethod
    def set_proxy(self):
        pass


class LeancloudStore(Store):
    pass
