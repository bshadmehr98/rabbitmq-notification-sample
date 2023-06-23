from consumers.base import RabbitMQConsumerBase


class SMSConsumer(RabbitMQConsumerBase):
    def __init__(
        self,
        queue_name,
        binding_key,
        host="localhost",
        port=5672,
        username=None,
        password=None,
    ):
        super().__init__(queue_name, binding_key, host, port, username, password)

    def process_message(self, channel, method, properties, body):
        # Custom logic to process the SMS message
        print("Received SMS message:", body.decode())
