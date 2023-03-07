# Kafka topics
Kafka topics are a way to send and receive data. Data is transmitted through topics, which you will now learn to configure. You have the option to either create a new kafka topic on the cluster or listen to an already existing kafka topic. This is all configured through [values.yaml](../chart/values.yaml):
```yaml
kafkaTopics:
  create:
    - name: "example-topic"
      replicas: 3
      partitions: 1
      retention:
        ms: 604800000
        bytes: -1
  access:
    - name: "example-topic"
      applicationName: "kafka-test-produce"
      namespace: "tenant-test"
      produce: false
      consume: true
    ...
```
This example creates a kafka topic called `example-topic` with 3 replicas, 1 partition and a retention rate of 1 week and no byte retention. The example also give access to the created kafka topic for an application called `kafka-test-produce` in the `tenant-test` namespace. It is important that the `kafkaTopics.access.name` is the same name that the topic was created as. This application is allowed to consume from the topic but not produce to it.
When producing to or consuming a topic in your application, you have to prefix the namespace of the topic in the topic name. `example-topic` should in your application be referenced as `tenant-test-example-topic`. If you need to produce to or consume the same topic from multiple applications, you will need to create multiple entries in the `access` list.
