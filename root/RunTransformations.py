from SynthesizeChainEnum import SynthesizeChainEnum
from TransformationStrategyInterface import TransformationStrategyInterface as TSI


class RunTransformations:
    def __init__(self, mode: SynthesizeChainEnum):
        self.mode: SynthesizeChainEnum = mode
        self.transformationss: list[TSI]

    def set_transformations(self, transformation: list[TSI]):
        self.transformations = transformation

    def get_transformations(self):
        return self.transformations

    def set_mode(self, mode: SynthesizeChainEnum):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def run_transformations(self):
        if self.mode == SynthesizeChainEnum.CHAIN:
            from run_chain import run_chain
            run_chain(self)
        elif self.mode == SynthesizeChainEnum.SYNTHESIZE:
            from run_synthesize import run_synthesize
            run_synthesize(self)
        else:
            print("fail")
