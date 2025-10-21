awesome — here are several practical, production-ready Python automation scripts for Azure, each with a short description, an ASCII diagram of how it fits together, and notes on running them as Azure Automation Runbooks or Timer-triggered Azure Functions. All scripts authenticate with DefaultAzureCredential, so they work cleanly with Managed Identity.

Common requirements (package names you’ll import into the runbook/Function app):
azure-identity, azure-mgmt-resource, azure-mgmt-compute, azure-mgmt-network, azure-keyvault-secrets, azure-storage-blob
(install via Automation Python3 packages, or include in Function app requirements.txt)

1) Start/Stop VMs by Tag (e.g., shut dev after hours)
[Timer] ──> [Runbook / Function]
                  │ uses DefaultAzureCredential
                  ▼
            [Azure Resource Manager]
                  │ filter VMs by tag (e.g., env=dev)
                  └── start/stop VMs


What it does: Finds all VMs with a tag (e.g., autoPower=true) and either starts or deallocates them based on a mode you pass (START/STOP). Great for cost control.

# start_stop_vms_by_tag.py
import os, logging
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

SUBSCRIPTION_ID = os.environ.get("AZ_SUBSCRIPTION_ID")
TAG_KEY = os.environ.get("TAG_KEY", "autoPower")
TAG_VAL = os.environ.get("TAG_VAL", "true")
MODE = os.environ.get("MODE", "STOP").upper()  # START or STOP

def run():
    logging.basicConfig(level=logging.INFO)
    cred = DefaultAzureCredential()
    rmc = ResourceManagementClient(cred, SUBSCRIPTION_ID)
    cmc = ComputeManagementClient(cred, SUBSCRIPTION_ID)

    for rg in rmc.resource_groups.list():
        for vm in cmc.virtual_machines.list(rg.name):
            tags = (vm.tags or {})
            if tags.get(TAG_KEY, "").lower() == TAG_VAL:
                name = vm.name
                if MODE == "START":
                    logging.info(f"Starting VM {name} in {rg.name}")
                    cmc.virtual_machines.begin_start(rg.name, name).result()
                else:
                    logging.info(f"Deallocating VM {name} in {rg.name}")
                    cmc.virtual_machines.begin_deallocate(rg.name, name).result()

if __name__ == "__main__":
    run()


Run it as:

Runbook on a schedule (Mon–Fri 19:00 STOP; Mon–Fri 08:00 START)

Function with a CRON timer trigger

2) Auto-tag new resources missing mandatory tags
[Timer] ──> [Runbook / Function]
                  │
                  ▼
        [Azure Resource Graph/ARM]
                  │
          add tags if missing


What it does: Enforces governance by ensuring every resource has required tags like env, owner, costCenter. (Idempotent: only adds what’s missing.)

# enforce_tags.py
import os, logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

SUBSCRIPTION_ID = os.environ["AZ_SUBSCRIPTION_ID"]
REQUIRED_TAGS = {
    "owner": os.environ.get("DEFAULT_OWNER", "platform-team"),
    "env": os.environ.get("DEFAULT_ENV", "dev"),
    "costCenter": os.environ.get("DEFAULT_CC", "0000")
}

def run():
    logging.basicConfig(level=logging.INFO)
    cred = DefaultAzureCredential()
    rmc = ResourceManagementClient(cred, SUBSCRIPTION_ID)

    for rg in rmc.resource_groups.list():
        for res in rmc.resources.list_by_resource_group(rg.name):
            current = res.tags or {}
            missing = {k:v for k,v in REQUIRED_TAGS.items() if k not in current}
            if missing:
                merged = {**current, **missing}
                logging.info(f"Tagging {res.id} with {missing}")
                rmc.tags.update_at_scope(
                    scope=res.id,
                    parameters={"operation": "Merge", "properties": {"tags": merged}}
                )

if __name__ == "__main__":
    run()

3) Nightly snapshots of all Managed Disks with retention
[Timer] ──> [Runbook / Function]
                  │
                  ▼
        [Compute Mgmt API] create snapshots
                  │
               delete old by tag (retention)


