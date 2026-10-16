import json
import logging
import sys
import pika
import config


class BaseAgent:

    def __init__(self, name, queue_name, routing_keys):
        self.name = name
        self.queue_name = queue_name
        self.routing_keys = routing_keys

        self.logger = logging.getLogger(name)
        logging.basicConfig(
            level=logging.INFO,
            format=f"[{name}] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(config.RABBITMQ_HOST)
        )
        self.channel = self.connection.channel()
        self.logger.info("Connected to RabbitMQ")

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        for rk in self.routing_keys:
            self.channel.queue_bind(
                exchange=config.MAIN_EXCHANGE,
                queue=self.queue_name,
                routing_key=rk,
            )
        self.logger.info(f"Queue '{self.queue_name}' bound to {self.routing_keys}")

    def publish(self, routing_key, payload):
        event = {
            'event_type': routing_key,
            'source': self.name,
            'payload': payload,
        }
        self.channel.basic_publish(
            exchange=config.MAIN_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        self.logger.info(f"Published {routing_key}")

    def handle_event(self, event):
        """Subclass overrides this."""
        raise NotImplementedError

    def run(self):
        self.connect()
        self.declare_queue()

        def callback(ch, method, properties, body):
            event = json.loads(body)
            self.logger.info(f"Received: {event['event_type']}")
            self.handle_event(event)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=False,
        )
        self.logger.info(f"Waiting for messages on '{self.queue_name}'...")
        self.channel.start_consuming()