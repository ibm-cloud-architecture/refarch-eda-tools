package ibm.gse.eda.domain;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.eclipse.microprofile.reactive.messaging.Message;
import org.eclipse.microprofile.reactive.messaging.Metadata;

import io.smallrye.mutiny.Multi;
import io.smallrye.reactive.messaging.kafka.KafkaRecord;
import io.smallrye.reactive.messaging.kafka.OutgoingKafkaRecordMetadata;

/**
 * Simulate item sale activities between multiple store
 */
@ApplicationScoped
public class ItemSimulator {
    Logger logger = Logger.getLogger(ItemSimulator.class.getName());

    String[] stores = { "Store_1", "Store_2", "Store_3", "Store_4" };
    String[] skus = { "Item_1", "Item_2", "Item_3", "Item_4", "Item_5" };
    Random random = new Random();
    int maxQuantity = 10;
    int maxPrice = 100;

    @Inject
    @Channel("items")
    Emitter<KafkaRecord<String,Item>> emitter;

    public ItemSimulator() {
    }

    public List<Item> buildItems(int nbItem) {
        logger.warning("buildItems " + nbItem);
        List<Item> items = new ArrayList<Item>();
        for (int i = 0; i < nbItem; i++) {
            items.add(buildRandonItem(i));
        }
        return items;
    }

    public void sendItems(Integer numberOfRecords) {
        Multi.createFrom().items(buildItems(numberOfRecords).stream()).subscribe().with(item -> {
            logger.warning("send " + item.toString());
            OutgoingKafkaRecordMetadata<String> metadata = OutgoingKafkaRecordMetadata.<String>builder()
                    .withKey(item.storeName)
                    .withTimestamp(Instant.now())
                    .build();
            KafkaRecord<String,Item> record = KafkaRecord.from(Message.of(item, Metadata.of(metadata)));
            emitter.send(record );
        }, failure -> System.out.println("Failed with " + failure.getMessage()));
    }

    private Item buildRandonItem(int id) {
        Item item = new Item();
        item.id = id;
        item.storeName = stores[random.nextInt(stores.length)];
        item.quantity = random.nextInt(maxQuantity);
        item.sku = skus[random.nextInt(skus.length)];
        item.type = random.nextDouble() > 0.5 ? Item.RESTOCK : Item.SALE;
        BigDecimal bd = BigDecimal.valueOf(random.nextDouble() * maxPrice);
        bd = bd.setScale(2, RoundingMode.HALF_UP);
        item.price = bd.doubleValue();
        return item;
    }
}
