# Database Automation - Design, Develop, and Maintain Solutions

## Overview
Database automation involves creating systematic, repeatable processes for managing database operations including deployments, schema changes, data migrations, backups, monitoring, and maintenance tasks. This reduces manual errors, improves consistency, and accelerates delivery cycles.

---

## Key Concepts & Explanation

### 1. **Database Operations Automation**
Automating routine database tasks to ensure consistency, reduce downtime, and minimize human error.

#### Key Areas:
- **Schema Management**: Version-controlled database schemas with automated migrations
- **Data Migrations**: Automated data transformation and movement between environments
- **Backup & Recovery**: Scheduled backups with automated testing of restore procedures
- **Monitoring & Alerting**: Automated health checks, performance monitoring, and incident response
- **Provisioning**: Automated database instance creation and configuration
- **Rollouts**: Controlled, automated deployment of database changes across environments

### 2. **Database Rollout Strategies**
Different approaches to deploying database changes safely:

- **Blue-Green Deployments**: Maintain two identical environments, switch traffic after validation
- **Canary Releases**: Gradual rollout to subset of users before full deployment
- **Rolling Updates**: Sequential updates across database replicas/shards
- **Feature Flags**: Control feature visibility at application level while database changes are deployed
- **Backward-Compatible Changes**: Design changes that work with old and new application versions

### 3. **Challenges in Database Automation**
- **State Management**: Databases are stateful, requiring careful handling of existing data
- **Zero-Downtime Deployments**: Maintaining availability during schema changes
- **Rollback Complexity**: Database rollbacks are more complex than application code rollbacks
- **Data Integrity**: Ensuring consistency across distributed systems
- **Performance Impact**: Migrations can impact production performance
- **Multiple Environments**: Maintaining consistency across dev, staging, and production

---

## Potential Solutions & Implementation Strategies

### 1. **Database Migration Tools**

#### **Flyway** (Java-based)
```yaml
# flyway.conf
flyway.url=jdbc:postgresql://localhost:5432/mydb
flyway.user=dbuser
flyway.password=${DB_PASSWORD}
flyway.locations=filesystem:./sql/migrations
flyway.baselineOnMigrate=true
```

```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- V2__Add_user_status.sql
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
CREATE INDEX idx_users_status ON users(status);
```

**Automation Script:**
```bash
#!/bin/bash
# run-migration.sh

set -e

echo "Running database migrations..."
flyway -configFiles=flyway.conf migrate

echo "Migration completed successfully"
flyway -configFiles=flyway.conf info
```

#### **Liquibase** (XML/YAML/JSON/SQL)
```yaml
# changelog.yaml
databaseChangeLog:
  - changeSet:
      id: 1
      author: devops
      changes:
        - createTable:
            tableName: products
            columns:
              - column:
                  name: id
                  type: int
                  autoIncrement: true
                  constraints:
                    primaryKey: true
              - column:
                  name: name
                  type: varchar(255)
                  constraints:
                    nullable: false
              - column:
                  name: price
                  type: decimal(10,2)
      rollback:
        - dropTable:
            tableName: products
```

#### **Alembic** (Python/SQLAlchemy)
```python
# alembic/versions/001_create_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )
    op.create_index('idx_username', 'users', ['username'])

def downgrade():
    op.drop_index('idx_username')
    op.drop_table('users')
```

---

### 2. **CI/CD Pipeline Integration**

#### **GitLab CI Example**
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - deploy-dev
  - deploy-staging
  - deploy-production

variables:
  FLYWAY_VERSION: "9.22.0"

validate-migrations:
  stage: validate
  image: flyway/flyway:${FLYWAY_VERSION}
  script:
    - flyway -configFiles=flyway.conf validate
    - flyway -configFiles=flyway.conf info
  only:
    - merge_requests

test-migrations:
  stage: test
  image: postgres:15
  services:
    - postgres:15
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
  script:
    - apt-get update && apt-get install -y wget
    - wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/${FLYWAY_VERSION}/flyway-commandline-${FLYWAY_VERSION}-linux-x64.tar.gz | tar xvz
    - ./flyway-${FLYWAY_VERSION}/flyway -url=jdbc:postgresql://postgres:5432/testdb -user=testuser -password=testpass -locations=filesystem:./sql/migrations migrate
    - ./flyway-${FLYWAY_VERSION}/flyway info
  only:
    - merge_requests

