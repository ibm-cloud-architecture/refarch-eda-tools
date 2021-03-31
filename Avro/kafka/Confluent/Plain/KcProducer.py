import json, os
from confluent_kafka import KafkaError, Producer

class KafkaProducer:

    def __init__(self, groupID = "KafkaProducer"):
        # Get the producer configuration
        self.producer_conf = self.getProducerConfiguration(groupID)
        # Create the producer
        self.producer = Producer(self.producer_conf)

    def getProducerConfiguration(self,groupID):
        try:
            options ={
                    'bootstrap.servers': os.environ['KAFKA_BROKERS'],
                    'group.id': groupID
            }
            if (os.getenv('KAFKA_PASSWORD','') != ''):
                # Set security protocol common to ES on prem and on IBM Cloud
                options['security.protocol'] = 'SASL_SSL'
                # Depending on the Kafka User, we will know whether we are talking to ES on prem or on IBM Cloud
                # If we are connecting to ES on IBM Cloud, the SASL mechanism is plain
                if (os.getenv('KAFKA_USER','') == 'token'):
                    options['sasl.mechanisms'] = 'PLAIN'
                # If we are connecting to ES on OCP, the SASL mechanism is scram-sha-512
                else:
                    options['sasl.mechanisms'] = 'SCRAM-SHA-512'
                # Set the SASL username and password
                options['sasl.username'] = os.getenv('KAFKA_USER','')
                options['sasl.password'] = os.getenv('KAFKA_PASSWORD','')
            # If we are talking to ES on prem, it uses an SSL self-signed certificate.
            # Therefore, we need the CA public certificate for the SSL connection to happen.
            if (os.path.isfile(os.getenv('KAFKA_CERT','/certs/es-cert.pem'))):
                options['ssl.ca.location'] = os.getenv('KAFKA_CERT','/certs/es-cert.pem')
            
            # Print out the producer configuration
            self.printProducerConfiguration(options)

            return options

        except KeyError as error:
            print('[KafkaProducer] - [ERROR] - A required environment variable does not exist: ' + error)
            exit(1)

    def printProducerConfiguration(self,options):
        # Printing out producer config for debugging purposes        
        print("[KafkaProducer] - This is the configuration for the producer:")
        print("[KafkaProducer] - -------------------------------------------")
        print('[KafkaProducer] - Bootstrap Server:      {}'.format(options['bootstrap.servers']))
        if (os.getenv('KAFKA_PASSWORD','') != ''):
            # Obfuscate password
            if (len(options['sasl.password']) > 3):
                obfuscated_password = options['sasl.password'][0] + "*****" + options['sasl.password'][len(options['sasl.password'])-1]
            else:
                obfuscated_password = "*******"
            print('[KafkaProducer] - Security Protocol:     {}'.format(options['security.protocol']))
            print('[KafkaProducer] - SASL Mechanism:        {}'.format(options['sasl.mechanisms']))
            print('[KafkaProducer] - SASL Username:         {}'.format(options['sasl.username']))
            print('[KafkaProducer] - SASL Password:         {}'.format(obfuscated_password))
            if (os.path.isfile(os.getenv('KAFKA_CERT','/certs/es-cert.pem'))): 
                print('[KafkaProducer] - SSL CA Location:       {}'.format(options['ssl.ca.location']))
        print("[KafkaProducer] - -------------------------------------------")

    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result. Triggered by poll() or flush(). """
        if err is not None:
            print('[KafkaProducer] - [ERROR] - Message delivery failed: {}'.format(err))
        else:
            print('[KafkaProducer] - Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, topicName, eventToSend, keyName):
        # Print the event to send
        dataStr = json.dumps(eventToSend)
        # Produce the message
        self.producer.produce(topicName,key=eventToSend[keyName],value=dataStr.encode('utf-8'), callback=self.delivery_report)
        # Flush
        self.producer.flush()