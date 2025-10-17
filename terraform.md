# HashiCorp Certified: Terraform Associate (003) - Exam Questions & Answers

## Section 1: Understand Infrastructure as Code (IaC) concepts

### Q1: What is Infrastructure as Code (IaC)?
**Answer:** Infrastructure as Code (IaC) is the practice of managing and provisioning infrastructure through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. Benefits include:
- Version control for infrastructure
- Reproducible environments
- Automation and consistency
- Documentation through code
- Faster deployment and recovery

### Q2: What are the benefits of using IaC patterns?
**Answer:**
- **Automation**: Reduces manual tasks and human error
- **Consistency**: Ensures identical environments across dev, staging, and production
- **Speed**: Faster provisioning and deployment
- **Version Control**: Track changes and rollback if needed
- **Cost Reduction**: Better resource management and optimization
- **Documentation**: Code serves as documentation
- **Collaboration**: Teams can work together using version control

### Q3: What is the difference between mutable and immutable infrastructure?
**Answer:**
- **Mutable Infrastructure**: Infrastructure that is updated in-place. Changes are applied to existing servers. Risk of configuration drift.
- **Immutable Infrastructure**: Infrastructure that is replaced rather than updated. Once deployed, servers are never modified. If changes are needed, new servers are created and old ones are destroyed. Terraform follows the immutable pattern.

---

## Section 2: Understand Terraform's Purpose (vs Other IaC)

### Q4: What is Terraform and what are its key features?
**Answer:** Terraform is an open-source Infrastructure as Code tool created by HashiCorp. Key features:
- **Multi-cloud**: Works with AWS, Azure, GCP, and 3000+ providers
- **Declarative syntax**: Describe desired state, not steps
- **Execution plans**: Preview changes before applying
- **Resource graph**: Understands dependencies between resources
- **State management**: Tracks real-world resources
- **Modular**: Reusable configurations through modules

### Q5: How does Terraform differ from configuration management tools like Ansible, Chef, or Puppet?
**Answer:**
- **Terraform**: Provisioning tool - focuses on creating infrastructure (servers, networks, storage)
- **Ansible/Chef/Puppet**: Configuration management - focuses on installing and managing software on existing infrastructure
- **Terraform**: Declarative, immutable infrastructure approach
- **CM Tools**: Often procedural, mutable infrastructure
- **Best Practice**: Use Terraform to provision infrastructure, then use CM tools to configure applications

### Q6: What is Terraform Cloud and Terraform Enterprise?
**Answer:**
- **Terraform Cloud**: SaaS offering by HashiCorp for team collaboration, remote state management, policy enforcement, and remote runs. Free tier available.
- **Terraform Enterprise**: Self-hosted version with additional features for large enterprises, including SSO, auditing, and private network connectivity.
- Both provide remote operations, state management, private module registry, and team collaboration features.

---

## Section 3: Understand Terraform Basics

### Q7: What is the basic Terraform workflow?
**Answer:** The core Terraform workflow consists of three stages:
1. **Write**: Author infrastructure as code
2. **Plan**: Preview changes before applying (`terraform plan`)
3. **Apply**: Provision reproducible infrastructure (`terraform apply`)

Additional commands: `init`, `validate`, `destroy`

### Q8: What does `terraform init` do?
**Answer:** `terraform init` initializes a Terraform working directory by:
- Downloading required provider plugins
- Initializing backend for state storage
- Downloading modules referenced in configuration
- Creating `.terraform` directory for plugins and modules
- Must be run before any other Terraform commands

### Q9: What is the purpose of `terraform plan`?
**Answer:** `terraform plan`:
- Creates an execution plan showing what actions Terraform will take
- Compares current state with desired configuration
- Shows resources to be created, modified, or destroyed
- Does NOT make any actual changes to infrastructure
- Helps prevent unexpected changes
- Can save plan to file: `terraform plan -out=planfile`

### Q10: Explain `terraform apply` command.
**Answer:** `terraform apply`:
- Executes the actions proposed in a Terraform plan
- Creates, updates, or deletes infrastructure resources
- Updates state file to match real-world resources
- Shows plan and asks for confirmation (unless `-auto-approve` flag used)
- Can apply a saved plan: `terraform apply planfile`

