from RunTransformations import RunTransformations


def run_synthesize(RT: RunTransformations):
    transformations = RT.get_transformations()
    for transformation in transformations:
        transformation.perform_transformation()
        print(0)
