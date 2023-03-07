# Config maps
Config maps hold information that is not sensitive. To use a configmap in your deployment, one has to be created first in the [values.yaml](../chart/values.yaml):
```yaml
configMaps:
  - name: foobar
    content:
      apiKey: qwertyuiop123456789
    ...
```
You can now reference the config map in a deployment and have the content mounted in as environment values. See how [here](./deployment.md#config-maps).
