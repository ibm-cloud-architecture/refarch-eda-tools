package ibm.gse.eda.domain;

import java.time.LocalDateTime;

import javax.json.bind.Jsonb;
import javax.json.bind.JsonbBuilder;

import io.quarkus.runtime.annotations.RegisterForReflection;

@RegisterForReflection
public class Item {
        public static String RESTOCK = "RESTOCK";
        public static String SALE = "SALE";
        public int id;
        public String storeName;
        public String sku;
        public int quantity;
        public String type;
        public Double price;
        public String timestamp;

        public Item() {
        }

        public Item(String store, String sku, String type, int quantity, double price) {
                this.storeName = store;
                this.sku = sku;
                this.type = type;
                this.quantity = quantity;
                this.price = price;
                this.timestamp = LocalDateTime.now().toString();
        }

        public Item(String store, String sku, String type, int quantity) {
                this.storeName = store;
                this.sku = sku;
                this.type = type;
                this.quantity = quantity;
                this.timestamp = LocalDateTime.now().toString();
        }

        public String toString() {
                Jsonb jsonb = JsonbBuilder.create();
                return jsonb.toJson(this);
        }
}