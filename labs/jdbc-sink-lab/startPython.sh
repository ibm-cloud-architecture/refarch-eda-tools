#!/bin/bash
echo "##########################################################"
echo " A docker image for python 3.7 development: "
echo "##########################################################"
echo
name=python37
source ../scripts/setenv.sh
echo "Run python connected to $KAFKA_BROKERS"
if [ "$KAFKA_BROKERS" != "localhost:9092" ]
then   
    docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY --rm --name $name -v $(pwd):/home -it  ibmcase/python37 bash
else
    docker run --network="labnet" -e KAFKA_BROKERS=$KAFKA_BROKERS --rm --name $name -v $(pwd):/home -it  ibmcase/python37 bash
fi 