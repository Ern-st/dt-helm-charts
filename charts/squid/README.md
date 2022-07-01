# Squid

A CA can be created with [`step` CLI](https://smallstep.com/docs/step-cli) per [their documentation](https://smallstep.com/docs/step-cli/basic-crypto-operations#create-and-work-with-x509-certificates):
```sh
$ step-cli certificate create --insecure --no-password --kty=RSA --profile root-ca "Proxy Root CA" root_ca.crt root_ca.key
```
