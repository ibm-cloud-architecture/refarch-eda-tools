/*
 *
 * Licensed Materials - Property of IBM
 *
 * 5737-H33
 *
 * (C) Copyright IBM Corp. 2019  All Rights Reserved.
 *
 * US Government Users Restricted Rights - Use, duplication or
 * disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
 *
 */

package application.kafka;

import java.net.ConnectException;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.KafkaException;
import org.apache.log4j.Logger;
public class Producer {

    private KafkaProducer<String, String> kafkaProducer;

    private Logger logger = Logger.getLogger(Producer.class);

    public Producer(String bootstrapServerAddress, String topic) throws InstantiationException {
        if (topic == null) {
            throw new InstantiationException("Missing required topic name.");
        } else if (bootstrapServerAddress == null) {
            throw new InstantiationException("Missing required bootstrap server address.");
        }
        try {
            KafkaConfig.getInstance().setBootstrapServerAddress(bootstrapServerAddress);
            KafkaConfig.getInstance().setTopicName(topic);
            kafkaProducer = createProducer();
        } catch (KafkaException e) {
            throw new InstantiationException(e.getMessage());
        }
    }

    public Producer() throws InstantiationException {
        kafkaProducer = createProducer();
    }

    private KafkaProducer<String, String> createProducer() throws InstantiationException {
        Properties properties = KafkaConfig.getInstance().buildProducerProperties(System.getenv("PRODUCER_API_KEY"));
        KafkaProducer<String, String> kafkaProducer = null;
        logger.debug(properties.toString());
        try {
            kafkaProducer = new KafkaProducer<>(properties);
        } catch (KafkaException kafkaError) {
            logger.error("Error while creating producer.", kafkaError);
            throw kafkaError;
        }
        return kafkaProducer;
    }

    public RecordMetadata produce(String message) throws InterruptedException, ConnectException, ExecutionException {
        ProducerRecord<String, String> record = new ProducerRecord<>(KafkaConfig.getInstance().getTopicName(), null, message);
        RecordMetadata recordMetadata = null;

        recordMetadata = kafkaProducer.send(record).get();
        return recordMetadata;
    }

    public void shutdown() {
        kafkaProducer.flush();
        kafkaProducer.close();
    }
}