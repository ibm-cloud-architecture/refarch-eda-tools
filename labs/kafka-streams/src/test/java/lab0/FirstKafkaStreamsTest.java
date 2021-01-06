package lab0;

import java.util.Properties;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.TestInputTopic;
import org.apache.kafka.streams.TestOutputTopic;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.TopologyTestDriver;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import io.quarkus.test.junit.QuarkusTest;

@QuarkusTest
public class FirstKafkaStreamsTest {
    private static TopologyTestDriver testDriver;
    private static String inTopicName = "my-input-topic";
    private static String outTopicName = "my-output-topic";
    private static TestInputTopic<String, String> inTopic;
    private static TestOutputTopic<String, String> outTopic;
    @BeforeEach
    public void buildTopology() {
        final Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "kstream-lab0");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummmy:2345");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        final StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> basicColors = builder.stream(inTopicName,Consumed.with(Serdes.String(), Serdes.String()));
        basicColors.peek((key, value) -> System.out.println("PRE-FILTER: key=" + key + ", value=" + value))
            .filter((key, value) -> ("BLUE".equalsIgnoreCase(value)))
            .peek((key, value) -> System.out.println("POST-FILTER: key=" + key + ", value=" + value))
            .to(outTopicName);
        Topology topology = builder.build();
        testDriver = new TopologyTestDriver(topology, props);
        inTopic = testDriver.createInputTopic(inTopicName, new StringSerializer(), new StringSerializer());
        outTopic = testDriver.createOutputTopic(outTopicName, new StringDeserializer(), new StringDeserializer());
    }
    @AfterEach
    public void teardown() {
        testDriver.close();
    }

    @Test
    public void isEmpty() {
        assertThat(outTopic.isEmpty(), is(true));
    }
    @Test
    public void isNotEmpty() {
        assertThat(outTopic.isEmpty(), is(true));
        inTopic.pipeInput("C01", "blue");
        assertThat(outTopic.getQueueSize(), equalTo(1L) );
        assertThat(outTopic.readValue(), equalTo("blue"));
        assertThat(outTopic.getQueueSize(), equalTo(0L) );
    }
    @Test
    public void selectBlues() {
        assertThat(outTopic.isEmpty(), is(true));
        inTopic.pipeInput("C01", "blue");
        inTopic.pipeInput("C02", "red");
        inTopic.pipeInput("C03", "green");
        inTopic.pipeInput("C04", "Blue");
        assertThat(outTopic.getQueueSize(), equalTo(2L) );
        assertThat(outTopic.isEmpty(), is(false));
        assertThat(outTopic.readValue(), equalTo("blue"));
        assertThat(outTopic.readValue(), equalTo("Blue"));
        assertThat(outTopic.getQueueSize(), equalTo(0L) );
    }
}
