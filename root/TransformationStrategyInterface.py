from abc import ABC, abstractmethod


class TransformationStrategyInterface(ABC):
    @abstractmethod
    def perform_transformation(self):
        pass