### Q11: What is `terraform destroy` used for?
**Answer:** `terraform destroy`:
- Destroys all resources managed by the Terraform configuration
- Opposite of `terraform apply`
- Shows destruction plan before executing
- Useful for cleaning up test environments
- Can target specific resources: `terraform destroy -target=resource_type.resource_name`

### Q12: What is the purpose of `terraform validate`?
**Answer:** `terraform validate`:
- Validates the syntax and internal consistency of Terraform configuration
- Checks for errors in resource blocks, variables, and expressions
- Does NOT check provider credentials or remote state
- Does NOT check if the plan is deployable
- Fast way to catch syntax errors
- Should be run after `terraform init`

---

## Section 4: Use the Terraform CLI (Outside of Core Workflow)

### Q13: What is `terraform fmt` and when should you use it?
**Answer:** `terraform fmt`:
- Formats Terraform configuration files to canonical style
- Ensures consistent formatting across team
- Modifies files in-place
- Useful flags:
  - `-recursive`: Format subdirectories
  - `-check`: Check if files need formatting (CI/CD)
  - `-diff`: Show formatting changes

### Q14: How do you show the current state with Terraform?
**Answer:** Using `terraform show`:
- Displays human-readable output of state or plan
- `terraform show`: Show current state
- `terraform show planfile`: Show saved plan
- `terraform show -json`: Output in JSON format

### Q15: What is `terraform output` used for?
**Answer:** `terraform output`:
- Extracts output values from state file
- Useful for getting information about infrastructure
- Can be used in scripts and automation
- Examples:
  - `terraform output`: Show all outputs
  - `terraform output instance_ip`: Show specific output
  - `terraform output -json`: JSON format

### Q16: How do you import existing infrastructure into Terraform?
**Answer:** Using `terraform import`:
- Imports existing resources into Terraform state
- Syntax: `terraform import resource_type.resource_name resource_id`
- Example: `terraform import aws_instance.example i-1234567890abcdef0`
- Must write configuration block before importing
- Does NOT generate configuration automatically (use tools like `terraformer` for that)

### Q17: What is `terraform taint` and why was it deprecated?
**Answer:**
- **`terraform taint`**: Marked a resource for recreation on next apply
- **Deprecated in Terraform v0.15.2**
- **Replacement**: Use `terraform apply -replace="resource_type.resource_name"`
- Reason: More explicit and clear in execution plans

