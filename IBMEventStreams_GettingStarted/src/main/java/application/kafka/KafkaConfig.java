package application.kafka;

import java.util.Properties;

import org.apache.kafka.clients.CommonClientConfigs;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.common.config.SslConfigs;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

public class KafkaConfig {
    private static final String BOOTSTRAP_SERVER_ENV_KEY = "BOOTSTRAP_SERVER";
    private static final String TOPIC_ENV_KEY = "TOPIC";
    private static final String USERNAME = "token";
    public  String bootstrapServerAddress = System.getenv(BOOTSTRAP_SERVER_ENV_KEY).replace("\"", "");
    public  String TOPIC = System.getenv(TOPIC_ENV_KEY).replace("\"", "");

    private static KafkaConfig instance = new KafkaConfig();

    public static KafkaConfig getInstance() {
        return instance;
    }
    
    public Properties buildCommonProperties() throws InstantiationException { 
        if (TOPIC == null) {
            throw new InstantiationException("Missing required topic name.");
        } else if (bootstrapServerAddress == null) {
            throw new InstantiationException("Missing required bootstrap server address.");
        }
        Properties properties = new Properties();
        properties.put(CommonClientConfigs.BOOTSTRAP_SERVERS_CONFIG, bootstrapServerAddress);
        properties.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        properties.put(CommonClientConfigs.CONNECTIONS_MAX_IDLE_MS_CONFIG, 10000);
        properties.put(SslConfigs.SSL_PROTOCOL_CONFIG, "TLSv1.2");
        if (Boolean.parseBoolean(System.getenv("USE_TLS"))) {
            properties.put(SslConfigs.SSL_TRUSTSTORE_LOCATION_CONFIG, System.getenv("SSL_TRUSTSTORE_LOCATION_CONFIG"));
            properties.put(SslConfigs.SSL_TRUSTSTORE_PASSWORD_CONFIG, System.getenv("SSL_TRUSTSTORE_PASSWORD_CONFIG"));
        }
        properties.put(SaslConfigs.SASL_MECHANISM, "PLAIN");
        return properties;
    }

    public  Properties buildProducerProperties(String apikey) throws InstantiationException {
        Properties properties = KafkaConfig.getInstance().buildCommonProperties();
        properties.put(ProducerConfig.MAX_BLOCK_MS_CONFIG, 7000);
        properties.put(ProducerConfig.RETRIES_CONFIG, 0);
        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        properties.put(SaslConfigs.SASL_MECHANISM, "PLAIN");
        String saslJaasConfig = "org.apache.kafka.common.security.plain.PlainLoginModule required username=\""
                + USERNAME + "\" password=" + apikey + ";";
        properties.put(SaslConfigs.SASL_JAAS_CONFIG, saslJaasConfig);
        return  properties;
    }

    public Properties buildConsumerProperties(String apikey, String consumerGroupId)
            throws InstantiationException {
        Properties properties = KafkaConfig.getInstance().buildCommonProperties();
        String saslJaasConfig = "org.apache.kafka.common.security.plain.PlainLoginModule required username=\""
                + USERNAME + "\" password=" + apikey + ";";
        properties.put(SaslConfigs.SASL_JAAS_CONFIG, saslJaasConfig);
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        properties.put(ConsumerConfig.GROUP_ID_CONFIG, consumerGroupId);
        properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        return  properties;
    }

    public  String getBootstrapServerAddress() {
        return bootstrapServerAddress;
    }

    public  void setBootstrapServerAddress(String bootstrapServers) {
        bootstrapServerAddress = bootstrapServers;
    }

    public  String getTopicName() {
        return TOPIC;
    }

    public  void setTopicName(String topic) {
        TOPIC = topic;
    }
}