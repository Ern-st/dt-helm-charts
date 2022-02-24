This application replicates messeges from on Kafka topic to another. It is possible to configure a delay so that the messges are not replicated instantly. 

### Running the application

The entrypoint for the application is the file `app/kafka_topic_replicator` which reads it input through environment variables:

| NAME  | REQUIRED  | DEFAULT  | DESCRIPTION  |
|---|---|---|---|
|KAFKA_BROKER_ENDPOINT   | true  | None  | The endpoint where the Kafka cluster can be reached  |  
|  INPUT_TOPIC | true  |  None | The name of the topic to replicate  |   
|  OUTPUT_TOPIC | true  | None  | The name of the topic where the records will be replicated   |   |
|  DELAY_MS | false |  0 | How long to delay the replication of a record. Counted from the timestamp of the input record  |

### Building the application 
To build the production image of the application use docer to build production image: 
`docker build -t kafka-topic-replicator --target production`

### Testing Building the application

To run the tests of the application use docker to build the test target:
`docker build -t kafka-topic-replicator-test --target test .`

And run the test image:
`docker run kafka-topic-replicator-test` 


