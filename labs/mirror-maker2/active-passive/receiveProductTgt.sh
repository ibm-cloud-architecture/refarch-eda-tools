#!/bin/bash
source .env

docker run -ti -v $(pwd)/..:/home --rm -e KAFKA_BROKERS=$ES_TGT_BROKERS \
    -e KAFKA_PWD=$ES_TGT_PASSWORD \
    -e KAFKA_USER=$ES_TGT_USER \
    -e KAFKA_CERT=/home/active-passive/es-tgt-cert.pem \
    -e KAFKA_TOPIC=es-src.products \
    -e KAFKA_SASL_MECHANISM=$ES_TGT_SASL_MECHANISM \
    ibmcase/kcontainer-python:itgtests python /home/consumer/ProductConsumer.py $1
