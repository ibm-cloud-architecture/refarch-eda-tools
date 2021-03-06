cd $(dirname $0)
pwd

source .env
echo $KAFKA_SOURCE_BROKERS

 TGT_PROP_FILE=./mm2.properties
 TMPL_PROP_FILE=./mm2-tmpl.properties
 echo "############################################################"
 echo "1. modify properties file : $TMPL_PROP_FILE to $TGT_PROP_FILE"
 echo "############################################################"
 
 cat  $TMPL_PROP_FILE | sed  -e "s/KAFKA_TARGET_BROKERS/$KAFKA_LOCAL_BROKERS/g" \
 -e "s/KAFKA_SOURCE_BROKERS/$ES_IC_BROKERS/g" \
 -e  "s/KAFKA_SOURCE_USER/$ES_IC_USER/g" \
 -e  "s/KAFKA_SOURCE_PASSWORD/$ES_IC_PASSWORD/g" \
 -e  "s/SOURCE_LOGIN_MODULE/$ES_IC_LOGIN_MODULE/g" \
 -e  "s/SOURCE_KAFKA_SASL_MECHANISM/$ES_IC_SASL_MECHANISM/g" > $TGT_PROP_FILE
 cat $TGT_PROP_FILE
 export LOG_DIR=/tmp/logs

chmod 755 mm2.properties

echo "############################################################"
echo "2. start a new container with mirror maker 2"
echo "############################################################"
 
 docker run -ti --network es-ic-to-local_default --rm --name mm2 -v $(pwd):/home -v $(pwd)/mirror-maker-2/logs:/opt/kafka/logs strimzi/kafka:latest-kafka-2.6.0 /bin/bash -c "/opt/kafka/bin/connect-mirror-maker.sh /home/mm2.properties"
 