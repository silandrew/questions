# Interview Questions

## About the Role

### Technical Questions
1. Can you describe your experience with automating the provisioning of servers and networks in physical environments and the cloud (e.g., AWS, GCP)?
	- Answer: I have provisioned both bare-metal and cloud servers using a mix of IaC and automation tools. In cloud (AWS/GCP) I use Terraform for infrastructure (VPCs, subnets, instances) and Ansible for configuration (packages, services). For physical environments I automate OS installs with PXE/Cloud-Init where possible and use Ansible to configure networking, VLANs, and device-specific settings. I always create reusable modules/roles and version control templates.
2. What tools or frameworks have you used to evolve Continuous Delivery pipelines? Can you provide an example of a pipeline you worked on?
	- Answer: I've used Jenkins, GitHub Actions, and GitLab CI. Example: a GitOps pipeline using GitHub Actions that runs linting and tests on PRs, builds container images, pushes to a registry, and then triggers a deployment job that runs Ansible to update configuration and rolling-update the service. The pipeline included artifact promotion, canary stages, and automated rollback on health-check failures.
3. How do you approach automating the configuration of servers and switches? Have you used tools like Ansible for this purpose?
	- Answer: For servers, I use Ansible (roles, idempotent tasks, templates). For network devices I use vendor modules (e.g., `ios`, `nxos`) or NAPALM where appropriate. I model desired state in YAML, test in labs, validate with check modes, and use orchestration for safe rollouts. For switches, I avoid destructive changes without pre-checks and maintain a known-good config repository.
4. Can you share your experience interacting with hardware vendors, telecom providers, or financial institutions? How do you ensure smooth communication and collaboration?
	- Answer: I keep clear SLAs, documented requirements, and runbooks. For vendors and telecoms, I verify compatibility early, request lab/dev access when possible, and escalate with clear reproduction steps. For financial institutions I follow stricter change management, compliance checks, and audit trails.
5. What is your process for provisioning employee laptops and arranging shipments? How do you ensure efficiency and accuracy?
	- Answer: I maintain an image or automation (MDM + provisioning scripts). Process: inventory request -> image/OS install -> configuration via Ansible or MDM (apps, accounts, security settings) -> QA -> asset tagging and shipment. Use checklists and automation to reduce manual errors.

### Coding Questions
6. What is your preferred programming language, and can you share an example of a project where you used it to automate a task?
	- Answer: I prefer Python for scripting and automation because of libraries and readability. Example: wrote a Python tool to ingest syslog, normalize events, and push alerts to Slack and an internal ticketing system. It used asyncio for concurrency and was packaged and deployed with simple CI.
7. How would you write a script to automate the deployment of a server in AWS? What considerations would you include?
	- Answer: Use Terraform for infra (VPC, subnets, security groups, EC2), then Ansible for post-provisioning. Considerations: idempotency, secrets management, IAM least privilege, networking (public/private subnets), tagging, monitoring, and cost controls. Include integration tests and rollback plans.
8. Can you demonstrate basic coding skills by solving a simple problem, such as writing a script to parse a log file and extract specific information?
	- Answer: Yes — I'd use a short Python or shell script using regex or the `csv` module depending on format, with unit tests for edge cases. Example: Python script reading lines, extracting timestamp and error codes, and outputting JSON.

### Behavioral Questions
9. Can you describe a time when you had to take the initiative to solve a problem in your role? What was the outcome?
	- Answer: Example: I automated a manual deployment that caused frequent outages by creating an Ansible role with health checks and rollback. The outcome was fewer incidents and faster recovery times.
10. How do you stay motivated and continue learning in a fast-paced environment?
	- Answer: Regularly read blogs, follow mailing lists, participate in meetups, build small lab projects, and dedicate time each week to learn new tools.
11. Can you share an example of how you managed 3rd parties, such as negotiating with vendors or purchasing hardware?
	- Answer: I coordinate requirements, run PoCs, compare quotes, and negotiate support terms and SLAs. I keep stakeholders informed and document decisions.
