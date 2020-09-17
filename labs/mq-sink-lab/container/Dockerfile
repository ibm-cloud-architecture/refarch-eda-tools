
FROM ubuntu:20.04

ADD https://mirrors.koehn.com/apache/kafka/2.5.0/kafka_2.12-2.5.0.tgz /tmp/

RUN apt update                                                                                                     && \
    apt install -y curl git maven                                                                                  && \
    tar -C /opt -xvf /tmp/kafka_2.12-2.5.0.tgz                                                                     && \
    rm -f /tmp/kafka_2.12-2.5.0.tgz                                                                                && \
    ln -s /opt/kafka_2.12-2.5.0 /opt/kafka                                                                         && \
    mv -f /opt/kafka/config/connect-distributed.properties /opt/kafka/config/connect-distributed.properties.bak    && \
    cd /opt                                                                                                        && \
    git clone https://github.com/ibm-messaging/kafka-connect-mq-sink.git                                           && \
    cd /opt/kafka-connect-mq-sink                                                                                  && \
    mvn clean package                                                                                              && \
    ln -s /opt/kafka-connect-mq-sink/target/kafka-connect-mq-sink-1.3.0-jar-with-dependencies.jar /opt/kafka/libs/ && \
    mv -f /opt/kafka-connect-mq-sink/config/mq-sink.json /opt/kafka-connect-mq-sink/config/mq-sink.json.bak

COPY connect-distributed.properties /opt/kafka/config/connect-distributed.properties
COPY mq-sink-connector-config.json /opt/kafka-connect-mq-sink/config/mq-sink.json
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
