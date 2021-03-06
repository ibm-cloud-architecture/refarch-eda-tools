import os,sys
from kafka.KcAvroConsumer import KafkaConsumer

print(" @@@ Executing script: ConsumeAvroMessage.py")

####################### READ ENV VARIABLES #######################
# Try to read the Kafka broker from the environment variables
try:
    KAFKA_BROKERS = os.environ['KAFKA_BROKERS']
except KeyError:
    print("[ERROR] - The KAFKA_BROKERS environment variable needs to be set.")
    exit(1)

# Try to read the Kafka API key from the environment variables
try:
    KAFKA_APIKEY = os.environ['KAFKA_APIKEY']
except KeyError:
    print("[ERROR] - The KAFKA_APIKEY environment variable needs to be set")
    exit(1)

# Try to read the schema registry url from the environment variables
try:
    SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']
except KeyError:
    print("[ERROR] - The SCHEMA_REGISTRY_URL environment variable needs to be set.")
    exit(1)

####################### FUNCTIONS #######################
# Parse arguments to get the container ID to poll for
def parseArguments():
    global TOPIC_NAME
    print("The arguments for this script are: " , str(sys.argv))
    if len(sys.argv) != 2:
        print("[ERROR] - The ConsumeAvroMessage.py script expects one arguments: The Kafka topic to consume messages from.")
        exit(1)
    TOPIC_NAME = sys.argv[1]

####################### MAIN #######################
if __name__ == '__main__':
    # Parse arguments
    parseArguments()
    # Create the Kafka Avro consumer
    kafka_consumer = KafkaConsumer(KAFKA_BROKERS,KAFKA_APIKEY,TOPIC_NAME,SCHEMA_REGISTRY_URL)
    # Prepare the consumer
    kafka_consumer.prepareConsumer()
    # Consume next Avro event
    kafka_consumer.pollNextEvent()
    # Close the Avro consumer
    kafka_consumer.close()