12. How do you handle situations where you need to provide desktop support while managing other responsibilities?
	- Answer: Triage requests, use remote tools, document fixes, automate repetitive fixes with scripts, and communicate expected timelines to stakeholders.

### Hypothetical Scenarios
13. If you were tasked with setting up a new office's network infrastructure, what steps would you take to ensure everything is automated and secure?
	- Answer: Design the network (VLANs, addressing, firewall zones), provision switches and APs via automation (Ansible/NAPALM), implement central logging and monitoring, configure NAC and secure Wi-Fi, and implement change control and backups. Test in a lab, then roll out with rollback playbooks.
14. Imagine a scenario where a critical server goes down. How would you troubleshoot and resolve the issue?
	- Answer: First determine scope (is it isolated?), check monitoring, review logs, attempt controlled restart of services, roll back recent changes, and escalate to hardware/OS vendor if needed. Use runbook steps and document remediation.
15. If a remote employee reports issues with their laptop, how would you diagnose and resolve the problem remotely?
	- Answer: Use remote management tools (RDP/SSH/MDM), request logs and system info, replicate in lab if necessary, apply fix or provide replacement, and update the incident tracker.

---

## Bonus Questions

1. Have you worked with financial institutions before? If so, what unique challenges did you face, and how did you address them?
	- Answer: Yes — challenges include strict compliance, auditing, and change control. I used stricter testing, staged environments, and documented approvals to meet compliance.
2. Are you familiar with any specific hardware vendors or telecom providers? How do you evaluate and choose between different vendors?
	- Answer: I evaluate vendor reliability, support, features, and TCO. I also run PoCs and check for ecosystem compatibility and community adoption.
3. How do you balance autonomy with collaboration in a team setting?
	- Answer: Clear ownership, documented APIs and interfaces, regular standups, and code reviews to keep autonomy while collaborating.

---

## Ansible playbooks & roles

### Basic/Conceptual
1. What is the difference between an Ansible playbook and an Ansible role? When would you use one over the other?
	- Answer: A playbook is a YAML file that defines which hosts to target and what tasks or roles to run; a role is a reusable, structured unit (tasks, handlers, templates, vars, defaults) for a specific function. Use roles for reuse and separation of concerns; use playbooks to orchestrate roles across hosts.
2. Explain idempotence in the context of Ansible. Why is it important for infrastructure automation?
	- Answer: Idempotence means running the same task multiple times results in the same final state; it's critical to ensure safe repeated runs, deterministic outcomes, and reliable automation.
3. How do you structure variables in Ansible (group_vars, host_vars, role defaults, inventory vars) and how do precedence rules work?
	- Answer: Put global settings in `group_vars/all`, environment-specific in `group_vars/<group>`, host overrides in `host_vars/<host>`, role defaults in `roles/<role>/defaults`, and role vars in `roles/<role>/vars`. Precedence: command-line vars > role vars > inventory vars > role defaults (many levels exist; refer to the docs). Keep secrets in vault.
4. What strategies do you use to keep secrets secure when using Ansible? Describe how Ansible Vault works and pros/cons.
	- Answer: Use Ansible Vault to encrypt variable files or use external secret managers (HashiCorp Vault, AWS Secrets Manager). Vault encrypts files; you can supply a password or use a password file/agent. Pros: simple to integrate; Cons: key management and rotation needs processes.

### Playbook/Role Design
5. How would you convert an existing playbook into a reusable role? What files and directories does a role commonly contain?
	- Answer: Create the role directory, move tasks to `roles/<role>/tasks/main.yml`, put templates into `roles/<role>/templates/`, handlers into `roles/<role>/handlers/main.yml`, defaults into `roles/<role>/defaults/main.yml`, vars into `roles/<role>/vars/main.yml`, and metadata in `roles/<role>/meta/main.yml`. Replace hard-coded values with variables and provide sensible defaults.
