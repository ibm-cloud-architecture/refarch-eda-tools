#!/bin/bash
source .env

docker run -ti -v $(pwd)/..:/home --rm -e KAFKA_BROKERS=$ES_IC_BROKERS \
    -e KAFKA_PWD=$ES_IC_PASSWORD \
    -e KAFKA_USER=$ES_IC_USER \
    -e KAFKA_SASL_MECHANISM=$ES_IC_SASL_MECHANISM \
    ibmcase/kcontainer-python:itgtests python /home/producer/SendProductToKafka.py --file /home/data/products.json
