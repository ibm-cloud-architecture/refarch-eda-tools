package application.kafka;

import java.time.Duration;
import java.util.Arrays;
import java.util.Properties;
import java.util.UUID;

import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.KafkaException;
import org.apache.log4j.Logger;

public class Consumer {

    private final String CONSUMER_GROUP_ID = "CONSUMER_GROUP_ID";
    private final String APP_NAME = "GettingStarted";
    private final String DEFAULT = "DEFAULT";
    private final long POLL_DURATION = 1000;

    private String consumerGroupId;
    private KafkaConsumer<String, String> kafkaConsumer;

    private Logger logger = Logger.getLogger(Consumer.class);


    public Consumer(String bootstrapServerAddress, String topic) throws InstantiationException {
        if (topic == null) {
            throw new InstantiationException("Missing required topic name.");
        } else if (bootstrapServerAddress == null) {
            throw new InstantiationException("Missing required bootstrap server address.");
        }
        KafkaConfig.getInstance().setBootstrapServerAddress(bootstrapServerAddress);
        KafkaConfig.getInstance().setTopicName(topic);
        init();
    }

    public Consumer() throws InstantiationException {
        init();
    }

    private void init() throws InstantiationException {
        setOrGenerateConsumerGroupId();
        try {
            kafkaConsumer = createConsumer();
        } catch (KafkaException e) {
            throw new InstantiationException(e.getMessage());
        }
        kafkaConsumer.subscribe(Arrays.asList( KafkaConfig.getInstance().getTopicName()));
     
    }

    private KafkaConsumer<String, String> createConsumer() throws InstantiationException {

        Properties properties = KafkaConfig.getInstance().buildConsumerProperties(
                System.getenv("CONSUMER_API_KEY"),
                consumerGroupId);
        KafkaConsumer<String, String> kafkaConsumer = null;

        try {
            kafkaConsumer = new KafkaConsumer<>(properties);
        } catch (KafkaException kafkaError) {
            logger.error("Error creating kafka consumer.", kafkaError);
            throw kafkaError;
        }
        
        return kafkaConsumer;
    }

    private void setOrGenerateConsumerGroupId() {
        consumerGroupId = System.getenv(CONSUMER_GROUP_ID);
        
        if (consumerGroupId == null) { 
            consumerGroupId = APP_NAME;
        } else if (consumerGroupId.equals(DEFAULT)) {
            consumerGroupId = UUID.randomUUID().toString(); 
        }
    }

    public ConsumerRecords<String, String> consume() {
        ConsumerRecords<String, String> records = kafkaConsumer.poll(Duration.ofMillis(POLL_DURATION));
        return records;
    }
    
    public void shutdown() {
        kafkaConsumer.close();
        logger.info(String.format("Closed consumer: %s", consumerGroupId));
    }
}