from abc import ABC, abstractmethod

class SearchBase(ABC):

    def tokenizer(self, text):
        return text.lower().split()

    @abstractmethod
    def search(self, query: str, top_k: int=5):
        pass
