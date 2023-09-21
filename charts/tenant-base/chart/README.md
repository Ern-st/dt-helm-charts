# Tenant-base
The tenant base helm chart is a chart that give an easy all in one place to make deployments. It is only designed to make deployments and the resources that could be useful for deployments, like configmaps, pvc's etc.

## Release Notes
This section will describe the changes done in each helm chart release
### 0.12.6
- Defined imagePullSecret as an option for a deployment. Is used to refer to a secret name containing credentials for the container registry in which the container image is stored. Tenants using the sandbox-dev environment should use this in their `environments/sandbox-dev` folder when upgrading to this version.
### 0.12.5
- Allows tenants to specify `allowEgressToFQDN` to allow egress to a FQDN outside the cluster. Wildcards can be used such as `*.microsoftonline.com`.
### 0.12.4
- Removed default value for `ImagePullSecret` in deployments
### 0.12.3
- Adds the `path` parameter to ingress so our tenants now can use paths when creating their ingress routes. This enables you to setup an ingress route to for example `lfc.preprod.ot.energinet.local/dashboard` rather than just `lfc.preprod.ot.energinet.local`.
### 0.12.2
- Sets the PVC storageclassname to "". This enforces pvc's storageclasses to be the default storageclass on the cluster. This change does not affect tenants, however, if they want to use a PVC they must upgrade to this version.
### 0.12.1
- Fixed bug that disallowed traffic through ingress. Ingress routes will not work until you upgrade to this version. No changes to values.yaml.
### 0.12.0
**BREAKING CHANGE:**
- Changed the way kafkaTopics are created. This has no syntactic impact on the `values.yaml` file, but tenants have to upgrade to this version when the dev-cluster is updated to the newest configuration.
### 0.11.0
- Added [ingress functionality](../docs/deployment.md#ingress) so tenants can now create ingress resources

## How to install locally
If you have a local kubernetes cluster, created with for example minikube or KinD, you can install the helm chart the following way:
```
helm repo add tenant-base https://distributed-technologies.github.io/helm-charts/
helm repo update
helm install my-release tenant-base/tenant-base
```

## Uninstalling the chart
To uninstall the helm chart locally, run:
```
helm delete my-release
```
## Documentation
The structure of this section has been made according to the [values.yaml file](./values.yaml), to make it as easy as possible for new developers to understand the helm chart. You should open this file now, so you can follow along in both this document and the values.yaml.

1. [Deployment](../docs/deployment.md)
A deployment is used to describe how we want to deploy one or more containers in a pod.

2. [Configmap](../docs/configmap.md)
Configmaps are a way to store non-sensitive information in kubernetes. This could be dashboards, configurations or environment variables.

3. [Persistent Volume Claims](../docs/pvc.md)
Persistent volume claims are a way to create persistent storage on the cluster, that will not be deleted if a pod dies. They can be used to store files that need to be kept through any pod restarts.

4. [KafkaTopics](../docs/kafkatopic.md)
Kafka topics are a way to describe which topics you want to create and which topics you want access to on the cluster.

## Configuration

| Parameter                                 | Description                                   | Default                                                 |
|-------------------------------------------|-----------------------------------------------|---------------------------------------------------------|
| `deployments`                             | A dictionary of the deployments               | `nil`                                                   |
| `deployments.podinfo`                     | The podinfo default deployment                | `nil`                                                   |
| `deployments.podinfo.enabled`             | Enable the podinfo deployment                 | `false`                                                 |
| `deployments.podinfo.image`               | A dictionary to configure the image           | `nil`                                                   |
| `deployments.podinfo.image.repository`    | The image repository                          | `ghcr.io/stefanprodan/podinfo`                          |
| `deployments.podinfo.image.tag`           | The image tag                                 | `6.2.1`                                                 |
| `deployments.podinfo.replicaCount`        | The replica count of the pod created          | `3`                                                     |
| `deployments.podinfo.ports`               | A list of ports to be opened on the port and for a service to point to | `nil`                          |
| `deployments.podinfo.ports.podPortName`   | A name for the podPort to use instead of the port | `http`                                              |
| `deployments.podinfo.ports.podPort`       | The port on the pod to be opened              | `5000`                                                  |
| `deployments.podinfo.ports.servicePortName` | The name of the port in the service         | `http`                                                  |
| `deployments.podinfo.ports.servicePort`   | The port to be opened on the created service  | `80`                                                    |
| `deployments.podinfo.ports.protocol`      | The protocol to use on the open port          | `TCP`                                                   |
| `deployments.podinfo.networkPolicy`       | A dictionary of ingress and egress rules      | `nil`                                                   |
| `deployments.podinfo.networkPolicy.ingress` | A list of ingress rules for the deployment  | `[]`                                                    |
| `deployments.podinfo.networkPolicy.ingress.releaseName` | The release name you want to allow ingress traffic from | `nil`                           |
| `deployments.podinfo.networkPolicy.ingress.deploymentName` | The deployment name you want to allow ingress traffic from | `nil`                     |
| `deployments.podinfo.networkPolicy.ingress.ports` | A list of port names to allow ingress traffic on | `nil`                                        |
| `deployments.podinfo.networkPolicy.egress` | A list of egress rules for the deployment    | `[]`                                                    |
| `deployments.podinfo.networkPolicy.egress.releaseName` | The release name you want to allow egress traffic to | `nil`                               |
| `deployments.podinfo.networkPolicy.egress.deploymentName` | The deployment name you want to allow egress traffic to | `nil`                         |
| `deployments.podinfo.networkPolicy.egress.ports` | A list of port names to allow egress traffic to | `nil`                                          |
| `deployments.podinfo.networkPolicy.egress.ports.protocol` | The protocol for the egress traffic | `nil`                                             |
| `deployments.podinfo.networkPolicy.egress.ports.port` | The port to allow egress traffic to | `nil`                                                 |
| `deployments.podinfo.allowEgressToFQDN`   | A list of FQDNs to allow egress traffic to    | `[]`                                                    |
| `deployments.podinfo.configMaps`          | A list of configmaps that should be mounted into the pod as environment variables | `[]`                |
| `deployments.podinfo.configMaps.name`     | The name of the configmap to fetch            | `nil`                                                   |
| `deployments.podinfo.persistentVolumeClaims` | A list of persistentVolumeClaims that should be mounted as folder on the main pod | `[]`             |
| `deployments.podinfo.persistentVolumeClaims.name` | The name of the pvc that is defined in persistentVolumeClaims | `nil`                           |
| `deployments.podinfo.persistentVolumeClaims.path`           | The path where the folder should be mounted   | `nil`                                 |
| `deployments.podinfo.readinessProbe`      | A readiness probe for the pod                 | `See the default probes underneath`                     |
| `deployments.podinfo.readinessProbe.httpGet` | A dictionary of the endpoint to perform readiness probe on | `nil`                                   |
| `deployments.podinfo.readinessProbe.httpGet.path` | The path to probe for readiness       | `/healthz`                                              |
| `deployments.podinfo.readinessProbe.httpGet.port` | The port to probe for readiness       | `9898`                                                  |
| `deployments.podinfo.livenessProbe`       | A liveness probe for the pod                  | `See the default probes underneath`                     |
| `deployments.podinfo.livenessProbe.httpGet` | A dictionary of the endpoint to perform liveness probe probe on | `nil`                               |
| `deployments.podinfo.livenessProbe.httpGet.path` | The path to probe for liveness         | `/healthz`                                              |
| `deployments.podinfo.livenessProbe.httpGet.port` | The port to probe for liveness         | `9898`                                                  |
| `deployments.podinfo.resources`           | Setting resources for you pod                 | `nil`                                                   |
| `deployments.podinfo.resources.memory`    | The amount of RAM reserved for your pod       | `100Mi`                                                 |
| `deployments.podinfo.resources.cpu`       | The amount of cores reserved for your pod     | `100m`                                                  |
| `deployments.podinfo.ingress`             | Setting ingress for your pod                  | `nil`                                                   |
| `deployments.podinfo.ingress.host`        | Setting ingress host name for your pod        | `nil`                                                   |
| `deployments.podinfo.ingress.path`        | Setting ingress path for your pod             | `nil`                                                   |
| `deployments.podinfo.ingress.serviceName` | Setting service name target for ingress       | `nil`                                                   |
| `deployments.podinfo.ingress.port`        | Setting service name target port for ingress  | `nil`                                                   |
| `deployments.podinfo.ingress.secretName`  | Setting cert and key secret name              | `nil`                                                   |
| `deployments.podinfo.imagePullSecret`     | The secret name containing container registry credentials | `nil`                                       |
| `configMaps`                              | A list of configmaps to be created            | `[]`                                                    |
| `configMaps.name`                         | The name of the configmap you want to create  | `nil`                                                   |
| `configMaps.content`                      | A dictionary of key-value pairs               | `nil`                                                   |
| `persistentVolumeClaims`                  | A list of persistent volume claims to be created | `[]`                                                 |
| `persistentVolumeClaims.name`             | The name of the persistent volume claim       | `nil`                                                   |
| `persistentVolumeClaims.size`             | The size of the persistent volume claim       | `nil`                                                   |
| `kafkaTopics`                             | A dictionary of kafka topics to be created or accessed | `nil`                                          |
| `kafkaTopics.create`                      | A list of kafka topics to be created          | `[]`                                                    |
| `kafkaTopics.create.name`                 | The name of the topic you want to create      | `nil`                                                   |
| `kafkaTopics.create.replicas`             | The number of replicas for the topic          | `nil`                                                   |
| `kafkaTopics.create.partitions`           | The number of partitions for the topic        | `nil`                                                   |
| `kafkaTopics.create.retention`            | A dictionary of the retention rate for the topic | `nil`                                                |
| `kafkaTopics.create.retention.ms`         | The retention rate of the topic in ms         | `nil`                                                   |
| `kafkaTopics.create.retention.bytes`      | The number of bytes to retain for the topic   | `nil`                                                   |
| `kafkaTopics.access`                      | A list of kafka topics to access              | `[]`                                                    |
| `kafkaTopics.access.name`                 | The name of the topic you want to access      | `nil`                                                   |
| `kafkaTopics.access.applicationName`      | The name of the deployment that is requesting access to the topic | `nil`                               |
| `kafkaTopics.access.namespace`            | The namespace of the deployment that is requesting access to the topic | `nil`                          |
| `kafkaTopics.access.produce`              | Whether the application can produce to the topic | `nil`                                                |
| `kafkaTopics.access.consume`              | Whether the application can consume from the topic | `[]`                                               |
