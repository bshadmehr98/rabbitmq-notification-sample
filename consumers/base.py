from abc import ABC, abstractmethod
from connection import RabbitMQConnection


class RabbitMQConsumerBase(ABC):
    def __init__(
        self,
        queue_name,
        binding_key,
        host="localhost",
        port=5672,
        username=None,
        password=None,
    ):
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.binding_key = binding_key

    @abstractmethod
    def process_message(self, channel, method, properties, body):
        pass

    def on_message_callback(self, channel, method, properties, body):
        self.process_message(channel, method, properties, body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        with RabbitMQConnection(
            self.host, self.port, self.username, self.password
        ) as connection:
            channel = connection.get_channel()
            channel.exchange_declare(
                exchange="notification_exchange", exchange_type="topic"
            )
            channel.queue_declare(queue=self.queue_name)
            channel.queue_bind(
                queue=self.queue_name,
                exchange="notification_exchange",
                routing_key=self.binding_key,
            )
            channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.on_message_callback,
                auto_ack=False,
            )

            print(f"Started consuming messages from queue: {self.queue_name}")
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()

            print("Consumer stopped.")
