import argparse
from kafka.Confluent.Plain.KcConsumer import KafkaConsumer

####################### MAIN #######################
if __name__ == '__main__':
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Avro Message Consumer Example")
    parser.add_argument('-t', dest="topic", required=True, help="Topic name")
    args = parser.parse_args()

    # Create a Kafka Consumer
    kafka_consumer = KafkaConsumer(args.topic)
    # Poll for next message
    kafka_consumer.pollNextEvent()
    # Close the consumer
    kafka_consumer.close()