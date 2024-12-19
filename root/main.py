from RunBlend import RunBlend
from blending_functions.DarkenBlending import DarkenBlending
from blending_functions.MultiplyBlending import MultiplyBlending
from blending_functions.NormalBlending import NormalBlending
from RunTransformations import RunTransformations
from transformation_functions.ColorTransformation import ColorTransformation
from transformation_functions.OrderTransformation import OrderTransformation
from transformation_functions.ResolutionTransformation import ResolutionTransformation  # noqa
from SynthesizeChainEnum import SynthesizeChainEnum


def main():
    RT = RunTransformations(SynthesizeChainEnum.SYNTHESIZE)
    RT.set_transformations([ColorTransformation(), ResolutionTransformation(), OrderTransformation()])  # noqa
    RT.run_transformations()

    RB = RunBlend()
    RB.set_blend(MultiplyBlending())
    RB.run_blend()
    RB.set_blend(DarkenBlending())
    RB.run_blend()
    RB.set_blend(NormalBlending())
    RB.run_blend()


if __name__ == "__main__":
    main()
