import abc

class Zone(abc.ABC):
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def add(self, card):
        pass

    @abc.abstractmethod
    def remove(self, id_num):
        pass
