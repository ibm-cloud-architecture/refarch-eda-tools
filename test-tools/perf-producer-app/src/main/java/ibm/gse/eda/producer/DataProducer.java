package ibm.gse.eda.producer;

import java.util.Date;

import javax.ws.rs.GET;

import com.fasterxml.jackson.databind.ObjectMapper;

import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.eclipse.microprofile.reactive.messaging.OnOverflow;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DataProducer {
    
    private final static Logger LOGGER = LoggerFactory.getLogger("producer");

    @OnOverflow(value = OnOverflow.Strategy.BUFFER, bufferSize = 393922)
    @Channel("dataproducer") Emitter<String> producerEmitter;
    
    @ConfigProperty(name = "kafka.produce.count", defaultValue="10000")
    private int numRecords;
    
    @GET
    public void produce() {
        for( int i=1; i <= numRecords; i++) {
            Date date = new Date();
            DataPayload p = new DataPayload(Integer.toString(i), "Value " + i, date.getTime());
            try {
                ObjectMapper mapper = new ObjectMapper();
                String jsonString = mapper.writeValueAsString(p);
                producerEmitter.send(jsonString);
                LOGGER.info(jsonString + " sent to kafka topic.");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}