from RunTransformations import RunTransformations


def run_chain(RT: RunTransformations):
    transformations = RT.get_transformations()
    i = 0
    for transformation in transformations:
        transformation.perform_transformation()
        print(i)
        i += 1
