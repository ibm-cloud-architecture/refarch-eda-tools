import argparse
from kafka.Confluent.Plain.KcProducer import KafkaProducer

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Avro Message Producer Example")
    parser.add_argument('-t', dest="topic", required=True, help="Topic name")
    args = parser.parse_args()
    
    # Create the event to be sent
    event = {"eventKey" : "1", "message" : "This is a test message"}
    
    # Print it out
    print("--- Event to be published: ---")
    print(event)
    print("----------------------------------------")
    
    # Create the Kafka Producer
    kafka_producer = KafkaProducer()
    # Publish the event
    kafka_producer.publishEvent(args.topic,event,"eventKey")
