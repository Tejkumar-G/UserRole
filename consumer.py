"""
Consumer
"""
import pika

params = pika.URLParameters('amqps://wgtwhloi:rm5L0lIh_HO912qtPbXwYO1MqAg8km6i@puffin.rmq2.cloudamqp.com/wgtwhloi')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in admin')
    print(body)

channel.basic_consume(queue='admin', on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()