# Kubernetes

Kubernetes is an open-source container orchestration platform.

## Pod

A Pod is the smallest deployable unit in Kubernetes. A Pod can contain one or more containers that share networking and storage.

## Deployment

A Deployment manages ReplicaSets and provides declarative updates for Pods.

A Deployment can be used to:

- Create Pods
- Scale applications
- Perform rolling updates
- Roll back to previous versions

## Service

A Kubernetes Service provides a stable network endpoint for accessing a set of Pods.

Common Service types include:

- ClusterIP
- NodePort
- LoadBalancer

## ConfigMap

A ConfigMap stores non-confidential configuration data as key-value pairs.

## Secret

A Secret is designed to hold sensitive information such as passwords, tokens, and keys.
