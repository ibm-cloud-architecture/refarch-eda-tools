package ut;

import java.time.Duration;
import java.util.concurrent.CompletableFuture;

import org.junit.jupiter.api.Test;

import ibm.gse.eda.domain.ItemSimulator;
import io.smallrye.mutiny.Multi;

public class TestMunity {
   
    @Test
    public void shouldProduce3FirstTicks(){
        Multi.createFrom().publisher(Multi.createFrom().ticks().every(Duration.ofMillis(3)))
        .transform().byTakingFirstItems(3)
        .subscribe().with(
                item -> System.out.println("Received tick " + item),
                failure -> System.out.println("Failed with " + failure.getMessage()));
    }

    @Test
    public void createFromList(){
        ItemSimulator simulator = new ItemSimulator();
        Multi.createFrom().items(simulator.buildItems(4).stream())
         .subscribe().with(
            item -> System.out.println("Received  " + item.toString()),
            failure -> System.out.println("Failed with " + failure.getMessage()));
    }

    @Test
    public void produce23Asynchronously(){
        Multi.createFrom().completionStage(CompletableFuture.supplyAsync(() -> 23))
        .stage(self -> {
            // Transform each item into a string of the item +1
            return self
                    .onItem().transform(i -> i + 1)
                    .onItem().transform(i -> Integer.toString(i));
        })
        .stage(self -> self
                .onItem().invoke(item -> System.out.println("The item is " + item))
                .collectItems().first())
        .stage(self -> self.await().indefinitely());
    }
}
