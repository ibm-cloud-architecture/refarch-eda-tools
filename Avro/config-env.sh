# Load this properties before executing the scripts:
# source config-env.sh

#####################
## Main properties ##
#####################
# Set the PYTHONPATH to where this project is located
export PYTHONPATH=
# Set these regardless of where your Event Streams on prem or on IBM Cloud or a local Kafka instance
export KAFKA_BROKERS=
# For IBM Event Streams on IBM Cloud and IBM Event Streams 10.5 or previous versions on OpenShift, the Schema Registry URL must be
# https://KAFKA_USER:KAFKA_PASSWORD@SCHEMA_REGISTRY_URL
# For IBM Event Streams 11.0.1 and onwards, there is a clash between IBM Event Streams APIs and Confluent APIs). As a result, you need to specify the Confluent Compatibility adding /api/ccompat at the end of your SCHEMA_REGISTRY_URL
# https://KAFKA_USER:KAFKA_PASSWORD@SCHEMA_REGISTRY_URL/api/ccompat
# See https://github.com/ibm-cloud-architecture/refarch-eda-tools/issues/15
# Make sure the SCHEMA_REGISTRY_URL your provide is in the form described above.
export SCHEMA_REGISTRY_URL=



######################
## OCP and IBMCLOUD ##
######################
# Set these if you are using Event Streams on prem or on IBM Cloud
export KAFKA_USER=
export KAFKA_PASSWORD=

#########
## OCP ##
#########
# Set the SSL certificate location if you are working against an Event Streams instance on OCP
export KAFKA_CERT=