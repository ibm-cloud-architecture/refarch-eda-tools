import os,sys,argparse
from kafka.Confluent.Avro.new.KcAvroConsumer import KafkaAvroConsumer
from avro_files.utils.avroEDAUtils import *

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description="Avro Message Consumer Example")
    parser.add_argument('-t', dest="topic", required=True, help="Topic name")
    args = parser.parse_args()

    # Get the avro schemas for the message's value. We are not sending the key Avro serialized but it can be if needed.
    # Presenting the schemas to the Avro Deserializer is needed. In the future it might change
    # https://github.com/confluentinc/confluent-kafka-python/issues/834
    event_value_schema = getDefaultEventValueSchema(os.getcwd().split("/src")[0] + "/avro_files")

    # Create the Kafka Avro consumer
    kafka_avro_consumer = KafkaAvroConsumer(json.dumps(event_value_schema.to_json()),args.topic, autocommit = False)
    # Consume next Avro event
    event = kafka_avro_consumer.pollNextEvent()
    # Close the Avro consumer
    kafka_avro_consumer.close()