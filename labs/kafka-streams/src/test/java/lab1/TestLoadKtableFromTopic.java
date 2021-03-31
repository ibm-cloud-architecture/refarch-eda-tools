package lab1;

import java.util.Properties;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.TestInputTopic;
import org.apache.kafka.streams.TestOutputTopic;
import org.apache.kafka.streams.TopologyTestDriver;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Materialized;
import org.apache.kafka.streams.processor.StateStore;
import org.apache.kafka.streams.state.KeyValueBytesStoreSupplier;
import org.apache.kafka.streams.state.KeyValueIterator;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.state.Stores;
import org.apache.kafka.streams.state.ValueAndTimestamp;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import io.quarkus.test.junit.QuarkusTest;

/**
 * This is a simple example of loading some reference data from stream into a
 * Ktable for lookup. It uses a persistent state store.
 */
@QuarkusTest
public class TestLoadKtableFromTopic {
    private static TopologyTestDriver testDriver;
    private static String companySectorsTopic = "sector-types";
    private static String storeName = "sector-types-store";

    private static TestInputTopic<String, String> inTopic;
    private static TestOutputTopic<String, Long> outTopic;
    private static TestOutputTopic<String, String> errorTopic;

    public static Properties getStreamsConfig() {
        final Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "kstream-lab1");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummmy:1234");
        return props;
    }

    @BeforeAll
    public static void buildTopology(){
        final StreamsBuilder builder = new StreamsBuilder();
        // Adding a state store is a simple matter of creating a StoreSupplier
        // instance with one of the static factory methods on the Stores class.
        // all persistent StateStore instances provide local storage using RocksDB
        KeyValueBytesStoreSupplier storeSupplier = Stores.persistentKeyValueStore(storeName);

        // A KTable is created from the companySectorsTopic, with key and value deserialized.
        // With Materialized.as() causing the Table to force a state store materialization (storeSupplier).
        KTable<String, String> sectorTypeTable = builder.table(companySectorsTopic,
                Consumed.with(Serdes.String(), Serdes.String()),
                Materialized.as(storeSupplier));

        testDriver = new TopologyTestDriver(builder.build(), getStreamsConfig());
        inTopic = testDriver.createInputTopic(companySectorsTopic, new StringSerializer(), new StringSerializer());

    }

    @AfterAll
    public static void close(){
        testDriver.close();
    }

    @Test
    public void shouldHaveSixSectorTypes(){
        inTopic.pipeInput("C01","Health Care");
        inTopic.pipeInput("C02","Finance");
        inTopic.pipeInput("C03","Consumer Services");
        inTopic.pipeInput("C04","Transportation");
        inTopic.pipeInput("C05","Capital Goods");
        inTopic.pipeInput("C06","Public Utilities");

        KeyValueStore<String,ValueAndTimestamp<String>> store = testDriver.getTimestampedKeyValueStore(storeName);
        Assertions.assertNotNull(store);

        ValueAndTimestamp<String> sector = store.get("C02");
        Assertions.assertNotNull(sector);
        Assertions.assertEquals("Finance", sector.value());
        Assertions.assertEquals(6, store.approximateNumEntries());


        // demonstrate how to get all the values from the table:
        KeyValueIterator<String, ValueAndTimestamp<String>> sectors = store.all();
        while (sectors.hasNext()) {
            KeyValue<String,ValueAndTimestamp<String>> s = sectors.next();
            System.out.println(s.key + ":" + s.value.value());
        }
        for ( StateStore s: testDriver.getAllStateStores().values()) {
            System.out.println(s.name());
        }
    }
}  

