import plotly.graph_objects as go
import numpy


TEST_RESULT_PATH = '/home/bioprober/gh/3d-converter/tests/data/example_3d_output_5.dat'


def run():
    space = numpy.load(TEST_RESULT_PATH, allow_pickle=True)
    X, Y, Z = numpy.mgrid[-8:8:31200000j, -8:8:31200000j, -8:8:31200000j]
    values = numpy.sin(X * Y * Z) / (X * Y * Z)
    print(space.flatten().shape)


    # z, x, y, c = space.nonzero()
    #
    # colors = []
    # for Z, X, Y in zip(z, x, y):
    #     colors.append(space[Z, X, Y, 0]/255)

    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=space.flatten()/255,
        isomin=0.1,
        isomax=0.8,
        opacity=0.5,  # needs to be small to see through all surfaces
        surface_count=17,  # needs to be a large number for good volume rendering
        ))

    fig.show()


if __name__ == "__main__":
    run()