deploy-dev:
  stage: deploy-dev
  image: flyway/flyway:${FLYWAY_VERSION}
  script:
    - export DB_PASSWORD=${DEV_DB_PASSWORD}
    - flyway -configFiles=flyway-dev.conf migrate
    - flyway info
  environment:
    name: development
  only:
    - develop

deploy-staging:
  stage: deploy-staging
  image: flyway/flyway:${FLYWAY_VERSION}
  script:
    - export DB_PASSWORD=${STAGING_DB_PASSWORD}
    - flyway -configFiles=flyway-staging.conf migrate
    - flyway info
  environment:
    name: staging
  when: manual
  only:
    - main

deploy-production:
  stage: deploy-production
  image: flyway/flyway:${FLYWAY_VERSION}
  script:
    - export DB_PASSWORD=${PROD_DB_PASSWORD}
    - flyway -configFiles=flyway-prod.conf migrate
    - flyway info
  environment:
    name: production
  when: manual
  only:
    - main
  needs:
    - deploy-staging
```

#### **GitHub Actions Example**
```yaml
# .github/workflows/database-deployment.yml
name: Database Deployment

on:
  push:
    branches: [main, develop]
    paths:
      - 'db/migrations/**'
  pull_request:
    paths:
      - 'db/migrations/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Flyway
        uses: joshuaavalon/flyway-action@v3
        with:
          version: 9.22.0
          
      - name: Validate Migrations
        run: |
          flyway -configFiles=flyway.conf validate
          flyway info

  test-migration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Migration on Test DB
        run: |
          flyway -url=jdbc:postgresql://localhost:5432/postgres \
                 -user=postgres \
                 -password=postgres \
                 -locations=filesystem:./db/migrations \
                 migrate

  deploy-production:
    runs-on: ubuntu-latest
    needs: [validate, test-migration]
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Production
        env:
          DB_PASSWORD: ${{ secrets.PROD_DB_PASSWORD }}
        run: |
          flyway -configFiles=flyway-prod.conf migrate
```

---

### 3. **Infrastructure as Code (IaC) for Database Provisioning**

#### **Terraform Example**
```hcl
# database.tf

# RDS PostgreSQL Instance
resource "aws_db_instance" "main" {
  identifier           = "${var.environment}-postgres-db"
  engine              = "postgres"
  engine_version      = "15.3"
  instance_class      = var.db_instance_class
  allocated_storage   = 100
  storage_encrypted   = true
  
  db_name  = var.database_name
  username = var.master_username
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  auto_minor_version_upgrade = true
  deletion_protection       = var.environment == "production" ? true : false
  skip_final_snapshot      = var.environment != "production"
  final_snapshot_identifier = "${var.environment}-postgres-final-snapshot"
  
  tags = {
    Name        = "${var.environment}-postgres"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Random password generation
resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Store password in AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.environment}/database/password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = var.master_username
    password = random_password.db_password.result
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.database_name
  })
}

