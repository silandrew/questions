# Problem-Solving and Troubleshooting Skills in Complex Automation Scenarios

## Table of Contents
1. [Core Problem-Solving Methodology](#core-problem-solving-methodology)
2. [Systematic Troubleshooting Approach](#systematic-troubleshooting-approach)
3. [Complex Automation Scenarios](#complex-automation-scenarios)
4. [Debugging Techniques](#debugging-techniques)
5. [Root Cause Analysis](#root-cause-analysis)
6. [Performance Optimization](#performance-optimization)
7. [Resilience and Recovery](#resilience-and-recovery)
8. [Real-World Examples](#real-world-examples)

---

## Core Problem-Solving Methodology

### 1. Structured Problem-Solving Framework

#### The 5-Step Approach
1. **Define the Problem**
   - Identify symptoms vs. root causes
   - Gather initial data and logs
   - Document the expected vs. actual behavior
   - Determine scope and impact

2. **Analyze the Situation**
   - Break down complex systems into components
   - Identify dependencies and relationships
   - Review recent changes and deployments
   - Check monitoring and alerting data

3. **Generate Hypotheses**
   - Create multiple possible explanations
   - Prioritize based on likelihood and impact
   - Consider both technical and process issues
   - Review similar past incidents

4. **Test and Validate**
   - Design experiments to test hypotheses
   - Isolate variables systematically
   - Use controlled environments when possible
   - Document all findings

5. **Implement and Monitor**
   - Apply the solution incrementally
   - Validate the fix in non-production first
   - Monitor key metrics post-deployment
   - Document the resolution for future reference

### 2. Critical Thinking Skills

#### Pattern Recognition
- Identify recurring issues across different systems
- Recognize similar failure patterns from past experiences
- Correlate events across multiple logs and data sources
- Spot anomalies in system behavior early

#### Systems Thinking
- Understand interconnections between components
- Consider cascading effects of changes
- Map data flow and control flow through pipelines
- Anticipate side effects and edge cases

#### Analytical Decomposition
- Break down monolithic problems into manageable parts
- Isolate specific components for testing
- Use divide-and-conquer strategies
- Create mental models of system architecture

---

## Systematic Troubleshooting Approach

### 1. Initial Assessment

#### Gathering Context
```bash
# Quick system health check
kubectl get nodes
kubectl get pods --all-namespaces | grep -v Running
kubectl top nodes
kubectl top pods -A

# Check recent events
kubectl get events --sort-by='.lastTimestamp' -A | tail -50

# Review recent deployments
kubectl get deployments -A -o wide
kubectl rollout history deployment/<deployment-name> -n <namespace>
```

#### Understanding the Baseline
- What is the normal behavior?
- What changed recently?
- When did the problem start?
- Who is affected and to what extent?

### 2. Log Analysis Strategy

#### Centralized Logging
```bash
# Kubernetes logs
kubectl logs <pod-name> -n <namespace> --previous
kubectl logs <pod-name> -n <namespace> --since=1h --timestamps

# Filter and pattern matching
kubectl logs <pod-name> -n <namespace> | grep -i error
kubectl logs <pod-name> -n <namespace> | grep -E "exception|failed|timeout"

# Multi-container pods
kubectl logs <pod-name> -n <namespace> -c <container-name>
```

#### Log Correlation Techniques
- Correlate timestamps across different services
- Use request IDs or trace IDs to follow transactions
- Identify patterns in error frequencies
- Compare logs before and after incidents

### 3. Network Troubleshooting

#### Connectivity Issues
```bash
# Test DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default

# Test service connectivity
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- /bin/bash
# Inside the container:
curl -v http://service-name.namespace.svc.cluster.local:port
nc -zv service-name.namespace.svc.cluster.local port

# Check network policies
kubectl get networkpolicies -A
kubectl describe networkpolicy <policy-name> -n <namespace>

# Verify service endpoints
kubectl get endpoints <service-name> -n <namespace>
```

#### Common Network Issues
- Service selector mismatches
- Network policy blocking traffic
- DNS resolution failures
- Ingress/LoadBalancer misconfigurations
- Certificate issues (TLS/SSL)

### 4. Resource Constraints

#### Memory and CPU Issues
```bash
# Check resource usage
kubectl top pods -n <namespace> --sort-by=memory
kubectl top pods -n <namespace> --sort-by=cpu

# Describe pod for resource limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Limits\|Requests"

# Check node resources
kubectl describe node <node-name> | grep -A 10 "Allocated resources"

# OOMKilled pods
kubectl get pods -A -o json | jq '.items[] | select(.status.containerStatuses != null) | select(.status.containerStatuses[].lastState.terminated.reason == "OOMKilled") | {name: .metadata.name, namespace: .metadata.namespace}'
```

### 5. Configuration Management

#### ConfigMap and Secret Verification
```bash
# Verify ConfigMaps
kubectl get configmap <configmap-name> -n <namespace> -o yaml
kubectl describe configmap <configmap-name> -n <namespace>

# Check Secrets
kubectl get secret <secret-name> -n <namespace> -o yaml
kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.data}'

# Validate environment variables in pods
kubectl exec <pod-name> -n <namespace> -- env | sort
kubectl exec <pod-name> -n <namespace> -- cat /path/to/config/file
```

---

## Complex Automation Scenarios

### 1. CI/CD Pipeline Failures

#### Scenario: Intermittent Build Failures

**Problem**: Pipeline fails randomly at different stages

**Troubleshooting Steps**:

1. **Collect Data**
```yaml
# Jenkins Pipeline Debug
pipeline {
    agent any
    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }
    stages {
        stage('Debug Info') {
            steps {
                sh '''
                    echo "=== Environment Variables ==="
                    env | sort
                    echo "=== System Resources ==="
                    df -h
                    free -m
                    echo "=== Network Connectivity ==="
                    ping -c 3 github.com
                    echo "=== Docker Info ==="
                    docker info
                    docker ps
                '''
            }
        }
    }
}
```

2. **Identify Patterns**
- Check failure frequency and timing
- Review resource utilization during failures
- Examine external dependencies (registry, Git, artifacts)
- Compare successful vs. failed build logs

3. **Common Root Causes**
- **Race conditions**: Parallel job conflicts
- **Resource exhaustion**: Disk space, memory, file descriptors
- **Network instability**: Timeout issues with external services
- **Dependency conflicts**: Version mismatches, cache corruption
- **Credential expiration**: Token or certificate timeouts

4. **Solutions**
```yaml
# Add retries for transient failures
steps {
    retry(3) {
        sh 'docker pull myimage:latest'
    }
}

# Add timeout to prevent hanging
timeout(time: 10, unit: 'MINUTES') {
    sh 'npm install'
}

# Lock resources to prevent conflicts
lock(resource: 'deployment', inversePrecedence: true) {
    sh 'kubectl apply -f deployment.yaml'
}

# Clean workspace to prevent cache issues
cleanWs()
```

### 2. Kubernetes Deployment Issues

#### Scenario: Pods Not Starting After Deployment

**Systematic Diagnosis**:

```bash
# 1. Check deployment status
kubectl get deployment <name> -n <namespace>
kubectl rollout status deployment/<name> -n <namespace>

# 2. Examine pod status
kubectl get pods -n <namespace> -l app=<label>
kubectl describe pod <pod-name> -n <namespace>

# 3. Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# 4. Review logs
kubectl logs <pod-name> -n <namespace> --all-containers=true
```

**Common Issues and Solutions**:

1. **ImagePullBackOff**
```yaml
# Check image pull secrets
kubectl get secrets -n <namespace>
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Events"

# Verify image exists
docker pull <image:tag>

# Solution: Correct image name or add pull secret
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  -n <namespace>
```

2. **CrashLoopBackOff**
```bash
# Check application logs
kubectl logs <pod-name> -n <namespace> --previous

# Common causes:
# - Missing environment variables
# - Configuration errors
# - Dependency unavailable
# - Port conflicts
# - Permission issues

# Debug with interactive shell
kubectl run -it debug --image=<same-image> --restart=Never -- /bin/sh
```

3. **Pending State**
```bash
# Check node resources
kubectl describe node | grep -A 5 "Allocated resources"

# Check PersistentVolumeClaims
kubectl get pvc -n <namespace>

# Check taints and tolerations
kubectl describe node <node-name> | grep Taints
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 tolerations
```

### 3. Terraform State Issues

#### Scenario: State File Corruption or Conflicts

**Problem Detection**:
```bash
# Check state file integrity
terraform state list
terraform state show <resource>

# Identify drift
terraform plan -refresh-only

# Check for locks
terraform force-unlock <lock-id>
```

**Resolution Strategies**:

1. **State Backup and Recovery**
```bash
# Manual backup
cp terraform.tfstate terraform.tfstate.backup

# Use state backups (S3 example)
aws s3 ls s3://my-terraform-state-bucket/env:/prod/

# Restore from backup
aws s3 cp s3://my-terraform-state-bucket/env:/prod/terraform.tfstate.backup terraform.tfstate
```

2. **Fixing State Drift**
```bash
# Import existing resources
terraform import aws_instance.example i-1234567890abcdef0

# Remove orphaned resources
terraform state rm aws_instance.old_instance

# Move resources between modules
terraform state mv module.old.aws_instance.example module.new.aws_instance.example

# Replace tainted resources
terraform taint aws_instance.example
terraform apply
```

3. **Handling Concurrent Modifications**
```hcl
# Use state locking (DynamoDB for S3 backend)
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### 4. Ansible Playbook Failures

#### Scenario: Tasks Failing Across Multiple Hosts

**Debugging Approach**:

```yaml
---
# Enable verbose output
ansible-playbook -vvv playbook.yml

# Run in check mode first
ansible-playbook --check playbook.yml

# Limit to specific hosts
ansible-playbook --limit host1,host2 playbook.yml

# Step through tasks interactively
ansible-playbook --step playbook.yml

# Start at specific task
ansible-playbook --start-at-task="Install packages" playbook.yml
```

**Enhanced Error Handling**:

```yaml
---
- name: Robust deployment playbook
  hosts: webservers
  gather_facts: yes
  
  tasks:
    - name: Check connectivity
      ping:
      register: ping_result
      ignore_errors: yes
      
    - name: Debug connectivity issues
      debug:
        msg: "Host {{ inventory_hostname }} is unreachable"
      when: ping_result is failed
      
    - name: Install package with retries
      package:
        name: nginx
        state: present
      register: result
      retries: 3
      delay: 5
      until: result is succeeded
      
    - name: Validate installation
      command: nginx -v
      register: nginx_version
      changed_when: false
      failed_when: nginx_version.rc != 0
      
    - name: Ensure service is running
      service:
        name: nginx
        state: started
        enabled: yes
      rescue:
        - name: Check service status
          command: systemctl status nginx
          register: service_status
          
        - name: Log failure details
          debug:
            msg: "Service failed: {{ service_status.stdout }}"
            
        - name: Rollback configuration
          copy:
            src: /etc/nginx/nginx.conf.backup
            dest: /etc/nginx/nginx.conf
            remote_src: yes
```

### 5. Multi-Cloud Deployment Challenges

#### Scenario: Cross-Cloud Networking Issues

**Problem**: Services in AWS cannot communicate with services in Azure

**Troubleshooting Framework**:

1. **Network Architecture Review**
```bash
# AWS side
aws ec2 describe-vpcs
aws ec2 describe-route-tables
aws ec2 describe-security-groups

# Azure side
az network vnet list
az network route-table list
az network nsg list

# Check VPN/Peering connections
aws ec2 describe-vpn-connections
az network vpn-connection list
```

2. **Connectivity Testing**
```bash
# Test from AWS to Azure
# In AWS EC2 instance:
ping <azure-vm-private-ip>
traceroute <azure-vm-private-ip>
nc -zv <azure-vm-private-ip> 443

# Check DNS resolution
nslookup <azure-service-endpoint>
dig <azure-service-endpoint>

# Test from Azure to AWS
# In Azure VM:
ping <aws-ec2-private-ip>
traceroute <aws-ec2-private-ip>
nc -zv <aws-ec2-private-ip> 443
```

3. **Common Issues**
- **CIDR overlap**: Overlapping IP ranges between clouds
- **Route table misconfigurations**: Missing or incorrect routes
- **Firewall rules**: Security groups/NSGs blocking traffic
- **MTU size issues**: Packet fragmentation problems
- **Asymmetric routing**: Return path differs from forward path

4. **Resolution Example**
```hcl
# Terraform: Configure VPN with proper routes
resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"
  static_routes_only  = true
  
  tags = {
    Name = "AWS-to-Azure-VPN"
  }
}

resource "aws_vpn_connection_route" "azure_network" {
  destination_cidr_block = "10.1.0.0/16"  # Azure VNET
  vpn_connection_id      = aws_vpn_connection.main.id
}

# Security group allowing Azure traffic
resource "aws_security_group_rule" "from_azure" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["10.1.0.0/16"]  # Azure VNET
  security_group_id = aws_security_group.main.id
}
```

---

## Debugging Techniques

### 1. Interactive Debugging

#### Kubernetes Debug Containers
```bash
# Ephemeral debug container (K8s 1.23+)
kubectl debug -it <pod-name> -n <namespace> --image=busybox --target=<container-name>

# Debug with different image
kubectl debug <pod-name> -n <namespace> --image=nicolaka/netshoot --share-processes --copy-to=<pod-name>-debug

# Debug node
kubectl debug node/<node-name> -it --image=ubuntu
```

#### Application-Level Debugging
```python
# Python: Remote debugging with debugpy
import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for debugger attach...")
debugpy.wait_for_client()

# Add to Kubernetes deployment
ports:
- containerPort: 5678
  name: debug
```

```javascript
// Node.js: Remote debugging
// Start with: node --inspect=0.0.0.0:9229 app.js

// In package.json
"scripts": {
  "debug": "node --inspect=0.0.0.0:9229 --inspect-brk app.js"
}
```

### 2. Tracing and Profiling

#### Distributed Tracing
```yaml
# OpenTelemetry instrumentation
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://jaeger-collector:4318"
        - name: OTEL_SERVICE_NAME
          value: "myapp"
        - name: OTEL_TRACES_EXPORTER
          value: "otlp"
```

#### Performance Profiling
```bash
# CPU profiling (Go application)
curl http://localhost:6060/debug/pprof/profile?seconds=30 > cpu.prof
go tool pprof cpu.prof

# Memory profiling
curl http://localhost:6060/debug/pprof/heap > heap.prof
go tool pprof heap.prof

# Continuous profiling
kubectl port-forward pod/<pod-name> 6060:6060
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/heap
```

### 3. Traffic Analysis

#### Network Packet Capture
```bash
# Capture traffic in Kubernetes
kubectl exec <pod-name> -n <namespace> -- tcpdump -i any -w /tmp/capture.pcap port 80

# Copy pcap file locally
kubectl cp <namespace>/<pod-name>:/tmp/capture.pcap ./capture.pcap

# Analyze with tshark
tshark -r capture.pcap -Y "http.request" -T fields -e http.request.method -e http.request.uri

# Filter specific traffic
tcpdump -i any -nn -A 'tcp port 443 and (tcp[tcpflags] & tcp-syn) != 0'
```

#### Service Mesh Observability
```bash
# Istio: Check traffic routing
istioctl analyze -n <namespace>
istioctl proxy-status
istioctl proxy-config routes <pod-name> -n <namespace>

# View Envoy configuration
kubectl exec <pod-name> -n <namespace> -c istio-proxy -- curl localhost:15000/config_dump

# Check metrics
kubectl exec <pod-name> -n <namespace> -c istio-proxy -- curl localhost:15000/stats/prometheus
```

---

## Root Cause Analysis

### 1. The 5 Whys Technique

#### Example: Service Downtime

**Problem**: Production API is returning 500 errors

1. **Why is the API returning 500 errors?**
   - The database connection pool is exhausted

2. **Why is the connection pool exhausted?**
   - Database queries are taking too long to complete

3. **Why are queries taking too long?**
   - A missing index on a frequently queried table

4. **Why is there a missing index?**
   - Recent schema migration didn't include index creation

5. **Why wasn't the index included?**
   - Migration review process didn't catch the performance impact

**Root Cause**: Inadequate migration review process
**Solution**: 
- Add index immediately
- Enhance migration review checklist
- Implement query performance testing in CI/CD

### 2. Fishbone Diagram Analysis

#### Categories to Consider

**People**
- Skills and training gaps
- Communication breakdowns
- Documentation inadequacy
- Team handoff issues

**Process**
- Insufficient testing
- Missing validation steps
- Inadequate monitoring
- Poor change management

**Technology**
- Infrastructure limitations
- Software bugs
- Configuration errors
- Dependency failures

**Environment**
- Resource constraints
- External service dependencies
- Network issues
- Security restrictions

### 3. Timeline Reconstruction

#### Building a Complete Picture

```bash
# Create incident timeline
# 1. Collect logs from all sources
kubectl logs --since-time="2024-10-18T10:00:00Z" --all-containers=true -n <namespace>

# 2. Aggregate events
kubectl get events --sort-by='.lastTimestamp' -A --since-time="2024-10-18T10:00:00Z"

# 3. Check deployment history
kubectl rollout history deployment/<name> -n <namespace>

# 4. Review infrastructure changes
git log --since="2024-10-18 10:00" --until="2024-10-18 12:00" --all --oneline

# 5. Check external dependencies
# Review cloud provider status pages
# Check third-party service incidents
# Review network connectivity logs
```

---

## Performance Optimization

### 1. Identifying Bottlenecks

#### Application Performance
```bash
# Monitor pod metrics
kubectl top pod -n <namespace> --sort-by=memory
kubectl top pod -n <namespace> --sort-by=cpu

# Application-specific metrics (Prometheus)
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Database query analysis
kubectl exec -it postgres-pod -n <namespace> -- psql -c "
SELECT 
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;"
```

#### Infrastructure Performance
```bash
# Disk I/O
kubectl exec <pod-name> -n <namespace> -- iostat -x 1 10

# Network throughput
kubectl exec <pod-name> -n <namespace> -- iperf3 -c <target-service>

# DNS resolution time
kubectl exec <pod-name> -n <namespace> -- time nslookup kubernetes.default
```

### 2. Optimization Strategies

#### Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
```

#### Caching Strategies
```yaml
# Redis cache deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        command:
        - redis-server
        - --maxmemory 256mb
        - --maxmemory-policy allkeys-lru
        - --save ""
        - --appendonly no
```

#### Database Optimization
```sql
-- Index optimization
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- Query optimization
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id, u.name;

-- Connection pooling configuration (PostgreSQL)
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET effective_cache_size = '6GB';
ALTER SYSTEM SET work_mem = '16MB';
```

---

## Resilience and Recovery

### 1. Circuit Breaker Pattern

#### Implementation Example
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30, expected_exception=RequestException)
def call_external_service(url, data):
    """
    Circuit breaker protects against cascading failures
    - Opens after 5 consecutive failures
    - Stays open for 30 seconds (recovery timeout)
    - Automatically closes when service recovers
    """
    response = requests.post(url, json=data, timeout=5)
    response.raise_for_status()
    return response.json()

# Usage with fallback
def process_order(order_data):
    try:
        result = call_external_service("https://payment-api/process", order_data)
        return result
    except CircuitBreakerError:
        logger.error("Payment service circuit breaker open, using fallback")
        # Queue for later processing
        queue_for_retry(order_data)
        return {"status": "queued", "message": "Payment service temporarily unavailable"}
```

### 2. Retry Logic with Exponential Backoff

```python
import time
from functools import wraps

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise
                    
                    wait = (backoff_in_seconds * 2 ** x)
                    logger.warning(f"Attempt {x + 1} failed: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                    x += 1
        return wrapper
    return decorator

@retry_with_backoff(retries=5, backoff_in_seconds=2)
def fetch_data_from_api(endpoint):
    response = requests.get(endpoint, timeout=10)
    response.raise_for_status()
    return response.json()
```

### 3. Graceful Degradation

```yaml
# Feature flags for gradual rollout
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  new_payment_provider: "false"
  enhanced_search: "true"
  ai_recommendations: "20"  # 20% of users
```

```python
# Application code
def get_recommendations(user_id):
    rollout_percentage = int(config.get("ai_recommendations", "0"))
    
    if hash(user_id) % 100 < rollout_percentage:
        try:
            # New AI-based recommendations
            return ai_service.get_recommendations(user_id, timeout=2)
        except Exception as e:
            logger.error(f"AI recommendations failed: {e}, falling back")
            # Fallback to traditional method
            return traditional_recommendations(user_id)
    else:
        return traditional_recommendations(user_id)
```

### 4. Automated Rollback

```yaml
# Progressive delivery with Argo Rollouts
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 5m}
      - setWeight: 40
      - pause: {duration: 5m}
      - setWeight: 60
      - pause: {duration: 5m}
      - setWeight: 80
      - pause: {duration: 5m}
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 2
        args:
        - name: service-name
          value: myapp
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v2
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 1m
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(
            http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]
          )) / 
          sum(rate(
            http_requests_total{service="{{args.service-name}}"}[5m]
          ))
```

---

## Real-World Examples

### Example 1: Memory Leak Investigation

#### Problem
Application pods gradually consuming more memory and eventually getting OOMKilled

#### Investigation Process

```bash
# 1. Confirm the issue
kubectl get pods -n production | grep OOMKilled
kubectl describe pod <pod-name> -n production | grep -A 5 "Last State"

# 2. Check memory trends
kubectl top pod -n production --sort-by=memory

# 3. Enable memory profiling
# Add to deployment:
env:
- name: NODE_OPTIONS
  value: "--max-old-space-size=2048 --expose-gc"
ports:
- containerPort: 9229
  name: debug
```

```javascript
// Add heap dump capability
const v8 = require('v8');
const fs = require('fs');

app.get('/heapdump', (req, res) => {
  const filename = `/tmp/heapdump-${Date.now()}.heapsnapshot`;
  const heapSnapshot = v8.writeHeapSnapshot(filename);
  res.download(heapSnapshot);
});

// Monitor memory usage
setInterval(() => {
  const used = process.memoryUsage();
  console.log(JSON.stringify({
    rss: `${Math.round(used.rss / 1024 / 1024)} MB`,
    heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)} MB`,
    heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)} MB`,
    external: `${Math.round(used.external / 1024 / 1024)} MB`,
  }));
}, 60000);
```

#### Root Cause Found
Event listeners not being removed, causing memory accumulation

#### Solution
```javascript
// Before (memory leak)
function setupWebSocket() {
  const ws = new WebSocket('wss://api.example.com');
  ws.addEventListener('message', handleMessage);
  return ws;
}

// After (fixed)
class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.handleMessage = this.handleMessage.bind(this);
  }
  
  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.addEventListener('message', this.handleMessage);
  }
  
  disconnect() {
    if (this.ws) {
      this.ws.removeEventListener('message', this.handleMessage);
      this.ws.close();
      this.ws = null;
    }
  }
  
  handleMessage(event) {
    // Process message
  }
}
```

### Example 2: Database Connection Pool Exhaustion

#### Problem
Application intermittently returns "Too many connections" errors

#### Investigation

```bash
# 1. Check database connections
kubectl exec -it postgres-0 -n production -- psql -c "
SELECT 
  state,
  COUNT(*) as connections,
  MAX(NOW() - state_change) as oldest
