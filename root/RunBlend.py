from BlendingStrategyInterface import BlendingStrategyInterface as BSI


class RunBlend:
    def __init__(self):
        self.blend: BSI

    def set_blend(self, blend: BSI):
        self.blend = blend

    def get_blend(self):
        return self.blend

    def run_blend(self):
        self.blend.perform_blend()
