from abc import ABC, abstractmethod

class IETFClassifier(ABC):
    @abstractmethod
    def classify(self, input: str):
        pass