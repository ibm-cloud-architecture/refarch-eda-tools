import os, time, sys, json, argparse
from kafka.Confluent.Avro.new.KcAvroProducer import KafkaAvroProducer
from avro_files.utils.avroEDAUtils import *


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Avro Message Producer Example")
    parser.add_argument('-t', dest="topic", required=True, help="Topic name")
    args = parser.parse_args()

    # Get the avro schemas for the message's value. We are not sending the key Avro serialized but it can be if needed.
    event_value_schema = getDefaultEventValueSchema(os.getcwd().split("/src")[0] + "/avro_files")

    # Create the event
    event_key = "A key"
    event_value = {"message" : "This is an avro test message using the new APIs"}

    # Print out the event to be sent
    print("[MAIN] -------- Event to be published: --------")
    print('[MAIN] Key: ' + event_key)
    print('[MAIN] Value:' + json.dumps(event_value))
    print("[MAIN] ----------------------------------------")

    # Create the Kafka Avro Producer
    kafka_avro_producer = KafkaAvroProducer(json.dumps(event_value_schema.to_json()))

    # Publish the event
    kafka_avro_producer.publishEvent(event_key, event_value, args.topic)
