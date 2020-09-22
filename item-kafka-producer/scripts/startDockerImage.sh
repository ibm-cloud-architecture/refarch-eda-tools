 source .env
 docker run -p 8080:8080 \
   -e KAFKA_BROKERS=$KAFKA_BROKERS \
   -e KAFKA_USER=$KAFKA_USER \
   -e KAFKA_PASSWORD=$KAFKA_PASSWORD \
   -e SECURE_PROTOCOL=$SECURE_PROTOCOL \
   -e KAFKA_CERT_PATH=/certs/ca.p12 \
   -e KAFKA_CERT_PWD=$KAFKA_CERT_PWD \
   -v $(pwd)/certs:/certs \
   ibmcase/item-kafka-producer:0.0.2