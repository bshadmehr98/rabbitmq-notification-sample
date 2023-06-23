import click
from consumers.sms_consumer import SMSConsumer
from producers.notif_sender import send_notifications
from consumers.all_consumers import ALLConsumer


@click.group()
def cli():
    pass


@cli.command()
@click.option("--host", "-h", default="localhost", help="RabbitMQ host")
@click.option("--port", "-p", default=5672, help="RabbitMQ port")
@click.option("--username", "-u", default=None, help="RabbitMQ username")
@click.option("--password", "-w", default=None, help="RabbitMQ password")
def sms(host, port, username, password):
    consumer = SMSConsumer("notif.sms", "notif.sms", host, port, username, password)
    consumer.consume()


@cli.command()
@click.option("--host", "-h", default="localhost", help="RabbitMQ host")
@click.option("--port", "-p", default=5672, help="RabbitMQ port")
@click.option("--username", "-u", default=None, help="RabbitMQ username")
@click.option("--password", "-w", default=None, help="RabbitMQ password")
def all(host, port, username, password):
    consumer = ALLConsumer("notif", "notif.*", host, port, username, password)
    consumer.consume()


@cli.command()
def send_message():
    send_notifications()
    print("Message sent successfully!")


if __name__ == "__main__":
    cli()
