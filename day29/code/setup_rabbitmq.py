import pika
import config

def main():
    # create credentials
    credentials = pika.PlainCredentials(
        username=config.RABBITMQ_USER, 
        password=config.RABBITMQ_PASSWORD
    )

    # create pika connection parameters
    params = pika.ConnectionParameters(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        credentials=credentials
    )

    # create pika connection
    connection = pika.BlockingConnection(params)

    # get the channel
    channel = connection.channel()

    # set exchange channel
    channel.exchange_declare(
        exchange=config.MAIN_EXCHANGE,
        exchange_type='topic',

        # store and forward
        durable=True
    )

    # create the queues
    queues = {
        config.QUEUE_SENSOR: [config.RK_SENSOR_READING],
        config.QUEUE_BRAIN: [config.RK_PATTERN_LOW, config.RK_PATTERN_HIGH],
        config.QUEUE_ACTUATOR: [config.RK_DECISION_PROPOSED]
    }

    # create the queue settings
    for queue_name, routing_keys in queues.items():
        
        # create a new queue
        channel.queue_declare(queue=queue_name, durable=True)
        for rk in routing_keys:

            # set the routing key
            channel.queue_bind(
                exchange=config.MAIN_EXCHANGE,
                queue=queue_name,
                routing_key=rk,
            )
        print(f"  {queue_name} ← {routing_keys}")

    # close the connection
    connection.close()

if __name__ == '__main__':
    main()