FROM pg_stat_activity
GROUP BY state;"

# 2. Identify long-running queries
kubectl exec -it postgres-0 -n production -- psql -c "
SELECT 
  pid,
  now() - pg_stat_activity.query_start AS duration,
  query,
  state
FROM pg_stat_activity
WHERE state != 'idle'
  AND (now() - pg_stat_activity.query_start) > interval '5 minutes'
ORDER BY duration DESC;"

# 3. Check connection pool settings
kubectl get configmap app-config -n production -o yaml | grep -A 10 database
```

#### Root Causes Identified
1. Connection pool too small for traffic volume
2. Connections not being released properly after errors
3. No connection timeout configured

#### Solutions

```python
# 1. Proper connection pool configuration
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,              # Base connections
    max_overflow=10,           # Additional connections under load
    pool_timeout=30,           # Wait for connection
    pool_recycle=3600,         # Recycle connections every hour
    pool_pre_ping=True,        # Verify connections before use
    echo_pool=True             # Log pool events
)

# 2. Context manager for proper cleanup
from contextlib import contextmanager

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()  # Always release connection

# Usage
with get_db_session() as session:
    user = session.query(User).filter_by(id=user_id).first()
    # Connection automatically released

# 3. Monitor connection usage
from prometheus_client import Gauge

