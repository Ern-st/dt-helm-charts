import os
import logging

from time import sleep
from datetime import datetime

from kafka import KafkaProducer, KafkaConsumer

# Constants
MS_TO_SEC_FACTOR=1000
INPUT_AND_DEFAULT = [
    ('KAFKA_BROKER_ENDPOINT', None), 
    ('INPUT_TOPIC', None), 
    ('OUTPUT_TOPIC', None), 
    ('DELAY_MS', 0),
]

log = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s - %(message)s")
    log.setLevel(logging.INFO)
    if 'DEBUG' in os.environ:
        log.setLevel(logging.DEBUG)

def get_input_value(variable_name, default_value):
    value = os.getenv(variable_name)
    if value is None:
        value = default_value
    if value is None:
        raise RuntimeError(f"Environment variable not set: {variable_name}")
    return value

def get_input():
    return  (get_input_value(input_variable, default) for input_variable, default in INPUT_AND_DEFAULT)

def create_consumer(kafka_broker_endpoint: str, input_topic: str):
    return KafkaConsumer(
            input_topic,
            bootstrap_servers=[kafka_broker_endpoint],
            group_id=f'delay-{input_topic}')

def create_producer(kafka_broker_endpoint: str):
    return  KafkaProducer(bootstrap_servers=[kafka_broker_endpoint])

def get_current_timestamp_ms():
    now_sec: float = datetime.now().timestamp()
    return now_sec * MS_TO_SEC_FACTOR 

def calculate_delay_ms(consumer_record, delay_ms: int):
    """
    Calculate the actual delay in seconds to wait before the record can be replicated to the output topic.
    In the case of the record being produced more than 'delay_ms' ago, this returns 0.

    Args:
        consumer_record (_type_): The record that is to be replicate to an output topic.
        delay_ms (int): The allowed delay before the record is replicated to the output topic. 

    Returns:
        int: The actual delay in miliseconds.
    """
    record_timestamp = consumer_record.timestamp
    timestamp_now = get_current_timestamp_ms()
    time_diff = timestamp_now - record_timestamp
    further_delay_ms = 0 if delay_ms - time_diff < 0 else delay_ms - time_diff 
    return further_delay_ms

def on_broker_acknowledge(record_metadata):
    log.info(f"Sucessfully replicated record: {record_metadata}")

def on_replication_fail(record_metadata):
    log.error(f"Failed to replcate record: {record_metadata}")

def start_replication(consumer, producer, output_topic: str, delay_ms: int):
    for record in consumer:
        time_until_replication = calculate_delay_ms(record, delay_ms)
        log.info(f"Sleeping for {time_until_replication} milliseconds")
        sleep(time_until_replication/MS_TO_SEC_FACTOR )
        producer.send(output_topic, record.value) \
            .add_callback(on_broker_acknowledge) \
            .add_errback(on_replication_fail)

def main():
    setup_logging()
    kafka_broker_endpoint, input_topic, output_topic, delay_ms = get_input()
    log.info(f"Read input: kafka_broker_endpoint:{kafka_broker_endpoint}, input_topic:{input_topic}, output_topic:{output_topic}, delay_ms:{delay_ms}")

    consumer = create_consumer(kafka_broker_endpoint, input_topic)
    log.info(f"Created Kafka consumer connected to endpoint {kafka_broker_endpoint}")

    producer = create_producer(kafka_broker_endpoint)
    log.info(f"Created Kafka producer connected to endpoint {kafka_broker_endpoint}")

    start_replication(consumer, producer, output_topic, delay_ms)

if __name__ == "__main__":
    main()
