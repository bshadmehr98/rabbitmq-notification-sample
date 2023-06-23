import json
from pika import BasicProperties, exceptions as pika_exceptions
from connection import RabbitMQConnection


class RabbitMQProducer:
    def __init__(self, connection):
        self.connection = connection
        self.channel = None

    def publish_message(self, exchange, routing_key, data):
        if self.channel is None:
            self.channel = self.connection.get_channel()

        if self.channel is not None:
            try:
                # self.channel.queue_declare(queue=routing_key, durable=True)
                self.channel.exchange_declare(exchange=exchange, exchange_type="topic")
                message = json.dumps(data)  # Serialize data as JSON
                properties = BasicProperties(
                    content_type="application/json", delivery_mode=2
                )
                self.channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=message,
                    properties=properties,
                )
                print(
                    f"Message sent to exchange '{exchange}' with routing key '{routing_key}'"
                )
            except pika_exceptions.ConnectionClosedByBroker:
                print("Connection closed by broker. Failed to publish message.")
        else:
            print("Failed to obtain a channel for message publishing")


def send_notifications():
    # User ID to notification preferences and data mapping
    user_notifications = {
        "user1": {
            "notifications": {"email": True, "sms": False},
            "email": "user1@example.com",
            "phone": "1234567890",
        },
        "user2": {
            "notifications": {"email": True, "sms": True},
            "email": "user2@example.com",
            "phone": "9876543210",
        },
        "user3": {
            "notifications": {"email": False, "sms": True},
            "email": "user3@example.com",
            "phone": "5555555555",
        },
    }

    with RabbitMQConnection() as connection:
        producer = RabbitMQProducer(connection)
        exchange_name = "notification_exchange"

        for user_id, user_data in user_notifications.items():
            notifications = user_data["notifications"]
            email = user_data["email"]
            phone = user_data["phone"]

            for notification_type, enabled in notifications.items():
                if enabled:
                    routing_key = f"notif.{notification_type}"

                    # Create data as a dictionary
                    data = {
                        "user_id": user_id,
                        "notification_type": notification_type,
                        "email": email,
                        "phone": phone,
                    }

                    producer.publish_message(exchange_name, routing_key, data)
                    print(
                        f"Notification sent to user '{user_id}' via '{notification_type}'"
                    )
