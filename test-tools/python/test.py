from kafka.KafkaConsumer import KafkaConsumer
import kafka.EventBackboneConfiguration as ebc
from confluent_kafka import KafkaException
import json, time , sys, os


## This script tests the delta time between a message's Timestamp metadata attribute and an expected timestamp_start event attribute:
#
#   Partition:   0
#   Offset:      0
#   Timestamp:   2020-05-05 09:33:22.784 -0700 PDT
#   {
#       "key": "key",
#       "attribute1": "value1",
#       "attribute2": "value2", 
#       "timestamp_start": 1587394651.4634368
#   }
# 
# The Timestamp attribute's value is controlled and managed by Kafka based on the topic's message.timestamp.type configuration value.
# message.timestamp.type defines whether the timestamp in the message is message create time or log append time:
#       https://kafka.apache.org/documentation/#log.message.timestamp.type

if __name__ == "__main__":
    CONSUMERGROUP = "PerfConsumer-group-1"
    try:
        consumer = KafkaConsumer(
                kafka_brokers = "<kafka_brokers>", 
                kafka_apikey = "<kafka_apikey>", 
                kafka_cacert = "<pem_certificate>",
                autocommit = False,
                fromWhere = 'earliest',
                topic_name = "<topic>")
        consumer.prepare(CONSUMERGROUP)
        gotIt = False
        while not gotIt:
            try :
                # Poll message
                msg = consumer.consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    # Get message value (that is, the "event")
                    event = msg.value()
                    try:
                        # Parse the event into a JSON object
                        event_json = json.loads(event)
                        
                        # Print timestamps to compare
                        print("**********************************************************")
                        print("Kafka timestamp:       " + str(msg.timestamp()[1]))              # This is the message's Timestamp attribute. That is, it is the metadata that goes along with the event and that kafka manages.
                        print("JSON timestamp:        " + str(event_json['timestamp_start']))   # This is the timestam_start attribute that should go within the event for comparison. Modify this as necessary for your tests.
                        
                        ## Calculate the difference
                        difference = msg.timestamp()[1] - event_json['timestamp_start']

                        # Print the difference in milliseconds and minutes 
                        print("                        ---------------------------------")
                        print("Result:                " + str( difference ) + " milliseconds")
                        print("Result:                " + str( difference / 60000 ) + " minutes")
                    except Exception as e:
                        continue
            except KeyboardInterrupt as identifier:
                print(identifier)
                input('Press enter to continue')
                print("Thank you")
    except Exception as identifier:
        print(identifier)
        input('Press enter to continue')
        print("Thank you")