### Q18: How do you manage Terraform state with CLI commands?
**Answer:** State management commands:
- `terraform state list`: List resources in state
- `terraform state show resource_type.resource_name`: Show specific resource
- `terraform state mv`: Move resource in state (rename)
- `terraform state rm`: Remove resource from state (doesn't destroy)
- `terraform state pull`: Download remote state
- `terraform state push`: Upload state (use with caution)

### Q19: What is `terraform refresh` and is it still recommended?
**Answer:**
- **`terraform refresh`**: Updates state file to match real-world infrastructure
- **Deprecated as standalone command** in newer versions
- Now automatic part of `terraform plan` and `terraform apply`
- Use `-refresh-only` flag: `terraform apply -refresh-only`
- Can be disabled: `terraform plan -refresh=false`

### Q20: How do you use workspaces in Terraform?
**Answer:** Workspace commands:
- `terraform workspace list`: Show all workspaces
- `terraform workspace new <name>`: Create new workspace
- `terraform workspace select <name>`: Switch workspace
- `terraform workspace show`: Show current workspace
- `terraform workspace delete <name>`: Delete workspace
- Each workspace has separate state file
- Default workspace: "default"

---

## Section 5: Interact with Terraform Modules

### Q21: What is a Terraform module?
**Answer:** A Terraform module is:
- A container for multiple resources used together
- A way to organize and reuse Terraform code
- Any directory with `.tf` files is a module
- **Root module**: Main working directory
- **Child modules**: Modules called by root or other modules
- Can be sourced from local paths, Terraform Registry, Git, HTTP URLs

### Q22: How do you call a module in Terraform?
**Answer:**
```hcl
module "vpc" {
  source = "./modules/vpc"  # or registry URL
  
  # Input variables
  vpc_cidr = "10.0.0.0/16"
  environment = "production"
}
```
- Must run `terraform init` after adding module
- Access outputs: `module.vpc.vpc_id`

### Q23: What are module sources in Terraform?
**Answer:** Module sources can be:
- **Local paths**: `source = "./modules/vpc"`
- **Terraform Registry**: `source = "terraform-aws-modules/vpc/aws"`
- **GitHub**: `source = "github.com/user/repo"`
- **Git**: `source = "git::https://example.com/repo.git"`
- **Bitbucket**: `source = "bitbucket.org/user/repo"`
- **HTTP URLs**: `source = "https://example.com/module.zip"`
- **S3 buckets**: `source = "s3::https://s3.amazonaws.com/bucket/module.zip"`

### Q24: How do you access module outputs?
**Answer:**
```hcl
# In module
output "vpc_id" {
  value = aws_vpc.main.id
}

# In root module
resource "aws_subnet" "example" {
  vpc_id = module.vpc.vpc_id
}
```

### Q25: What is the Terraform Registry?
**Answer:**
- Public registry of Terraform modules and providers
- Located at registry.terraform.io
- Verified modules from HashiCorp partners
- Community modules
- Provider documentation
- Can host private registry in Terraform Cloud/Enterprise

### Q26: How do you version modules?
**Answer:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"  # Specific version
  # version = ">= 3.0.0, < 4.0.0"  # Version constraints
}
```
- Best practice: Always specify version in production
- Use semantic versioning
- Test updates before applying

---

## Section 6: Navigate Terraform Workflow

### Q27: What happens during `terraform init`?
**Answer:** During initialization:
1. Reads configuration files
2. Downloads provider plugins to `.terraform/providers/`
3. Downloads modules to `.terraform/modules/`
4. Initializes backend configuration
5. Creates `.terraform.lock.hcl` (dependency lock file)
6. Safe to run multiple times

### Q28: What is the `.terraform.lock.hcl` file?
**Answer:**
- Dependency lock file for providers
- Records exact provider versions used
- Ensures consistent provider versions across team
- Should be committed to version control
- Updated with `terraform init -upgrade`

### Q29: Explain the Terraform execution plan process.
**Answer:**
1. **Read Configuration**: Parse `.tf` files
2. **Read State**: Load current state
3. **Refresh**: Query real infrastructure (optional)
4. **Build Graph**: Create resource dependency graph
5. **Determine Changes**: Compare desired vs current state
6. **Generate Plan**: Create execution plan
7. **Display**: Show planned changes to user

Symbols: `+` create, `-` destroy, `~` update in-place, `-/+` replace

### Q30: What is the purpose of `-target` flag?
**Answer:**
- Focuses Terraform operations on specific resources
- Useful for: debugging, applying subset of changes
- Syntax: `terraform apply -target=resource_type.resource_name`
- Can specify multiple targets
- **Not recommended for regular use** - breaks dependency graph
- Use cases: emergency fixes, troubleshooting

---

## Section 7: Implement and Maintain State

### Q31: What is Terraform state?
**Answer:**
- File that tracks metadata about infrastructure
- Maps configuration to real-world resources
- Stores resource attributes for use in other resources
- Default: `terraform.tfstate` (local file)
- Contains sensitive information (encrypt/protect)
- Essential for Terraform operations

### Q32: Why is state important in Terraform?
**Answer:**
- **Mapping**: Links config to real resources
- **Metadata**: Tracks resource dependencies
- **Performance**: Avoids querying providers for every operation
- **Collaboration**: Enables team to work together
- **Change Detection**: Determines what needs to be updated

### Q33: What is remote state and why use it?
**Answer:** Remote state:
- State file stored in remote backend (S3, Azure Blob, Terraform Cloud)
- **Benefits**:
  - Team collaboration
  - State locking (prevents concurrent modifications)
  - Encryption at rest
  - Versioning/backup
  - Secure - no local sensitive data

### Q34: How do you configure a remote backend?
**Answer:**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```
- Run `terraform init` after configuring backend
- Use `-migrate-state` flag to move existing state

