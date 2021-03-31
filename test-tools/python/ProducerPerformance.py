import time 
import json, os, sys

from kafka.KafkaProducer import KafkaProducer
import kafka.EventBackboneConfiguration as ebc

## This script will produce an amount X of messages into the specified kafka topic from the specified data file

GROUP_ID="ProducerPerformanceTest"

def parseArguments():
    
    # Defaults
    version = "0"
    fileName = "./data/testpayload.json"
    topic = "test"
    size = 1000
    keyname = 'identifier'

    # Check there are arguments
    if len(sys.argv) == 1:
        print("Usage: python ProducerPerformance.py  --file <data_file_name> --size <number_of_messages_to_send> --topic <topic_name> --keyname <attribute_name_used_as_key>")
        exit(1)
    else:
        for idx in range(1, len(sys.argv)):
            arg=sys.argv[idx]
            if arg == "--size":
                size = int(sys.argv[idx+1])
            if arg == "--file":
                fileName = sys.argv[idx+1]
            if arg == "--topic":
                topic = sys.argv[idx+1]
            if arg == "--keyname":
                keyname = sys.argv[idx+1]
            if arg == "--help":
                print(" Send n messages to a kafka cluster. Use environment variables KAFKA_BROKERS")
                print(" and KAFKA_APIKEY is the cluster accept sasl connection with token user")
                print(" and KAFKA_CERT to ca.crt path to add for TLS communication when using TLS")
                print(" --file <filename including records to send in json format>")
                print(" --size <number of messages to send>")
                print(" --topic <topic name>")
                print(" --keyname <the attribute name in the json file to be used as record key>")
                exit(0)
    return fileName, size, topic, keyname

def readMessages(filename):
    p = open(filename,'r')
    return json.load(p)

def processRecords(nb_records, topicname, keyname,docsToSend):
    print("Producer to the topic " + topicname)
    try:
        producer = KafkaProducer(
                kafka_brokers = ebc.getBrokerEndPoints(), 
                kafka_apikey = ebc.getEndPointAPIKey(), 
                kafka_cacert = ebc.getKafkaCertificate(),
                topic_name = topicname)

        producer.prepare(groupID= GROUP_ID)

        a = nb_records / len(docsToSend)
        b =  nb_records % len(docsToSend)
        for i in range(0,int(a)):
            for doc in docsToSend:
                doc['timestamp'] = time.time()
                print("sending -> " + str(doc))
                producer.publishEvent(doc,keyname)
        for i in range(0,int(b)):
            docsToSend[i]['timestamp'] = time.time()
            print("sending -> " + str(docsToSend[i]))
            producer.publishEvent(docsToSend[i],keyname)
    except KeyboardInterrupt:
        input('Press enter to continue')
        print("Thank you")

if __name__ == "__main__":
    fileName, size, topic, keyname = parseArguments()
    messages = readMessages(fileName)
    print("Sending " + str(size) + " messages to topic: " + topic)
    processRecords(size,topic,keyname, messages)