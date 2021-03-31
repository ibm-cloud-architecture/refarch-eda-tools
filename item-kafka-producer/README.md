# Item sale / restock Kafka producer project

This project uses Quarkus, Reactive Messaging for Kafka and [Quarkus Funqy(https://quarkus.io/guides/funqy) function to trigger the generation of items messages to kafka.

The code is part of testing item and inventory management and can be used with [this item - aggregator repository](https://github.com/ibm-cloud-architecture/refarch-eda-item-inventory).

## Core principles

The app is not exposed with API defined in Swagger or with JAXRS annotations, but expose one method to be exposed as a service. See the [ ItemSimulatorFunction code](https://github.com/ibm-cloud-architecture/refarch-eda-tools/blob/05fcdcb7d09d674d9eb2cda2e28601171ba51166/item-kafka-producer/src/main/java/ibm/gse/eda/api/ItemSimulatorFunction.java#L18-L25). 

The simulator of sale and restock item in store is using reactive messaging, but as we mix imperative with reactive programming, the code is using Emitter, and then Munity Multi to create and send the Kafka records:

```java
@Inject
@Channel("items")
Emitter<Item> emitter;


public void sendItems(Integer numberOfRecords) {
    Multi.createFrom().items(buildItems(numberOfRecords).stream()).subscribe().with(item -> {
            logger.warning("send " + item.toString());
            Message<Item> record = KafkaRecord.of(item.storeName,item);
            emitter.send(record );
        }, failure -> System.out.println("Failed with " + failure.getMessage()));
   
```

## Running the application in dev mode

You can run your application in dev mode that enables live coding using:

```
./mvnw quarkus:dev
```

But as we connect to a remote Kafka Cluster you need to define environment variables as:

```shell
KAFKA_BROKERS=....containers.appdomain.cloud:443
KAFKA_USER=<a>-scram-user
KAFKA_PASSWORD=<a-password>
KAFKA_CERT_PATH=${PWD}/certs/es-cert.p12
KAFKA_CERT_PWD=<server-ca-certificate-password>
SECURE_PROTOCOL=SASL_SSL
```

## Packaging and running the application

The application can be packaged using `./mvnw package`.
It produces the `item-kafka-producer-1.0.0-SNAPSHOT-runner.jar` file in the `/target` directory.
Be aware that it’s not an _über-jar_ as the dependencies are copied into the `target/lib` directory.

The application is now runnable using `java -jar target/item-kafka-producer-1.0.0-SNAPSHOT-runner.jar`.

## Deployment to OpenShift

The code includes declaration to build the necessary environment variables, secrets, volumes to get connected to a Kafka cluster using TLS authentication, and deploy in one command:

```shell
mvn package -DskipTests -Dquarkus.kubernetes.deploy=true
```

See the application.properties for `quarkus.openshift.env-vars.*` settings.

It is also supposed to be deployed as knative app, but there is an issue on the generation of volume declarations in the knative.yaml file, so we could not make it in one command.

The code is also available as docker image: [ibmcase/item-kafka-producer](https://hub.docker.com/r/ibmcase/item-kafka-producer).

## Creating a native executable

You can create a native executable using: `./mvnw package -Pnative`.

Or, if you don't have GraalVM installed, you can run the native executable build in a container using: `./mvnw package -Pnative -Dquarkus.native.container-build=true`.

You can then execute your native executable with: `./target/item-kafka-producer-1.0.0-SNAPSHOT-runner`

If you want to learn more about building native executables, please consult https://quarkus.io/guides/building-native-image.