### Q35: What is state locking?
**Answer:**
- Prevents concurrent state modifications
- Automatically applied during operations
- Prevents corruption and conflicts
- Supported by: S3 (with DynamoDB), Azure Blob, Terraform Cloud, Consul
- Can disable: `terraform apply -lock=false` (not recommended)

### Q36: How do you share data between Terraform configurations?
**Answer:** Using `terraform_remote_state` data source:
```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

# Access outputs
resource "aws_instance" "example" {
  subnet_id = data.terraform_remote_state.vpc.outputs.subnet_id
}
```

### Q37: What are state file best practices?
**Answer:**
- **Never edit state file manually**
- Use remote state for teams
- Enable encryption
- Enable versioning/backup
- Use state locking
- Keep sensitive data in secrets manager
- Use `.gitignore` to exclude local state
- Regular backups
- Separate state files per environment

### Q38: How do you recover from state file issues?
**Answer:**
- **Backup**: Always have backups (versioning in S3)
- **State commands**: Use `terraform state` commands carefully
- **Import**: Re-import resources if needed
- **Manual recovery**: Edit state as last resort (JSON format)
- **Terraform Cloud**: Automatic state versioning and rollback

---

## Section 8: Read, Generate, and Modify Configuration

### Q39: What are the main Terraform configuration file types?
**Answer:**
- **`.tf` files**: Main configuration (HCL format)
- **`.tfvars` files**: Variable values
- **`.tf.json`**: JSON format configuration
- **`terraform.tfstate`**: State file
- **`.terraform.lock.hcl`**: Dependency lock file
- **`.terraformrc` / `terraform.rc`**: CLI configuration

### Q40: What is HCL (HashiCorp Configuration Language)?
**Answer:**
- Terraform's configuration language
- Declarative syntax
- Human-readable and machine-friendly
- Supports:
  - Blocks (resources, variables, outputs)
  - Arguments (key-value pairs)
  - Expressions (references, functions)
  - Comments (`#`, `//`, `/* */`)

### Q41: What are the main block types in Terraform?
**Answer:**
1. **terraform**: Terraform settings
2. **provider**: Provider configuration
3. **resource**: Infrastructure resources
4. **data**: Data sources (read-only)
5. **variable**: Input variables
6. **output**: Output values
7. **module**: Call child modules
8. **locals**: Local values

### Q42: How do you define and use variables in Terraform?
**Answer:**
```hcl
# Define variable
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
  
  validation {
    condition     = contains(["t2.micro", "t2.small"], var.instance_type)
    error_message = "Must be t2.micro or t2.small."
  }
}

# Use variable
resource "aws_instance" "example" {
  instance_type = var.instance_type
}
```

### Q43: What are the ways to assign variable values?
**Answer:**
1. **Default value** in variable definition
2. **Command line**: `-var="instance_type=t2.small"`
3. **Variable files**: `terraform.tfvars` or `*.auto.tfvars`
4. **Environment variables**: `TF_VAR_instance_type=t2.small`
5. **Interactive prompt** if no value provided

**Precedence** (highest to lowest):
- Command line flags
- `*.auto.tfvars` (alphabetical order)
- `terraform.tfvars`
- Environment variables

### Q44: What variable types does Terraform support?
**Answer:**
- **Primitive types**:
  - `string`: "hello"
  - `number`: 42, 3.14
  - `bool`: true, false
- **Complex types**:
  - `list(type)`: ["a", "b", "c"]
  - `set(type)`: Unique values
  - `map(type)`: {key1 = "value1"}
  - `object({attr=type})`: Complex object
  - `tuple([type])`: Fixed-length collection
- **Type `any`**: Any type (not recommended)

### Q45: What are output values and how are they used?
**Answer:**
```hcl
output "instance_ip" {
  description = "Public IP of instance"
  value       = aws_instance.example.public_ip
  sensitive   = false  # Set true for secrets
}
```
**Uses**:
- Display information after apply
- Pass data between modules
- Share data with other configurations (remote state)
- Query with `terraform output`

### Q46: What are local values (locals)?
**Answer:**
```hcl
locals {
  common_tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
  }
  
  instance_name = "${var.project}-${var.environment}-instance"
}

resource "aws_instance" "example" {
  tags = local.common_tags
  
  tags = {
    Name = local.instance_name
  }
}
```
- Assign names to expressions
- Reuse values multiple times
- Simplify complex expressions

