# Azure Services and DevOps Guide

## Table of Contents
1. [Azure DevOps Services](#azure-devops-services)
2. [Infrastructure as Code](#infrastructure-as-code)
3. [Azure CLI](#azure-cli)
4. [Monitoring and Observability](#monitoring-and-observability)
5. [Security Services](#security-services)
6. [Cost Management](#cost-management)
7. [Log Flow Architecture: Azure to Datadog](#log-flow-architecture)

---

## Azure DevOps Services

Azure DevOps is a comprehensive suite of development tools for planning, developing, delivering, and maintaining software.

### Key Components:

#### 1. **Azure Boards**
- Agile planning tools
- Work item tracking (User Stories, Bugs, Tasks)
- Kanban boards and Sprint planning
- Backlogs and roadmaps

#### 2. **Azure Repos**
- Git repositories (distributed version control)
- TFVC (Team Foundation Version Control)
- Pull request workflows
- Branch policies and code reviews

#### 3. **Azure Pipelines**
- CI/CD automation
- Multi-stage pipelines (YAML or Classic)
- Build and release automation
- Integration with multiple platforms (Linux, Windows, macOS)
- Container and Kubernetes deployment support

**Example Pipeline Structure:**
```yaml
trigger:
  branches:
    include:
    - main
    - develop

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - task: Docker@2
      inputs:
        command: 'build'
        Dockerfile: '**/Dockerfile'
        tags: '$(Build.BuildId)'

- stage: Deploy
  dependsOn: Build
  jobs:
  - deployment: DeployToAKS
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            inputs:
              action: 'deploy'
              manifests: 'k8s/*.yaml'
```

#### 4. **Azure Test Plans**
- Manual and exploratory testing
- Test case management
- Automated test execution

#### 5. **Azure Artifacts**
- Package management (NuGet, npm, Maven, Python)
- Universal packages
- Upstream sources and caching

---

## Infrastructure as Code

### Azure Resource Manager (ARM) Templates

ARM templates are JSON files that define infrastructure and configuration for Azure resources declaratively.

#### Key Concepts:
- **Declarative syntax**: Define "what" you want, not "how" to create it
- **Idempotent**: Can be run multiple times with same result
- **Modular**: Use linked templates and parameters
- **Validation**: Built-in validation before deployment

**Example ARM Template:**
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "vmName": {
      "type": "string",
      "metadata": {
        "description": "Name of the virtual machine"
      }
    },
    "adminUsername": {
      "type": "string"
    },
    "adminPassword": {
      "type": "securestring"
    }
  },
  "variables": {
    "nicName": "[concat(parameters('vmName'), '-nic')]",
    "vnetName": "[concat(parameters('vmName'), '-vnet')]"
  },
  "resources": [
    {
      "type": "Microsoft.Network/virtualNetworks",
      "apiVersion": "2021-02-01",
      "name": "[variables('vnetName')]",
      "location": "[resourceGroup().location]",
      "properties": {
        "addressSpace": {
          "addressPrefixes": ["10.0.0.0/16"]
        },
        "subnets": [
          {
            "name": "default",
            "properties": {
              "addressPrefix": "10.0.0.0/24"
            }
          }
        ]
      }
    }
  ],
  "outputs": {
    "vnetId": {
      "type": "string",
      "value": "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]"
    }
  }
}
```

#### Deployment via Azure DevOps Pipeline:
```yaml
- task: AzureResourceManagerTemplateDeployment@3
  inputs:
    deploymentScope: 'Resource Group'
    azureResourceManagerConnection: 'Azure-Service-Connection'
    subscriptionId: '$(subscriptionId)'
    action: 'Create Or Update Resource Group'
    resourceGroupName: '$(resourceGroupName)'
    location: 'East US'
    templateLocation: 'Linked artifact'
    csmFile: '$(Build.SourcesDirectory)/arm-templates/main.json'
    csmParametersFile: '$(Build.SourcesDirectory)/arm-templates/parameters.json'
    deploymentMode: 'Incremental'
```

### Alternative IaC Tools:
- **Terraform** (multi-cloud support)
- **Bicep** (DSL for ARM templates, more readable)
- **Pulumi** (programmatic IaC)

---

## Azure CLI

The Azure CLI is a cross-platform command-line tool to manage Azure resources.

### Key Use Cases:

#### 1. **Authentication**
```bash
# Login interactively
az login

# Login with service principal
az login --service-principal \
  --username $APP_ID \
  --password $PASSWORD \
  --tenant $TENANT_ID

# Set subscription
az account set --subscription "Subscription Name"
```

#### 2. **Resource Group Management**
```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# List resource groups
az group list --output table

# Delete resource group
az group delete --name myResourceGroup --yes --no-wait
```

#### 3. **VM Management**
```bash
# Create VM
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_DS2_v2

# Start/Stop VM
az vm start --resource-group myResourceGroup --name myVM
az vm stop --resource-group myResourceGroup --name myVM

# Get VM details
az vm show --resource-group myResourceGroup --name myVM --output json
```

#### 4. **Container Registry and AKS**
```bash
# Create container registry
az acr create --resource-group myResourceGroup \
  --name myContainerRegistry --sku Basic

# Build and push image
az acr build --registry myContainerRegistry \
  --image myapp:v1 .

# Create AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```

#### 5. **Automation in DevOps Pipeline**
```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: 'Azure-Service-Connection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      # Deploy application
      az webapp up --name myWebApp \
        --resource-group myResourceGroup \
        --runtime "PYTHON|3.9"
      
      # Configure app settings
      az webapp config appsettings set \
        --name myWebApp \
        --resource-group myResourceGroup \
        --settings KEY1=VALUE1 KEY2=VALUE2
```

---

## Monitoring and Observability

### Azure Monitor

Azure Monitor is a comprehensive monitoring solution for collecting, analyzing, and acting on telemetry data.

#### Components:

##### 1. **Metrics**
- Real-time numeric data
- Time-series database
- Auto-collected from Azure resources
- Custom metrics via Application Insights

##### 2. **Logs (Log Analytics)**
- Centralized log repository
- Kusto Query Language (KQL) for analysis
- Integration with multiple sources

**Example KQL Queries:**
```kql
// Find failed requests in last 24 hours
requests
| where timestamp > ago(24h)
| where success == false
| summarize count() by resultCode, bin(timestamp, 1h)
| render timechart

// Monitor CPU usage across VMs
Perf
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| where TimeGenerated > ago(1h)
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 5m)
| render timechart

// Application errors
exceptions
| where timestamp > ago(24h)
| summarize count() by type, outerMessage
| order by count_ desc
```

##### 3. **Alerts**
- Metric alerts (threshold-based)
- Log query alerts (KQL-based)
- Activity log alerts (Azure operations)
- Action groups (email, SMS, webhooks, Logic Apps)

**Alert Configuration Example:**
```json
{
  "name": "High CPU Alert",
  "condition": {
    "allOf": [
      {
        "metricName": "Percentage CPU",
        "operator": "GreaterThan",
        "threshold": 80,
        "timeAggregation": "Average"
      }
    ]
  },
  "actions": {
    "actionGroups": ["/subscriptions/.../actionGroups/DevOps-Team"]
  }
}
```

##### 4. **Workbooks**
- Interactive reporting
- Custom dashboards
- Parameterized queries

### Azure Application Insights

APM (Application Performance Management) service for web applications.

#### Key Features:

##### 1. **Automatic Instrumentation**
```csharp
// .NET Core example
public void ConfigureServices(IServiceCollection services)
{
    services.AddApplicationInsightsTelemetry();
}
```

```javascript
// Node.js example
const appInsights = require('applicationinsights');
appInsights.setup('YOUR_INSTRUMENTATION_KEY')
    .setAutoDependencyCorrelation(true)
    .setAutoCollectRequests(true)
    .setAutoCollectPerformance(true)
    .start();
```

##### 2. **Performance Monitoring**
- Request rates and response times
- Dependency tracking (DB, APIs, external services)
- Server metrics (CPU, memory, network)
- Browser page load times

##### 3. **Availability Testing**
- URL ping tests
- Multi-step web tests
- Track uptime and response times

##### 4. **Application Map**
- Visualize dependencies
- Identify bottlenecks
- Spot failures across components

##### 5. **Custom Telemetry**
```python
# Python example
from applicationinsights import TelemetryClient

tc = TelemetryClient('YOUR_INSTRUMENTATION_KEY')

# Track custom event
tc.track_event('UserLogin', {'userId': '12345', 'source': 'mobile'})

# Track metric
tc.track_metric('QueueLength', 42)

# Track trace
tc.track_trace('Processing order', severity='INFO')

tc.flush()
```

##### 6. **Smart Detection**
- Automatic anomaly detection
- Performance degradation alerts
- Memory leak detection
- Security anomalies

---

## Security Services

### Azure Key Vault

Secure storage for secrets, keys, and certificates.

#### Use Cases:

##### 1. **Secret Management**
```bash
# Create Key Vault
az keyvault create --name myKeyVault \
  --resource-group myResourceGroup \
  --location eastus

# Store secret
az keyvault secret set --vault-name myKeyVault \
  --name DatabasePassword \
  --value "SuperSecretPassword123!"

# Retrieve secret
az keyvault secret show --vault-name myKeyVault \
  --name DatabasePassword --query value -o tsv
```

##### 2. **Integration with Applications**
```csharp
// .NET example
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var client = new SecretClient(
    new Uri("https://mykeyvault.vault.azure.net/"),
    new DefaultAzureCredential()
);

KeyVaultSecret secret = await client.GetSecretAsync("DatabasePassword");
string password = secret.Value;
```

##### 3. **DevOps Pipeline Integration**
```yaml
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'Azure-Service-Connection'
    KeyVaultName: 'myKeyVault'
    SecretsFilter: '*'
    RunAsPreJob: true

- script: |
    echo "Using secret: $(DatabasePassword)"
  displayName: 'Deploy with secrets'
```

##### 4. **Certificate Management**
- SSL/TLS certificates
- Automatic renewal
- Integration with Azure services

##### 5. **Access Policies and RBAC**
```bash
# Grant access to service principal
az keyvault set-policy --name myKeyVault \
  --spn $APP_ID \
  --secret-permissions get list \
  --key-permissions get list \
  --certificate-permissions get list
```

### Azure Security Center (Microsoft Defender for Cloud)

Unified security management and threat protection.

#### Key Features:

##### 1. **Security Posture Management**
- Secure Score
- Recommendations for hardening
- Compliance dashboards (PCI-DSS, ISO, HIPAA)

##### 2. **Threat Protection**
- Advanced threat detection
- Behavioral analytics
- Machine learning-based anomaly detection
- Integration with Microsoft Threat Intelligence

##### 3. **Just-in-Time (JIT) VM Access**
```bash
# Enable JIT access
az security jit-policy create \
  --resource-group myResourceGroup \
  --location eastus \
  --name default \
  --virtual-machines "/subscriptions/.../myVM" \
  --ports '[{"number":22,"protocol":"TCP","allowedSourceAddressPrefix":"*","maxRequestAccessDuration":"PT3H"}]'
```

##### 4. **Vulnerability Assessment**
- Container image scanning
- SQL vulnerability assessment
- VM vulnerability scanning

##### 5. **Regulatory Compliance**
- Built-in compliance policies
- Continuous compliance assessment
- Audit reports

### Additional Security Services:

#### Azure Active Directory (Azure AD)
- Identity and access management
- Single sign-on (SSO)
- Multi-factor authentication (MFA)
- Conditional access policies

#### Azure Policy
- Enforce organizational standards
- Assess compliance at scale
- Remediation tasks

```json
{
  "if": {
    "allOf": [
      {
        "field": "type",
        "equals": "Microsoft.Compute/virtualMachines"
      },
      {
        "not": {
          "field": "Microsoft.Compute/virtualMachines/storageProfile.osDisk.managedDisk.storageAccountType",
          "in": ["Premium_LRS", "StandardSSD_LRS"]
        }
      }
    ]
  },
  "then": {
    "effect": "deny"
  }
}
```

---

## Cost Management

### Azure Cost Management and Billing

Tools for monitoring, allocating, and optimizing cloud costs.

#### Key Features:

##### 1. **Cost Analysis**
- Historical cost views
- Forecasting
- Breakdown by resource, service, tag, or resource group
- Custom date ranges

##### 2. **Budgets and Alerts**
```bash
# Create budget via CLI
az consumption budget create \
  --budget-name MonthlyBudget \
  --amount 1000 \
  --time-grain Monthly \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --resource-group myResourceGroup
```

##### 3. **Cost Allocation**
- Tagging strategy
- Showback/chargeback reports
- Department/team cost tracking

**Tagging Example:**
```yaml
- task: AzureCLI@2
  inputs:
    inlineScript: |
      az resource tag \
        --ids /subscriptions/.../resourceGroups/myResourceGroup \
        --tags Environment=Production CostCenter=Engineering Team=Platform
```

##### 4. **Recommendations**
- Right-size underutilized resources
- Reserved instances for cost savings
- Spot VMs for non-critical workloads
- Delete unused resources

##### 5. **Azure Advisor**
- Cost optimization recommendations
- Performance improvements
- Security enhancements
- Operational excellence

### Azure Policy for Cost Control

```json
{
  "displayName": "Allowed VM SKUs",
  "description": "Restrict VM sizes to control costs",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Compute/virtualMachines"
        },
        {
          "not": {
            "field": "Microsoft.Compute/virtualMachines/sku.name",
            "in": ["Standard_B2s", "Standard_B4ms", "Standard_D2s_v3"]
          }
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

---

## Log Flow Architecture: Azure to Datadog

### Overview

This architecture ensures reliable log delivery from Azure to Datadog with queuing mechanisms to handle Datadog API downtime and automatic retransmission when service is restored.

### Architecture Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AZURE ENVIRONMENT                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Azure VMs  │  │     AKS      │  │  App Service │              │
│  │   (Logs)     │  │  (Logs)      │  │   (Logs)     │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                       │
│         └──────────────────┼──────────────────┘                      │
│                            │                                          │
│                            ▼                                          │
│         ┌──────────────────────────────────────┐                     │
│         │   Azure Monitor / Log Analytics      │                     │
│         │   (Central Log Collection)           │                     │
│         └──────────────┬───────────────────────┘                     │
│                        │                                              │
│                        │ Diagnostic Settings                         │
│                        ▼                                              │
│         ┌──────────────────────────────────────┐                     │
│         │      Azure Event Hub (Namespace)     │                     │
│         │  ┌────────────────────────────────┐  │                     │
│         │  │  Event Hub: logs-stream        │  │                     │
│         │  │  - Partitions: 4               │  │                     │
│         │  │  - Retention: 7 days           │  │                     │
│         │  │  - Throughput Units: 2         │  │                     │
│         │  └────────────────────────────────┘  │                     │
│         └──────────────┬───────────────────────┘                     │
│                        │                                              │
│                        │                                              │
│         ┌──────────────▼───────────────────────┐                     │
│         │    Azure Function App                │                     │
│         │    (Event Hub Trigger)               │                     │
│         │                                       │                     │
│         │  - Runtime: Python 3.9               │                     │
│         │  - Consumption Plan / Premium Plan   │                     │
│         │                                       │                     │
│         │  Functions:                          │                     │
│         │  1. event_hub_processor()            │                     │
│         │  2. retry_queue_processor()          │                     │
│         │  3. dead_letter_processor()          │                     │
│         └──────────────┬───────────────────────┘                     │
│                        │                                              │
│            ┌───────────┴──────────┐                                  │
│            │                       │                                  │
│            ▼                       ▼                                  │
│  ┌─────────────────┐    ┌──────────────────────┐                    │
│  │ Azure Storage   │    │  Azure Service Bus   │                    │
│  │ Queue           │    │  (Retry Queue)       │                    │
│  │ (Dead Letter)   │    │                      │                    │
│  │                 │    │  - Max Retry: 5      │                    │
│  └─────────────────┘    │  - TTL: 24 hours     │                    │
│                         │  - Retry Delays:     │                    │
│                         │    1m, 5m, 15m, 1h   │                    │
│                         └──────────┬───────────┘                    │
│                                    │                                  │
│                                    │ Retry Logic                     │
│                                    └─────┐                           │
│                                          │                           │
└──────────────────────────────────────────┼───────────────────────────┘
                                           │
                                           │ HTTPS
                                           ▼
                            ┌──────────────────────────┐
                            │   Datadog API Endpoint   │
                            │   (api.datadoghq.com)    │
                            │                          │
                            │   - Logs Ingestion API   │
                            │   - With API Key         │
                            └──────────────────────────┘
```

### Implementation Details

#### 1. **Azure Monitor to Event Hub Configuration**

```bash
# Create Event Hub Namespace
az eventhubs namespace create \
  --name logs-eventhub-ns \
  --resource-group monitoring-rg \
  --location eastus \
  --sku Standard \
  --capacity 2

# Create Event Hub
az eventhubs eventhub create \
  --name logs-stream \
  --namespace-name logs-eventhub-ns \
  --resource-group monitoring-rg \
  --partition-count 4 \
  --message-retention 7

# Configure Diagnostic Settings to send logs to Event Hub
az monitor diagnostic-settings create \
  --name logs-to-eventhub \
  --resource /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/{resource} \
  --event-hub logs-stream \
  --event-hub-rule /subscriptions/{subscription-id}/resourceGroups/monitoring-rg/providers/Microsoft.EventHub/namespaces/logs-eventhub-ns/authorizationRules/RootManageSharedAccessKey \
  --logs '[{"category":"Administrative","enabled":true}]' \
  --metrics '[{"category":"AllMetrics","enabled":true}]'
```

#### 2. **Azure Function - Event Hub Processor**

**requirements.txt:**
```
azure-functions
azure-eventhub
azure-storage-queue
azure-servicebus
requests
tenacity
```

**function_app.py:**
```python
import azure.functions as func
import json
import logging
import os
import requests
from datetime import datetime, timedelta
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.storage.queue import QueueClient
from tenacity import retry, stop_after_attempt, wait_exponential

app = func.FunctionApp()

# Configuration
DATADOG_API_KEY = os.environ['DATADOG_API_KEY']
DATADOG_SITE = os.environ.get('DATADOG_SITE', 'datadoghq.com')
DATADOG_LOGS_URL = f"https://http-intake.logs.{DATADOG_SITE}/v1/input"
SERVICE_BUS_CONN_STR = os.environ['SERVICE_BUS_CONNECTION_STRING']
RETRY_QUEUE_NAME = "log-retry-queue"
DEAD_LETTER_QUEUE_CONN_STR = os.environ['STORAGE_CONNECTION_STRING']
DEAD_LETTER_QUEUE_NAME = "log-dead-letter"

# Initialize clients
sb_client = ServiceBusClient.from_connection_string(SERVICE_BUS_CONN_STR)
dead_letter_client = QueueClient.from_connection_string(
    DEAD_LETTER_QUEUE_CONN_STR, 
    DEAD_LETTER_QUEUE_NAME
)


def send_to_datadog(log_data, max_attempts=3):
    """
    Send logs to Datadog with retry logic
    Returns: (success: bool, should_retry: bool)
    """
    headers = {
        'DD-API-KEY': DATADOG_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            DATADOG_LOGS_URL,
            headers=headers,
            json=log_data,
            timeout=10
        )
        
        if response.status_code == 200 or response.status_code == 202:
            logging.info(f"Successfully sent logs to Datadog")
            return True, False
        elif response.status_code >= 500:
            # Server error - should retry
            logging.warning(f"Datadog API server error: {response.status_code}")
            return False, True
        elif response.status_code == 429:
            # Rate limited - should retry
            logging.warning("Datadog API rate limit exceeded")
            return False, True
        elif response.status_code >= 400:
            # Client error - should not retry
            logging.error(f"Datadog API client error: {response.status_code} - {response.text}")
            return False, False
        else:
            logging.warning(f"Unexpected Datadog API response: {response.status_code}")
            return False, True
            
    except requests.exceptions.Timeout:
        logging.warning("Datadog API timeout")
        return False, True
    except requests.exceptions.ConnectionError:
        logging.warning("Datadog API connection error")
        return False, True
    except Exception as e:
        logging.error(f"Unexpected error sending to Datadog: {str(e)}")
        return False, True


def send_to_retry_queue(log_data, retry_count=0):
    """Send failed logs to Service Bus retry queue"""
    try:
        sender = sb_client.get_queue_sender(RETRY_QUEUE_NAME)
        
        message_body = {
            'log_data': log_data,
            'retry_count': retry_count,
            'original_timestamp': datetime.utcnow().isoformat()
        }
        
        # Calculate delay based on retry count (exponential backoff)
        delays = [60, 300, 900, 3600, 7200]  # 1m, 5m, 15m, 1h, 2h
        delay_seconds = delays[min(retry_count, len(delays)-1)]
        
        message = ServiceBusMessage(
            body=json.dumps(message_body),
            scheduled_enqueue_time_utc=datetime.utcnow() + timedelta(seconds=delay_seconds)
        )
        
        sender.send_messages(message)
        logging.info(f"Sent to retry queue with {delay_seconds}s delay (retry #{retry_count})")
        
    except Exception as e:
        logging.error(f"Failed to send to retry queue: {str(e)}")
        send_to_dead_letter(log_data, f"Retry queue failed: {str(e)}")


def send_to_dead_letter(log_data, reason):
    """Send logs to dead letter queue when all retries exhausted"""
    try:
        message = {
            'log_data': log_data,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat()
        }
        dead_letter_client.send_message(json.dumps(message))
        logging.error(f"Sent to dead letter queue: {reason}")
    except Exception as e:
        logging.critical(f"Failed to send to dead letter queue: {str(e)}")


@app.function_name(name="EventHubProcessor")
@app.event_hub_message_trigger(
    arg_name="events",
    event_hub_name="logs-stream",
    connection="EVENT_HUB_CONNECTION_STRING",
    cardinality="many"
)
def event_hub_processor(events: list[func.EventHubEvent]):
    """
    Main processor for Event Hub messages
    Receives logs from Azure Monitor and forwards to Datadog
    """
    for event in events:
        try:
            # Parse the event body
            log_data = json.loads(event.get_body().decode('utf-8'))
            
            # Enrich with metadata
            enriched_log = {
                'ddsource': 'azure',
                'service': log_data.get('resourceId', '').split('/')[-1],
                'hostname': log_data.get('hostname', 'azure-resource'),
                'timestamp': log_data.get('time', datetime.utcnow().isoformat()),
                'message': json.dumps(log_data),
                'ddtags': f"environment:{os.environ.get('ENVIRONMENT', 'production')},source:azure"
            }
            
            # Try to send to Datadog
            success, should_retry = send_to_datadog(enriched_log)
            
            if not success and should_retry:
                # Send to retry queue
                send_to_retry_queue(enriched_log, retry_count=0)
            elif not success and not should_retry:
                # Permanent failure - send to dead letter
                send_to_dead_letter(enriched_log, "Permanent Datadog API error")
                
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse event: {str(e)}")
        except Exception as e:
            logging.error(f"Error processing event: {str(e)}")


@app.function_name(name="RetryQueueProcessor")
@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name=RETRY_QUEUE_NAME,
    connection="SERVICE_BUS_CONNECTION_STRING"
)
def retry_queue_processor(msg: func.ServiceBusMessage):
    """
    Process messages from retry queue
    Attempts to resend to Datadog with exponential backoff
    """
    try:
        message_body = json.loads(msg.get_body().decode('utf-8'))
        log_data = message_body['log_data']
        retry_count = message_body.get('retry_count', 0)
        
        logging.info(f"Processing retry queue message (attempt #{retry_count + 1})")
        
        # Try to send to Datadog
        success, should_retry = send_to_datadog(log_data)
        
        if success:
            logging.info(f"Successfully sent log after {retry_count + 1} retries")
        elif should_retry and retry_count < 5:
            # Retry again with increased counter
            send_to_retry_queue(log_data, retry_count + 1)
        else:
            # Max retries exhausted or permanent failure
            send_to_dead_letter(
                log_data, 
                f"Max retries exhausted ({retry_count + 1} attempts)"
            )
            
    except Exception as e:
        logging.error(f"Error processing retry queue message: {str(e)}")


@app.function_name(name="DeadLetterProcessor")
@app.timer_trigger(
    arg_name="timer",
    schedule="0 */30 * * * *"  # Every 30 minutes
)
def dead_letter_processor(timer: func.TimerRequest):
    """
    Periodically check dead letter queue and attempt to reprocess
    """
    try:
        messages = dead_letter_client.receive_messages(max_messages=10)
        
        for message in messages:
            try:
                msg_body = json.loads(message.content)
                log_data = msg_body['log_data']
                
                # Try to send to Datadog
                success, _ = send_to_datadog(log_data)
                
                if success:
                    # Successfully recovered, delete from dead letter
                    dead_letter_client.delete_message(message)
                    logging.info("Recovered log from dead letter queue")
                    
            except Exception as e:
                logging.error(f"Error processing dead letter message: {str(e)}")
                
    except Exception as e:
        logging.error(f"Error checking dead letter queue: {str(e)}")


@app.function_name(name="HealthCheck")
@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint for monitoring"""
    try:
        # Check Datadog connectivity
        response = requests.get(
            f"https://api.{DATADOG_SITE}/api/v1/validate",
            headers={'DD-API-KEY': DATADOG_API_KEY},
            timeout=5
        )
        
        datadog_status = "healthy" if response.status_code == 200 else "unhealthy"
        
        return func.HttpResponse(
            json.dumps({
                'status': 'healthy',
                'datadog': datadog_status,
                'timestamp': datetime.utcnow().isoformat()
            }),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'unhealthy',
                'error': str(e)
            }),
            mimetype="application/json",
            status_code=503
        )
```

#### 3. **Infrastructure Deployment**

**Azure CLI Script:**
```bash
#!/bin/bash

# Variables
RESOURCE_GROUP="monitoring-rg"
LOCATION="eastus"
EVENTHUB_NAMESPACE="logs-eventhub-ns"
EVENTHUB_NAME="logs-stream"
SERVICE_BUS_NAMESPACE="logs-servicebus-ns"
RETRY_QUEUE="log-retry-queue"
STORAGE_ACCOUNT="logstorage$(date +%s)"
FUNCTION_APP="log-forwarder-func"
DATADOG_API_KEY="your-datadog-api-key"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Event Hub
az eventhubs namespace create \
  --name $EVENTHUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard

az eventhubs eventhub create \
  --name $EVENTHUB_NAME \
  --namespace-name $EVENTHUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --partition-count 4 \
  --message-retention 7

# Create Service Bus for retry queue
az servicebus namespace create \
  --name $SERVICE_BUS_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard

az servicebus queue create \
  --name $RETRY_QUEUE \
  --namespace-name $SERVICE_BUS_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --max-delivery-count 10 \
  --default-message-time-to-live P1D

# Create Storage Account for dead letter and function
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

az storage queue create \
  --name log-dead-letter \
  --account-name $STORAGE_ACCOUNT

# Create Function App
az functionapp create \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --storage-account $STORAGE_ACCOUNT \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4

# Get connection strings
EVENT_HUB_CONN=$(az eventhubs namespace authorization-rule keys list \
  --namespace-name $EVENTHUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv)

SERVICE_BUS_CONN=$(az servicebus namespace authorization-rule keys list \
  --namespace-name $SERVICE_BUS_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv)

STORAGE_CONN=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query connectionString -o tsv)

# Configure Function App settings
az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    EVENT_HUB_CONNECTION_STRING="$EVENT_HUB_CONN" \
    SERVICE_BUS_CONNECTION_STRING="$SERVICE_BUS_CONN" \
    STORAGE_CONNECTION_STRING="$STORAGE_CONN" \
    DATADOG_API_KEY="$DATADOG_API_KEY" \
    DATADOG_SITE="datadoghq.com" \
    ENVIRONMENT="production"

echo "Infrastructure deployed successfully!"
```

#### 4. **Monitoring and Alerting**

**Application Insights Queries:**
```kql
// Monitor retry queue depth
customMetrics
| where name == "RetryQueueDepth"
| summarize avg(value) by bin(timestamp, 5m)
| render timechart

// Track Datadog API failures
traces
| where message contains "Datadog API"
| where severityLevel >= 3
| summarize count() by bin(timestamp, 5m), message
| render timechart

// Dead letter queue growth
customMetrics
| where name == "DeadLetterQueueDepth"
| summarize avg(value) by bin(timestamp, 15m)
| render timechart
```

**Alert Configuration:**
```bash
# Alert on high retry queue depth
az monitor metrics alert create \
  --name "High Retry Queue Depth" \
  --resource-group $RESOURCE_GROUP \
  --scopes "/subscriptions/.../servicebus/$SERVICE_BUS_NAMESPACE" \
  --condition "avg ActiveMessages > 1000" \
  --description "Retry queue is backing up"

# Alert on dead letter queue growth
az monitor metrics alert create \
  --name "Dead Letter Queue Growing" \
  --resource-group $RESOURCE_GROUP \
  --scopes "/subscriptions/.../storageAccounts/$STORAGE_ACCOUNT" \
  --condition "total MessageCount > 100" \
  --description "Dead letter queue requires attention"
```

---

## Best Practices Summary

### DevOps Pipelines
- Use YAML pipelines for version control
- Implement multi-stage pipelines (build, test, deploy)
- Use pipeline templates for reusability
- Implement approval gates for production
- Store secrets in Azure Key Vault

### Infrastructure as Code
- Use ARM templates or Bicep for Azure-specific resources
- Consider Terraform for multi-cloud
- Implement parameterization and modularity
- Version control all IaC files
- Use separate environments (dev, staging, prod)

### Monitoring
- Enable Application Insights for all applications
- Set up meaningful alerts (avoid alert fatigue)
- Use Log Analytics for centralized logging
- Implement distributed tracing
- Regular review of metrics and dashboards

### Security
- Store all secrets in Key Vault
- Enable Azure Security Center/Defender
- Implement RBAC with least privilege
- Use managed identities when possible
- Regular security assessments

### Cost Optimization
- Tag all resources appropriately
- Right-size resources based on actual usage
- Use reserved instances for predictable workloads
- Implement auto-scaling
- Regular cost reviews and optimization

---

## Additional Resources

- [Azure Documentation](https://docs.microsoft.com/azure)
- [Azure DevOps Documentation](https://docs.microsoft.com/azure/devops)
- [Datadog Azure Integration](https://docs.datadoghq.com/integrations/azure)
- [Azure Architecture Center](https://docs.microsoft.com/azure/architecture)
- [Azure Well-Architected Framework](https://docs.microsoft.com/azure/architecture/framework)