6. Describe how you would design a role for installing and configuring Nginx, including templates and handlers.
	- Answer: Role should install package per-distro, deploy templates for site and index.html, provide default variables (`www_root`, `server_name`), and include handlers to `reload`/`restart` nginx when configs change. Add tests and molecule scenarios.
7. For a role that compiles and installs a custom Linux kernel, what safety checks and safeguards would you include?
	- Answer: Check OS and bootloader compatibility, verify available disk space, require an explicit `force: true` var to run on production, perform build in isolated workspace, update grub safely and optionally only stage install, and require manual approval before reboot. Provide rollback instructions and keep previous kernels.
8. How do you make your roles cross-distro (Debian/RedHat)? Give examples of task patterns you would use.
	- Answer: Use `when: ansible_os_family == 'Debian'` or `'RedHat'`, leverage package manager abstractions (use `package` module when possible), and provide distro-specific templates or files under `templates/` selected by conditions.

### Advanced/Integration
9. Explain how you would automate joining a Linux host to Active Directory using `realmd` and `sssd`. What sensitive data is required and how would you store it?
	- Answer: Install `realmd` and `sssd`, configure `/etc/krb5.conf` and `/etc/sssd/sssd.conf` via templates, then run `realm join --user=ADJOINUSER ad.example.com` using credentials stored in Ansible Vault (or a credential manager). Ensure services (`sssd`) are restarted and permissions for `sssd.conf` are correct. Test user lookups and sudo mapping.
10. For OAuth2/SAML integrations (Dex, Keycloak, Shibboleth), describe what parts can be automated with Ansible and what parts usually require manual/provider-side setup.
	- Answer: You can automate installation, configuration files, container deployment, certificates, and initial realm/client creation via APIs. Provider-side work (IDP configuration, tenant approvals, user consent screens) often requires manual steps or API interactions that depend on the provider.
11. How would you deploy Dex or Keycloak in a containerized setup using Ansible? What role boundaries would you create (e.g., app, certs, ingress)?
	- Answer: Create roles: `dex/keycloak` (deploy container image), `certs` (manage TLS via certbot or ACME), `ingress` (configure Nginx/HAProxy or k8s ingress), and `monitoring` (expose metrics). Use docker-compose or systemd units for container runtime, and keep credentials in vault.
12. When configuring firewalls and kernel networking parameters, how do you validate changes safely and provide rollback paths?
	- Answer: Use `--check`/dry-run for validation where available, stage changes during maintenance windows, add pre-checks and post-checks (connectivity tests), and implement a rollback playbook or automated reversal if connectivity is lost. Always keep console access or out-of-band recovery.

### Testing, CI, and Quality
13. What tools and approaches do you use to test Ansible roles/playbooks (molecule, testinfra, ansible-lint)? Describe a simple CI pipeline for a role.
	- Answer: Use `molecule` with Docker or Vagrant drivers to spin test instances, `testinfra` or `serverspec` for assertions, and `ansible-lint` for style. CI pipeline: on PR run `ansible-lint`, run `molecule test` (unit + converge + verify) and report results.
14. How do you ensure idempotency and that playbooks are safe to run repeatedly during automated tests?
	- Answer: Write tasks using built-in modules (not shell) where possible, assert state with `changed_when`/`check_mode`, run tests twice in CI to ensure second run results in zero changes, and write unit tests for modules that interact with external systems.
15. Describe how you'd use Ansible to manage TLS certificates (Let's Encrypt) across many hosts reliably and how you'd test renewal.
	- Answer: Use a centralized certificate manager (certbot with DNS challenge or an ACME client) or a role that requests certs and distributes them via Ansible Vault or secure copy. Automate renewal hooks and test renewal by simulating expiry in staging. Use healthchecks and monitoring to alert failed renewals.

