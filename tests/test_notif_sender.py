from pika.exceptions import ConnectionClosedByBroker
from producers.notif_sender import RabbitMQProducer
from unittest.mock import MagicMock


def test_publish_message(mocker, capsys):
    # Create a mock RabbitMQProducer instance
    connection = mocker.Mock()
    producer = RabbitMQProducer(connection)

    # Create a MagicMock object for the channel
    channel = MagicMock()
    channel.exchange_declare.return_value = None
    channel.basic_publish.return_value = None

    # Configure the connection's get_channel method to return the MagicMock channel
    connection.get_channel.return_value = channel

    # Define test data
    exchange = "test_exchange"
    routing_key = "test_routing_key"
    data = {"key": "value"}

    # Call the publish_message method
    producer.publish_message(exchange, routing_key, data)

    # Assert that the channel's basic_publish method was called once
    channel.basic_publish.assert_called_once()

    # Assert the number of times the publish_message method was called on the channel
    assert channel.basic_publish.call_count == 1

    # Assert any other expectations you have for the test case

    # Assert that the printed output is empty
    captured = capsys.readouterr()
    assert captured.out.startswith("Message sent to exchange '")


def test_publish_message_connection_closed(mocker, capsys):
    connection = mocker.Mock()
    producer = RabbitMQProducer(connection)

    # Create a MagicMock object for the channel
    channel = MagicMock()
    channel.exchange_declare.return_value = None
    channel.basic_publish.return_value = None

    def side_effect(exchange, routing_key, body, properties):
        raise ConnectionClosedByBroker(0, "sample")

    channel.basic_publish.side_effect = side_effect

    # Mock the channel returned by the connection
    connection.get_channel.return_value = channel

    # Define test data
    exchange = "test_exchange"
    routing_key = "test_routing_key"
    data = {"key": "value"}

    # Call the publish_message method
    producer.publish_message(exchange, routing_key, data)

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that the expected error message was printed
    assert "Connection closed by broker. Failed to publish message." in captured.out
