import os, time, sys, json, argparse
from kafka.Confluent.Avro.old.KcAvroProducer import KafkaAvroProducer
from avro_files.utils.avroEDAUtils import *


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Avro Message Producer Example")
    parser.add_argument('-t', dest="topic", required=True, help="Topic name")
    args = parser.parse_args()

    
    # Get the avro schemas for the message's key. The confluent_kafka.AvroProducer
    # requires the key to be Avro encoded too.
    event_key_schema = getDefaultEventKeySchema(os.getcwd().split("/src")[0] + "/avro_files")
    # Get the avro schemas for the message's value
    event_value_schema = getDefaultEventValueSchema(os.getcwd().split("/src")[0] + "/avro_files")

    # Create the event
    event_key = {"key" : 1}
    event_value = {"message" : "This is an avro test message using the old APIs"}

    # Print out the event to be sent
    print("[MAIN] -------- Event to be published: --------")
    print('[MAIN] Key: ' + json.dumps(event_key))
    print('[MAIN] Value:' + json.dumps(event_value))
    print("[MAIN] ----------------------------------------")

    # Create the Kafka Avro Producer
    kafka_avro_producer = KafkaAvroProducer(event_key_schema,event_value_schema)

    # Publish the event
    kafka_avro_producer.publishEvent(event_key, event_value, args.topic)