### Q47: What are data sources in Terraform?
**Answer:**
- Read information from existing resources
- **Not managed** by Terraform
- Read-only operations
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*"]
  }
  
  owners = ["099720109477"]
}

resource "aws_instance" "example" {
  ami = data.aws_ami.ubuntu.id
}
```

### Q48: What are resource meta-arguments?
**Answer:**
- **`depends_on`**: Explicit dependencies
- **`count`**: Create multiple instances
- **`for_each`**: Create instances from map/set
- **`provider`**: Select non-default provider
- **`lifecycle`**: Lifecycle customization
- **`provisioner`**: Post-creation actions

### Q49: Explain `count` meta-argument.
**Answer:**
```hcl
resource "aws_instance" "server" {
  count = 3
  
  ami           = "ami-12345"
  instance_type = "t2.micro"
  
  tags = {
    Name = "server-${count.index}"
  }
}

# Reference: aws_instance.server[0].id
```
- Creates multiple resource instances
- Access via index: `count.index`
- Reference as list: `resource_type.name[index]`

### Q50: Explain `for_each` meta-argument.
**Answer:**
```hcl
resource "aws_instance" "server" {
  for_each = toset(["web", "app", "db"])
  
  ami           = "ami-12345"
  instance_type = "t2.micro"
  
  tags = {
    Name = each.value
  }
}

# Reference: aws_instance.server["web"].id
```
- Iterates over map or set
- Access: `each.key` and `each.value`
- Better than count for maps

### Q51: What is the `lifecycle` block used for?
**Answer:**
```hcl
resource "aws_instance" "example" {
  # ... other config ...
  
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags]
    replace_triggered_by  = [aws_security_group.example]
  }
}
```
- **`create_before_destroy`**: Create new before destroying old
- **`prevent_destroy`**: Prevent accidental deletion
- **`ignore_changes`**: Ignore changes to specific attributes
- **`replace_triggered_by`**: Replace when other resource changes

---

## Section 9: Understand Terraform Cloud and Enterprise

### Q52: What are the main features of Terraform Cloud?
**Answer:**
- **Remote operations**: Run Terraform in cloud
- **State management**: Secure remote state storage
- **VCS integration**: GitHub, GitLab, Bitbucket integration
- **Team collaboration**: Access controls and permissions
- **Private registry**: Host private modules and providers
- **Policy as code**: Sentinel policies
- **Cost estimation**: Estimate costs before apply
- **Notifications**: Slack, email notifications

### Q53: What is a Terraform Cloud workspace?
**Answer:**
- Similar to working directory in CLI
- Contains:
  - Terraform configuration
  - State file
  - Variables
  - Run history
- Different from CLI workspaces
- Mapped to VCS branches or directories

### Q54: What are the Terraform Cloud workflow types?
**Answer:**
1. **VCS-driven workflow**: Triggers runs on VCS commits
2. **CLI-driven workflow**: Run from local CLI with remote execution
3. **API-driven workflow**: Programmatic automation via API

### Q55: What is Sentinel in Terraform?
**Answer:**
- Policy as code framework
- Available in Terraform Cloud/Enterprise
- Enforces compliance and governance
- Enforcement levels:
  - **Advisory**: Warning only
  - **Soft mandatory**: Can be overridden
  - **Hard mandatory**: Cannot be overridden
- Examples: cost limits, resource tagging, security rules

---

## Section 10: Advanced Terraform Concepts

### Q56: What are provisioners and when should you use them?
**Answer:**
```hcl
resource "aws_instance" "example" {
  # ... config ...
  
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx"
    ]
  }
  
  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> ips.txt"
  }
}
```
- Execute scripts on resource creation
- **Types**: `local-exec`, `remote-exec`, `file`
- **Last resort** - use native tools instead (cloud-init, user_data)
- Can specify `when = destroy` for cleanup

### Q57: What are Terraform functions? Give examples.
**Answer:** Built-in functions for transformations:
- **Numeric**: `min()`, `max()`, `ceil()`, `floor()`
- **String**: `lower()`, `upper()`, `split()`, `join()`, `format()`
- **Collection**: `length()`, `concat()`, `merge()`, `flatten()`
- **Type conversion**: `tostring()`, `tolist()`, `tomap()`, `tonumber()`
- **Filesystem**: `file()`, `templatefile()`, `fileexists()`
- **Date/Time**: `timestamp()`, `formatdate()`
- **IP/Network**: `cidrsubnet()`, `cidrhost()`

```hcl
locals {
  uppercase_name = upper(var.name)
  subnet_cidr    = cidrsubnet("10.0.0.0/16", 8, 1)
}
```

### Q58: What are dynamic blocks?
**Answer:**
```hcl
resource "aws_security_group" "example" {
  name = "example"
  
  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```
- Dynamically generate nested blocks
- Use `for_each` to iterate
- Access via `iterator_name.value` or `iterator_name.key`

### Q59: What are Terraform expressions?
**Answer:**
- **References**: `var.name`, `resource_type.name.attribute`
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Conditional**: `condition ? true_val : false_val`
- **For expressions**: `[for item in list : upper(item)]`
- **Splat expressions**: `aws_instance.example[*].id`

### Q60: What is `terraform import` and its limitations?
**Answer:**
- Imports existing resources into state
- **Limitations**:
  - Doesn't generate configuration (must write manually)
  - One resource at a time (no bulk import)
  - Must know resource ID
  - Some resources not importable
- **Tools**: `terraformer`, `former2` for bulk import

### Q61: How do you handle secrets in Terraform?
**Answer:**
**Best practices**:
- Never hardcode secrets in `.tf` files
- Use **sensitive = true** for outputs
- Store secrets in:
  - **AWS Secrets Manager / SSM Parameter Store**
  - **Azure Key Vault**
  - **HashiCorp Vault**
  - **Environment variables**
- Use data sources to fetch secrets
```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "database-password"
}

