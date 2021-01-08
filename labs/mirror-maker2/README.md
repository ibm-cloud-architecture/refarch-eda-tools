# Mirror maker 2 labs

This folder includes labs to demonstrate topic mirroring between Kafka clusters using Mirror Maker 2.

Updated 01/07/2021

To learn more about Mirror Maker 2, see our summary in [this note](https://ibm-cloud-architecture.github.io/refarch-eda/technology/kafka-mirrormaker/).

## Event Streams on Cloud to local cluster Strimzi

The lab instructions are in [this note](https://ibm-cloud-architecture.github.io/refarch-eda/use-cases/kafka-mm2/lab-1/) with [configuration file](https://github.com/ibm-cloud-architecture/refarch-eda-tools/tree/master/labs/mirror-maker2/es-to-local/).

## Event Streams Cloud Pak for Integration to local cluster Strimzi

The lab instructions are in [Kafka Mirror Maker 2 - Lab 2](/use-cases/kafka-mm2/lab-2/) and the source configuration in [mirror-maker2/](https://github.com/ibm-cloud-architecture/refarch-eda-tools/tree/master/labs/mirror-maker2/es-cp4i-to-local/)


## Active - Passive mirroring

This lab presents how to leverage Mirror Maker 2 between two on-premise Kafka clusters running on OpenShift, one having no consumer and producer connected to it: it is in passive mode. The cluster is still getting replicated data. The lab goes up to the failover and reconnect consumers to the newly promoted active cluster. See the instructions in [Kafka Mirror Maker 2 - Lab 3](/use-cases/kafka-mm2/lab-3/)
