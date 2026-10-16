import pika
import config
import time
import random
import uuid
import datetime
import json

# get the data from sensors and publish that in QUEUE_SENSOR
def main():
    # create connection with RabbitMQ
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(host=config.RABBITMQ_HOST)
    )

    # get the channel
    channel = connection.channel()

    print("[sensor-agent] starting the agent")

    while True:

        # get a random temerature
        temperature = round(random.uniform(10, 30), 1)

        # build the event message
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': config.RK_SENSOR_READING,
            'timestamp': datetime.datetime.now().isoformat(),
            'source': 'sensor-agent',
            'payload': {
                'temperature': temperature
            }
        }

        # publish the event
        channel.basic_publish(
            exchange=config.MAIN_EXCHANGE,
            routing_key=config.RK_SENSOR_READING,
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[sensor-agent] Published a new message with temperature: {temperature}")

        # sleep for 5 seconds
        time.sleep(5)

if __name__ == '__main__':
    main()