variable "db_password" {
  sensitive = true
}
```

### Q62: What is the difference between `count` and `for_each`?
**Answer:**
- **`count`**: 
  - Integer-based indexing
  - Creates list of resources
  - Changing order causes recreation
  - Best for simple duplication
- **`for_each`**:
  - Map/set-based
  - Creates map of resources
  - Keyed by map keys
  - No recreation when order changes
  - **Preferred for most use cases**

### Q63: How do you manage multiple environments in Terraform?
**Answer:**
**Approaches**:
1. **Separate directories**: Different folders per environment
2. **Workspaces**: `terraform workspace` (same code, different state)
3. **Separate state files**: Different backend configs
4. **Variable files**: Different `.tfvars` per environment
5. **Separate branches**: Git branches per environment

**Best practice**: Separate directories with shared modules

### Q64: What is Terraform registry module versioning?
**Answer:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"
  
  # Operators:
  # version = ">= 3.0.0"       # Greater than or equal
  # version = "~> 3.14"        # Pessimistic (3.14.x)
  # version = ">= 3.0, < 4.0"  # Range
}
```
- Use semantic versioning
- Always pin versions in production
- Test upgrades in non-prod first

### Q65: What are Terraform providers and how are they versioned?
**Answer:**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```
- Plugins that interact with APIs
- Downloaded during `terraform init`
- 3000+ providers available
- Version constraints in `required_providers`

---

## Section 11: Troubleshooting and Debugging

### Q66: How do you enable Terraform debug logging?
**Answer:**
```bash
# Set log level
export TF_LOG=TRACE  # TRACE, DEBUG, INFO, WARN, ERROR
export TF_LOG_PATH=terraform.log

# Run Terraform
terraform apply
```
- Detailed logging for troubleshooting
- Logs API calls and internal operations
- **TRACE**: Most verbose

### Q67: What are common Terraform errors and how to fix them?
**Answer:**
1. **State lock errors**: Wait or force unlock (`terraform force-unlock`)
2. **Provider errors**: Check credentials, network, API limits
3. **Dependency errors**: Add explicit `depends_on`
4. **Resource conflicts**: Import existing resources
5. **Validation errors**: Run `terraform validate`
6. **Syntax errors**: Run `terraform fmt`

### Q68: How do you perform a Terraform refresh?
**Answer:**
```bash
# Old way (deprecated)
terraform refresh

