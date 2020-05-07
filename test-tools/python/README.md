# Python Performance Test

![implementation](implementation.png)

This repository contains all the performance test assets used for a client data pipeline project where data would be sent to input topics and then consumed by a streams operator that, after some processing, would produce an output message. We wanted to test the performance of this data pipeline by calculating the delta time between when the input data is available at the input topics and when the actual output is produced.

Data sent in **can not** be expected to contain any type of timestamp in it for our performance consumer to calculate the delta time. As a result, the streams operator would include a _timestamp_start_ attribute equal to the messages' timestamp attribute value. Messages' timestamp metadata attribute is managed by kafka and it can be either **CreationTime** or **LogAppend**: <https://kafka.apache.org/documentation/#log.message.timestamp.type>

For this type of testing, where you are trying to see how long it takes some flow to complete, we highly recommend to set your topics _message.timestamp.type_ configuration attribute to **LogAppend** so that messages' timestamp attribute is equal to the time when the message was appended to the kafka's log rather than it being when the message was created which, for black box testing, it is never known what time this would be.

Once we have the topics properly configured and our streams operator adding the message's metadata timestamp as the event's *timestamp_start* attribute, we can use our performance consumer to calculate the average delta time for messages to get from the begin to the end of our data pipeline.

## Local Execution

In order to execute the python scripts locally against any kafka deployment:

```bash
docker run  -e KAFKA_BROKERS=<> \
            -e KAFKA_APIKEY=<> \
            -e KAFKA_CERT=<> \
            -v ${PWD}:/tmp \
            --rm \
            -ti ibmcase/kcontainer-python:itgtests bash
```

Then execute either of the `PerfConsumer.py`, `ProducerPerformance.py` or `test.py`. Check them out first for instructions as to how to execute them and how these work.

## Remote Execution

### Producer

A producer is just a Kubernetes job ([PerformanceProducer.yaml](PerformanceProducer.yaml)) that will be given

1. A data set to iterate over:

    ```yaml
      volumeMounts:
      # Location where the file with the data to be sent as message(s) is
      - mountPath: "/tmp/performance_data"
        name: data-file
    volumes:
        # You MUST create this configMap with the data you want to send in advance. The file containing the data MUST be called data.json
        # Create the configMap: oc create configmap data-file --from-file <LOCATION_OF_YOUR_DATA_FILE> -n <namespace>
        - name: data-file
          configMap:
            name: "data-file"
            optional: true
    ```

1. The topic it needs to produce data into as well as the amount of messages:

    ```yaml
    env:
    # Topic name where the producer will send messages to
    - name: TOPIC_NAME
      value: "performance-test"
    # Number of messages to be sent
    - name: SIZE
      value: "10"
    ```

1. Any configuration parameters to connect to IBM Event Streams such as the _bootstrap server_, the _api key_, the _pem certificate_, etc:

    ```yaml
    env:
      - name: KAFKA_BROKERS
        valueFrom:
          configMapKeyRef:
            name: "kafka-brokers"
            key: brokers
      # Your Event Streams API Key. You can find it in the Event Streams UI on the connect to this cluster link
      # You MUST create this secret in advance with the Event Streams API key:
      # oc create secret generic eventstreams-apikey --from-literal=binding='<replace with api key>' -n <namespace>
      - name: KAFKA_APIKEY
        valueFrom:
          secretKeyRef:
            name: "eventstreams-apikey"
            key: binding
            optional: true
      # Location of your Event Streams pem certificate for ssl connections. You MUST download it in advance.
      # This can be downloaded from the Event Streams UI.
      - name: PEM_CERT
        value: "/tmp/certs/es-cert.pem"
      volumeMounts:
      - mountPath: "/tmp/certs"
        name: eventstreams-pem-file
    volumes:
        # You MUST create this secret with the Event Streams pem certificate in advance. First, download the Event Streams pem certificate.
        # Then create the secret: oc create secret generic eventstreams-pem-file --from-file=es-cert.pem=<LOCATION_OF_YOUR_EVENT_STREAMS_PEM_CERTIFICATE> -n <namespace>
        - name: eventstreams-pem-file
          secret:
            secretName: "eventstreams-pem-file"
            optional: true
    ```

