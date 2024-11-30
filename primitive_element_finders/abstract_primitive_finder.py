from abc import abstractmethod


class AbstractPrimitiveFinder:
    @abstractmethod
    def find_first(self):
        pass

    @abstractmethod
    def find_all(self):
        pass