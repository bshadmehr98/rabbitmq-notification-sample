import os


def test_env_variable():
    assert os.environ['RUN_MODE'] == 'TESTING'
