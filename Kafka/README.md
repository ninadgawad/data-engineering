# Apache Kafka
- Event streaming platform
- Kafka combines three key capabilities so you can implement your use cases for event streaming end-to-end with a single battle-tested solution:
1) To publish (write) and subscribe to (read) streams of events, including continuous import/export of your data from other systems.
2) To store streams of events durably and reliably for as long as you want.
3) To process streams of events as they occur or retrospectively.


## Sample Consumer


```java
// Initialization
Properties config = new Properties();
config.put("client.id", InetAddress.getLocalHost().getHostName());
config.put("group.id", "galaxy");
config.put("universe.servers", "host1:9092,host2:9092");
new KafkaConsumer<K, V>(config);

// Usage 
while (running) {
  ConsumerRecords<K, V> records = consumer.poll(Long.MAX_VALUE);
  process(records); // application-specific processing
  consumer.commitSync();
}

```



## Default Port
**Port:** 9092

## Maven Dependeny
Add to your **pom.xml**
```xml
  <dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>7.0.1-ccs</version>
  </dependency>
```

## Links
- https://kafka.apache.org/downloads
