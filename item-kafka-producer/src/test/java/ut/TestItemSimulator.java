package ut;

import java.util.List;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import ibm.gse.eda.domain.Item;
import ibm.gse.eda.domain.ItemSimulator;

public class TestItemSimulator {
  
    @Test
    public void testCreateOneItemSale(){
        ItemSimulator itemSimulator = new ItemSimulator();
        List<Item> itemsGenerated = itemSimulator.buildItems(1);
        Assertions.assertNotNull(itemsGenerated);
        Assertions.assertTrue(itemsGenerated.size() == 1);
        Assertions.assertNotNull(itemsGenerated.get(0));
        Assertions.assertTrue(itemsGenerated.get(0).id == 0);
        Assertions.assertNotNull(itemsGenerated.get(0).sku);
        Assertions.assertNotNull(itemsGenerated.get(0).storeName);
        Assertions.assertNotNull(itemsGenerated.get(0).type);
        Assertions.assertTrue(itemsGenerated.get(0).price >= 0);
        traceResults(itemsGenerated);
    }

    @Test
    public void testCreateTenItemSale(){
        ItemSimulator itemSimulator = new ItemSimulator();
        List<Item> itemsGenerated = itemSimulator.buildItems(10);
        Assertions.assertNotNull(itemsGenerated);
        Assertions.assertTrue(itemsGenerated.size() == 10);
        traceResults(itemsGenerated);
    }

    public void traceResults(List<Item> itemsGenerated ){
        for (Item i : itemsGenerated){
            System.out.println(i.toString());
        }
    }
}