# Security Group
resource "aws_security_group" "db" {
  name_prefix = "${var.environment}-db-"
  vpc_id      = var.vpc_id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "database_cpu" {
  alarm_name          = "${var.environment}-db-cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors RDS CPU utilization"
  alarm_actions       = [var.sns_topic_arn]
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }
}
```

#### **Ansible Playbook for Database Setup**
```yaml
# playbooks/setup-database.yml
---
- name: Setup and Configure Database
  hosts: database_servers
  become: yes
  vars:
    postgres_version: "15"
    db_name: "myapp"
    db_user: "appuser"
    
  tasks:
    - name: Install PostgreSQL
      apt:
        name:
          - postgresql-{{ postgres_version }}
          - postgresql-contrib
          - python3-psycopg2
        state: present
        update_cache: yes
        
    - name: Ensure PostgreSQL is running
      service:
        name: postgresql
        state: started
        enabled: yes
        
    - name: Create application database
      postgresql_db:
        name: "{{ db_name }}"
        state: present
      become_user: postgres
      
    - name: Create database user
      postgresql_user:
        name: "{{ db_user }}"
        password: "{{ db_password }}"
        db: "{{ db_name }}"
        priv: ALL
        state: present
      become_user: postgres
      
    - name: Configure PostgreSQL authentication
      template:
        src: templates/pg_hba.conf.j2
        dest: /etc/postgresql/{{ postgres_version }}/main/pg_hba.conf
        owner: postgres
        group: postgres
        mode: '0640'
      notify: restart postgresql
      
    - name: Configure PostgreSQL settings
      template:
        src: templates/postgresql.conf.j2
        dest: /etc/postgresql/{{ postgres_version }}/main/postgresql.conf
        owner: postgres
        group: postgres
        mode: '0644'
      notify: restart postgresql
      
    - name: Setup automated backups
      cron:
        name: "PostgreSQL backup"
        minute: "0"
        hour: "2"
        job: "/usr/local/bin/backup-postgres.sh {{ db_name }}"
        user: postgres
        
  handlers:
    - name: restart postgresql
      service:
        name: postgresql
        state: restarted
```

---

### 4. **Zero-Downtime Migration Strategies**

#### **Expand-Contract Pattern**
```sql
-- Phase 1: EXPAND - Add new column (backward compatible)
-- Deploy this first, application still uses old column
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Create trigger to sync data between old and new columns
CREATE OR REPLACE FUNCTION sync_email_columns()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email IS NOT NULL THEN
        NEW.email_address := NEW.email;
    END IF;
    IF NEW.email_address IS NOT NULL THEN
        NEW.email := NEW.email_address;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_email_trigger
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION sync_email_columns();

-- Backfill existing data (can be done in batches)
UPDATE users SET email_address = email WHERE email_address IS NULL;

-- Phase 2: Deploy new application version that uses email_address

-- Phase 3: CONTRACT - Remove old column (after application deployment)
DROP TRIGGER IF EXISTS sync_email_trigger ON users;
DROP FUNCTION IF EXISTS sync_email_columns();
ALTER TABLE users DROP COLUMN email;
```

#### **Online Schema Change Tools**

**gh-ost (GitHub's Online Schema Change)**
```bash
# gh-ost-migration.sh
#!/bin/bash

gh-ost \
  --user="root" \
  --password="${DB_PASSWORD}" \
  --host="db-master.example.com" \
  --database="myapp" \
  --table="users" \
  --alter="ADD COLUMN last_login TIMESTAMP NULL" \
  --allow-on-master \
  --max-load="Threads_running=25" \
  --critical-load="Threads_running=100" \
  --chunk-size=1000 \
  --throttle-control-replicas="db-replica1.example.com:3306" \
  --execute
```

**pt-online-schema-change (Percona Toolkit)**
```bash
# pt-osc-migration.sh
#!/bin/bash

pt-online-schema-change \
  --alter="ADD COLUMN status VARCHAR(20) DEFAULT 'active'" \
  --execute \
  --max-load="Threads_running=25" \
  --critical-load="Threads_running=100" \
  --chunk-size=1000 \
  --progress=time,30 \
  h=localhost,D=myapp,t=users
```

---

### 5. **Database Backup & Recovery Automation**

#### **Automated Backup Script (PostgreSQL)**
```bash
#!/bin/bash
# /usr/local/bin/backup-postgres.sh

set -e

# Configuration
DB_NAME="${1:-myapp}"
BACKUP_DIR="/var/backups/postgres"
S3_BUCKET="s3://my-company-db-backups"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Perform backup
echo "Starting backup of ${DB_NAME}..."
pg_dump -Fc ${DB_NAME} | gzip > ${BACKUP_FILE}

# Verify backup
if [ -f "${BACKUP_FILE}" ]; then
    echo "Backup created: ${BACKUP_FILE}"
    SIZE=$(du -h ${BACKUP_FILE} | cut -f1)
    echo "Backup size: ${SIZE}"
else
    echo "ERROR: Backup failed!"
    exit 1
fi

