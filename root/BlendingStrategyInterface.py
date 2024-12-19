from abc import ABC, abstractmethod


class BlendingStrategyInterface(ABC):
    @abstractmethod
    def perform_blend(self):
        pass