db_connections_active = Gauge('db_connections_active', 'Active database connections')
db_connections_idle = Gauge('db_connections_idle', 'Idle database connections')

def update_connection_metrics():
    pool = engine.pool
    db_connections_active.set(pool.size() - pool.overflow())
    db_connections_idle.set(pool.overflow())
```

### Example 3: Kubernetes DNS Resolution Delays

#### Problem
Intermittent 5-second delays in service-to-service communication

#### Investigation

```bash
# 1. Measure DNS resolution time
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- /bin/bash
# Inside container:
for i in {1..10}; do
  time nslookup my-service.production.svc.cluster.local
done

# 2. Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100

# 3. Check CoreDNS configuration
kubectl get configmap coredns -n kube-system -o yaml

# 4. Examine network policies
kubectl get networkpolicies -A

# 5. Check DNS pod resources
kubectl top pod -n kube-system -l k8s-app=kube-dns
```

#### Root Cause
Alpine-based images experiencing DNS resolution issues due to musl libc bug with ndots

#### Solution

```yaml
# 1. Adjust DNS policy in pod spec
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      dnsPolicy: ClusterFirst
      dnsConfig:
        options:
        - name: ndots
          value: "1"  # Reduce from default 5
        - name: timeout
          value: "2"
        - name: attempts
          value: "2"
        - name: single-request-reopen
      containers:
      - name: myapp
        image: myapp:latest

