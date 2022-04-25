# Resource-helper

The resource-helper chart is a helper chart that will
facilitate the creation of ArgoCD project, Resource Quotas
and network policies

This is desgined so that one is deployed pr. namespace

One proposed use method is to deploy this using ArgoCD and enabeling `createNamespace` so that when this app is created it creates the namespace, with the resources that is needed in it.
Then on app that will live in the namespace it will have to wait for the namespace to exist with the right resources.

## Why

This chart exists currently to be used in the [helm-overdrive POC](https://github.com/distributed-technologies/helm-overdrive-poc) where it's used as described above.
