import json,os
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError


class KafkaConsumer:

    def __init__(self, kafka_brokers = "", kafka_apikey = "", topic_name = "", schema_registry_url = "", autocommit = True):
        self.kafka_brokers = kafka_brokers
        self.kafka_apikey = kafka_apikey
        self.topic_name = topic_name
        self.schema_registry_url = schema_registry_url 
        self.kafka_auto_commit = autocommit

    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    def prepareConsumer(self, groupID = "pythonconsumers"):
        options ={
                'bootstrap.servers':  self.kafka_brokers,
                'group.id': groupID,
                'auto.offset.reset': 'earliest',
                'schema.registry.url': self.schema_registry_url,
                'enable.auto.commit': self.kafka_auto_commit,
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': 'token',
                'sasl.password': self.kafka_apikey
        }
        # Print the configuration
        print("--- This is the configuration for the Avro consumer: ---")
        print(options)
        print("---------------------------------------------------")
        # Create the Avro consumer
        self.consumer = AvroConsumer(options)
        # Subscribe to the topic
        self.consumer.subscribe([self.topic_name])
    
    def traceResponse(self, msg):
        print('[Message] - Next message consumed from {} partition: [{}] at offset {} with key {}:\n\tvalue: {}'
                    .format(msg.topic(), msg.partition(), msg.offset(), msg.key(), msg.value() ))

    # Polls for next event
    def pollNextEvent(self):
        # Poll for messages
        msg = self.consumer.poll(timeout=10.0)
        # Validate the returned message
        if msg is None:
            print("[INFO] - No new messages on the topic")
        elif msg.error():
            if ("PARTITION_EOF" in msg.error()):
                print("[INFO] - End of partition")
            else:
                print("[ERROR] - Consumer error: {}".format(msg.error()))
        else:
            # Print the message
            msgStr = self.traceResponse(msg)
    
    def close(self):
        self.consumer.close()