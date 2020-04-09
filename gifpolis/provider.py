import abc

class GifProvider:
    def __init__(self):
        pass

    @abc.abstractmethod
    def search(query):
        pass

    