# Upload to S3
echo "Uploading to S3..."
aws s3 cp ${BACKUP_FILE} ${S3_BUCKET}/${DB_NAME}/ --storage-class STANDARD_IA

# Verify S3 upload
if aws s3 ls ${S3_BUCKET}/${DB_NAME}/$(basename ${BACKUP_FILE}) > /dev/null; then
    echo "Successfully uploaded to S3"
    
    # Remove local backup after successful upload
    rm ${BACKUP_FILE}
else
    echo "ERROR: S3 upload failed!"
    exit 1
fi

# Cleanup old backups from S3
echo "Cleaning up old backups..."
aws s3 ls ${S3_BUCKET}/${DB_NAME}/ | while read -r line; do
    FILE_DATE=$(echo $line | awk '{print $1" "$2}')
    FILE_NAME=$(echo $line | awk '{print $4}')
    FILE_EPOCH=$(date -d "$FILE_DATE" +%s)
    CURRENT_EPOCH=$(date +%s)
    DAYS_OLD=$(( ($CURRENT_EPOCH - $FILE_EPOCH) / 86400 ))
    
    if [ $DAYS_OLD -gt $RETENTION_DAYS ]; then
        echo "Deleting old backup: ${FILE_NAME} (${DAYS_OLD} days old)"
        aws s3 rm ${S3_BUCKET}/${DB_NAME}/${FILE_NAME}
    fi
done

echo "Backup completed successfully!"
```

#### **Kubernetes CronJob for Backups**
```yaml
# k8s/postgres-backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: databases
spec:
  schedule: "0 2 * * *"  # Every day at 2 AM
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: postgres-backup
            image: postgres:15
            env:
            - name: PGHOST
              value: postgres-service
            - name: PGDATABASE
              value: myapp
            - name: PGUSER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: username
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-access-key
            command:
            - /bin/bash
            - -c
            - |
              set -e
              DATE=$(date +%Y%m%d_%H%M%S)
              BACKUP_FILE="/tmp/backup_${DATE}.sql.gz"
              
              echo "Starting backup..."
              pg_dump -Fc | gzip > ${BACKUP_FILE}
              
              echo "Installing AWS CLI..."
              apt-get update && apt-get install -y awscli
              
              echo "Uploading to S3..."
              aws s3 cp ${BACKUP_FILE} s3://my-company-db-backups/postgres/
              
              echo "Backup completed successfully"
            volumeMounts:
            - name: backup-storage
              mountPath: /tmp
          volumes:
          - name: backup-storage
            emptyDir: {}
```

---

### 6. **Monitoring & Alerting Automation**

#### **Prometheus + Grafana Setup**
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:latest
    environment:
      DATA_SOURCE_NAME: "postgresql://exporter:${EXPORTER_PASSWORD}@postgres:5432/myapp?sslmode=disable"
    ports:
      - "9187:9187"
    depends_on:
      - postgres
      
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      
  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

```yaml
# alerts.yml
groups:
  - name: database_alerts
    interval: 30s
    rules:
      - alert: PostgreSQLDown
        expr: pg_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "PostgreSQL is down"
          description: "PostgreSQL instance {{ $labels.instance }} is down"
          
      - alert: HighConnections
        expr: pg_stat_database_numbackends / pg_settings_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High number of database connections"
          description: "Database connections at {{ $value | humanizePercentage }}"
          
      - alert: SlowQueries
        expr: rate(pg_stat_statements_mean_exec_time[5m]) > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow query detected"
          description: "Average query execution time is {{ $value }}ms"
          
      - alert: ReplicationLag
        expr: pg_replication_lag > 60
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Replication lag detected"
          description: "Replication is lagging by {{ $value }} seconds"
```

---

### 7. **Database Rollout Orchestration**

#### **Kubernetes Operator Pattern**
```yaml
# Custom Resource Definition for Database Migration
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databasemigrations.db.example.com
spec:
  group: db.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                database:
                  type: string
                version:
                  type: string
                strategy:
                  type: string
                  enum: [rolling, bluegreen, canary]
  scope: Namespaced
  names:
    plural: databasemigrations
    singular: databasemigration
    kind: DatabaseMigration
    shortNames:
    - dbmig