What it does: Snapshots every managed disk with backup=true tag. Names snapshots with date stamp and removes older ones beyond RETENTION_DAYS.

# snapshot_disks.py
import os, logging
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

SUBSCRIPTION_ID = os.environ["AZ_SUBSCRIPTION_ID"]
RETENTION_DAYS = int(os.environ.get("RETENTION_DAYS", "7"))
TAG_KEY, TAG_VAL = "backup", "true"

def run():
    logging.basicConfig(level=logging.INFO)
    cred = DefaultAzureCredential()
    cmc = ComputeManagementClient(cred, SUBSCRIPTION_ID)
    rmc = ResourceManagementClient(cred, SUBSCRIPTION_ID)
    today = datetime.now(timezone.utc).strftime("%Y%m%d")

    # create snapshots for tagged disks
    for rg in rmc.resource_groups.list():
        for disk in cmc.disks.list_by_resource_group(rg.name):
            if (disk.tags or {}).get(TAG_KEY) == TAG_VAL:
                snap_name = f"{disk.name}-snap-{today}"
                params = {
                    "location": disk.location,
                    "creation_data": {"create_option": "Copy", "source_resource_id": disk.id},
                    "tags": {"createdBy": "snapshot_disks.py", "date": today}
                }
                logging.info(f"Creating snapshot {snap_name} for disk {disk.name}")
                cmc.snapshots.begin_create_or_update(rg.name, snap_name, params).result()

    # clean old snapshots (createdBy tag)
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    for rg in rmc.resource_groups.list():
        for snap in cmc.snapshots.list_by_resource_group(rg.name):
            t = (snap.tags or {}).get("date")
            if (snap.tags or {}).get("createdBy") == "snapshot_disks.py" and t:
                dt = datetime.strptime(t, "%Y%m%d").replace(tzinfo=timezone.utc)
                if dt < cutoff:
                    logging.info(f"Deleting old snapshot {snap.name}")
                    cmc.snapshots.begin_delete(rg.name, snap.name).result()

if __name__ == "__main__":
    run()

4) Resize a VM Scale Set for business hours
[Timer] ──> [Runbook / Function]
        Work hours: capacity=N
        Off hours:  capacity=M


What it does: Sets a deterministic capacity for a VM Scale Set depending on whether it’s business hours. Useful when native autoscale isn’t preferable for predictable schedules.

# schedule_vmss_capacity.py
import os, logging, datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

SUBSCRIPTION_ID = os.environ["AZ_SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["VMSS_RG"]
VMSS_NAME = os.environ["VMSS_NAME"]
WORK_CAPACITY = int(os.environ.get("WORK_CAPACITY", "4"))
OFF_CAPACITY = int(os.environ.get("OFF_CAPACITY", "1"))
WORK_DAYS = set((os.environ.get("WORK_DAYS", "Mon,Tue,Wed,Thu,Fri")).split(","))
START_HOUR = int(os.environ.get("START_HOUR", "8"))
END_HOUR = int(os.environ.get("END_HOUR", "19"))

def run():
    logging.basicConfig(level=logging.INFO)
    now = datetime.datetime.now()
    day = now.strftime("%a")
    in_hours = (day in WORK_DAYS) and (START_HOUR <= now.hour < END_HOUR)
    target = WORK_CAPACITY if in_hours else OFF_CAPACITY

    cred = DefaultAzureCredential()
    cmc = ComputeManagementClient(cred, SUBSCRIPTION_ID)
    vmss = cmc.virtual_machine_scale_sets.get(RESOURCE_GROUP, VMSS_NAME)
    if vmss.sku.capacity != target:
        logging.info(f"Setting VMSS capacity {vmss.sku.capacity} -> {target}")
        vmss.sku.capacity = target
        cmc.virtual_machine_scale_sets.begin_create_or_update(RESOURCE_GROUP, VMSS_NAME, vmss).result()
    else:
        logging.info("Capacity already at target.")

if __name__ == "__main__":
    run()

5) Rotate a Key Vault secret (generate & version)
[Timer] ──> [Runbook / Function]
                  │
                  ▼
            [Azure Key Vault]
           new random value → new version


