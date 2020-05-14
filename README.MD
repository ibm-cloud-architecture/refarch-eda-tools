# Different tools for EDA project

## Latency measurement

To measure latency we need to get the timestamp of the input record at the first topic and the timestamp at the record from the last topic topic, with the same key and see the difference for each message, and average it.

When producer write code to kafka the record has a timestamp at the creation time. The topic can be configured to use the time of the append log time. If we need to measure the latency we need to have the TS0 or TS1 propagated to the end topic or use a consumer that poll from the first topic and the last topic in the kafka streams chain. Here is an example of such timestamps in the context of kafka streaming:

![](docs/images/streams-ts.png)

* TS1: is a timestamp added to the record payload or the ProducerRecord timestamp attribute.
* TS2: is the append log time stamp, on input topic,  when the topic configuration is done this way, or the ProducerRecord timestamp attribute
* TS3: is the append log time stamp, on last output topic
* TS4: is a time stamp at runtime around the poll method of the consumer code.

And in the case of data replication between data centers with MirrorMaker 2, the timestamps have the same meaning but developer has less control on managing the timestamps. 

![](docs/images/mm2-ts-test.png)

To measure latency between TS2 and TS3 we need to get a consumer that polls from both topic, or TS1 = TS2 and is injected by the producer in the payload. 

Those timestamps are per message, so a performance monitoring tool needs to keep measurment per message. 

## Kafka performance considerations

As a distributed processing and persistent system, Kafka is not an easy beast for assessing throughput and scalability. We will try to summaryze our studies in this section. Some kafka deployments are able to process 30+ millions events per second... so how to do that?

* Latency and throughput are orthogonal dimension: Understand the needs for both, and the type of application traffic: near real time, real time processing, data reliability...
* Data reliability impacts performance: number of replicas and acknowledge level
* The characteristics of the producer settings impact performance: Acknowledge level, transactional, buffer size
* The topic configuration, replication, fetching characteristics...
* Typical cluster side is around 20 brokers in average from 3 to 50 brokers. Ingestion can reach 4GB / s at peak volumes.
* Producer can use partition affinity to avoid having too many TCP connection to brokers
* Producer can be multi threaded
* Consider looking at the disk used to persist, be sure for example that each nodes on which the brokers run have different hardware driver, mounted in separate directory.
* Disk has a direct impact on throughput. Kafka always immediately writes all data to the filesystem and supports the ability to configure the flush policy that controls when data is forced out of the OS cache and onto disk using the flush.
* Monitor CPU utilization of each brokers and each consumer / producer apps

### Producer

For the producer the following parameter impact throughtput and latency:

* Tuning the batch.size as increasing batch size could result in higher throughput. A 512kB gives good result for getting around 1.5GB throughput.
* linger: when records comes from external source, the producer could groups records in the batch, but publishes once the delay goes over the `linger.ms` settings. In low-load scenarios, this improves throughput by sacrificing latency.
* The level of expected acknowledge
* `buffer.memory` The total bytes of memory the producer can use to buffer records waiting to be sent to the server. Set close to the total memory of the producer.

[See producer configuration from Kafka doc](https://kafka.apache.org/documentation/#producerconfigs)

### Consumer

Size of the poll

## Simple test framework

* Use kafka connect to send data and Null Sink to read and commit offset from output topic

## Performance test tool in Java

Considering looking at the producer and consumer heap size. 
Revisit the garbage collection settings. Remember that GC impact latency as the JVM is paused while doing GC. As a core principle, the more memory you give the JVM, the lower the collection frequency. The more you have short lived object the higher the cost of GC reclamation.

* Heap size control: -Xmx for maximum heap size and -Xms for heap mem start size
* -XX:+UseG1GC   : This is the default GC for the JVM for JRE 9+ so set this one if you use JRE 8. G1 GC helps to keep good throughput.
* -XX:MaxGCPauseMillis= ? : 
* -XX:InitiatingHeapOccupancyPercent= 35 : Sets the Java heap occupancy threshold that triggers a marking cycle. The default occupancy is 45 percent of the entire Java heap.
* -XX:G1HeapRegionSize= ?  he size of a G1 region
* -XX:XX:MetaspaceSize= ? -XX:MinMetaspaceFreeRatio= ? and -XX:MaxMetaspaceFreeRatio= ?: hold class metadata. *MetaspaceSize*: Sets the size of the allocated class metadata space that will trigger a garbage collection the first time it is exceeded. *MinMetaspaceFreeRatio* o make Metaspaces grow more agressively, and *XX:MaxMetaspaceFreeRatio* to reduce the chance of Metaspaces shrinking

## Performance test tool in Python


## Source of informanation

* [Monitoring kafka - product documentation](https://kafka.apache.org/documentation/#monitoring)
* [Garbage First Garbage Collector Tuning](https://www.oracle.com/technical-resources/articles/java/g1gc.html)
* [Monitoring Kafka at scale with Splunk](https://www.splunk.com/en_us/blog/it/how-we-monitor-and-run-kafka-at-scale.html)
* [Processing trillions of events per day with Apache Kafka](https://azure.microsoft.com/en-us/blog/processing-trillions-of-events-per-day-with-apache-kafka-on-azure/)