```

```yaml
# Example Database Migration Resource
apiVersion: db.example.com/v1
kind: DatabaseMigration
metadata:
  name: add-user-status
  namespace: production
spec:
  database: myapp
  version: "v2.5.0"
  strategy: rolling
  migrations:
    - name: "V2.5.0__add_user_status"
      checksum: "abc123def456"
  rollback:
    enabled: true
    onFailure: automatic
  validation:
    preCheck: true
    postCheck: true
  notifications:
    slack: "#database-ops"
    email: "devops@example.com"
```

#### **ArgoCD for GitOps-based Database Deployments**
```yaml
# argocd/database-migration-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: database-migrations
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/mycompany/database-migrations.git
    targetRevision: main
    path: migrations/production
  destination:
    server: https://kubernetes.default.svc
    namespace: databases
  syncPolicy:
    automated:
      prune: false
      selfHeal: false
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  hooks:
    - name: pre-sync-backup
      kind: Job
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command: ["/bin/bash", "-c"]
            args:
              - |
                pg_dump -h postgres-service -U admin myapp > /backup/pre-migration-$(date +%s).sql
```

---

### 8. **Testing Automation for Database Changes**

#### **Database Test Framework**
```python
# tests/test_migrations.py
import pytest
import psycopg2
from testcontainers.postgres import PostgresContainer

