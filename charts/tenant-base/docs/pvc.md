# Persistent volume claims
Persistent volume claims(PVC) is a way to create persistent storage on the cluster. To use a PVC in your deployment, one has to be created first in the [values.yaml](../chart/values.yaml):
```yaml
persistentVolumeClaims:
  - name: foobar
    size: 8Gi
    ...
```
You can now reference the PVC in a deployment and have it mounted in as a folder. See how [here](./deployment.md#persistent-volume-claims).
