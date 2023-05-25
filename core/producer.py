"""
Producer.
"""
import pika
from pika import exceptions

# RabbitMQ connection URL
url = 'amqps://wgtwhloi:rm5L0lIh_HO912qtPbXwYO1MqAg8km6i@puffin.rmq2.cloudamqp.com/wgtwhloi@localhost:5672/%2f'

# Attempt to establish a connection
try:
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    print("Connection established successfully!")


    def publish():
        channel.basic_publish(exchange='', routing_key='admin', body='hello')

    connection.close()
except Exception as e:
    print(f"Failed to establish a connection to RabbitMQ {e}.")