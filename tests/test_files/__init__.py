import os

CURDIR = os.path.dirname(os.path.abspath(__file__))


def get_python_icon_png():
    """Return fully defined path to a png file containing the python logo."""
    return os.path.join(CURDIR, "python-icon.png")
