import os
from dotenv import load_dotenv


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, load_from_file=True):
        self.RUN_MODE = os.environ.get("RUN_MODE", "DEBUG")

        if load_from_file:
            env_file_path = self.RUN_MODE + ".env"
            load_dotenv(env_file_path)

        self.RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
        self.RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", 5672)
        self.RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "admin")
        self.RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "admin")
        self.RABBITMQ_VHOST = os.environ.get("RABBITMQ_VHOST", "localhost")

    def is_test_mode(self):
        return self.RUN_MODE == "TESTING"

    def is_debug_mode(self):
        return self.RUN_MODE == "DEBUG"

    def waiting_factor(self):
        if self.is_test_mode():
            return 0

        return 2
