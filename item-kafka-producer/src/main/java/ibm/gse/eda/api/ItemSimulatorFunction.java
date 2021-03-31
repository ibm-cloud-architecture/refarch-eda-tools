package ibm.gse.eda.api;

import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

import javax.inject.Inject;

import ibm.gse.eda.domain.ItemSimulator;
import io.quarkus.funqy.Funq;
import io.reactivex.Flowable;


public class ItemSimulatorFunction {
    Logger logger = Logger.getLogger(ItemSimulatorFunction.class.getName());
    @Inject
    public ItemSimulator simulator;
    
    @Funq
    public String start( Integer numberOfRecords){
        if (numberOfRecords == null) {
            numberOfRecords = 1;
        }
        logger.warning("Sending " + numberOfRecords + " records");
        simulator.sendItems(numberOfRecords);
        return "Started";
    }
}