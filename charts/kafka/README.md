# services-kafka
A repo for a Kafka helm chart. The charts sets up a [Strimzi](https://strimzi.io/) Kafka operator in kubernetes and exposes functionality through kubernetes Custom Resource Definitions. 

A quickstart guide to Strimzi can be found [here](https://strimzi.io/docs/operators/latest/quickstart.html).

# Examples 
Example of the Strimzi resources for Kafka can be found [here](https://github.com/strimzi/strimzi-kafka-operator/tree/0.22.1/examples)


# Testing 
For testing the helm chart we use [ Kubernetes In Docker ](https://kind.sigs.k8s.io/). We create a 3 node cluster with the command `kind create cluster -config ci/kind.yaml`.
Then we install and test our chart with ` helm install default chart/ && helm test default`. 


# Monitoring 

Kafka Strimzi does not export metrics by default and needs to have a exporter installed from this chart https://github.com/prometheus-community/helm-charts/blob/main/charts/prometheus-kafka-exporter/
