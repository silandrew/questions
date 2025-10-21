# CI/CD Pipelines Using Jenkins - Complete Guide

## Table of Contents
1. [Introduction to CI/CD](#introduction-to-cicd)
2. [What is Jenkins?](#what-is-jenkins)
3. [Jenkins Architecture](#jenkins-architecture)
4. [Jenkins Installation & Setup](#jenkins-installation--setup)
5. [Jenkins Pipeline Fundamentals](#jenkins-pipeline-fundamentals)
6. [Declarative vs Scripted Pipelines](#declarative-vs-scripted-pipelines)
7. [Jenkins Pipeline Syntax](#jenkins-pipeline-syntax)
8. [Jenkins Plugins](#jenkins-plugins)
9. [Integration with Version Control](#integration-with-version-control)
10. [Build, Test, and Deploy](#build-test-and-deploy)
11. [Jenkins Best Practices](#jenkins-best-practices)
12. [Security in Jenkins](#security-in-jenkins)
13. [Distributed Builds (Master-Slave)](#distributed-builds-master-slave)
14. [Jenkins with Docker](#jenkins-with-docker)
15. [Jenkins with Kubernetes](#jenkins-with-kubernetes)
16. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)

---

## Introduction to CI/CD

### What is CI/CD?

**CI/CD** stands for **Continuous Integration** and **Continuous Delivery/Deployment**.

#### **Continuous Integration (CI)**
Continuous Integration is a development practice where developers frequently merge their code changes into a central repository (like Git), after which automated builds and tests are run.

**Key Principles:**
- **Frequent commits**: Developers commit code multiple times per day
- **Automated builds**: Every commit triggers an automated build
- **Automated testing**: Automated tests run with each build
- **Fast feedback**: Developers get immediate feedback on their changes
- **Early bug detection**: Issues are caught early in the development cycle

**Benefits:**
- ✅ Reduces integration problems
- ✅ Catches bugs early
- ✅ Improves code quality
- ✅ Reduces time to release
- ✅ Increases developer productivity

#### **Continuous Delivery (CD)**
Continuous Delivery extends CI by automatically deploying all code changes to a testing and/or production environment after the build stage.

**Key Principles:**
- **Automated deployment pipeline**: Code flows through build → test → staging → production
- **Manual approval gate**: Human approval required for production deployment
- **Always deployment-ready**: Code in main branch is always in deployable state
- **Automated testing**: Comprehensive automated tests at each stage

#### **Continuous Deployment**
Continuous Deployment goes one step further than Continuous Delivery by automatically deploying every change that passes all stages of the pipeline to production **without manual intervention**.

**Difference:**
- **Continuous Delivery**: Manual approval before production
- **Continuous Deployment**: Fully automated to production

### Traditional Development vs CI/CD

**Traditional (Waterfall) Development:**
```
Developer → (weeks/months) → Integration → (days) → Testing → (days) → Deployment → (hours/days) → Production
                                    ↓
                            Integration Hell!
```
**Problems:**
- Long feedback cycles
- Integration conflicts
- Late bug discovery
- Risky deployments
- Slow time to market

**CI/CD Development:**
```
Developer → (minutes) → Commit → (seconds) → Automated Build → (minutes) → Automated Test → (minutes) → Deploy
              ↓                      ↓                              ↓                            ↓
         Quick feedback        Immediate alerts              Fast validation              Rapid delivery
```
**Benefits:**
- Short feedback cycles (minutes vs days)
- Early integration
- Early bug detection
- Safe, frequent deployments
- Fast time to market

### Real-World CI/CD Example

**Scenario:** E-commerce web application

**Without CI/CD:**
1. Developer writes code for 2 weeks
2. Commits to repository
3. QA team manually tests (3-5 days)
4. Bugs found, sent back to developer
5. Fixes take another week
6. Manual deployment on Friday night
7. Production issues discovered over weekend
8. Emergency fixes required
9. **Total time: 3-4 weeks**

**With CI/CD:**
1. Developer writes code, commits multiple times daily
2. Each commit triggers:
   - Automated build (2 minutes)
   - Automated unit tests (5 minutes)
   - Automated integration tests (10 minutes)
   - Automated security scans (5 minutes)
3. Code review happens on pull request
4. Merge triggers:
   - Deployment to staging (automatic)
   - Automated smoke tests
5. Manual approval for production
6. Automated deployment to production (blue-green)
7. Automated monitoring and rollback if issues
8. **Total time: Hours to 1 day**

---

## What is Jenkins?

**Jenkins** is an open-source automation server written in Java that helps automate the software development process through continuous integration and continuous delivery.

### History
- **Created:** 2011 (originally Hudson in 2004)
- **Creator:** Kohsuke Kawaguchi
- **Language:** Java
- **License:** MIT License
- **Governance:** Jenkins Project (part of Continuous Delivery Foundation)

### Key Features

#### 1. **Open Source & Free**
- No licensing costs
- Large community support
- Extensive documentation
- Active development

#### 2. **Easy Installation**
- Simple Java-based installation
- Available as:
  - WAR file
  - Docker container
  - Native packages (apt, yum, brew)
  - Cloud images (AWS, Azure, GCP)

#### 3. **Extensible Plugin Architecture**
- **1,800+ plugins** available
- Plugins for:
  - Source control (Git, SVN, Mercurial)
  - Build tools (Maven, Gradle, npm)
  - Cloud providers (AWS, Azure, GCP)
  - Containers (Docker, Kubernetes)
  - Testing frameworks
  - Notification systems

#### 4. **Pipeline as Code**
- Define pipelines in code (Jenkinsfile)
- Version controlled with application code
- Reusable and shareable
- Supports both Declarative and Scripted syntax

#### 5. **Distributed Builds**
- Master-Agent architecture
- Parallel execution
- Platform-specific builds
- Resource optimization

#### 6. **Rich Web UI**
- User-friendly interface
- Real-time build logs
- Visualization of pipeline stages
- Build history and trends

#### 7. **Integration Capabilities**
- Git/GitHub/GitLab/Bitbucket
- Docker and Kubernetes
- AWS, Azure, GCP
- Slack, Email, JIRA
- SonarQube, Nexus, Artifactory

### Jenkins Use Cases

1. **Continuous Integration**
   - Automated builds on every commit
   - Automated testing
   - Code quality checks

2. **Continuous Delivery/Deployment**
   - Automated deployments to environments
   - Production releases
   - Blue-green deployments

3. **Automated Testing**
   - Unit tests
   - Integration tests
   - Performance tests
   - Security scans

4. **Infrastructure as Code**
   - Terraform/CloudFormation deployments
   - Ansible playbook execution
   - Infrastructure provisioning

5. **Scheduled Jobs**
   - Database backups
   - Data processing
   - Report generation
   - Cleanup tasks

### When to Use Jenkins?

**✅ Use Jenkins When:**
- You need a self-hosted CI/CD solution
- You require extensive customization
- You have complex build requirements
- You want full control over infrastructure
- You have diverse technology stack
- Budget constraints (free and open-source)

**❌ Consider Alternatives When:**
- Simple projects with standard workflows (GitHub Actions)
- Fully cloud-native (AWS CodePipeline, Azure Pipelines)
- SaaS preference over self-hosting (CircleCI, Travis CI)
- Limited maintenance resources

---

## Jenkins Architecture

### Core Components

#### 1. **Jenkins Master (Controller)**
The main Jenkins server responsible for:
- Scheduling build jobs
- Dispatching builds to agents
- Monitoring agents
- Recording and presenting build results
- Serving the Jenkins UI
- Managing plugins and configuration

**Responsibilities:**
- Job configuration storage
- Build queue management
- Agent orchestration
- Serving HTTP requests
- Triggering builds

**Resource Usage:**
- Memory: 2-4 GB minimum
- CPU: Moderate (mainly for coordination)
- Disk: For build history, artifacts, and plugins

#### 2. **Jenkins Agent (formerly Slave)**
Machines that execute build jobs dispatched by the master.

**Types of Agents:**
- **Permanent Agents**: Always connected, dedicated servers
- **Cloud Agents**: Dynamically provisioned (AWS EC2, Docker, Kubernetes)
- **SSH Agents**: Connected via SSH
- **JNLP Agents**: Java Web Start agents

**Key Concepts:**
- **Executor**: A slot for running builds (e.g., 2 executors = 2 concurrent builds)
- **Node**: A machine (master or agent) with executors
- **Label**: Tag for grouping agents (e.g., "linux", "docker", "maven")

#### 3. **Jobs/Projects**
A job (or project) is a runnable task configured in Jenkins.

**Types of Jobs:**
- **Freestyle Project**: Simple, UI-configured jobs
- **Pipeline**: Pipeline as code (Jenkinsfile)
- **Multibranch Pipeline**: Pipeline for multiple branches
- **Organization Folder**: Scans entire GitHub org for Jenkinsfiles
- **Folder**: Organize jobs into folders

#### 4. **Build**
A single execution of a job.

**Build Properties:**
- Build number (incremental)
- Build status (Success, Failure, Unstable, Aborted)
- Console output
- Artifacts
- Test results
- Duration

#### 5. **Workspace**
A directory on an agent where Jenkins checks out source code and executes the build.

**Characteristics:**
- One workspace per job per agent
- Location: `/var/jenkins_home/workspace/` (Linux)
- Can be cleaned automatically or manually
- Reused across builds for efficiency

#### 6. **Plugins**
Extensions that add functionality to Jenkins.

**Plugin Categories:**
- Source Code Management (Git, SVN)
- Build Tools (Maven, Gradle, npm)
- Cloud (AWS, Azure, Docker, Kubernetes)
- Notifications (Slack, Email)
- Security (LDAP, OAuth, Role-Based Access)
- Reporting (HTML Publisher, JUnit)

### Jenkins Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Jenkins Master                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │   Web UI    │  │  REST API    │  │  Build Scheduler       │ │
│  └─────────────┘  └──────────────┘  └────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Job Configuration & Storage                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Plugin Manager                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬─────────────────┬─────────────────┬───────────────┘
             │                 │                 │
             │ SSH/JNLP        │ SSH/JNLP       │ SSH/JNLP
             ↓                 ↓                 ↓
   ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
   │  Jenkins Agent  │ │  Jenkins Agent  │ │  Jenkins Agent  │
   │   (Linux)       │ │   (Windows)     │ │   (Docker)      │
   │                 │ │                 │ │                 │
   │ Executors: 2    │ │ Executors: 4    │ │ Executors: 1    │
   │ Labels: linux,  │ │ Labels: windows,│ │ Labels: docker, │
   │         maven   │ │         .net    │ │         k8s     │
   │                 │ │                 │ │                 │
   │ Workspace:      │ │ Workspace:      │ │ Workspace:      │
   │ /workspace/job1 │ │ C:\workspace\   │ │ /workspace/     │
   └─────────────────┘ └─────────────────┘ └─────────────────┘
             │                 │                 │
             ↓                 ↓                 ↓
        Build Jobs         Build Jobs       Build Jobs
```

### Jenkins Workflow

#### Standard Jenkins Build Flow:

```
1. Trigger
   ├── Manual (user clicks "Build Now")
   ├── SCM Polling (Jenkins checks Git for changes)
   ├── Webhook (Git notifies Jenkins of push)
   ├── Scheduled (cron-like schedule)
   └── Upstream (triggered by another job)
   
2. Master Receives Build Request
   └── Adds job to build queue
   
3. Master Schedules Build
   ├── Checks agent availability
   ├── Matches agent labels with job requirements
   └── Assigns build to available executor on agent
   
4. Agent Executes Build
   ├── Checks out source code
   ├── Runs build steps (compile, test, package)
   ├── Collects artifacts
   └── Publishes results
   
5. Master Processes Results
   ├── Updates build status
   ├── Stores artifacts
   ├── Sends notifications
   └── Triggers downstream jobs (if configured)
```

### Detailed Pipeline Execution Flow

```
Developer Push → GitHub → Webhook → Jenkins Master
                                          ↓
                                    [Build Queue]
                                          ↓
                                    Check Labels
                                          ↓
                              ┌───────────┴───────────┐
                              ↓                       ↓
                     [Agent: label=docker]   [Agent: label=maven]
                              ↓                       ↓
                         Workspace              Workspace
                              ↓                       ↓
                    ┌─────────────────┐    ┌─────────────────┐
                    │ Stage: Checkout │    │ Stage: Build    │
                    │ - git clone     │    │ - mvn clean     │
                    └────────┬────────┘    │ - mvn install   │
                             ↓             └────────┬────────┘
                    ┌─────────────────┐             ↓
                    │ Stage: Build    │    ┌─────────────────┐
                    │ - docker build  │    │ Stage: Test     │
                    └────────┬────────┘    │ - mvn test      │
                             ↓             └────────┬────────┘
                    ┌─────────────────┐             ↓
                    │ Stage: Test     │    ┌─────────────────┐
                    │ - Run tests     │    │ Stage: Deploy   │
                    └────────┬────────┘    │ - deploy to ENV │
                             ↓             └─────────────────┘
                    ┌─────────────────┐
                    │ Stage: Push     │
                    │ - docker push   │
                    └────────┬────────┘
                             ↓
                       [Artifacts]
                             ↓
                    ┌─────────────────┐
                    │ Master Collects │
                    │ - Store results │
                    │ - Send alerts   │
                    └─────────────────┘
```

### Master-Agent Communication

#### **SSH Agent Connection:**
```
Master → SSH → Agent (port 22)
- Master initiates connection
- Uses SSH credentials
- Copies agent.jar to agent
- Starts agent process
```

#### **JNLP Agent Connection:**
```
Agent → JNLP → Master (port 50000)
- Agent initiates connection
- Downloads agent.jar from master
- Maintains persistent connection
- Good for agents behind firewall
```

#### **Docker Agent:**
```
Master → Docker API → Docker Host
- Master requests container
- Container launched with Jenkins agent
- Executes build
- Container destroyed after build
```

### Distributed Build Benefits

1. **Parallel Execution**
   - Multiple builds simultaneously
   - Faster feedback
   - Better resource utilization

2. **Platform Diversity**
   - Linux builds on Linux agents
   - Windows builds on Windows agents
   - macOS builds on macOS agents

3. **Specialized Environments**
   - Different JDK versions
   - Different tool installations
   - GPU-enabled agents for ML builds

4. **Resource Isolation**
   - Heavy builds don't affect master
   - Master remains responsive
   - Agent failures don't bring down master

5. **Scalability**
   - Add agents as needed
   - Cloud-based auto-scaling
   - Handle increased load

### Jenkins File System Structure

```
JENKINS_HOME/
├── config.xml                 # Main Jenkins configuration
├── credentials.xml            # Stored credentials
├── jobs/                      # Job configurations
│   ├── my-pipeline/
│   │   ├── config.xml         # Job configuration
│   │   ├── builds/            # Build history
│   │   │   ├── 1/
│   │   │   │   ├── build.xml  # Build metadata
│   │   │   │   ├── log        # Console output
│   │   │   │   └── archive/   # Archived artifacts
│   │   │   └── 2/
│   │   └── workspace/         # Job workspace
│   └── another-job/
├── plugins/                   # Installed plugins
│   ├── git.jpi
│   ├── workflow-aggregator.jpi
│   └── ...
├── users/                     # User accounts
├── secrets/                   # Encrypted secrets
├── nodes/                     # Agent configurations
│   ├── linux-agent/
│   └── windows-agent/
├── logs/                      # Jenkins logs
└── updates/                   # Plugin update info
```

**Important Directories:**
- **`JENKINS_HOME`**: Main directory (default: `/var/jenkins_home` or `~/.jenkins`)
- **`jobs/`**: All job configurations and history
- **`workspace/`**: Where builds execute
- **`plugins/`**: Installed plugins
- **`secrets/`**: Encrypted credentials and secrets

---

## Jenkins Installation & Setup

### Prerequisites

**System Requirements:**
- **Operating System**: Linux, Windows, macOS
- **Java**: OpenJDK 11 or 17 (LTS versions)
- **RAM**: Minimum 256 MB, Recommended 4+ GB
- **Disk**: Minimum 1 GB, Recommended 50+ GB for Jenkins home
- **Port**: 8080 (default), customizable

### Installation Methods

#### 1. **Docker Installation (Recommended for Development)**

**Why Docker?**
- ✅ Easy to install and remove
- ✅ Isolated environment
- ✅ Consistent across platforms
- ✅ Easy to upgrade

**Installation Steps:**

```bash
# Pull Jenkins LTS image
docker pull jenkins/jenkins:lts

# Run Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# Check if running
docker ps

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

**With Docker Compose:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: jenkins
    privileged: true
    user: root
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - JAVA_OPTS=-Djenkins.install.runSetupWizard=false
    restart: unless-stopped

volumes:
  jenkins_home:
```

```bash
# Start Jenkins
docker-compose up -d

# View logs
docker-compose logs -f jenkins

# Stop Jenkins
docker-compose down
```

#### 2. **Linux Installation (Ubuntu/Debian)**

```bash
# Update package index
sudo apt update

# Install Java 11
sudo apt install -y openjdk-11-jdk

# Verify Java installation
java -version

# Add Jenkins repository key
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# Add Jenkins repository
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Update package index again
sudo apt update

# Install Jenkins
sudo apt install -y jenkins

# Start Jenkins
sudo systemctl start jenkins

# Enable Jenkins to start on boot
sudo systemctl enable jenkins

# Check Jenkins status
sudo systemctl status jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

#### 3. **Linux Installation (RedHat/CentOS)**

```bash
# Install Java
sudo yum install -y java-11-openjdk-devel

# Add Jenkins repository
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
  
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# Install Jenkins
sudo yum install -y jenkins

# Start and enable Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Check status
sudo systemctl status jenkins

# Configure firewall
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload

# Get initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

#### 4. **Windows Installation**

**Option A: Windows Installer**

1. Download Jenkins Windows installer from [jenkins.io](https://jenkins.io)
2. Run the installer (.msi file)
3. Follow installation wizard
4. Jenkins installs as Windows service
5. Access at `http://localhost:8080`

**Option B: WAR File**

```cmd
# Download jenkins.war from jenkins.io

# Install Java first (if not installed)
# Download from: https://adoptium.net/

# Run Jenkins
java -jar jenkins.war

# Custom port
java -jar jenkins.war --httpPort=9090

# Access at http://localhost:8080
```

#### 5. **macOS Installation**

**Using Homebrew:**

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Jenkins LTS
brew install jenkins-lts

# Start Jenkins
brew services start jenkins-lts

# Stop Jenkins
brew services stop jenkins-lts

# Restart Jenkins
brew services restart jenkins-lts

# Get initial password
cat ~/.jenkins/secrets/initialAdminPassword
```

#### 6. **Kubernetes Installation (Helm)**

```bash
# Add Jenkins Helm repository
helm repo add jenkins https://charts.jenkins.io
helm repo update

# Create namespace
kubectl create namespace jenkins

# Install Jenkins with Helm
helm install jenkins jenkins/jenkins \
  --namespace jenkins \
  --set controller.serviceType=LoadBalancer \
  --set controller.adminPassword=admin123

# Get Jenkins URL
export SERVICE_IP=$(kubectl get svc --namespace jenkins jenkins --template "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
echo "Jenkins URL: http://$SERVICE_IP:8080"

# Get admin password
kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo
```

### Initial Setup Wizard

After installation, access Jenkins at `http://localhost:8080` (or your server IP).

#### Step 1: Unlock Jenkins

```
┌─────────────────────────────────────────────┐
│         Unlock Jenkins                      │
│                                             │
│  Please copy the password from either       │
│  location and paste it below.               │
│                                             │
│  /var/jenkins_home/secrets/                 │
│  initialAdminPassword                       │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │ [Paste password here]              │    │
│  └────────────────────────────────────┘    │
│                                             │
│              [Continue]                     │
└─────────────────────────────────────────────┘
```

**Get the password:**
```bash
# Docker
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Linux
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# macOS
cat ~/.jenkins/secrets/initialAdminPassword
```

#### Step 2: Customize Jenkins

**Option A: Install Suggested Plugins (Recommended for beginners)**
- Git
- Pipeline
- GitHub
- Credentials
- SSH Build Agents
- and ~50 other common plugins

**Option B: Select Plugins to Install (For advanced users)**
- Choose specific plugins
- Skip unnecessary ones
- Can install more later

**Recommended Plugins for CI/CD:**
- ✅ Pipeline (workflow-aggregator)
- ✅ Git plugin
- ✅ GitHub plugin
- ✅ Docker Pipeline
- ✅ Kubernetes plugin
- ✅ Blue Ocean (modern UI)
- ✅ Credentials Binding
- ✅ Email Extension
- ✅ Slack Notification
- ✅ JUnit
- ✅ HTML Publisher

#### Step 3: Create First Admin User

```
Username: admin
Password: ********
Full name: Administrator
Email: admin@company.com
```

#### Step 4: Instance Configuration

```
Jenkins URL: http://localhost:8080/
(or your domain: https://jenkins.company.com/)
```

#### Step 5: Jenkins is Ready!

```
┌─────────────────────────────────────────────┐
│         Jenkins is ready!                   │
│                                             │
│  Your Jenkins installation is complete!     │
│                                             │
│         [Start using Jenkins]               │
└─────────────────────────────────────────────┘
```

### Post-Installation Configuration

#### 1. **Configure System Settings**

Navigate to: **Manage Jenkins → System**

**Important Settings:**
- **# of executors**: Number of concurrent builds on master (set to 0 for master)
- **Jenkins Location**: Jenkins URL and admin email
- **GitHub Server**: Configure GitHub integration
- **Email Notification**: SMTP server configuration

#### 2. **Configure Global Tool Configuration**

Navigate to: **Manage Jenkins → Global Tool Configuration**

**Configure Tools:**
- **JDK installations**
- **Git installations**
- **Maven installations**
- **Gradle installations**
- **Node.js installations**
- **Docker installations**

**Example: Configure Maven**
```
Name: Maven 3.9
Install automatically: ✓
Version: 3.9.5
```

#### 3. **Configure Security**

Navigate to: **Manage Jenkins → Security**

**Security Realm (Authentication):**
- Jenkins' own user database
- LDAP
- Active Directory
- SAML Single Sign-On
- GitHub OAuth

**Authorization:**
- Anyone can do anything (Not recommended for production!)
- Legacy mode (Not recommended)
- Logged-in users can do anything
- Matrix-based security (Recommended)
- Project-based Matrix Authorization (Most flexible)
- Role-Based Strategy (Plugin required)

**Example: Matrix-based Security**
```
User/Group           | Overall/Read | Overall/Administer | Job/Build | Job/Read
---------------------|--------------|--------------------|-----------|-----------
Anonymous            |      ✓       |                    |           |
Authenticated Users  |      ✓       |                    |     ✓     |    ✓
admin                |      ✓       |         ✓          |     ✓     |    ✓
developers           |      ✓       |                    |     ✓     |    ✓
```

#### 4. **Configure Credentials**

Navigate to: **Manage Jenkins → Credentials → System → Global credentials**

**Add credentials for:**
- Git (username/password or SSH key)
- Docker registries (username/password)
- Cloud providers (AWS, Azure, GCP)
- Deployment servers (SSH keys)
- Slack/Email (API tokens)

**Credential Types:**
- **Username with password**
- **SSH Username with private key**
- **Secret text**
- **Secret file**
- **Certificate**

#### 5. **Install Additional Plugins**

Navigate to: **Manage Jenkins → Plugins → Available plugins**

**Essential Plugins:**
```
☑ Blue Ocean (Modern UI)
☑ Pipeline: AWS Steps
☑ Pipeline: GitHub
☑ Pipeline: Docker
☑ Kubernetes
☑ Ansible
☑ SonarQube Scanner
☑ JaCoCo (Code coverage)
☑ Checkstyle (Code quality)
☑ Email Extension Template
☑ Slack Notification
☑ Build Timeout
☑ Timestamper
☑ Workspace Cleanup
```

#### 6. **Configure Agents (Optional)**

Navigate to: **Manage Jenkins → Nodes → New Node**

**Add Agent:**
```
Node name: linux-agent-1
Type: Permanent Agent

Remote root directory: /home/jenkins
Labels: linux docker maven
Usage: Use this node as much as possible
Launch method: Launch agent via SSH
Host: 192.168.1.100
Credentials: jenkins-ssh-key
```

### Verify Installation

#### 1. **Create Test Job**

```
1. Click "New Item"
2. Enter name: "test-job"
3. Select: "Freestyle project"
4. Click OK
5. Build Steps → Add build step → Execute shell
6. Command: echo "Hello Jenkins!"
7. Save
8. Click "Build Now"
9. Check Console Output
```

Expected output:
```
Started by user admin
Running as SYSTEM
Building in workspace /var/jenkins_home/workspace/test-job
[test-job] $ /bin/sh -xe /tmp/jenkins123456.sh
+ echo Hello Jenkins!
Hello Jenkins!
Finished: SUCCESS
```

#### 2. **Check System Information**

Navigate to: **Manage Jenkins → System Information**

Verify:
- Jenkins version
- Java version
- OS version
- Available memory
- Disk space

#### 3. **Check Plugins**

Navigate to: **Manage Jenkins → Plugins → Installed plugins**

Verify essential plugins are installed and up-to-date.

### Backup Jenkins

**Important Files to Backup:**
- `JENKINS_HOME/` (entire directory)
  - `config.xml` (main configuration)
  - `jobs/` (all jobs)
  - `users/` (user accounts)
  - `credentials.xml` (credentials)
  - `plugins/` (installed plugins)

**Backup Methods:**

**Option 1: File System Backup**
```bash
# Stop Jenkins
sudo systemctl stop jenkins

# Create backup
sudo tar -czf jenkins-backup-$(date +%Y%m%d).tar.gz /var/lib/jenkins/

# Start Jenkins
sudo systemctl start jenkins
```

**Option 2: Periodic Backup Plugin**
```
1. Install "Periodic Backup" plugin
2. Manage Jenkins → Periodic Backup Manager
3. Configure backup location and schedule
4. Set retention policy
```

**Option 3: ThinBackup Plugin**
```
1. Install "ThinBackup" plugin
2. Manage Jenkins → ThinBackup
3. Configure backup directory
4. Set backup schedule (e.g., daily at 2 AM)
5. Exclude workspace and build records
```

**Docker Volume Backup:**
```bash
# Backup Jenkins volume
docker run --rm \
  -v jenkins_home:/source \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/jenkins-backup.tar.gz -C /source .

# Restore Jenkins volume
docker run --rm \
  -v jenkins_home:/target \
  -v $(pwd):/backup \
  ubuntu \
  tar xzf /backup/jenkins-backup.tar.gz -C /target
```

---

## Jenkins Pipeline Fundamentals

### What is a Jenkins Pipeline?

A **Jenkins Pipeline** is a suite of plugins that supports implementing and integrating **continuous delivery pipelines** into Jenkins. It provides an extensible set of tools for modeling simple-to-complex delivery pipelines "as code" via the Pipeline DSL (Domain-Specific Language).

### Key Concepts

#### 1. **Pipeline**
The entire CD/CI process defined as code.

#### 2. **Node**
A machine that executes the pipeline (master or agent).

#### 3. **Stage**
A distinct phase in the pipeline (e.g., Build, Test, Deploy).
- Stages show up in the Blue Ocean visualization
- Useful for organizing work and understanding progress

#### 4. **Step**
A single task within a stage (e.g., run shell command, checkout code).

#### 5. **Agent**
Specifies where the pipeline or stage will execute.

**Agent Types:**
- `any`: Run on any available agent
- `none`: No global agent (specify per stage)
- `label`: Run on agent with specific label
- `docker`: Run in a Docker container
- `kubernetes`: Run in Kubernetes pod

### Pipeline Structure

```
Pipeline
  ├── Agent (where to run)
  ├── Environment (variables)
  ├── Options (pipeline options)
  ├── Parameters (build parameters)
  ├── Triggers (when to run)
  ├── Tools (auto-install tools)
  └── Stages
       ├── Stage 1: Checkout
       │    ├── Agent (optional, overrides global)
       │    ├── Environment (optional, stage-specific)
       │    ├── Steps
       │    │    ├── Step 1
       │    │    ├── Step 2
       │    │    └── Step 3
       │    └── Post actions (optional)
       │
       ├── Stage 2: Build
       │    └── Steps
       │
       ├── Stage 3: Test
       │    └── Steps
       │
       ├── Stage 4: Deploy
       │    └── Steps
       │
       └── Post Actions (cleanup, notifications)
```

### Simple Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'mvn clean package'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'mvn test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh './deploy.sh'
            }
        }
    }
}
```

**Visual Representation:**
```
┌──────────────────────────────────────────────────────────────┐
│  Pipeline: my-app                                            │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Build      │    Test      │   Deploy     │   Status       │
│   ✓ 30s      │    ✓ 45s     │   ✓ 20s      │   SUCCESS      │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### Pipeline Benefits

#### 1. **Pipeline as Code**
- Stored in version control (Jenkinsfile)
- Code review process
- Track changes over time
- Branch-specific pipelines

#### 2. **Durable**
- Survives Jenkins restarts
- Pipeline can continue after master restart

#### 3. **Pausable**
- Can pause for human input
- Can wait for external events

#### 4. **Versatile**
- Supports complex workflows
- Conditional logic
- Parallel execution
- Error handling

#### 5. **Extensible**
- Custom steps via plugins
- Shared libraries
- Reusable functions

### Jenkinsfile

A **Jenkinsfile** is a text file that contains the definition of a Jenkins Pipeline.

**Location Options:**
1. **In SCM (Source Code Management)** - Recommended
   - Stored in project repository
   - Versioned with code
   - Filename: `Jenkinsfile` (at repository root)

2. **Inline in Jenkins UI**
   - Defined in job configuration
   - Not versioned with code
   - Good for testing

**Example Jenkinsfile in Repository:**
```
my-project/
├── src/
├── tests/
├── pom.xml
├── Jenkinsfile           ← Pipeline definition
└── README.md
```

**Basic Jenkinsfile:**
```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/user/repo.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean install'
            }
        }
    }
}
```

### Creating Your First Pipeline

#### Method 1: Inline Pipeline in Jenkins UI

**Steps:**
1. Click **"New Item"**
2. Enter name: `my-first-pipeline`
3. Select: **"Pipeline"**
4. Click **OK**
5. Scroll to **"Pipeline"** section
6. Definition: **"Pipeline script"**
7. Enter pipeline code:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Hello') {
            steps {
                echo 'Hello, Jenkins Pipeline!'
            }
        }
        
        stage('Build Info') {
            steps {
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "Job Name: ${env.JOB_NAME}"
                sh 'date'
                sh 'hostname'
            }
        }
    }
}
```

8. Click **"Save"**
9. Click **"Build Now"**
10. Check **"Console Output"**

#### Method 2: Pipeline from SCM (Jenkinsfile)

**Steps:**

1. **Create Jenkinsfile in your repository:**

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from SCM'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building application'
                sh 'echo "Build commands here"'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests'
                sh 'echo "Test commands here"'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

2. **Commit and push Jenkinsfile:**
```bash
git add Jenkinsfile
git commit -m "Add Jenkinsfile"
git push origin main
```

3. **Create Pipeline Job in Jenkins:**
   - Click **"New Item"**
   - Enter name: `my-scm-pipeline`
   - Select: **"Pipeline"**
   - Click **OK**
   - Definition: **"Pipeline script from SCM"**
   - SCM: **Git**
   - Repository URL: `https://github.com/user/repo.git`
   - Credentials: (select or add)
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
   - Click **"Save"**

4. **Run Pipeline:**
   - Click **"Build Now"**
   - Watch stage view
   - Check console output

### Pipeline Visualization

Jenkins provides multiple ways to visualize pipelines:

#### 1. **Stage View (Classic UI)**
```
┌──────────────────────────────────────────────────────────────┐
│  Build #5 - Success - 2 min 30 sec ago                       │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│  Checkout   │   Build     │    Test     │    Deploy        │
│  ✓ 10s      │   ✓ 45s     │   ✓ 30s     │    ✓ 25s         │
└─────────────┴─────────────┴─────────────┴──────────────────┘
```

#### 2. **Blue Ocean (Modern UI)**
```
┌────────────────────────────────────────────────────────────┐
│  my-pipeline                                  #5 ✓ Success │
│  ═══════════════════════════════════════════════════════  │
│                                                            │
│  Checkout ──→ Build ──→ Test ──→ Deploy                   │
│    10s         45s       30s       25s                    │
│                                                            │
│  Total: 1 min 50s                                         │
└────────────────────────────────────────────────────────────┘
```

**Enable Blue Ocean:**
```
1. Manage Jenkins → Plugins
2. Search: "Blue Ocean"
3. Install without restart
4. Access via: http://jenkins-url/blue
```

#### 3. **Console Output**
```
Started by user admin
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/jenkins_home/workspace/my-pipeline
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
[Pipeline] echo
Code checked out from SCM
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build)
[Pipeline] echo
Building application
[Pipeline] sh
+ echo Build commands here
Build commands here
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS
```

### Common Pipeline Patterns

#### Pattern 1: Multi-Branch Pipeline

For projects with multiple branches (feature branches, develop, main):

```
my-project/
├── main branch
│   └── Jenkinsfile (production deployment)
├── develop branch
│   └── Jenkinsfile (staging deployment)
└── feature/new-feature branch
    └── Jenkinsfile (dev deployment)
```

**Create Multi-Branch Pipeline:**
1. New Item → **Multibranch Pipeline**
2. Branch Sources → Add source → Git
3. Repository URL
4. Scan Multibranch Pipeline Triggers
5. Build Configuration → Script Path: `Jenkinsfile`
6. Save

**Jenkins will:**
- Scan repository for branches
- Create pipeline job for each branch with Jenkinsfile
- Auto-trigger builds on push
- Auto-remove jobs when branch deleted

#### Pattern 2: Parameterized Pipeline

Accept user input before running:

```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Select deployment environment'
        )
        string(
            name: 'VERSION',
            defaultValue: '1.0.0',
            description: 'Version to deploy'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run tests before deployment'
        )
    }
    
    stages {
        stage('Deploy') {
            steps {
                echo "Deploying version ${params.VERSION} to ${params.ENVIRONMENT}"
                script {
                    if (params.RUN_TESTS) {
                        echo "Running tests..."
                    } else {
                        echo "Skipping tests"
                    }
                }
            }
        }
    }
}
```

When you click "Build Now", Jenkins prompts for parameters.

#### Pattern 3: Pipeline with Manual Approval

Pause pipeline for human approval:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        
        stage('Approval') {
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
            }
        }
        
        stage('Deploy to Production') {
            steps {
                echo 'Deploying to production...'
            }
        }
    }
}
```

Pipeline pauses at Approval stage until someone clicks "Deploy" or "Abort".

---

## Declarative vs Scripted Pipelines

Jenkins supports two syntaxes for defining pipelines:
1. **Declarative Pipeline** (Recommended, introduced in 2016)
2. **Scripted Pipeline** (Original, more powerful but complex)

### Declarative Pipeline

**Characteristics:**
- ✅ Structured, opinionated syntax
- ✅ Easier to read and write
- ✅ Better error checking
- ✅ Recommended for most use cases
- ✅ Rich visual representation in Blue Ocean
- ❌ Less flexible than Scripted

**Structure:**
```groovy
pipeline {
    // Declarative directives
    agent any
    environment { }
    options { }
    parameters { }
    triggers { }
    tools { }
    
    stages {
        stage('Stage 1') {
            steps {
                // Steps here
            }
        }
    }
    
    post {
        // Post-build actions
    }
}
```

**Example:**
```groovy
pipeline {
    agent any
    
    environment {
        APP_NAME = 'my-app'
        VERSION = '1.0.0'
    }
    
    stages {
        stage('Build') {
            steps {
                echo "Building ${env.APP_NAME} version ${env.VERSION}"
                sh 'mvn clean package'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
                junit 'target/surefire-reports/*.xml'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded!'
            emailext to: 'team@company.com',
                     subject: "SUCCESS: ${env.JOB_NAME}",
                     body: "Build ${env.BUILD_NUMBER} succeeded"
        }
        failure {
            echo 'Pipeline failed!'
            emailext to: 'team@company.com',
                     subject: "FAILURE: ${env.JOB_NAME}",
                     body: "Build ${env.BUILD_NUMBER} failed"
        }
    }
}
```

### Scripted Pipeline

**Characteristics:**
- ✅ Based on Groovy DSL
- ✅ Maximum flexibility
- ✅ Supports complex logic
- ✅ Imperative programming style
- ❌ More verbose
- ❌ Harder to maintain
- ❌ Requires Groovy knowledge

**Structure:**
```groovy
node {
    // Groovy code
    stage('Stage 1') {
        // Steps
    }
    stage('Stage 2') {
        // Steps
    }
}
```

**Example:**
```groovy
node {
    def appName = 'my-app'
    def version = '1.0.0'
    
    try {
        stage('Build') {
            echo "Building ${appName} version ${version}"
            sh 'mvn clean package'
        }
        
        stage('Test') {
            sh 'mvn test'
            junit 'target/surefire-reports/*.xml'
        }
        
        stage('Deploy') {
            if (env.BRANCH_NAME == 'main') {
                sh './deploy.sh'
            } else {
                echo 'Skipping deployment for non-main branch'
            }
        }
        
        // Success notification
        emailext to: 'team@company.com',
                 subject: "SUCCESS: ${env.JOB_NAME}",
                 body: "Build ${env.BUILD_NUMBER} succeeded"
                 
    } catch (Exception e) {
        // Failure notification
        emailext to: 'team@company.com',
                 subject: "FAILURE: ${env.JOB_NAME}",
                 body: "Build ${env.BUILD_NUMBER} failed: ${e.message}"
        throw e
    }
}
```

### Comparison

| Feature | Declarative | Scripted |
|---------|-------------|----------|
| **Syntax** | Structured, declarative | Imperative, Groovy |
| **Ease of Use** | ✅ Easier | ❌ Harder |
| **Readability** | ✅ Better | ❌ More verbose |
| **Validation** | ✅ Better error checking | ❌ Runtime errors |
| **Flexibility** | ❌ Limited | ✅ Maximum |
| **Learning Curve** | ✅ Gentler | ❌ Steeper (Groovy) |
| **Use Cases** | Standard pipelines | Complex logic |
| **Recommendation** | ✅ Recommended | Use when needed |
| **Blue Ocean Support** | ✅ Full support | ⚠️ Limited |

### When to Use Each

**Use Declarative When:**
- ✅ Standard CI/CD workflows
- ✅ Team has limited Groovy experience
- ✅ Want better tooling support
- ✅ Need good visual representation
- ✅ Want easier maintenance

**Use Scripted When:**
- ✅ Complex conditional logic
- ✅ Dynamic pipeline generation
- ✅ Need maximum flexibility
- ✅ Team comfortable with Groovy
- ✅ Existing scripted pipelines

### Mixing Declarative and Scripted

You can use `script` block in Declarative Pipeline for complex logic:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Complex Logic') {
            steps {
                script {
                    // Groovy code here
                    def environments = ['dev', 'staging', 'prod']
                    for (env in environments) {
                        echo "Processing ${env}"
                        if (env == 'prod') {
                            input message: "Deploy to ${env}?"
                        }
                        sh "deploy.sh ${env}"
                    }
                }
            }
        }
    }
}
```

### Recommendation

**For most users: Use Declarative Pipeline**
- Easier to learn and maintain
- Better error handling
- Future-proof (HashiCorp's focus)
- Good enough for 95% of use cases

**Use Scripted only when:**
- You need features not available in Declarative
- You have complex logic that's hard to express declaratively
- You're maintaining existing Scripted pipelines

---

*Note: This document continues with more sections. Would you like me to continue with the remaining sections?*

**Remaining sections to be added:**
- Jenkins Pipeline Syntax (detailed)
- Jenkins Plugins
- Integration with Version Control
- Build, Test, and Deploy strategies
- Jenkins Best Practices
- Security in Jenkins
- Distributed Builds (Master-Slave)
- Jenkins with Docker
- Jenkins with Kubernetes
- Monitoring and Troubleshooting
- Real-world examples and case studies
