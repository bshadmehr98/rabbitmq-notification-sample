from unittest.mock import patch, MagicMock, ANY
from consumers.base import RabbitMQConsumerBase
from connection import RabbitMQConnection
import pytest


class SampleRabbitMQConsumer(RabbitMQConsumerBase):
    def process_message(self, channel, method, properties, body):
        pass


@pytest.fixture
def consumer_mock(mocker):
    consumer = SampleRabbitMQConsumer("queue_name", "sample")
    connection_mock = MagicMock()

    connection_context_mock = mocker.patch("connection.RabbitMQConnection.__enter__")
    connection_context_mock.return_value = connection_mock
    return consumer, connection_mock


def test_consume_declares_topic(consumer_mock):
    consumer, connection_mock = consumer_mock
    consumer.consume()

    assert connection_mock.get_channel.return_value.exchange_declare.call_count == 1
    connection_mock.get_channel.return_value.exchange_declare.assert_called_with(exchange="notification_exchange",
                                                                                 exchange_type="topic")


def test_consume_declares_queue(consumer_mock):
    consumer, connection_mock = consumer_mock
    consumer.consume()

    assert connection_mock.get_channel.return_value.queue_declare.call_count == 1
    connection_mock.get_channel.return_value.queue_declare.assert_called_with(queue="queue_name")


def test_consume_binds_queue(consumer_mock):
    consumer, connection_mock = consumer_mock
    consumer.consume()

    assert connection_mock.get_channel.return_value.queue_bind.call_count == 1
    connection_mock.get_channel.return_value.queue_bind.assert_called_with(exchange="notification_exchange",
                                                                           queue="queue_name", routing_key="sample")


def test_consume_uses_basic_consume(consumer_mock):
    consumer, connection_mock = consumer_mock
    consumer.consume()

    assert connection_mock.get_channel.return_value.basic_consume.call_count == 1
    connection_mock.get_channel.return_value.basic_consume.assert_called_with(auto_ack=False,
                                                                              on_message_callback=ANY,
                                                                              queue="queue_name")


def test_consume_uses_starts_consuming(consumer_mock):
    consumer, connection_mock = consumer_mock
    consumer.consume()

    assert connection_mock.get_channel.return_value.start_consuming.call_count == 1


def test_consume_keyboard_interrupt_stops_consuming(consumer_mock):
    consumer, connection_mock = consumer_mock
    connection_mock.get_channel.return_value.start_consuming.side_effect = KeyboardInterrupt
    consumer.consume()

    assert connection_mock.get_channel.return_value.stop_consuming.call_count == 1
