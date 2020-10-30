
### RabbitMQ operator and instance

See [the installation instructions](https://www.rabbitmq.com/kubernetes/operator/install-operator.html) to get a RabbitMQ **operator** installed 

```
kubectl apply -f rabbitmq/cluster-operator.yml
```

and [this note for one instance](https://www.rabbitmq.com/kubernetes/operator/using-operator.html). 

```shell
# install rabbitmq operator
oc new-project rabbitmq-system
kubectl create -f cluster-operator.yam
kubectl get customresourcedefinitions.apiextensions.k8s.io
# create a cluster instance in a solution project
oc new-project eda-inventory
oc apply -f update-ns.yaml
oc apply -f rmq-definition.yml
```