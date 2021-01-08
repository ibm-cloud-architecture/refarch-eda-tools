from confluent_kafka import Producer, KafkaError
import json, os, sys
import numpy as np

'''
This is a basic python code to read products data and send them to kafka.
This is a good scenario for sharing reference data
'''
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS')
KAFKA_CERT = os.getenv('KAFKA_CERT','')
KAFKA_USER =  os.getenv('KAFKA_USER','token')
KAFKA_PWD =  os.getenv('KAFKA_PWD','')
KAFKA_SASL_MECHANISM=  os.getenv('KAFKA_SASL_MECHANISM','SCRAM-SHA-512')
SOURCE_TOPIC='products'

options ={
    'bootstrap.servers': KAFKA_BROKERS,
    'group.id': 'ProductsProducer',
    'delivery.timeout.ms': 15000,
    'request.timeout.ms' : 15000
}

options['security.protocol'] = 'SASL_SSL'
options['sasl.mechanisms'] = KAFKA_SASL_MECHANISM
options['sasl.username'] = KAFKA_USER
options['sasl.password'] = KAFKA_PWD

if (KAFKA_CERT != '' ):
    options['ssl.ca.location'] = KAFKA_CERT
    

print("--- This is the configuration for the producer: ---")
print('[KafkaProducer] - {}'.format(options))
print("---------------------------------------------------")

producer=Producer(options)

def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('[ERROR] - [KafkaProducer] - Message delivery failed: {}'.format(err))
        else:
            print('[KafkaProducer] - Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def publishEvent(topicName, products):
    dataStr = ''
    try:
        for p in products:
            print(p)
            dataStr = json.dumps(p).encode('utf-8')
            producer.produce(topicName,
                key=p["product_id"],
                value=dataStr, 
                callback=delivery_report)
    except Exception as err:
        print('Failed sending message {0}'.format(dataStr))
        print(err)
    producer.flush()
    
def readProducts(filename):
    p = open(filename,'r')
    return json.load(p)

def generateProducts(nb_record):
    products = []
    for i in range(1,nb_records):
        p = { "product_id": "T" + str(i), "description": "Product " + str(i), "target_temperature": np.random.normal(4,2),"target_humidity_level": 0.4,"content_type": 1}
        products.append(p)
    return products

def signal_handler(sig,frame):
    producer.close()
    sys.exit(0)

def parseArguments():
    version="0"
    arg2="./data/products2.json"
    nb_records = 0
    if len(sys.argv) == 1:
        print("Usage: SendProductToKafka  [--file datafilename] [--random n] ")
        exit(1)
    else:
        for idx in range(1, len(sys.argv)):
            arg=sys.argv[idx]
            if arg == "--file":
                arg2=sys.argv[idx+1]
            if arg == "--random":
                nb_records=int(sys.argv[idx+1])
            if arg == "--help":
                print("Send product json documents to a kafka cluster. Use environment variables KAFKA_BROKERS")
                print(" and KAFKA_PWD is the cluster accept sasl connection with token user")
                print(" and KAFKA_CERT foto define the path to the pem file, for TLS communication")
                exit(0)
    return nb_records,arg2

if __name__ == "__main__":
    nb_records,filename = parseArguments()
    if (nb_records > 0):
        products = generateProducts(nb_records)
    else:
        products = readProducts(filename)
    try:
        publishEvent(SOURCE_TOPIC,products)
    except KeyboardInterrupt:
        producer.close()
        sys.exit(0)
    