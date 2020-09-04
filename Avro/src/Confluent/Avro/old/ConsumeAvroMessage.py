import os,sys,argparse
from kafka.Confluent.Avro.old.KcAvroConsumer import KafkaAvroConsumer

if __name__ == '__main__':
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Avro Message Consumer Example")
    parser.add_argument('-t', dest="topic", required=True, help="Topic name")
    args = parser.parse_args()

    # Create the Kafka Avro consumer
    kafka_avro_consumer = KafkaAvroConsumer(args.topic, autocommit = False)
    # Consume next Avro event
    event = kafka_avro_consumer.pollNextEvent()
    # Close the Avro consumer
    kafka_avro_consumer.close()