package ibm.gse.eda.producer;

public class DataPayload {
    public long timestamp;
    public String value;
    public String id;
    public DataPayload(){}
    public DataPayload(String id, String v, long ts) {
        this.id = id;
        this.value = v;
        this.timestamp = ts;
    }
}