### Troubleshooting & Operations
16. A playbook that worked yesterday now fails on a host; how do you diagnose and repair it? Which logs and tools do you use?
	- Answer: Reproduce locally with `--limit` to the host and increase verbosity (`-vvv`), check Ansible output and target host logs (`/var/log/syslog`, `journalctl`), verify network and package repository reachability, and inspect recent changes (git history, cron jobs). Check permissions and file contents.
17. How do you handle long-running tasks (e.g., kernel compilation) in Ansible and report progress or resume after failure?
	- Answer: Run long tasks asynchronously with `async`/`poll`, log output to files and fetch them, or run the build in CI/worker nodes and distribute artifacts. Use id files or markers to resume. Ensure tasks are segmented (build, install, reboot) and require explicit approval for reboots.
18. In a production environment, how would you orchestrate a rolling update of a web fleet managed via Ansible while avoiding downtime?
	- Answer: Use a rolling strategy: update one host at a time, drain traffic from a load balancer, run health checks after updates, and re-add to LB. Use orchestration tools or a playbook with serial: 1 and health checks, and have automatic rollback upon failures.

---

## Topic deep-dives — explanations and related questions

### Automated provisioning & evolving Continuous Delivery pipelines
Explanation:
Automated provisioning and CD pipelines are built around clear separation of concerns: immutable infrastructure (images, templates), infrastructure-as-code (Terraform, CloudFormation), configuration management (Ansible, Puppet), and CI/CD orchestration (Jenkins, GitHub Actions, GitLab CI). Start by modeling environment blueprints, build golden images (Packer) with baked-in agents, and codify networking and security. Pipeline evolution requires tests at every stage (unit/lint, integration, smoke), artifact promotion (dev → staging → prod), staged deployments (canary/blue-green), observability and automated rollback. Secrets and credentials should be managed by Vault or cloud secret stores; policies, access controls and artifact signing improve safety.

Related interview questions:
1. Describe an end-to-end automated provisioning flow from image build to production deployment.
2. How do you incorporate tests into your CD pipeline to reduce risk when promoting artifacts?
3. When would you choose immutable images vs configuration management at boot time? List trade-offs.
4. How do you design a pipeline that supports canary releases and automated rollback?
5. What metrics and alerts do you add to guardrails for CD (SLOs, error rates, deployment latency)?
6. How do you automate secrets, artifact signing, and access control in a pipeline?

### Automated provisioning for physical environments and Cloud (AWS, GCP)
Explanation:
Provisioning physical servers requires boot automation (PXE, iPXE), image provisioning (preseed Kickstart, cloud-init equivalents), and out-of-band management (IPMI, Redfish) for power and firmware. For cloud, use Terraform/CloudFormation to declare networks, subnets, routing, and compute instances; use cloud-init or configuration management to finalize. Network automation for both domains uses vendor APIs (NAPALM, vendor modules) or NetConf/REST for switches/routers. Hybrid setups require IPAM, VPN/Direct Connect, and careful design of CIDR allocations. Validate in labs, automate firmware and BIOS settings where possible, and provide idempotent playbooks for provisioning and configuration drift correction.

Related interview questions:
1. What tools and processes do you use to automate bare-metal provisioning and firmware management?
2. How do you design network automation to work across on-prem switches and cloud virtual networks?
3. Explain an approach to maintain consistent image and configuration state across cloud and physical servers.
4. How do you handle IP address management, VLAN planning and cross-site connectivity in automation?
5. What are common pitfalls when moving infrastructure provisioning code from dev to production and how do you avoid them?
6. Describe how you'd implement out-of-band recovery in automated workflows (e.g., failed network boot).

### Elasticsearch technologies — especially Kibana
Explanation:
Elasticsearch is a distributed search and analytics engine; Kibana is the visualization and management UI. Key concepts: indices, shards, replicas, mappings (schema), and ingest pipelines. Design indices for query patterns (time-based vs entity-based), use index lifecycle management (ILM) for retention, and tune shard counts by node capacity and expected query/ingest rates. Secure the cluster with TLS and authentication (native, proxy or SAML), and monitor with dedicated indices and metrics. Kibana dashboards should use efficient queries and saved searches; use Kibana spaces, roles and alerts for operations.

