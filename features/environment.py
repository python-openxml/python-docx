"""Set testing environment before and after behave acceptance test runs."""

import os

scratch_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], "_scratch"))


def before_all(context):
    if not os.path.isdir(scratch_dir):
        os.mkdir(scratch_dir)
