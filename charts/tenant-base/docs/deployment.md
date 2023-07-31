# Deployment
A deployment is used to describe how we want to deploy one or more containers in a pod. All the things described in this document can also be found in [this table](../chart/README.md#configuration).

## Deployment name
A deployment is started by making a key in the deployments object, this key can be anything and will be used as part of the name for the deployment.

```yaml
deployments:
  foo: #<-- this will be the name of the deployment
    ...
```
The name of the deployment should be as descriptive as possible for what you are deploying. If you set the name of the deployment to `foo`, the name of the pods now contains foo as part of their name.

```bash
podinfo-tenant-base-foo-57c9487678-dncs8
podinfo-tenant-base-foo-57c9487678-kg9j7
podinfo-tenant-base-foo-57c9487678-shlmj
```

## Enabling a deployment
You can enable and disable deployments with the `enabled` flag:
```yaml
deployments:
  foo:
    enabled: true
    ...
```

## Setting the image of a deployment
The image of the deployment is the container image that will be run in a pod in the deployment. You should set this accordingly to point to your container image and the correct version:
```yaml
deployments:
  foo:
    image:
      repository: ghcr.io/stefanprodan/podinfo
      tag: 6.2.1
    ...
```

## Setting the replica count
Replica count is the number of replicas of the pod that the deployment creates. For high avilability concerns, it is a good idea to have multiple replicas of your pod running. If one dies, another takes over.
```yaml
deployments:
  foo:
    replicaCount: 3
    ...
```

## Opening of a port in the pod
You can define a list of ports that should be opened in your pod. This should be done if you would like to allow network traffic to flow into or out from your container. An explanation of the configurations you can make for a port can be found [here](../chart/README.md#configuration).
When you create an entry in the `ports` list, the port will have a port opened for traffic. This is called the `podPort`. A kubernetes [service](https://kubernetes.io/docs/concepts/services-networking/service/) will also be created, which will be accessible on the port specified under `servicePort`. If you would like to send traffic to your pod, simply direct it towards the service and service port. The service will then forward the traffic to the correct pod and port.
```yaml
deployments:
  foo:
    ports:
      - podPortName: http
        podPort: 5000
        servicePortName: http
        servicePort: 80
        protocol: TCP
    ...
```

## Network policy
`networkPolicy` controls how traffic can flow to (`ingress`) and from (`egress`) the pods created by the deployment. In this example we create a deployment which allows:
- Ingress traffic from a release called `dlr`, in which the deployment is called `data` and the traffic has to come on the port `http` which is defined under `ports`.
- Egress traffic to the same release and deployment but only on port `8080` and with `TCP` as the protocol.

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
        - releaseName: dlr
          deploymentName: data
          ports:
            - http
      egress:
        - releaseName: dlr
          deploymentName: data
          ports:
            - protocol: TCP
              port: 8080
```
### Example
NetworkPolicies can be used for pod to pod traffic. To send traffic from one pod to another, you need to configure ingress on the receiving pod and egress on the transmitting pod. This can look like this:
```yaml
deployments:
  sender:
    networkPolicy:
      ingress: []
      egress:
        - releaseName: test
          deploymentName: receiver
          ports:
            - protocol: TCP
              port: 9898
  receiver:
    ports:
      - podPortName: http
        podPort: 9898
        servicePortName: http
        servicePort: 80
        protocol: TCP
    networkPolicy:
      ingress:
        - releaseName: test
          deploymentName: sender
          ports:
            - http
      egress: []
```
This example creates a deployment called `sender`. It creates a pod with an egress network policy that allows traffic on port 9898 with the protocol TCP to another pod in the same helm release. This deployment is called `receiver`. This `receiver` deployment will create a network policy for its pod to receive ingress traffic on the `http` port. We can see this defined as port 9898 with TCP as the protocol.
When you allow egress traffic from a pod, you will automatically create a policy that allows for the egress pod to contact the kubernetes DNS server. This allows you to use a pod's service instead of contacting the pod directly. To find the DNS name for the service of the pod you are trying to contact, use: `<release-name>-<deployment-name>.<namespace>.svc.cluster.local:<servicePort>`. In this example, this would look like this: `test-receiver.tenant-testing.svc.cluster.local:80`. This is the endpoint you can use inside your pod `sender` to send traffic to your pod `receiver`.

## Config maps
Config maps is a list that contains the config maps you would like to be mounted into the pod in the deployment as environment variables. Before you can mount a config map one has to be created on the cluster. See [config maps](configmap.md). In this example we mount a config map called `foobar` into our pod.
```yaml
deployments:
  foo:
    configMaps:
      - name: foobar
    ...
```

## Persistent volume claims
Persistent volume claims(PVC) is a list that contains the PVC's you would like to be mounted into the pod in the deployment as folders. Before you can mount a PVC one has to be created on the cluster. See [Persistent volume claims](pvc.md). In this example we mount a PVC called `foobar` into our pod on the path `/tmp/foo`.
```yaml
deployments:
  foo:
    persistentVolumeClaims:
      - name: foobar
        path: /tmp/foo
    ...
```

## Readiness and liveness probes
Probes are a way of ensuring that your pod has started successfully and is running continously on the cluster. There are default readiness and liveness probes configured that you can use. They look like this:
```yaml
deployments:
  foo:
    readinessProbe:
      httpGet:
        path: /healthz
        port: 9898
    livenessProbe:
      httpGet:
        path: /healthz
        port: 9898
    ...
```

If you would like to configure your own, simply configure the example above in your [values.yaml](../chart/values.yaml).
NB: Exposing health checks is required for your application to run on the platform

## Resource control
Setting the resources for your pod can be a good way to make sure enough memory and cpu is dedicated to making your application run in a stable way on the cluster. You can set the resources for your pod like this:
```yaml
deployments:
  foo:
    resources:
      memory: 200Mi
      cpu: 200m
    ...
```
In this example, we reserve 200 megabyte of RAM for your pod and 200 milli CPU's, equivalent to 1/5 core.
It is important to manage resources in your own namespace. Currently, the total RAM reserved for a namespace is 10 gigabyte and the total CPU reserved is 5 cores.
Note: If you do not configure resources for your pod, you will be assigned the default resources which is 100 megabyte of RAM and 100 mili CPU's, equivalent to 1/10 core.

## Ingress
Setting up ingress for your pod is an idea if you would like to send traffic to the pod for example by accessing a dashboard that the pod is exposing
```yaml
    ingress:
      host: "podinfo.teamdt.net"
      serviceName: "test-podinfo"
      port: 80
      secretName: "podinfo-tls"
```
In order for this to work, you need to create a secret manually called `<application-name>-tls` and apply it in your namespace. This can be done with the following manifest, which you should save as `<application-name>-tls-secret.yaml`:
```yaml
---
apiVersion: v1
type: kubernetes.io/tls
kind: Secret
metadata:
  name: test-tls
  namespace: traefik
data:
  tls.crt: ""
  tls.key: ""
```
You should fill in the `tls.crt` and `tls.key` with a valid `x.509` certificate and key. You can generate this with the following command. Remember to substitute the CN with your own host name:
```yaml
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=foo.bar.com"
```
After generating the `tls.crt` and `tls.key` you need to base64 encode them before pasting them into the secret:
```yaml
base64 -w 0 tls.key
base64 -w 0 tls.crt
```
Paste these two base64 encoding into the `data.tls.crt` and `data.tls.key` fields. now apply the secret on the cluster with:
```yaml
kubectl create -f <application-name>-tls-secret.yaml
```
If you have filled in all the information correctly and applied it on the cluster, you should be able to access your pod on `https://podinfo.teamdt.net`.