# 2. Use fully qualified domain names
# Instead of: http://my-service
# Use: http://my-service.production.svc.cluster.local

# 3. Scale CoreDNS for higher throughput
kubectl scale deployment coredns -n kube-system --replicas=3

# 4. Enable DNS caching in application
```

```python
# Application-level DNS cache
import socket
from functools import lru_cache
import time

class DNSCache:
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.cache = {}
    
    def resolve(self, hostname):
        now = time.time()
        if hostname in self.cache:
            ip, timestamp = self.cache[hostname]
            if now - timestamp < self.ttl:
                return ip
        
        ip = socket.gethostbyname(hostname)
        self.cache[hostname] = (ip, now)
        return ip

dns_cache = DNSCache(ttl=300)

# Use cached resolution
def make_request(service_name):
    ip = dns_cache.resolve(f"{service_name}.production.svc.cluster.local")
    url = f"http://{ip}:8080/api/endpoint"
    response = requests.get(url, headers={"Host": service_name})
    return response.json()
```

### Example 4: Terraform Deadlock in CI/CD

#### Problem
Terraform apply jobs timing out and blocking each other

#### Investigation

```bash
# 1. Check for state locks
terraform force-unlock -force <lock-id>

# 2. Query DynamoDB lock table
aws dynamodb scan --table-name terraform-state-lock

