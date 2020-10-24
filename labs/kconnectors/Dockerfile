# Build a custom image for kafka connect, using kafka 2.5 from strimzi image
# but change user to be esuser, so to do not run as root on k8s / Openshift

FROM strimzi/kafka:latest-kafka-2.6.0 as builder
FROM ibmjava:8-jre

RUN addgroup --gid 5000 --system esgroup && \
    adduser --uid 5000 --ingroup esgroup --system esuser

COPY --chown=esuser:esgroup --from=builder /opt/kafka/bin/ /opt/kafka/bin/
COPY --chown=esuser:esgroup --from=builder /opt/kafka/libs/ /opt/kafka/libs/
COPY --chown=esuser:esgroup --from=builder /opt/kafka/config/connect-log4j.properties /opt/kafka/config/
RUN mkdir /opt/kafka/logs && chown esuser:esgroup /opt/kafka/logs && \
    mkdir /opt/connectors && chown esuser:esgroup /opt/connectors
COPY --chown=esuser:esgroup libs/*.jar /opt/kafka/libs/
COPY connect-distributed.properties /opt/kafka/config/connect-distributed.properties
# Uncomment following is you use kafka with TLS certificate or schema registry
# COPY --chown=esuser:esgroup certs/registry-es-cert.jks /opt/kafka/registry-es-cert.jks 
# COPY --chown=esuser:esgroup es-cert.jks /opt/kafka/
COPY --chown=esuser:esgroup libs /opt/connectors/

WORKDIR /opt/kafka
EXPOSE 8083
USER esuser
ENTRYPOINT ["./bin/connect-distributed.sh", "config/connect-distributed.properties"]