Related interview questions:
1. How do you design an index and shard strategy for a high-ingest time-series dataset?
2. Explain mappings and why dynamic mapping can be dangerous in production.
3. How do you secure Elasticsearch and Kibana in a multi-tenant environment?
4. Describe snapshot/restore for backup and cross-cluster replication for DR.
5. What techniques do you use to troubleshoot slow queries and high GC/heap usage?
6. How would you automate Kibana dashboard deployment and upgrades?

### Apache Kafka and Druid
Explanation:
Apache Kafka is a distributed streaming platform for high-throughput messaging with topics, partitions and consumer groups. Key design choices: partitioning strategy, replication factor, retention policy, and choice of delivery semantics (at-most-once, at-least-once, exactly-once via transactions). Kafka Connect and Streams provide integration and stream processing. Apache Druid is a column-oriented, distributed OLAP data store optimized for time-series analytics and fast aggregations; ingestion can be batch or real-time (via Kafka). Druid uses segments stored in deep storage (S3/HDFS) and has historical/broker/coordinator nodes. Combining Kafka and Druid is common for streaming analytics: Kafka as the ingestion buffer, Druid for fast queries and dashboards.

Related interview questions:
1. How do you choose partition keys for Kafka topics to ensure even load and good consumer parallelism?
2. Explain trade-offs between retention, compaction, and cleanup policies in Kafka.
3. How would you implement exactly-once processing in a Kafka-based pipeline?
4. Describe how Druid ingests from Kafka and the role of segments and deep storage.
5. What monitoring and alerting would you set up for Kafka and Druid clusters?
6. How do you tune Kafka and Druid for low-latency queries at scale?

### Gluster and storage technologies
Explanation:
GlusterFS is a software-defined distributed filesystem composed of bricks (storage units) aggregated into volumes. It supports replication, striping, and distributed volumes. Design choices include replication factor, striping, and translator stacks (performance vs durability). Alternatives include Ceph (object + block + filesystem), NFS with HA controllers, or SAN. Storage design must consider performance (IOPS, throughput), durability (replication, erasure coding), backup strategy, and maintenance (rebalance, healing). For metadata-heavy workloads or small-file workloads, choose technologies optimized for metadata performance.

Related interview questions:
1. When would you choose GlusterFS over Ceph or a traditional SAN? List trade-offs.
2. How do you handle split-brain and heal operations in Gluster volumes?
3. Describe how you'd benchmark and capacity-plan a distributed filesystem for mixed read/write workloads.
4. What backup and snapshot strategies are appropriate for distributed filesystems?
5. How do you ensure consistent performance under rebalancing and failure scenarios?
6. Explain how you would automate storage provisioning and mounting across many hosts.

### Nginx and web server technologies
Explanation:
Nginx is a high-performance web server and reverse proxy used for TLS termination, caching, load balancing and as an ingress for applications. It supports upstream health checks, various load balancing algorithms, HTTP/2, gRPC, and edge features like rate-limiting and WAF integration. When designing Nginx architectures, consider TLS offload, caching policies, buffer sizes, worker processes and connections, and how to manage configuration changes without downtime (graceful reloads). For large systems, pair Nginx with a dedicated caching layer (Varnish) or CDN and use centralized configuration management and templating for consistency.

Related interview questions:
1. How do you configure Nginx for TLS best practices (ciphers, HSTS, HTTP/2)?
2. Explain strategies for caching dynamic content and invalidation.
3. How do you implement blue-green or canary deployments with Nginx as the reverse proxy/load balancer?
4. What tuning parameters in Nginx affect high-concurrency workloads and how do you choose them?
5. How would you automate certificate renewal and deployment across multiple Nginx instances?
6. Compare Nginx and HAProxy for load balancing — when to choose one over the other?