What it does: Periodically rotates a generic secret (e.g., app shared secret). It generates a cryptographically strong value and sets a new version in Key Vault, leaving older versions for rollback.

# rotate_keyvault_secret.py
import os, secrets, base64, logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = os.environ["KEYVAULT_URL"]   # e.g., https://mykv.vault.azure.net/
SECRET_NAME = os.environ.get("SECRET_NAME", "app-shared-secret")
BYTES_LEN = int(os.environ.get("BYTES_LEN", "32"))

def run():
    logging.basicConfig(level=logging.INFO)
    cred = DefaultAzureCredential()
    client = SecretClient(vault_url=VAULT_URL, credential=cred)
    raw = secrets.token_bytes(BYTES_LEN)
    value = base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")
    client.set_secret(SECRET_NAME, value)
    logging.info(f"Rotated secret '{SECRET_NAME}' with a new version.")

if __name__ == "__main__":
    run()


(If you need to rotate linked credentials like Storage keys, fetch the new key first via the respective management client, then store it here.)

6) Inventory public IPs → CSV in Blob Storage
[Timer] ──> [Runbook / Function]
                  │
                  ▼
        [Network Mgmt API] list IPs
                  │
                  ▼
            [Blob Storage] upload CSV


What it does: Audits all public IP addresses across the subscription, writes a CSV, and uploads it to a specified container for security reviews.

# export_public_ips_to_blob.py
import os, csv, io, logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.blob import BlobServiceClient

SUBSCRIPTION_ID = os.environ["AZ_SUBSCRIPTION_ID"]
STORAGE_URL = os.environ["BLOB_ENDPOINT"]  # e.g., https://mystorage.blob.core.windows.net
CONTAINER = os.environ.get("BLOB_CONTAINER", "reports")
BLOB_NAME = os.environ.get("BLOB_NAME", "public-ips.csv")

def run():
    logging.basicConfig(level=logging.INFO)
    cred = DefaultAzureCredential()
    nmc = NetworkManagementClient(cred, SUBSCRIPTION_ID)
    rmc = ResourceManagementClient(cred, SUBSCRIPTION_ID)

    rows = [("resourceGroup","name","ipAddress","sku","allocationMethod","location","tags")]
    for rg in rmc.resource_groups.list():
        for pip in nmc.public_ip_addresses.list(rg.name):
            rows.append((
                rg.name, pip.name, (pip.ip_address or ""), getattr(pip.sku, "name", ""),
                pip.public_ip_allocation_method, pip.location, str(pip.tags or {})
            ))

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    data = buf.getvalue().encode("utf-8")

    bsc = BlobServiceClient(account_url=STORAGE_URL, credential=cred)
    bsc.get_container_client(CONTAINER).upload_blob(BLOB_NAME, data, overwrite=True)
    logging.info(f"Uploaded {len(rows)-1} rows to {CONTAINER}/{BLOB_NAME}")

if __name__ == "__main__":
    run()

How to deploy/run these
As Azure Automation Runbooks

Create an Automation Account (with System-Assigned Managed Identity enabled).

Grant the identity suitable roles (least privilege!), e.g. Reader or Contributor on target scopes; Key Vault Secrets Officer for secret rotation; Storage Blob Data Contributor for blob uploads.

Import the script, set environment variables as Automation variables, schedule with CRON-like schedules.

As Azure Functions (Timer trigger)

Create a Python Function App, add a Timer trigger per job (CRON expression).

Put config in App settings (same env var names).

Assign a System-Assigned Managed Identity and grant roles.

Bonus hardening tips

Add dry-run flags for destructive actions (delete/stop).

Emit to Application Insights (structured logs).

Use scope-limited identities (resource-group level where possible).

Wrap long-running Azure SDK calls with .result() and try/except for transient failures.

Build a shared tagging standard (e.g., owner, env, compliance, dataClass).

If you want, I can package any of these as a ready-to-import .zip for a Function App or an Automation Runbook bundle with a sample schedule and RBAC notes.