1. Configured in a way that multiple producers can run in parallel in order to reach the message input throughput required:

    ```yaml
    spec:
      # Controls how many times this job must be run
      completions: 1
      # Controls how many jobs can run in parallel (the higher the more input throughput)
      parallelism: 1
    ```

The most important thing, as you can see, is that all the configuration and data the producer may need mentioned above is **provided through Kubernetes configuration**, either by configmaps, secrets or environment variables.

### Consumer

Likewise the producer, the consumer will is defined in its [PerformanceConsumer.yaml](PerformanceConsumer.yaml) file and will be no more than a Kubernetes job that will be given the topic to consume messages from and the IBM Event Streams configuration needed to properly consume messages (that is the _bootstrap server_, the _api key_ and the _pem certificate_)

```yaml
  env:
  # Topic name where the producer will send messages to
  - name: TOPIC_NAME
    value: "performance-test"
  # Event Streams Kafka brokers. You MUST create a configmap in advance with the brokers information:
  # oc create configmap kafka-brokers --from-literal=brokers='<replace with comma-separated list of brokers>' -n <namespace>
  # You can find the list of brokers either in the Event Streams UI or when you login through the CLI: cloudctl es init
  - name: KAFKA_BROKERS
    valueFrom:
      configMapKeyRef:
        name: "kafka-brokers"
        key: brokers
  # Your Event Streams API Key. You can find it in the Event Streams UI on the connect to this cluster link
  # You MUST create this secret in advance with the Event Streams API key:
  # oc create secret generic eventstreams-apikey --from-literal=binding='<replace with api key>' -n <namespace>
  - name: KAFKA_APIKEY
    valueFrom:
      secretKeyRef:
        name: "eventstreams-apikey"
        key: binding
        optional: true
  # Location of your Event Streams pem certificate for ssl connections. You MUST download it in advance.
  # This can be downloaded from the Event Streams UI.
  - name: PEM_CERT
    value: "/tmp/certs/es-cert.pem"
  # Location where the Event Streams pem certificate contained in the eventstreams-pem-file secret will be loaded to.
  volumeMounts:
  - mountPath: "/tmp/certs"
    name: eventstreams-pem-file
volumes:
    # You MUST create this secret with the Event Streams pem certificate in advance. First, download the Event Streams pem certificate.
    # Then create the secret: oc create secret generic eventstreams-pem-file --from-file=es-cert.pem=<LOCATION_OF_YOUR_EVENT_STREAMS_PEM_CERTIFICATE> -n <namespace>
    - name: eventstreams-pem-file
      secret:
        secretName: "eventstreams-pem-file"
        optional: true
restartPolicy: Never
```

The consumer will be constantly trying to consume data and calculating the timestamp delta between when the data was sent into the input topic and when the streams operator produced the result of its computation into the output topic. The consumer will output the average timestamp delta for the last 100, 1k, 10k and 100k message batch processed like this:

```shell
[STAT 100] - Average 62870.0 milliseconds / message
[STAT 100] - Average 13550.8 milliseconds / message
[STAT 100] - Average 60351.8 milliseconds / message
[STAT 100] - Average 60223.4 milliseconds / message
[STAT 100] - Average 53522.0 milliseconds / message
[STAT 100] - Average 53336.4 milliseconds / message
[STAT 100] - Average 49312.8 milliseconds / message
[STAT 100] - Average 46505.2 milliseconds / message
[STAT 100] - Average 45093.4 milliseconds / message
[STAT 100] - Average 39771.8 milliseconds / message
[STAT 1K] - Average 3977.18 milliseconds / message
[TOTAL] - Total Number of messages read: 100000
[STAT 10K] - Average 397.718 milliseconds / message
[STAT 100K] - Average 39.7718 milliseconds / message
```

## Files

