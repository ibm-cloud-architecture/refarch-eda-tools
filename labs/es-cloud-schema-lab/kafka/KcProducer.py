import json, os
from confluent_kafka import KafkaError, Producer

class KafkaProducer:

    def __init__(self,kafka_brokers = "",kafka_apikey = ""):
        self.kafka_brokers = kafka_brokers
        self.kafka_apikey = kafka_apikey

    def prepareProducer(self,groupID = "pythonproducers"):
        # Configure the Kafka Producer (https://docs.confluent.io/current/clients/confluent-kafka-python/#kafka-client-configuration)
        options ={
                'bootstrap.servers':  self.kafka_brokers,
                'group.id': groupID,
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': 'token',
                'sasl.password': self.kafka_apikey
        }
        # Print out the configuration
        print("--- This is the configuration for the producer: ---")
        print(options)
        print("---------------------------------------------------")
        # Create the producer
        self.producer = Producer(options)

    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result. Triggered by poll() or flush(). """
        if err is not None:
            print('[ERROR] - Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, topicName, eventToSend, keyName):
        # Print the event to send
        dataStr = json.dumps(eventToSend)
        # Produce the message
        self.producer.produce(topicName,key=eventToSend[keyName],value=dataStr.encode('utf-8'), callback=self.delivery_report)
        # Flush
        self.producer.flush()