# 3. Check CI/CD job history
# Review Jenkins/GitLab job logs for patterns

# 4. Identify concurrent jobs
# Check timestamps of failed jobs
```

#### Root Causes
1. Multiple pipelines modifying shared infrastructure
2. Jobs not releasing locks on failure
3. No job queuing mechanism

#### Solutions

```yaml
# 1. Implement job queuing in GitLab CI
terraform-apply:
  stage: deploy
  resource_group: production-infrastructure  # Only one job at a time
  script:
    - terraform init
    - terraform apply -auto-approve
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  timeout: 30m

# 2. Automated lock cleanup
stages:
  - pre-deploy
  - deploy
  - post-deploy

cleanup-stale-locks:
  stage: pre-deploy
  script:
    - |
      # Remove locks older than 1 hour
      LOCK_AGE_THRESHOLD=3600
      CURRENT_TIME=$(date +%s)
      
      aws dynamodb scan --table-name terraform-state-lock \
        --output json | jq -r '.Items[].LockID.S' | while read lock_id; do
        
        LOCK_INFO=$(aws dynamodb get-item \
          --table-name terraform-state-lock \
          --key "{\"LockID\": {\"S\": \"$lock_id\"}}")
        
        CREATED=$(echo $LOCK_INFO | jq -r '.Item.Created.S')
        CREATED_EPOCH=$(date -d "$CREATED" +%s)
        AGE=$((CURRENT_TIME - CREATED_EPOCH))
        
        if [ $AGE -gt $LOCK_AGE_THRESHOLD ]; then
          echo "Removing stale lock: $lock_id (age: ${AGE}s)"
          terraform force-unlock -force $lock_id
        fi
      done
  when: always