---

### Kubernetes / EKS integration workflows (explanation + questions)
Explanation:
Kubernetes (and managed distributions like Amazon EKS) is frequently used as the deployment platform for modern microservices and data platforms. When integrating the technologies discussed previously, you should choose which components run inside Kubernetes and which remain outside (managed services or VMs). Common patterns:

- Control plane and cluster provisioning: use Terraform or eksctl to provision EKS clusters (VPC, subnets, node groups / managed node groups or Fargate). Use Infrastructure-as-code to reproducibly create cluster networking and IAM roles.

- CI/CD integration: build container images in CI (GitHub Actions, Jenkins) and push to a registry (ECR/Artifact Registry). Use GitOps (ArgoCD/Flux) or pipeline-based deploys (kubectl, helm) to apply manifests or Helm charts; tie promotions to environment branches and automated tests.

- Service deployment and ingress: use Helm charts or Kustomize to template app manifests. Use an Ingress controller (NGINX Ingress, AWS ALB Ingress) for TLS termination and routing. Certificates are managed via cert-manager with ACME or integrated with AWS ACM for LB-level certs.

- Stateful/analytics stacks: Deploy Elasticsearch/Kibana, Kafka, Druid, and storage solutions carefully: either use managed services (Amazon OpenSearch Service / MSK / Druid Cloud) or run them in the cluster using StatefulSets and persistent volumes backed by EBS/EFS (on AWS) or S3 for deep storage. For high-throughput Kafka/Druid, consider using node groups with provisioned IO or dedicated storage classes.

- Storage and deep storage: use Kubernetes StorageClasses to provision PVs (dynamic provisioning with EBS, EFS, or CSI drivers). For distributed filesystems like Gluster or Ceph, either deploy via operators or use managed equivalents. Keep deep storage (Druid segments, ES snapshots) in object storage (S3/GCS) for durability.

- Observability and logging: run Prometheus and Grafana via the Prometheus Operator, and use Fluentd/Fluent Bit or Filebeat to ship logs to Elasticsearch. Use ServiceMonitors and PodMonitors for metrics discovery.

- Secrets and identity: use Kubernetes Secrets integrated with tools like SealedSecrets, external Secrets Operator, or Vault Agent Injector to avoid storing plaintext secrets. Use IAM roles for service accounts (IRSA) on EKS for secure cloud access.

- Scaling and resilience: rely on HPA/VPA and cluster autoscaler. For critical components (Kafka, Elasticsearch), maintain node anti-affinity and dedicated node pools. Use PodDisruptionBudgets and readiness/liveness probes to achieve safe rollouts.

Operational workflow summary (example):
1. Dev pushes code → CI builds container image and runs unit/integration tests.
2. Image pushed to registry → CI triggers deployment to dev cluster (or GitOps reconciler picks up manifest changes).
3. Smoke tests run → promote to staging via pipeline; run canary or blue-green tests.
4. On approval, promote to production cluster. Monitor via dashboards and set alerts for SLO breaches.

Related interview questions:
1. Describe how you'd provision an EKS cluster with Terraform and ensure node pools are isolated for different workloads.
2. How does GitOps (ArgoCD/Flux) change the way you design CD pipelines versus imperative Ansible deploys?
3. For stateful systems like Elasticsearch and Kafka, what are the pros/cons of running them inside Kubernetes vs using managed services?
4. How do you manage persistent volumes and deep storage for Druid or Elasticsearch on EKS?
5. Explain how you would secure secrets and service credentials in an EKS environment (IRSA, Vault, External Secrets).
6. How do you implement zero-downtime deployments for web apps running on EKS using Ingress and health checks?
7. Describe how you'd integrate monitoring and alerting for a Kafka + Druid pipeline running on EKS.
8. What are the operational differences when running log aggregation (Fluent Bit/Elastic) inside the cluster vs shipping to an external logging service?

