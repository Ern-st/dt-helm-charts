# Secrets
Before you can use a secret in your deployment, you have to create it on the cluster.
On the RTP platform, this is done by putting your secret information into our vault and then referencing it on the platform.

## Add secret to vault
To add a secret to the vault, simply run the following commands, substituting the necessary information:
```
PROJECT_NAME='your-project-name'
SECRET_NAME='your-secret-name'
vault kv put --address=https://vault.teamdt.net -mount=secret secret/tenant-$PROJECT_NAME/$SECRET_NAME passcode=my-long-passcode username=my-username
```

## Create secret on the cluster
Now that you have created the secret in the vault, you need to get the secret into the cluster. You do this by referencing the secret in your [values.yaml](../chart/values.yaml).

```yaml
secrets:
  - name: <your-secret-name>
    key: secret/tenant-<your-project-name>/<your-secret-name>
    ...
```
After this, you can now reference the secret in the deployment of the pod you would like it mounted into. See how [here](./deployment.md#secrets).
