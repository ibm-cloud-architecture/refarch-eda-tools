#!/bin/sh

set -x

sed -i "s/KAFKA_BOOTSTRAP_SERVERS/${KAFKA_BOOTSTRAP_SERVERS}/g" /opt/kafka/config/connect-distributed.properties
sed -i "s/KAFKA_API_KEY/${KAFKA_API_KEY}/g"                     /opt/kafka/config/connect-distributed.properties


sed -i "s/KAFKA_TOPICS/${KAFKA_TOPICS}/g"         /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_QUEUE_MANAGER/${MQ_QUEUE_MANAGER}/g" /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_HOST/${MQ_HOST}/g"                   /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_PORT/${MQ_PORT}/g"                   /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_USER/${MQ_USER}/g"                   /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_PASSWORD/${MQ_PASSWORD}/g"           /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_CHANNEL/${MQ_CHANNEL}/g"             /opt/kafka-connect-mq-sink/config/mq-sink.json
sed -i "s/MQ_QUEUE/${MQ_QUEUE}/g"                 /opt/kafka-connect-mq-sink/config/mq-sink.json

/opt/kafka/bin/connect-distributed.sh /opt/kafka/config/connect-distributed.properties &

sleep 60
curl -X DELETE -H "Content-Type: application/json" http://localhost:8083/connectors/mq-sink-connector
curl -X POST -H "Content-Type: application/json" http://localhost:8083/connectors --data "@/opt/kafka-connect-mq-sink/config/mq-sink.json"

tail -f /dev/null
