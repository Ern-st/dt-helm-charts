# Tenant-base

The tenant base helm chart is a chart that give an easy all in one place to make deployments, it is only designed to make deployments and the resources that could be useful for deployments, like configmaps, pvc's etc.

The chart is made in a way that allows for creation of a number of resources using only the `values.yaml` file,
the chart supports the creation of the following resources in some way:

- [ObjectBucketClaims](https://rook.io/docs/rook/v1.9/ceph-object-bucket-claim.html)
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ExternalSecrets](https://external-secrets.io/v0.6.0/api/externalsecret/)
- [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)

## Values

The `values.yaml` consists of several lists of resources, these are either lists with simple objects e.g. the bucketClaim list only takes a name, or more complex objects like the deployments.

To begin with we will start with the values that are not lists:

### `fullenameOverride`

[`fullnameOverride`](chart/values.yaml#l2) is used to override the name of the chart, the reason this exists is because the name of the chart is `tenant-base` and the name is used in the names of most of the resources, so if we could'nt change the name we would end up with a lot of resources that contains the name of this chart instead of the application the resource actually belong to.

For example if we set `fullnameOverride` to an empty string and use the chart name we get pods that is names:

```bash
podinfo-tenant-base-podinfo-57c9487678-d6s2z
podinfo-tenant-base-podinfo-57c9487678-q6lgc
podinfo-tenant-base-podinfo-57c9487678-x9j6
```

As we can see `tenant-base` is the middle of the name.

If we set the value of `fullnameOverride` to e.g. `foobar` we would get

```bash
podinfo-foobar-podinfo-57c9487678-d6s2z
podinfo-foobar-podinfo-57c9487678-q6lgc
podinfo-foobar-podinfo-57c9487678-x9j6
```

Now `tenant-base` has been replaced with `foobar`.

> The structure of the name is built like this `<release-name>-<chart-name or fullnameOverride>-<deployment-name>-<uid>`

### SecretStore

>[external-secrets.io#clustersecretstore](https://external-secrets.io/v0.6.0/api-clustersecretstore/)

The secretStore resources comes from the external-secrets application, the secretStore defines how we want to interact and authenticate with any number of secrets stores like Hashicorp vault or Azure key vault.

[`secretStore`](chart/values.yaml#l125) is where we define the reference of the secretStore we want to use in the external secrets.

[`name`](chart/values.yaml#l126) is the name of the secretStore we want to use.

[`kind`](chart/values.yaml#l127) is the kind of the secretStore we wish to use, this can be either `SecretStore` or `ClusterSecretStore`.

> This does not create the secretStore, this is a reference to already existing resources.

These values will be used in the creation of [external-secrets](https://external-secrets.io/v0.5.9/api-externalsecret/) in the [deployment section](#deployment).

### Deployments

See [deployment](docs/deployment.md)

### ConfigMaps

> [Kubernetes.io#configmaps](https://kubernetes.io/docs/concepts/configuration/configmap/)

[`configMaps`](chart/values.yaml#l84) is a way to handle configuration files of variables.

A config map is an object that stores configurations which can be mounted in to one or more pods either as environment variables or as files.
The config map can contain multiple configs at once, both [entire files](chart/values.yaml#l89) or [`single values`](chart/values.yaml#l88).

### BucketClaims

> [rook.io#ObjectBucketClaim](https://rook.io/docs/rook/v1.9/ceph-object-bucket-claim.html)

[`BucketClaims`](chart/values.yaml#l95) allows for the creation of a s3 object storage,
The bucketClaim creates a secret and configMap that needs to be mounted on the pod that will use it.
The name of the secret and configMap is `<release-name>-<chart-name>-<name>`.

All we need to do is to supply a list of names for buckets that we want, this will then request a bucket from Ceph.
To provide a pod with the credentials needed to access the bucket, the `ObjectBuckerClaim` provides a secret and a configMap that we will have to mount in the relevant deployments,
This is done by adding the following the documentation regarding [volumes](docs/deployment.md#volumes) and [volumeMounts](docs/deployment.md#volumemounts).

### PersistentVolumeClaims

> [kubernetes.io#persistentvolumeclaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)

Persistent volume claims (PVC) is a volume that persists even if the pod it's mounted to is destroyed.

[`persistentvolumeclaims`](chart/values.yaml#l100) is a list which creates PVC's for each entry in the list, the objects in the list consists of:

- The [`name`](chart/values.yaml#l101) for the PVC
- The [`size`](chart/values.yaml#l102) of the PVC
- (optional) The [`storageClass`](chart/values.yaml#l102) the PVC will use.
