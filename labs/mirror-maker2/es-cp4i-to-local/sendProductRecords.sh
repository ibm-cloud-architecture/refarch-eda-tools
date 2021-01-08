#!/bin/bash
source .env

docker run -ti -v $(pwd)/..:/home --rm -e KAFKA_BROKERS=$ES_OCP_BROKERS \
    -e KAFKA_PWD=$ES_OCP_PASSWORD \
    -e KAFKA_USER=$ES_OCP_USER \
    -e KAFKA_CERT=/home/es-cp4i-to-local/es-cert.pem \
    -e KAFKA_SASL_MECHANISM=$ES_OCP_SASL_MECHANISM \
    ibmcase/kcontainer-python:itgtests python /home/producer/SendProductToKafka.py --file /home/data/products.json
