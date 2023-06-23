import os


def pytest_configure(config):
    os.environ["RUN_MODE"] = "TESTING"
