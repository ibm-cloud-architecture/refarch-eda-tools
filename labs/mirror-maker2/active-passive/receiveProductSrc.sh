#!/bin/bash
source .env

docker run -ti -v $(pwd)/..:/home --rm -e KAFKA_BROKERS=$ES_SRC_BROKERS \
    -e KAFKA_PWD=$ES_SRC_PASSWORD \
    -e KAFKA_USER=$ES_SRC_USER \
    -e KAFKA_CERT=/home/active-passive/es-src-cert.pem \
    -e KAFKA_SASL_MECHANISM=$ES_SRC_SASL_MECHANISM \
    -e KAFKA_TOPIC=products \
    ibmcase/kcontainer-python:itgtests python /home/consumer/ProductConsumer.py $1
