'''
Produce inventory events to kafka inventory topic.

This is an integration test to validate the JDBC Sink to DB2
'''
import time 
from datetime import datetime
import json, os, sys
import random

from kafka.KafkaProducer import KafkaProducer
import kafka.eventStreamsConfig as config

GROUPID="ProducerInventory"
NBRECORDS=1
TOPICNAME="inventory"
STORES = [ "Store_1","Store_2","Store_3","Store_4", "Store_5" ]
KEYNAME = "storeName"

def parseArguments():
    topic = TOPICNAME
    size = NBRECORDS

    if len(sys.argv) == 1:
        print("Usage: ProduceInventoryEvents --size integer --topic topicname")
        exit(1)
    else:
        for idx in range(1, len(sys.argv)):
            arg=sys.argv[idx]
            if arg == "--size":
                sizeArg = sys.argv[idx+1]
                if sizeArg not in ['small','medium', 'large']:
                    size = int(sizeArg)
                if sizeArg == "medium":
                    size = 10000
                if sizeArg == "large":
                    size = 100000
            if arg == "--topic":
                topic =sys.argv[idx+1]
            if arg == "--help":
                print("Send n messages to a kafka cluster. Use environment variables KAFKA_BROKERS")
                print(" and KAFKA_APIKEY is the cluster accept sasl connection with token user")
                print(" and KAFKA_CERT to ca.crt path to add for TLS communication when using TLS")
                print(" --size small  | medium| large | a_number")
                print("        small= 1000| medium= 10k| large= 100k")
                print(" --topic topicname")
                exit(0)
    return size, topic

def processRecords(nb_records,topicname):
    print("Produce " + str(nb_records) + " messages to the topic " + topicname)
    try:
        producer = KafkaProducer(kafka_brokers = config.KAFKA_BROKERS, 
                kafka_user = config.KAFKA_USER, 
                kafka_pwd = config.KAFKA_PASSWORD, 
                kafka_cacert = config.KAFKA_CERT_PATH, 
                kafka_sasl_mechanism=config.KAFKA_SASL_MECHANISM,
                topic_name = topicname)
        producer.prepare(groupID= GROUPID)
        for i in range(0,nb_records):
            docToSend = {"schema": 
                            {"type": "struct",
                            "fields": [
                                {"type": "string","optional": False,"field": "storeName"},
                                {"type": "string","optional": False,"field": "sku"},
                                {"type": "decimal","optional": False,"field": "id"},
                                {"type": "decimal","optional": True,"field": "quantity"},
                                {"type": "decimal","optional": True,"field": "price"},
                                {"type": "string","optional": True,"field": "timestamp"}
                            ],
                            "optional": False,"name": "Inventory"},
                        }
            payload = {}
            payload["storeName"] = STORES[random.randint(0,len(STORES)-1)]
            payload["sku"] = "Item_" + str(random.randint(0,9))
            payload["quantity"] = random.randint(0,20)
            payload["price"] = random.randint(20,200)
            payload["id"]=i;
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S")
            payload["timestamp"] = timestampStr
            docToSend["payload"] = payload
            print("sending -> " + str(docToSend))
            producer.publishEvent(docToSend, payload["storeName"])
    except KeyboardInterrupt:
        input('Press enter to continue')
        print("Thank you")

if __name__ == "__main__":
    size, topic = parseArguments()
    processRecords(size,topic)