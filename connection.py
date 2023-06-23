import time
from pika import BlockingConnection, ConnectionParameters, PlainCredentials, exceptions
import config


class RabbitMQConnection:
    _instance = None

    def __new__(cls, host="localhost", port=5672, username="admin", password="admin"):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host="localhost", port=5672, username="admin", password="admin"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if not self.is_connected():
            retries = 0
            while retries < 10:
                try:
                    credentials = PlainCredentials(self.username, self.password)
                    parameters = ConnectionParameters(
                        host=self.host, port=self.port, credentials=credentials
                    )
                    self.connection = BlockingConnection(parameters)
                    print("Connected to RabbitMQ")
                    return
                except exceptions.AMQPConnectionError as e:
                    print("Failed to connect to RabbitMQ:", str(e))
                    retries += 1
                    wait_time = config.Config().waiting_factor() ** retries
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

            print("Exceeded maximum number of connection retries. Stopping the code.")

    def is_connected(self):
        return self.connection is not None and self.connection.is_open

    def close(self):
        if self.is_connected():
            self.connection.close()
            print("Connection to RabbitMQ closed")

    def get_channel(self):
        if self.is_connected():
            return self.connection.channel()

        return None
