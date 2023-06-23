from unittest.mock import patch
import pytest
from click.testing import CliRunner
from cli import sms, all, send_message
import cli
from consumers.sms_consumer import SMSConsumer
from consumers.all_consumers import ALLConsumer

# Define test data
host = "localhost"
port = 5672
username = "user"
password = "pass"


@pytest.mark.parametrize("cli_command, consumer_class, queue_name, exchange_name, routing_key", [
    (sms, SMSConsumer, "notif.sms", "notification_exchange", "notif.sms"),
    (all, ALLConsumer, "notif", "notification_exchange", "notif.*"),
])
def test_consumer_commands(cli_command, consumer_class, queue_name, exchange_name, routing_key):
    # Patch the consumer class
    with patch("cli.{}".format(consumer_class.__name__), autospec=True) as MockConsumer:
        # Create a CLI runner
        runner = CliRunner()
        # Execute the CLI command
        result = runner.invoke(cli_command,
                               ["--host", host, "--port", str(port), "--username", username, "--password", password])
        # Check if the command executed successfully
        assert result.exit_code == 0
        # # Check if the consumer class was instantiated with the correct arguments
        MockConsumer.assert_called_once_with(queue_name, routing_key, host, port, username, password)
        # # Check if the consume method was called on the consumer object
        consumer_instance = MockConsumer.return_value
        consumer_instance.consume.assert_called_once()


# Define test case for send_message command
def test_send_message_command():
    # Patch the send_notifications function
    with patch("cli.send_notifications") as mock_send_notifications:
        # Create a CLI runner
        runner = CliRunner()
        # Execute the CLI command
        result = runner.invoke(send_message)
        # Check if the command executed successfully
        assert result.exit_code == 0
        # Check if the send_notifications function was called
        mock_send_notifications.assert_called_once()
        # Check if the expected message is printed
        assert "Message sent successfully!" in result.output


# Define test case for main CLI entry point
def test_cli():
    # Patch the main script to avoid executing the CLI commands
    with patch.object(cli, "__name__", "__main__"):
        # Create a CLI runner
        runner = CliRunner()
        # Execute the main script without any command
        result = runner.invoke(cli.cli)
        # Check if the command executed successfully
        assert result.exit_code == 0
        # Check if the expected help output is displayed
        assert "Options:" in result.output
        assert "Commands:" in result.output
