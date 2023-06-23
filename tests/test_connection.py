import pytest
from unittest.mock import patch, MagicMock
from pika import BlockingConnection, ConnectionParameters, exceptions
from connection import RabbitMQConnection


def test_singleton_instance():
    # Test that only one instance of Config is created
    connection1 = RabbitMQConnection()
    connection2 = RabbitMQConnection()
    assert connection1 is connection2


@pytest.fixture
def rabbitmq_connection():
    # Create an instance of RabbitMQConnection with mock parameters
    connection = RabbitMQConnection(host="test_host", port=1234, username="test_user", password="test_pass")
    return connection


def test_connect_successful(rabbitmq_connection):
    # Patch the BlockingConnection class to return a MagicMock
    with patch.object(BlockingConnection, "__init__", return_value=None), \
         patch.object(BlockingConnection, "is_open", return_value=True):
        rabbitmq_connection.connect()

        # Assert that the connection was established
        assert rabbitmq_connection.connection is not None
        assert rabbitmq_connection.connection.is_open


def test_connect_failed(rabbitmq_connection):
    # Patch the BlockingConnection class to raise an exception
    with patch.object(BlockingConnection, "__init__", side_effect=exceptions.AMQPConnectionError("Connection error")):
        rabbitmq_connection.connect()

        # Assert that the connection was not established
        assert rabbitmq_connection.connection is None


def test_is_connected(rabbitmq_connection):
    # Patch the BlockingConnection class to return a MagicMock
    with patch.object(BlockingConnection, "__init__", return_value=None), \
         patch.object(BlockingConnection, "is_open", return_value=True):
        rabbitmq_connection.connect()

        # Assert that the connection is reported as connected
        assert rabbitmq_connection.is_connected()


def test_is_not_connected(rabbitmq_connection):
    # Assert that the connection is reported as not connected
    assert not rabbitmq_connection.is_connected()


def test_close(rabbitmq_connection):
    # Create a MagicMock for the connection object
    connection_mock = MagicMock(spec=BlockingConnection)
    rabbitmq_connection.connection = connection_mock

    rabbitmq_connection.close()

    # Assert that the connection was closed
    connection_mock.close.assert_called_once()


def test_get_channel_connected(rabbitmq_connection):
    # Create a MagicMock for the connection object
    connection_mock = MagicMock(spec=BlockingConnection)
    rabbitmq_connection.connection = connection_mock

    channel_mock = MagicMock()
    connection_mock.channel.return_value = channel_mock

    channel = rabbitmq_connection.get_channel()

    # Assert that the channel was retrieved from the connection
    assert channel is channel_mock


def test_get_channel_not_connected(rabbitmq_connection):
    # Assert that the channel is None when the connection is not open
    channel = rabbitmq_connection.get_channel()
    assert channel is None