# New way
terraform apply -refresh-only

# Or during plan/apply
terraform plan -refresh=true  # default
```
- Updates state with real-world infrastructure
- Doesn't modify infrastructure
- Detects drift

### Q69: How do you handle Terraform state drift?
**Answer:**
**State drift**: When actual infrastructure differs from state

**Detection**:
```bash
terraform plan -refresh-only
```

**Resolution**:
1. **Apply configuration**: `terraform apply` (recommended)
2. **Update state**: `terraform apply -refresh-only`
3. **Import**: Re-import resources
4. **Manual state edit**: Last resort

### Q70: How do you rollback Terraform changes?
**Answer:**
1. **State file versioning**: Restore previous state (if using S3/remote)
2. **Version control**: Revert to previous config and apply
3. **Manual changes**: Modify resources back manually then refresh
4. **Terraform Cloud**: Built-in state rollback feature

---

## Section 12: Best Practices and Tips

### Q71: What are Terraform best practices?
**Answer:**
- Use remote state with locking
- Pin provider and module versions
- Use modules for reusability
- Separate environments (dev/staging/prod)
- Store secrets securely (not in code)
- Use `.gitignore` for state files
- Run `terraform fmt` and `terraform validate`
- Use `terraform plan` before apply
- Document with README files
- Use consistent naming conventions
- Tag all resources
- Regular state backups

### Q72: How should you structure a Terraform project?
**Answer:**
```
project/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── ec2/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── prod/
├── .gitignore
└── README.md
```

### Q73: What should be in `.gitignore` for Terraform?
**Answer:**
```gitignore
# Local state files
*.tfstate
*.tfstate.*

# Crash log files
crash.log

# Variable files (if containing secrets)
*.tfvars
*.tfvars.json

# Directory for plugins
.terraform/

# Override files
override.tf
override.tf.json

# CLI configuration files
.terraformrc
terraform.rc
```

### Q74: How do you test Terraform code?
**Answer:**
**Testing approaches**:
1. **Terraform validate**: Syntax and consistency
2. **Terraform plan**: Dry run
3. **Terraform fmt -check**: Style checking
4. **tflint**: Linting tool
5. **Terratest**: Automated testing (Go)
6. **Kitchen-Terraform**: Testing framework
7. **Checkov**: Security scanning
8. **TFSec**: Security scanner
9. **Sentinel**: Policy testing (Cloud/Enterprise)

### Q75: What are some Terraform security best practices?
**Answer:**
- Never commit secrets to version control
- Use `sensitive = true` for sensitive outputs
- Encrypt state files at rest and in transit
- Use IAM roles instead of access keys
- Implement least privilege access
- Scan code with security tools (Checkov, TFSec)
- Use private registry for modules
- Enable state locking
- Audit changes with version control
- Use Sentinel policies for governance

---

## Exam Tips and Study Resources

### Exam Format:
- **Duration**: 60 minutes
- **Questions**: 57 multiple choice and multiple select
- **Passing Score**: Not disclosed (varies)
- **Delivery**: Online proctored or test center
- **Cost**: $70.50 USD
- **Validity**: 2 years

### Study Resources:
1. **Official Study Guide**: HashiCorp Learn platform
2. **Documentation**: terraform.io/docs
3. **Hands-on Practice**: Create real infrastructure
4. **Sample Exams**: HashiCorp practice tests
5. **Terraform Associate Tutorials**: learn.hashicorp.com

### Key Topics to Focus:
- Terraform workflow (init, plan, apply)
- State management and remote backends
- Modules and module registry
- Variables, outputs, locals
- Resource meta-arguments (count, for_each, lifecycle)
- Terraform Cloud features
- CLI commands and their purposes
- Provider configuration and versioning

### Final Tips:
- ✅ Practice with real Terraform deployments
- ✅ Understand when to use each CLI command
- ✅ Know the difference between similar concepts
- ✅ Read questions carefully (multiple select vs single)
- ✅ Manage your time (about 60 seconds per question)
- ✅ Review flagged questions at the end

---

**Good luck with your HashiCorp Certified: Terraform Associate (003) exam!** 🚀