```

```hcl
# 3. Workspace isolation
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "${var.environment}/${var.component}/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Workspace-specific locking
    workspace_key_prefix = "workspaces"
  }
}

# 4. Partial apply for reduced blast radius
# Instead of applying everything at once:
terraform apply -target=module.networking
terraform apply -target=module.compute
terraform apply -target=module.database
```

---

## Key Takeaways

### Problem-Solving Mindset
1. **Stay Calm**: Panic leads to mistakes
2. **Be Systematic**: Follow a methodical approach
3. **Document Everything**: Logs, steps, findings
4. **Think Incrementally**: Small changes, validate each step
5. **Learn from Failures**: Post-mortems and retrospectives

### Troubleshooting Best Practices
1. **Gather Context First**: Don't jump to solutions
2. **Reproduce the Issue**: Understand the conditions
3. **Isolate Variables**: Test one thing at a time
4. **Use Version Control**: Know what changed and when
5. **Monitor Everything**: Logs, metrics, traces

### Automation Excellence
1. **Idempotency**: Scripts should be safely re-runnable
2. **Error Handling**: Anticipate and handle failures gracefully
3. **Logging**: Comprehensive but meaningful logs
4. **Testing**: Test automation code like application code
5. **Documentation**: README files, inline comments, runbooks

### Continuous Improvement
1. **Postmortems**: Learn from incidents without blame
2. **Metrics**: Measure MTTR, MTBF, success rates
3. **Knowledge Sharing**: Document solutions, conduct training
4. **Tooling**: Invest in better observability and automation
5. **Feedback Loops**: Continuously refine processes

---

## Additional Resources

### Tools for Troubleshooting
- **Observability**: Prometheus, Grafana, Jaeger, ELK Stack
- **Debugging**: kubectl debug, telepresence, skaffold
- **Network**: Wireshark, tcpdump, netshoot container
- **Performance**: pprof, flamegraphs, k6, Apache Bench
- **Chaos Engineering**: Chaos Mesh, Litmus Chaos, Gremlin

### Learning Resources
- "The Site Reliability Workbook" by Google
- "Troubleshooting Kubernetes" by James Turnbull
- "Database Reliability Engineering" by Laine Campbell
- Kubernetes troubleshooting documentation
- Cloud provider troubleshooting guides
