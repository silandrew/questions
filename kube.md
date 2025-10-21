# Kubernetes Troubleshooting Guide
## Comprehensive Guide for Automation, Scripting, APIs, and Containerized Environments

---

## Table of Contents
1. [Cluster-Level Troubleshooting](#cluster-level-troubleshooting)
2. [Pod and Container Issues](#pod-and-container-issues)
3. [Networking Troubleshooting](#networking-troubleshooting)
4. [Storage and Persistent Volume Issues](#storage-and-persistent-volume-issues)
5. [API Server and Authentication](#api-server-and-authentication)
6. [Automation and CI/CD Issues](#automation-and-cicd-issues)
7. [Scripting and kubectl Automation](#scripting-and-kubectl-automation)
8. [Performance and Resource Issues](#performance-and-resource-issues)
9. [Security and RBAC](#security-and-rbac)
10. [Monitoring and Logging](#monitoring-and-logging)
11. [Common Error Messages and Solutions](#common-error-messages-and-solutions)

---

## 1. Cluster-Level Troubleshooting

### Check Cluster Health
```bash
# Check cluster info
kubectl cluster-info
kubectl cluster-info dump

# Check node status
kubectl get nodes
kubectl get nodes -o wide

# Describe a node for detailed information
kubectl describe node <node-name>

# Check component status
kubectl get componentstatuses
kubectl get cs

# Check API server health
kubectl get --raw='/readyz?verbose'
kubectl get --raw='/healthz?verbose'
```

### Node Issues

#### Node Not Ready
```bash
# Check node conditions
kubectl describe node <node-name> | grep -A 5 Conditions

# Common causes:
# 1. Disk pressure
df -h
# Clean up unused images
docker system prune -a

# 2. Memory pressure
free -h
# Check for memory-intensive pods

# 3. Network issues
systemctl status kubelet
journalctl -u kubelet -f

# 4. Kubelet not running
systemctl restart kubelet
systemctl status kubelet
```

#### Check Node Logs
```bash
# Kubelet logs
journalctl -u kubelet -n 100 --no-pager

# Container runtime logs (containerd)
journalctl -u containerd -n 100 --no-pager

# Docker logs (if using Docker)
journalctl -u docker -n 100 --no-pager

# System logs
dmesg | tail -50
```

### Control Plane Issues
```bash
# Check etcd health
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health

# Check control plane pods
kubectl get pods -n kube-system

# Check API server logs
kubectl logs -n kube-system kube-apiserver-<master-node>

# Check controller manager
kubectl logs -n kube-system kube-controller-manager-<master-node>

# Check scheduler
kubectl logs -n kube-system kube-scheduler-<master-node>
```

---

## 2. Pod and Container Issues

### Pod Status Troubleshooting

#### ImagePullBackOff / ErrImagePull
```bash
# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Common solutions:
# 1. Check image name and tag
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}'

# 2. Verify image exists in registry
# For Docker Hub
docker pull <image-name>

# 3. Check image pull secrets
kubectl get secrets -n <namespace>
kubectl describe secret <secret-name> -n <namespace>

# 4. Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  -n <namespace>

# 5. Verify private registry authentication
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 3 imagePullSecrets
```

#### CrashLoopBackOff
```bash
# Check pod logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Check for multiple containers
kubectl logs <pod-name> -c <container-name> -n <namespace>

# Common causes and checks:
# 1. Application errors - check logs
kubectl logs <pod-name> -n <namespace> --tail=50

# 2. Missing environment variables
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 env:

# 3. Volume mount issues
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 volumeMounts:

# 4. Resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 Limits

# 5. Liveness/Readiness probe failures
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Liveness
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Readiness
```

#### Pending State
```bash
# Check why pod is pending
kubectl describe pod <pod-name> -n <namespace>

# Common reasons:
# 1. Insufficient resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# 2. Node selector/affinity issues
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 nodeSelector
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 affinity

# 3. Taints and tolerations
kubectl describe nodes | grep Taints
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 tolerations

# 4. PVC not bound
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>
```

#### OOMKilled (Out of Memory)
```bash
# Check pod status
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[0].lastState}'

# View memory limits and requests
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].resources}'

# Check actual memory usage
kubectl top pod <pod-name> -n <namespace>

# Increase memory limits
kubectl set resources deployment <deployment-name> \
  --limits=memory=1Gi \
  --requests=memory=512Mi \
  -n <namespace>
```

### Container Debugging
```bash
# Execute commands in container
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# For specific container in multi-container pod
kubectl exec -it <pod-name> -c <container-name> -n <namespace> -- /bin/bash

# Check running processes
kubectl exec <pod-name> -n <namespace> -- ps aux

# Check network connectivity
kubectl exec <pod-name> -n <namespace> -- ping <target>
kubectl exec <pod-name> -n <namespace> -- curl <url>
kubectl exec <pod-name> -n <namespace> -- nslookup <service>

# Debug with temporary pod
kubectl run debug-pod --image=nicolaka/netshoot -it --rm -- /bin/bash
kubectl run debug-pod --image=busybox -it --rm -- /bin/sh
```

---

## 3. Networking Troubleshooting

### Service Discovery Issues
```bash
# Check service
kubectl get svc -n <namespace>
kubectl describe svc <service-name> -n <namespace>

# Verify endpoints
kubectl get endpoints <service-name> -n <namespace>
kubectl describe endpoints <service-name> -n <namespace>

# Test DNS resolution
kubectl run dnsutils --image=tutum/dnsutils -it --rm -- nslookup <service-name>
kubectl run dnsutils --image=tutum/dnsutils -it --rm -- nslookup <service-name>.<namespace>.svc.cluster.local

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns

# Verify kube-dns service
kubectl get svc -n kube-system kube-dns
```

### Network Policy Issues
```bash
# List network policies
kubectl get networkpolicies -n <namespace>
kubectl get netpol -n <namespace>

# Describe network policy
kubectl describe networkpolicy <policy-name> -n <namespace>

# Check if network plugin supports network policies
kubectl get pods -n kube-system | grep -E 'calico|cilium|weave'

# Test connectivity
kubectl run test-pod --image=busybox -it --rm -- wget -O- http://<service-name>:<port>
```

### Ingress Troubleshooting
```bash
# Check ingress resources
kubectl get ingress -n <namespace>
kubectl describe ingress <ingress-name> -n <namespace>

# Check ingress controller
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx <ingress-controller-pod>

# Verify ingress class
kubectl get ingressclass

# Check ingress annotations
kubectl get ingress <ingress-name> -n <namespace> -o yaml

# Test ingress from within cluster
kubectl run curl-test --image=curlimages/curl -it --rm -- curl -H "Host: <domain>" http://<ingress-ip>
```

### Load Balancer Issues
```bash
# Check service type LoadBalancer
kubectl get svc <service-name> -n <namespace>

# For cloud providers, check external IP assignment
kubectl describe svc <service-name> -n <namespace>

# Check cloud provider events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# MetalLB troubleshooting (on-prem)
kubectl get ipaddresspool -n metallb-system
kubectl logs -n metallb-system -l app=metallb
```

### CNI Plugin Issues
```bash
# Check CNI plugin pods
kubectl get pods -n kube-system | grep -E 'calico|flannel|weave|cilium'

# Calico troubleshooting
kubectl get pods -n kube-system -l k8s-app=calico-node
kubectl logs -n kube-system -l k8s-app=calico-node

# Check CNI configuration
ls /etc/cni/net.d/
cat /etc/cni/net.d/*.conf

# Verify pod network CIDR
kubectl cluster-info dump | grep -m 1 cluster-cidr
```

---

## 4. Storage and Persistent Volume Issues

### PVC Not Binding
```bash
# Check PVC status
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>

# Check available PVs
kubectl get pv

# Check storage class
kubectl get storageclass
kubectl describe storageclass <storage-class-name>

# Common issues:
# 1. No matching PV
kubectl get pv -o custom-columns=NAME:.metadata.name,CAPACITY:.spec.capacity.storage,ACCESSMODES:.spec.accessModes

# 2. Storage class issues
kubectl get pvc <pvc-name> -n <namespace> -o jsonpath='{.spec.storageClassName}'
kubectl get sc

# 3. Check provisioner logs
kubectl get pods -n kube-system | grep provisioner
kubectl logs -n kube-system <provisioner-pod>
```

### Volume Mount Issues
```bash
# Check pod volume mounts
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.volumes}'
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].volumeMounts}'

# Describe pod for volume events
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Volumes

# Check if volume is mounted in container
kubectl exec <pod-name> -n <namespace> -- df -h
kubectl exec <pod-name> -n <namespace> -- ls -la /path/to/mount

# Check PV and PVC binding
kubectl get pv <pv-name> -o jsonpath='{.spec.claimRef}'
kubectl get pvc <pvc-name> -n <namespace> -o jsonpath='{.spec.volumeName}'
```

### Storage Performance Issues
```bash
# Test I/O performance
kubectl exec <pod-name> -n <namespace> -- dd if=/dev/zero of=/mnt/test bs=1M count=1024

# Check volume metrics
kubectl top pod <pod-name> -n <namespace> --containers

# For CSI drivers, check logs
kubectl get pods -n kube-system | grep csi
kubectl logs -n kube-system <csi-pod>
```

---

## 5. API Server and Authentication

### Authentication Issues
```bash
# Test authentication
kubectl auth can-i list pods --as=<user>
kubectl auth can-i create deployments --as=<user> -n <namespace>

# Check current context
kubectl config current-context
kubectl config view

# Verify user credentials
kubectl config view --raw

# Check certificate expiration
kubeadm certs check-expiration

# Renew certificates
kubeadm certs renew all
```

### API Server Access
```bash
# Test API server connectivity
kubectl get --raw /healthz
kubectl get --raw /api/v1/namespaces

# Check API server logs
kubectl logs -n kube-system kube-apiserver-<master-node>

# API server configuration
ps aux | grep kube-apiserver
cat /etc/kubernetes/manifests/kube-apiserver.yaml

# Direct API access with curl
TOKEN=$(kubectl create token default)
curl -k -H "Authorization: Bearer $TOKEN" https://<api-server>:6443/api/v1/namespaces
```

### Service Account Issues
```bash
# Check service account
kubectl get sa -n <namespace>
kubectl describe sa <service-account> -n <namespace>

# Get service account token
kubectl get secrets -n <namespace>
kubectl describe secret <sa-token-secret> -n <namespace>

# Create service account token (Kubernetes 1.24+)
kubectl create token <service-account> -n <namespace>

# Verify pod service account
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.serviceAccountName}'
```

---

## 6. Automation and CI/CD Issues

### GitOps and ArgoCD
```bash
# Check ArgoCD application status
kubectl get applications -n argocd
kubectl describe application <app-name> -n argocd

# ArgoCD sync issues
argocd app get <app-name>
argocd app sync <app-name>
argocd app diff <app-name>

# Check ArgoCD logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server

# Manual sync
argocd app sync <app-name> --force
```

### Helm Issues
```bash
# List helm releases
helm list -A
helm list -n <namespace>

# Check release status
helm status <release-name> -n <namespace>

# Get release values
helm get values <release-name> -n <namespace>

# Helm upgrade issues
helm upgrade --debug --dry-run <release-name> <chart> -n <namespace>

# Rollback helm release
helm rollback <release-name> <revision> -n <namespace>

# Check helm history
helm history <release-name> -n <namespace>
```

### Kustomize Issues
```bash
# Build kustomize manifests
kubectl kustomize <directory>
kustomize build <directory>

# Apply with dry-run
kubectl apply -k <directory> --dry-run=client

# Check kustomization
kubectl kustomize <directory> | kubectl diff -f -

# Debug kustomization
kustomize build <directory> --enable-alpha-plugins
```

### CI/CD Pipeline Issues
```bash
# Jenkins Kubernetes Plugin
# Check pod templates
kubectl get pods -n jenkins -l jenkins=slave

# Tekton troubleshooting
kubectl get pipelineruns -n <namespace>
kubectl describe pipelinerun <run-name> -n <namespace>
kubectl logs -n <namespace> <pod-name> -c step-<step-name>

# FluxCD troubleshooting
kubectl get helmreleases -A
kubectl describe helmrelease <release-name> -n <namespace>
flux logs
```

---

## 7. Scripting and kubectl Automation

### Kubectl Scripting Best Practices
```bash
# Set error handling in scripts
set -euo pipefail

# Check if resource exists before creating
if ! kubectl get namespace <namespace> 2>/dev/null; then
  kubectl create namespace <namespace>
fi

# Wait for deployment to be ready
kubectl wait --for=condition=available --timeout=300s \
  deployment/<deployment-name> -n <namespace>

# Retry logic
for i in {1..5}; do
  kubectl apply -f manifest.yaml && break || sleep 5
done

# Get resource with error handling
PODS=$(kubectl get pods -n <namespace> -o jsonpath='{.items[*].metadata.name}' 2>/dev/null || echo "")
if [ -z "$PODS" ]; then
  echo "No pods found"
fi
```

### Advanced kubectl Queries
```bash
# Get all pods with specific label
kubectl get pods -l app=myapp --all-namespaces

# Custom columns output
kubectl get pods -o custom-columns=\
NAME:.metadata.name,\
STATUS:.status.phase,\
NODE:.spec.nodeName,\
IP:.status.podIP

# JSONPath queries
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'

# Filter by field
kubectl get pods --field-selector=status.phase=Running
kubectl get events --field-selector involvedObject.kind=Pod

# Sort output
kubectl get pods --sort-by=.metadata.creationTimestamp
kubectl get pods --sort-by=.status.startTime
```

### Batch Operations
```bash
# Delete all pods with label
kubectl delete pods -l app=myapp -n <namespace>

# Scale all deployments
kubectl get deployments -n <namespace> -o name | \
  xargs -I {} kubectl scale {} --replicas=3 -n <namespace>

# Restart all deployments
kubectl get deployments -n <namespace> -o name | \
  xargs -I {} kubectl rollout restart {} -n <namespace>

# Export all resources in namespace
kubectl get all -n <namespace> -o yaml > backup.yaml

# Apply multiple manifests
find manifests/ -name '*.yaml' -exec kubectl apply -f {} \;
```

### Automation Scripts Examples

#### Health Check Script
```bash
#!/bin/bash
# health-check.sh

NAMESPACE=$1
DEPLOYMENT=$2

echo "Checking deployment: $DEPLOYMENT in namespace: $NAMESPACE"

# Check if deployment exists
if ! kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" &>/dev/null; then
  echo "ERROR: Deployment not found"
  exit 1
fi

# Check replicas
DESIRED=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" -o jsonpath='{.spec.replicas}')
READY=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" -o jsonpath='{.status.readyReplicas}')

if [ "$DESIRED" -eq "$READY" ]; then
  echo "SUCCESS: All $READY replicas are ready"
  exit 0
else
  echo "WARNING: Only $READY out of $DESIRED replicas are ready"
  kubectl get pods -n "$NAMESPACE" -l app="$DEPLOYMENT"
  exit 1
fi
```

#### Rolling Update Script
```bash
#!/bin/bash
# rolling-update.sh

DEPLOYMENT=$1
IMAGE=$2
NAMESPACE=${3:-default}

echo "Updating deployment $DEPLOYMENT to image $IMAGE"

# Update image
kubectl set image deployment/"$DEPLOYMENT" \
  "$DEPLOYMENT=$IMAGE" \
  -n "$NAMESPACE" \
  --record

# Wait for rollout
if kubectl rollout status deployment/"$DEPLOYMENT" -n "$NAMESPACE" --timeout=5m; then
  echo "Rollout successful"
else
  echo "Rollout failed, rolling back..."
  kubectl rollout undo deployment/"$DEPLOYMENT" -n "$NAMESPACE"
  exit 1
fi
```

#### Resource Cleanup Script
```bash
#!/bin/bash
# cleanup-failed-pods.sh

NAMESPACE=$1

echo "Cleaning up failed pods in namespace: $NAMESPACE"

# Get failed pods
FAILED_PODS=$(kubectl get pods -n "$NAMESPACE" \
  --field-selector=status.phase=Failed \
  -o jsonpath='{.items[*].metadata.name}')

if [ -z "$FAILED_PODS" ]; then
  echo "No failed pods found"
  exit 0
fi

# Delete failed pods
for pod in $FAILED_PODS; do
  echo "Deleting pod: $pod"
  kubectl delete pod "$pod" -n "$NAMESPACE"
done

echo "Cleanup complete"
```

---

## 8. Performance and Resource Issues

### Resource Monitoring
```bash
# Check node resources
kubectl top nodes
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check pod resources
kubectl top pods -A
kubectl top pods -n <namespace> --containers

# Get resource requests and limits
kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources}{"\n"}{end}'

# Find pods without resource limits
kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | .metadata.name'
```

### CPU and Memory Issues
```bash
# Check CPU throttling
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "cpu"

# Identify high CPU consumers
kubectl top pods -A --sort-by=cpu

# Identify high memory consumers
kubectl top pods -A --sort-by=memory

# Set resource quotas
kubectl create quota my-quota \
  --hard=requests.cpu=4,requests.memory=8Gi,limits.cpu=8,limits.memory=16Gi \
  -n <namespace>

# Check quota usage
kubectl describe resourcequota -n <namespace>
```

### Horizontal Pod Autoscaling (HPA)
```bash
# Check HPA status
kubectl get hpa -n <namespace>
kubectl describe hpa <hpa-name> -n <namespace>

# HPA not scaling
# 1. Check metrics server
kubectl get deployment metrics-server -n kube-system
kubectl logs -n kube-system deployment/metrics-server

# 2. Verify metrics availability
kubectl top pods -n <namespace>

# 3. Check HPA conditions
kubectl get hpa <hpa-name> -n <namespace> -o yaml

# Create HPA
kubectl autoscale deployment <deployment-name> \
  --cpu-percent=50 \
  --min=1 \
  --max=10 \
  -n <namespace>
```

### Vertical Pod Autoscaling (VPA)
```bash
# Check VPA recommendations
kubectl get vpa -n <namespace>
kubectl describe vpa <vpa-name> -n <namespace>

# View VPA recommendations
kubectl get vpa <vpa-name> -n <namespace> -o jsonpath='{.status.recommendation}'
```

---

## 9. Security and RBAC

### RBAC Troubleshooting
```bash
# Check user permissions
kubectl auth can-i <verb> <resource> --as=<user>
kubectl auth can-i create deployments --as=john -n production
kubectl auth can-i '*' '*' --as=admin

# List user permissions
kubectl auth can-i --list --as=<user>

# Check role bindings
kubectl get rolebindings -n <namespace>
kubectl get clusterrolebindings

# Describe role binding
kubectl describe rolebinding <binding-name> -n <namespace>
kubectl describe clusterrolebinding <binding-name>

# Check roles
kubectl get roles -n <namespace>
kubectl get clusterroles

# Describe role
kubectl describe role <role-name> -n <namespace>
kubectl describe clusterrole <role-name>
```

### Pod Security
```bash
# Check pod security policies (deprecated in 1.25)
kubectl get psp
kubectl describe psp <psp-name>

# Pod Security Standards (1.23+)
kubectl label namespace <namespace> \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted

# Check security context
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.securityContext}'
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].securityContext}'

# Identify privileged pods
kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | .metadata.name'
```

### Secrets Management
```bash
# Check secrets
kubectl get secrets -n <namespace>
kubectl describe secret <secret-name> -n <namespace>

# Decode secret
kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data.<key>}' | base64 -d

# Create secret from literal
kubectl create secret generic my-secret \
  --from-literal=username=admin \
  --from-literal=password=secret \
  -n <namespace>

# Create secret from file
kubectl create secret generic my-secret \
  --from-file=ssh-privatekey=~/.ssh/id_rsa \
  -n <namespace>

# Check if secret is mounted
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.volumes[*].secret}'
```

### Network Security
```bash
# Audit network policies
kubectl get networkpolicies -A

# Check default deny policy
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: <namespace>
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# Test connectivity with network policies
kubectl run test-pod --image=busybox -n <namespace> -it --rm -- wget -O- --timeout=2 http://<service>
```

---

## 10. Monitoring and Logging

### Log Collection
```bash
# Get logs from pod
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl logs <pod-name> -n <namespace> --since=1h
kubectl logs <pod-name> -n <namespace> --previous

# Follow logs
kubectl logs -f <pod-name> -n <namespace>

# Logs from all containers in pod
kubectl logs <pod-name> -n <namespace> --all-containers=true

# Logs from specific container
kubectl logs <pod-name> -c <container-name> -n <namespace>

# Logs from multiple pods
kubectl logs -l app=myapp -n <namespace>

# Stream logs from all pods with label
kubectl logs -f -l app=myapp --all-containers=true -n <namespace>
```

### Events
```bash
# Get all events
kubectl get events -A --sort-by='.lastTimestamp'

# Get events for specific namespace
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Watch events
kubectl get events -n <namespace> --watch

# Get events for specific resource
kubectl get events --field-selector involvedObject.name=<pod-name> -n <namespace>

# Get warning events only
kubectl get events -n <namespace> --field-selector type=Warning
```

### Prometheus and Grafana
```bash
# Check Prometheus
kubectl get pods -n monitoring -l app=prometheus

# Port forward to Prometheus
kubectl port-forward -n monitoring svc/prometheus-k8s 9090:9090

# Port forward to Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000

# Check ServiceMonitor resources
kubectl get servicemonitor -n monitoring
```

### Cluster Auditing
```bash
# Check audit logs location
ps aux | grep kube-apiserver | grep audit

# View audit logs
tail -f /var/log/kubernetes/audit/audit.log

# Parse audit logs for specific user
cat /var/log/kubernetes/audit/audit.log | jq 'select(.user.username == "john")'

# Parse audit logs for specific resource
cat /var/log/kubernetes/audit/audit.log | jq 'select(.objectRef.resource == "secrets")'
```

---

## 11. Common Error Messages and Solutions

### Error: "Unable to connect to the server"
```bash
# Check if API server is running
kubectl get nodes
curl -k https://<api-server>:6443/healthz

# Verify kubeconfig
kubectl config view
export KUBECONFIG=~/.kube/config

# Check network connectivity
ping <api-server-ip>
telnet <api-server-ip> 6443

# Restart kubelet
systemctl restart kubelet
```

### Error: "The connection to the server was refused"
```bash
# Check if API server is running
systemctl status kube-apiserver
kubectl get pods -n kube-system | grep apiserver

# Check API server logs
journalctl -u kube-apiserver -f
kubectl logs -n kube-system kube-apiserver-<master>

# Verify certificates
ls -la /etc/kubernetes/pki/
```

### Error: "error: You must be logged in to the server (Unauthorized)"
```bash
# Check current context
kubectl config current-context
kubectl config get-contexts

# Verify credentials
kubectl config view --raw

# Use correct context
kubectl config use-context <context-name>

# Get token for service account
kubectl create token <service-account> -n <namespace>
```

### Error: "Insufficient CPU/Memory"
```bash
# Check node resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# Scale down or delete unused pods
kubectl scale deployment <deployment> --replicas=1 -n <namespace>

# Adjust resource requests
kubectl set resources deployment <deployment> \
  --requests=cpu=100m,memory=128Mi \
  -n <namespace>

# Add more nodes to cluster
```

### Error: "FailedScheduling"
```bash
# Check scheduler logs
kubectl logs -n kube-system kube-scheduler-<master>

# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Common causes:
# 1. No nodes available - check node status
kubectl get nodes

# 2. Resource constraints - check resources
kubectl describe nodes

# 3. Taints and tolerations - verify
kubectl describe nodes | grep Taints

# 4. Node selector - check labels
kubectl get nodes --show-labels
```

### Error: "ErrImageNeverPull"
```bash
# Change imagePullPolicy
kubectl patch deployment <deployment> -n <namespace> \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","imagePullPolicy":"Always"}]}}}}'

# Or edit deployment
kubectl edit deployment <deployment> -n <namespace>
# Change imagePullPolicy to Always or IfNotPresent
```

### Error: "BackOff restarting failed container"
```bash
# Check container logs
kubectl logs <pod-name> -n <namespace> --previous

# Check container command
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].command}'

# Verify entrypoint
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 Command
```

---

## Advanced Troubleshooting Techniques

### Debug Running Pods
```bash
# Create debug container in running pod (Kubernetes 1.23+)
kubectl debug <pod-name> -n <namespace> -it --image=busybox

# Debug with ephemeral container
kubectl debug <pod-name> -n <namespace> -it --image=nicolaka/netshoot --target=<container-name>

# Copy pod for debugging
kubectl debug <pod-name> -n <namespace> --copy-to=<debug-pod-name> --share-processes
```

### Network Debugging
```bash
# Create netshoot pod for network debugging
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- bash

# DNS debugging
kubectl run dnsutils --image=tutum/dnsutils -it --rm -- bash
nslookup kubernetes.default
nslookup <service-name>.<namespace>.svc.cluster.local

# Test service connectivity
kubectl run curl --image=curlimages/curl -it --rm -- sh
curl http://<service-name>.<namespace>.svc.cluster.local:<port>
```

### Performance Profiling
```bash
# Enable CPU profiling for API server
kubectl get --raw /debug/pprof/profile?seconds=30 > cpu-profile.prof

# Get heap profile
kubectl get --raw /debug/pprof/heap > heap-profile.prof

# Analyze with pprof
go tool pprof cpu-profile.prof
```

### Backup and Recovery
```bash
# Backup etcd
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Restore etcd
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db

# Backup all resources
kubectl get all --all-namespaces -o yaml > all-resources-backup.yaml

# Backup specific namespace
kubectl get all -n <namespace> -o yaml > namespace-backup.yaml
```

---

## Useful kubectl Plugins and Tools

### krew (kubectl plugin manager)
```bash
# Install krew
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)

# Useful plugins
kubectl krew install ctx      # Switch contexts
kubectl krew install ns       # Switch namespaces
kubectl krew install tail     # Tail logs from multiple pods
kubectl krew install tree     # Show resource hierarchy
kubectl krew install neat     # Clean up kubectl output
kubectl krew install resource-capacity  # Show resource usage
```

### kubectx and kubens
```bash
# Switch contexts
kubectx                    # List contexts
kubectx <context-name>     # Switch context

# Switch namespaces
kubens                     # List namespaces
kubens <namespace>         # Switch namespace
```

### stern (Multi-pod log tailing)
```bash
# Install stern
brew install stern  # macOS
# or download from https://github.com/stern/stern

# Tail logs from multiple pods
stern <pod-query> -n <namespace>
stern . -n <namespace>                    # All pods
stern ^my-pod -n <namespace>              # Regex match
stern --selector app=myapp -n <namespace> # By label
```

### k9s (Terminal UI)
```bash
# Install k9s
brew install k9s  # macOS
# or download from https://github.com/derailed/k9s

# Run k9s
k9s
```

---

## Best Practices for Troubleshooting

### 1. Systematic Approach
- Start from top (cluster) to bottom (container)
- Check logs before making changes
- Document your findings
- Use labels and annotations for organization

### 2. Logging Best Practices
- Use structured logging (JSON)
- Include correlation IDs
- Log at appropriate levels
- Rotate logs to prevent disk issues

### 3. Monitoring Best Practices
- Set up alerts for critical metrics
- Monitor resource usage trends
- Use dashboards for visualization
- Implement health checks

### 4. Automation Best Practices
- Use CI/CD pipelines for deployments
- Implement GitOps workflows
- Automate routine tasks
- Use configuration management

### 5. Security Best Practices
- Follow principle of least privilege
- Use RBAC effectively
- Scan images for vulnerabilities
- Encrypt secrets at rest
- Use network policies

---

## Quick Reference Commands

```bash
# Cluster information
kubectl cluster-info
kubectl get nodes
kubectl get componentstatuses

# Pod debugging
kubectl get pods -A
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- /bin/bash

# Service and networking
kubectl get svc
kubectl get endpoints
kubectl get ingress
kubectl get networkpolicy

# Resource usage
kubectl top nodes
kubectl top pods -A

# Events and logs
kubectl get events --sort-by='.lastTimestamp'
kubectl logs -f <pod-name>

# Configuration
kubectl get configmap
kubectl get secrets
kubectl get pv,pvc

# Workload management
kubectl get deployments
kubectl get statefulsets
kubectl get daemonsets
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>

# RBAC
kubectl get roles,rolebindings
kubectl get clusterroles,clusterrolebindings
kubectl auth can-i <verb> <resource>

# Apply and manage resources
kubectl apply -f <file>
kubectl delete -f <file>
kubectl diff -f <file>
kubectl patch <resource> <name> -p '<json-patch>'
```

---

## Conclusion

This guide covers comprehensive troubleshooting scenarios for Kubernetes environments. Remember to:
- Always check logs and events first
- Use describe commands to get detailed information
- Test changes in non-production environments
- Keep your cluster and tools updated
- Document your solutions for future reference

For more information, refer to:
- Official Kubernetes documentation: https://kubernetes.io/docs/
- kubectl cheat sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- Kubernetes GitHub: https://github.com/kubernetes/kubernetes
