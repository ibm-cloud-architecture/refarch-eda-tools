from kafka.KafkaConsumer import KafkaConsumer
import kafka.EventBackboneConfiguration as ebc
from confluent_kafka import KafkaException
import json, time , sys, os

## This script calculates the delta time between a message's Timestamp metadata attribute and an expected timestamp_start event attribute:
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

## IMPORTANT: For now it prints out the average delta timestamp for 100, 1k, 10k and 100k messages

def parseArguments():
    # Defaults
    version = "0"
    topic = "test"
    for idx in range(1, len(sys.argv)):
        arg=sys.argv[idx]
        if arg == "--topic":
            topic =sys.argv[idx+1]
        if arg == "--help":
            print("Usage: PerfConsumer --topic topicName")
            print(" read messages from a kafka cluster. Use environment variables KAFKA_BROKERS")
            print(" and KAFKA_APIKEY is the cluster accept sasl connection with token user")
            print(" and KAFKA_CERT to ca.crt path to add for TLS communication")
            print(" --topic topicname")
            exit(0)
    return topic


if __name__ == "__main__":
    TOPICNAME = parseArguments()
    CONSUMERGROUP = "PerfConsumer-group-1"
    print("Consumer from the topic " + TOPICNAME)
    try:
        consumer = KafkaConsumer(
                kafka_brokers = ebc.getBrokerEndPoints(), 
                kafka_apikey = ebc.getEndPointAPIKey(), 
                kafka_cacert = ebc.getKafkaCertificate(),
                autocommit = False,
                fromWhere = 'earliest',
                topic_name = TOPICNAME)
        consumer.prepare(CONSUMERGROUP)

        # Initialize counters to 0
        delta = 0
        delta1k = 0
        delta10k = 0
        delta100k = 0
        totalMessageCount = 0
        totalMessageCountWarning = 0

        ## In case we wanted to save the metrics into a file. This is not recommended as this goes into the container's filestorage.
        # os.mkdir('consumerOutput')
        # f100=open("consumerOutput/f100.log", "a+")
        # f1k=open("consumerOutput/f1k.log", "a+")
        # f10k=open("consumerOutput/f10k.log", "a+")
        # f100k=open("consumerOutput/f100k.log", "a+")
        # f_warning = open("consumerOutput/f_warning.log", "a+")
        # f_output=open("consumerOutput/f_output.log", "a+")

        gotIt = False
        while not gotIt:
            try :
                # Poll messages
                msg = consumer.consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    # Get message's body (that is, the event)
                    event = msg.value()
                    try:
                        # Parse the event into a JSON object
                        event_json = json.loads(event)
                    except Exception as e:
                        continue
                    
                    # Calculate the difference between the message's timestamp and the event timestamp_start attribute's value
                    timestamp_delta = msg.timestamp()[1] - event_json['timestamp_start']
                    # Increase the counter
                    totalMessageCount += 1
                    
                    if (timestamp_delta < 0):
                        print("[WARNING] - Message with offset " +  str(msg.offset()) + " have a negative timestamp delta --> Start timestamp: " + str( event_json['timestamp_start'] ) + " -- Ship-doc timestamp: " +  str(msg.timestamp()[1]) )
                    
                    # Adding new delta
                    delta += timestamp_delta

                    # Reporting
                    # print("Message's output timestamp: " + str(msg.timestamp()[1]) + " - Message's input timestamp: " + str(event_json['timestamp_start']) + " -- Delta: " + str(timestamp_delta) + " milliseconds" + "\n")
                    # f_output.write("Message's output timestamp: " + str(msg.timestamp()[1]) + " - Message's input timestamp: " + str(event_json['timestamp_start']) + " -- Delta: " + str(timestamp_delta) + " milliseconds" + "\n")
                    if totalMessageCount % 100 == 0:
                        print('[STAT 100] - Average ' + str(delta / 100 ) + ' milliseconds / message')
                        # f100.write('[STAT 100] - Average ' + str(delta / 100 ) + ' milliseconds / message' + "\n")
                        delta1k =+ delta
                        delta = 0
                    if totalMessageCount % 1000 == 0:
                        print('[STAT 1K] - Average ' + str(delta1k / 1000 ) + ' milliseconds / message')
                        print("[TOTAL] - Total Number of messages read: " + str(totalMessageCount))
                        # f1k.write('[STAT 1K] - Average ' + str(delta1k / 1000 ) + ' milliseconds / message' + "\n")
                        delta10k =+ delta1k
                        delta1k = 0
                    if totalMessageCount % 10000 == 0:
                        print('[STAT 10K] - Average ' + str(delta10k / 10000 ) + ' milliseconds / message')
                        print("[TOTAL] - Total Number of messages read: " + str(totalMessageCount))
                        # f10k.write('[STAT 10K] - Average ' + str(delta10k / 10000 ) + ' milliseconds / message' + "\n")
                        delta100k =+ delta10k
                        delta10k = 0
                    if totalMessageCount % 100000 == 0:
                        print('[STAT 100K] - Average ' + str(delta100k / 100000 ) + ' milliseconds / message')
                        print("[TOTAL] - Total Number of messages read: " + str(totalMessageCount))
                        # f100k.write('[STAT 100K] - Average ' + str(delta100k / 100000 ) + ' milliseconds / message' + "\n")
                        delta100k = 0
            except KeyboardInterrupt as identifier:
                print(identifier)
                input('Press enter to continue')
                print("Thank you")
    except Exception as identifier:
        print(identifier)
        input('Press enter to continue')
        print("Thank you")