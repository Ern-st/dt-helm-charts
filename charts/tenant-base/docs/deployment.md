# Deployment

A deployment is used to describe how we want to deploy one or more containers in a pod.

> [kubernetes.io#Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

The [deployments list](../chart/values.yaml#l5) is used to describe one or more deployments that we want to run on kubernetes, to describe a deployment we need to set some values:

## name

[`name`](../chart/values.yaml#l7) is the name of the deployment, this should be descriptive of what this deployment deploys.
This name is also being used to in the name of the pods, like we saw in [fullnameOverride](../README.md#fullenameoverride).

If we set the name of the deployment to `foo` the name of the pods now contains foo as part of their name.

```bash
podinfo-tenant-base-foo-57c9487678-dncs8
podinfo-tenant-base-foo-57c9487678-kg9j7
podinfo-tenant-base-foo-57c9487678-shlmj
```

## image

[`image`](../chart/values.yaml#l8) describes the image we wish to use in the deployment, as a default we are using the [podinfo](https://github.com/stefanprodan/podinfo) image.

[`repository`](../chart/values.yaml#l10) is the URL to the container registry that the container we wish to use is located in.

[`pullPolicy`](../chart/values.yaml#l15) is the rule that defines when we want to pull the image there are three options for this:

* `IfNotPresent`   - This will try to fetch the image if the it's not already located on the node.
* `Always`         - Will always try to fetch the newest image
* `Never`          - Will not try to fetch the image - if image is not present on the machine startup fails

[`tag`](../chart/values.yaml#l17) is the version of the image we wish to run, this cannot be `latest`.

## ImagePullSecret

> [kubernetes.io#pull-image-private-registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)

[`imagePullSecret`](../chart/values.yaml#l20) is a list of secret references containing the information needed to authenticate with a private container registry.

## replicaCount

[`replicaCount`](../chart/values.yaml#l25) is the amount of identical copies wanted of the pod defines in the deployment, it is advised to have a replicaCount of 2 or 3 for redundancy.

> The deployment is using [topologySpreadConstrains](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/) to evenly distribute replicas on different nodes.

## Liveness and Readiness Probes

> [kubernetes.io#types-of-probe](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#types-of-probe)

The liveness probe is used to determine whether the container is running, if the probe fails the container is killed and restarted.

The readiness probe is used to determine if the container is ready to respond to requests.

>It is recommended to always supply both liveness and readiness probes.

There are several ways of configuring both of the probes depending on what type of probe e.g. HTTP or CMD, and we would recommend looking at the [official documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes).

## Volumes

> [kubernetes.io#volumes](https://kubernetes.io/docs/concepts/storage/volumes/)

[volumes](../chart/values.yaml#l45) is a list of volumes that we want to make available to all containers in the deployment, there are several types of volumes that can be provided, we aid in the creation of some of those, configMaps, secrets, emptyDir and persistentVolumeClaims.

Some examples on how to make different types of volumes available.

```yaml
volumes:
  - name: cache
    emptyDir: {}
  - name: configMap
    configMaps:
      name: foobar-cm
  - name: secret
    secret:
      secretName: foobar-sec
  - name: PVC
    persistentVolumeClaim:
      claimName: foobar-pvc
```

All volumes in the example above, except the emptyDir, requires a resources to exist, with the same name used to reference the resource.

## VolumeMounts

> [kubernetes.io#volumeMounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-volume-storage/#configure-a-volume-for-a-pod)

[`volumeMounts`](../chart/values.yaml#l53) is a list of where each object describe what volume and where we want to mount said volume.

`name` is the name of the volumes that we described in the [volumes](../chart/values.yaml#l45) list.
`mountPath` is the path **in** the container we want to mount the content of the volume.

Doing this will mount the volume on the path, and override anything the already existed on that path (if any),
To circumvent this behavior we can define a [subPath](https://kubernetes.io/docs/concepts/storage/volumes/#using-subpath) on our volumeMount.

A `subpath` allows us to define a path within the `mountPath` to mount the content, using a `subPath` does not override the content that could exist in the `mountPath`

```yaml
volumeMounts:
  - mountPath: /cache
    name: cache
    subPath: tmp
```

## Resources

> [kubernetes.io#resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)

[`resources`](../chart/values.yaml#l60) describes the available resources (CPU and memory) for the containers, this is done by defining requests and limits.

Requests describes the resources that the container need to be able to run, this gives kubernetes the ability to intelligently choose the most suitable node to create the pod in and reserves the resources requested.

Limits is the max amount of resources a container is allowed to use.

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
