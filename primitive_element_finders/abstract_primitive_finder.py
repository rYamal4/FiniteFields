from abc import abstractmethod


class AbstractPrimitiveFinder:
    @abstractmethod
    def find_any(self):
        pass

    @abstractmethod
    def find_all(self):
        pass