class TestDatabaseMigrations:
    @pytest.fixture(scope="class")
    def postgres_container(self):
        with PostgresContainer("postgres:15") as postgres:
            yield postgres
    
    @pytest.fixture
    def db_connection(self, postgres_container):
        conn = psycopg2.connect(postgres_container.get_connection_url())
        yield conn
        conn.close()
    
    def test_migration_v1_creates_users_table(self, db_connection):
        """Test that migration V1 creates users table correctly"""
        cursor = db_connection.cursor()
        
        # Run migration
        with open('migrations/V1__create_users_table.sql', 'r') as f:
            cursor.execute(f.read())
        
        # Verify table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        assert cursor.fetchone()[0] is True
        
        # Verify columns
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        columns = {row[0]: row[1] for row in cursor.fetchall()}
        
        assert 'id' in columns
        assert 'username' in columns
        assert 'email' in columns
        assert columns['username'] == 'character varying'
    
    def test_migration_v2_adds_status_column(self, db_connection):
        """Test that migration V2 adds status column"""
        cursor = db_connection.cursor()
        
        # Run migrations V1 and V2
        with open('migrations/V1__create_users_table.sql', 'r') as f:
            cursor.execute(f.read())
        with open('migrations/V2__add_user_status.sql', 'r') as f:
            cursor.execute(f.read())
        
        # Verify status column exists
        cursor.execute("""
            SELECT column_name, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'status'
        """)
        result = cursor.fetchone()
        assert result is not None
        assert 'active' in result[1]  # Check default value
    
    def test_migration_idempotency(self, db_connection):
        """Test that running migrations multiple times is safe"""
        cursor = db_connection.cursor()
        
        # Run migration twice
        with open('migrations/V1__create_users_table.sql', 'r') as f:
            migration_sql = f.read()
            cursor.execute(migration_sql)
            # This should not fail
            try:
                cursor.execute(migration_sql)
            except psycopg2.errors.DuplicateTable:
                db_connection.rollback()
                # Expected behavior - migration should check IF NOT EXISTS
                pass
    
    def test_rollback_functionality(self, db_connection):
        """Test that rollback works correctly"""
        cursor = db_connection.cursor()
        
        # Run migration
        with open('migrations/V2__add_user_status.sql', 'r') as f:
            cursor.execute(f.read())
        
        # Run rollback
        cursor.execute("ALTER TABLE users DROP COLUMN IF EXISTS status")
        
        # Verify column is removed
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'status'
            );
        """)
        assert cursor.fetchone()[0] is False
```

---

### 9. **Disaster Recovery Automation**

#### **Automated DR Failover Script**
```bash
#!/bin/bash
# dr-failover.sh

set -e

PRIMARY_HOST="db-primary.us-east-1.rds.amazonaws.com"
REPLICA_HOST="db-replica.us-west-2.rds.amazonaws.com"
APP_NAMESPACE="production"

echo "========================================="
echo "DATABASE DISASTER RECOVERY FAILOVER"
echo "========================================="

# 1. Verify primary is down
echo "Checking primary database status..."
if pg_isready -h ${PRIMARY_HOST} -p 5432 > /dev/null 2>&1; then
    echo "WARNING: Primary database is still accessible!"
    read -p "Do you want to continue with failover? (yes/no): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Failover cancelled."
        exit 0
    fi
fi

# 2. Promote replica to primary
echo "Promoting replica to primary..."
aws rds promote-read-replica \
    --db-instance-identifier db-replica-us-west-2 \
    --backup-retention-period 7

# Wait for promotion to complete
echo "Waiting for promotion to complete..."
aws rds wait db-instance-available \
    --db-instance-identifier db-replica-us-west-2

# 3. Update application configuration
echo "Updating application database connection..."
kubectl set env deployment/app \
    -n ${APP_NAMESPACE} \
    DB_HOST=${REPLICA_HOST}

# 4. Verify new connections
echo "Verifying database connectivity..."
sleep 10
if pg_isready -h ${REPLICA_HOST} -p 5432; then
    echo "✓ New primary is accessible"
else
    echo "✗ ERROR: Cannot connect to new primary!"
    exit 1
fi

# 5. Send notifications
echo "Sending notifications..."
curl -X POST ${SLACK_WEBHOOK} \
    -H 'Content-Type: application/json' \
    -d "{\"text\":\"🚨 Database failover completed. New primary: ${REPLICA_HOST}\"}"

echo "========================================="
echo "FAILOVER COMPLETED SUCCESSFULLY"
echo "New Primary: ${REPLICA_HOST}"
echo "========================================="
```

---

## Best Practices

### 1. **Version Control Everything**
- Store all database scripts in Git
- Use semantic versioning for migrations
- Tag releases for production deployments

### 2. **Always Test Migrations**
- Test in identical staging environment
- Use containerized databases for testing
- Implement automated testing in CI/CD

### 3. **Implement Rollback Strategies**
- Design backward-compatible changes when possible
- Always have rollback scripts ready
- Test rollback procedures regularly

### 4. **Monitor Everything**
- Track migration execution time
- Monitor database performance during deployments
- Set up alerts for failures

### 5. **Documentation**
- Document each migration clearly
- Maintain runbooks for manual interventions
- Keep database schema diagrams updated

### 6. **Security**
- Never commit credentials to version control
- Use secrets management (Vault, AWS Secrets Manager)
- Implement least-privilege access
- Encrypt backups at rest and in transit

### 7. **Performance Considerations**
- Run large migrations during low-traffic periods
- Use batch processing for data migrations
- Consider using online schema change tools for large tables
- Monitor query performance and optimize indexes

---

## Tools Ecosystem Summary

| Category | Tools | Use Case |
|----------|-------|----------|
| **Migration** | Flyway, Liquibase, Alembic, golang-migrate | Schema version control |
| **IaC** | Terraform, CloudFormation, Pulumi | Database provisioning |
| **Configuration** | Ansible, Chef, Puppet | Database setup and configuration |
| **CI/CD** | GitLab CI, GitHub Actions, Jenkins, ArgoCD | Automated deployments |
| **Monitoring** | Prometheus, Grafana, Datadog, New Relic | Performance and health monitoring |
| **Backup** | pgBackRest, Barman, AWS Backup | Automated backup and recovery |
| **Testing** | pytest, testcontainers, DBUnit | Migration testing |
| **Online Schema Change** | gh-ost, pt-online-schema-change | Zero-downtime migrations |
| **Secrets** | HashiCorp Vault, AWS Secrets Manager | Credential management |

---

## Conclusion

Database automation requires a combination of the right tools, processes, and cultural practices. Start with version-controlled migrations, implement CI/CD pipelines, automate testing, and gradually introduce advanced techniques like zero-downtime deployments and disaster recovery automation. The key is to make database changes as reliable, repeatable, and auditable as application code deployments.
