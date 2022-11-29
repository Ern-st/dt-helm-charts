# Deployment

A deployment is used to describe how we want to deploy one or more containers in a pod.

> [kubernetes.io#Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

The [deployments](../chart/values.yaml#l5) is used to describe one or more deployments that we want to run on kubernetes, to describe a deployment we need to set some values:

A deployment is started by making a key in the deployments object, this key can be anything and will be used as part of the name for the deployment.

```yaml
deployments:
  foo: #<-- this will be the name of the deployments
    image: foo-bar
    ...
```

[`name`](../chart/values.yaml#l7) is the name of the deployment, this should be descriptive of what this deployment deploys.
This name is also being used to in the name of the pods.

Name is also the key of the deployment object.

If we set the name of the deployment to `foo` the name of the pods now contains foo as part of their name.

```bash
podinfo-tenant-base-foo-57c9487678-dncs8
podinfo-tenant-base-foo-57c9487678-kg9j7
podinfo-tenant-base-foo-57c9487678-shlmj
```

This value of they key will then contain the rest of the deployment configuration.

## image

[`image`](../chart/values.yaml#l8) describes the image we wish to use in the deployment, as a default we are using the [podinfo](https://github.com/stefanprodan/podinfo) image.

[`repository`](../chart/values.yaml#l10) is the URL to the container registry that the container we wish to use is located in.

[`tag`](../chart/values.yaml#l17) is the version of the image we wish to run, this cannot be `latest`.

## replicaCount

[`replicaCount`](../chart/values.yaml#l25) is the amount of identical copies wanted of the pod defines in the deployment, it is advised to have a replicaCount of 2 or 3 for redundancy.

> The deployment is using [topologySpreadConstrains](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) to evenly distribute replicas on different nodes.

## Liveness and Readiness Probes

> [kubernetes.io#types-of-probe](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#types-of-probe)

The liveness probe is used to determine whether the container is running, if the probe fails the container is killed and restarted.

The readiness probe is used to determine if the container is ready to respond to requests.

This chart configures liveness and readiness probes to check a HTTP endpoint on port `9898`. The endpoint is expected to return with a `200` HTTP code at `/healthz` if the application is ready and healthy.

For ASP.NET Core applications the [AspNetCore.Diagnostics.HealthChecks](https://github.com/Xabaril/AspNetCore.Diagnostics.HealthChecks) package can be used for adding health check endpoints as explained in [this article](https://andrewlock.net/deploying-asp-net-core-applications-to-kubernetes-part-6-adding-health-checks-with-liveness-readiness-and-startup-probes/#creating-a-custom-health-check)

## Ports

[`ports`](../chart/values.yaml#l70) is a list of objects, the objects in the list consists of two ports, the [podPort](../chart/values.yaml#l72) and the [servicePort](../chart/values.yaml#l74).

The `podPort` tell us what port on the pod we want to map to the `servicePort` on the service, This allows us to access the application through the service on the `servicePort`.

> Every deployment gets it's own service.

## secrets

> [External-secrets.io#ExternalSecrets](https://external-secrets.io/v0.6.0/api/externalsecret/)

[`secrets`](../chart/values.yaml#l78) is a list that describes the where to fetch a secret from the vault store, and the name of that secret.

[`name`](../chart/values.yaml#l80) is a arbitrary name for the secret, that is used to describe what the secret contains.

[`key`](../chart/values.yaml#l81) is the path in the secret store where the secret is located.

This list also adds the secret to the pod as environment variables.

## configMaps

> [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)

[`ConfigMaps`](../chart/values.yaml#54) is a list that describes which configMaps to mount into the main pod as environment variables.

[`name`](../chart/values.yaml#56) is a arbitrary name for the configmap, that has to match the defined configMap you would like to mount in.

## PVCS

> [PeristantVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)

[PVCS](../chart/values.yaml#43) A list of PVCs that should be mounted as a folder in the main pod

[name](../chart/values.yaml#45) - Name of the PVC defined in the persistentVolumesClaims list on line ~71

[path](../chart/values.yaml#46) - The path where the folder should be mounted. NOTE! the WILL remove the content of the folder on the host, if it exists already, so aim to choose a path that is know empty.

## `networkPolicy`

`networkPolicy` controls how traffic can flow to (`ingress`) and from (`egress`) the pods created by the deployment.

Please also read Kubernetes documentation on [network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/).

Example:

```yaml
deployments:
  - name: podinfo

    ports:
      - podPortName: http
        podPort: 9898
        servicePortName: http
        servicePort: 80
        protocol: TCP

    networkPolicy:
      ingress:
        - labels:
            app.kubernetes.io/name: foo
          ports:
            - http
      egress:
        - labels:
            app.kubernetes.io/name: foo
          ports:
            - protocol: TCP
              port: 8080
```

This would allow traffic to flow from pods with the label `app.kubernetes.io/name: foo` to the pods created by the deployment on the port defined with `podPortName: http` in `ports`.

It would also allow traffic to flow from the pods creatd by this deployment to pods with the label `app.kubernetes.io/name: foo` on port `8080/TCP`.