- data (folder): contains the default data file the performance testing docker image was built in with.
- kafka (folder): contains the python scripts that allow us to produce and consume from IBM Event Streams.
- Dockerfile: the dockerfile to build the docker image that will contains all the assets to carry out the performance testing.
- Dockerfile_ubi: dockerfile to build the docker image that will contains all the assets to carry out the performance testing from a UBI docker image (not working yet).
- PerfConsumer.py: python script that will consume messages from a topic and compute the timestamp delta for the messages consumed.
- PerformanceProducer.yaml: This is the default producer kubernetes job.
- PerformanceConsumer.yaml: This is the default consumer kubernetes job.
- ProducerPerformance.py: python script that will produce messages to a topic based on the configuration specified in the PerformanceProducer.yaml file.

## CLI

This section contains several CLI commands useful for running the performance testing.

### Initialize

1. `cloudctl` to login to your ICP control plane running on top of OpenShift (ROKS cluster) to manage CP4I Event Streams instance:

    ```bash
    $ cloudctl login -a https://icp-console.roks3.eu-de.containers.appdomain.cloud -u admin -p <password> -n eventstreams --skip-ssl-validation

    Authenticating...
    OK

    Targeted account mycluster Account

    Targeted namespace eventstreams

    Configuring kubectl ...
    Property "clusters.mycluster" unset.
    Property "users.mycluster-user" unset.
    Property "contexts.mycluster-context" unset.
    Cluster "mycluster" set.
    User "mycluster-user" set.
    Context "mycluster-context" created.
    Switched to context "mycluster-context".
    OK

    Configuring helm: /Users/user/.helm
    OK
    ```

1. `oc` to login to your OpenShift cluster. Log in to your OpenShift dashboard UI and in the top right corner click on _Copy login command_ and execute in your terminal:

    ```bash
    $ oc login https://c100-e.eu-de.containers.cloud.ibm.com:32659 --token=<token>

    Logged into "https://c100-e.eu-de.containers.cloud.ibm.com:32659" as "IAM#<your_user>" using the token provided.

    You have access to the following projects and can switch between them with 'oc project <projectname>':

        ace
        apic
        aspera
        assetrepo
        cassandra
        cert-manager
        cp4i
        datapower
        default
        eventstreams
        ibm-cert-store
        ibm-observe
        ibm-system
        icp-system
        istio-system
      * performance
        kube-proxy-and-dns
        kube-public
        kube-service-catalog
        kube-system
        mpoc-logic
        mq
        openshift
        openshift-ansible-service-broker
        openshift-console
        openshift-infra
        openshift-monitoring
        openshift-node
        openshift-template-service-broker
        openshift-web-console
        services
        tracing

    Using project "performance".
    ```

1. Initialize the `es` plugin for the `cloudctl` CLI in order to manager your Event Streams instance through CLI:

    ```bash
    $ cloudctl es init

    ICP endpoint:                      https://icp-console.roks3.eu-de.containers.appdomain.cloud
    Namespace:                         eventstreams
    Helm release:                      es-1
    Event Streams API endpoint:        https://icp-proxy.roks3.eu-de.containers.appdomain.cloud:30569
    Event Streams API status:          OK
    Event Streams UI address:          https://icp-proxy.roks3.eu-de.containers.appdomain.cloud:32015
    Event Streams bootstrap address:   icp-proxy.roks3.eu-de.containers.appdomain.cloud:30948
    ```

### Event Streams Topics

#### Create topics

```bash
$ for i in `echo performance-test-topic-1 performance-test-topic-2`; do cloudctl es topic-create --name $i --partitions 1 --replication-factor 1 --config message.timestamp.type=LogAppendTime; done

Created topic performance-test-topic-1
OK
Created topic performance-test-topic-2
OK
```

#### List topics

```bash
$ cloudctl es topics

Topic name
performance-test-topic-1
performance-test-topic-2
OK
```

#### Delete topics

```bash
$ for i in `echo performance-test-topic-1 performance-test-topic-2`; do cloudctl es topic-delete -f $i; done

Topic performance-test-topic-1 deleted successfully
OK
Topic performance-test-topic-2 deleted successfully
OK
```
