# Tenant-base

The tenant base helm chart is a chart that give an easy all in one place to make deployments, it is only designed to make deployments and the resources that could be useful for deployments, like configmaps, pvc's etc.

The name of helm release should be the name of the higher level application that this chart deploys, e.g. if we're deploying a web application and a database, we could call the whole release "wordpress".

The chart is made in a way that allows for creation of a number of resources using only the `values.yaml` file,
the chart supports the creation of the following resources in some way:

- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)

## Values

The `values.yaml` consists of several lists of resources, these are either lists with simple objects e.g. the bucketClaim list only takes a name, or more complex objects like the deployments.

To begin with we will start with the values that are not lists:

### Deployments

See [deployment](docs/deployment.md)

### ConfigMaps

> [Kubernetes.io#configmaps](https://kubernetes.io/docs/concepts/configuration/configmap/)

[`configMaps`](chart/values.yaml#l84) is a way to handle configuration files of variables.

A config map is an object that stores configurations which can be mounted in to one or more pods either as environment variables or as files.
The config map can contain multiple configs at once, both [entire files](chart/values.yaml#l89) or [`single values`](chart/values.yaml#l88).

### PersistentVolumeClaims

> [kubernetes.io#persistentvolumeclaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)

Persistent volume claims (PVC) is a volume that persists even if the pod it's mounted to is destroyed.

[`persistentvolumeclaims`](chart/values.yaml#l100) is a list which creates PVC's for each entry in the list, the objects in the list consists of:

- The [`name`](chart/values.yaml#l101) for the PVC
- The [`size`](chart/values.yaml#l102) of the PVC
