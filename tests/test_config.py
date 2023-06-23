from config import Config
import os


def test_singleton_instance():
    # Test that only one instance of Config is created
    config1 = Config()
    config2 = Config()
    assert config1 is config2


def test_default_values():
    # Unset environment variables
    os.environ.pop("RABBITMQ_HOST", None)
    os.environ.pop("RABBITMQ_PORT", None)
    os.environ.pop("RABBITMQ_USER", None)
    os.environ.pop("RABBITMQ_PASSWORD", None)
    os.environ.pop("RABBITMQ_VHOST", None)
    os.environ.pop("RUN_MODE", None)

    # Test that default values are set if environment variables are not present
    config = Config(load_from_file=False)
    assert config.RABBITMQ_HOST == "localhost"
    assert config.RABBITMQ_PORT == 5672
    assert config.RABBITMQ_USER == "admin"
    assert config.RABBITMQ_PASSWORD == "admin"
    assert config.RABBITMQ_VHOST == "localhost"
    assert config.RUN_MODE == "DEBUG"

    os.environ["RUN_MODE"] = "TESTING"


def test_is_test_mode():
    config = Config()

    config.RUN_MODE = "TESTING"
    assert config.is_test_mode() is True

    config.RUN_MODE = "DEBUG"
    assert config.is_test_mode() is False

    config.RUN_MODE = "TESTING"


def test_is_debug_mode():
    config = Config()

    config.RUN_MODE = "DEBUG"
    assert config.is_debug_mode() is True

    config.RUN_MODE = "TESTING"
    assert config.is_debug_mode() is False


def test_waiting_factor():
    config = Config()

    config.RUN_MODE = "DEBUG"
    assert config.waiting_factor() == 2

    config.RUN_MODE = "PRODUCTION"
    assert config.waiting_factor() == 2

    config.RUN_MODE = "TESTING"
    assert config.waiting_factor() == 0
