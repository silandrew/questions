# Red Hat Certified Engineer (RHCE) Exam - Ansible Guide

## Table of Contents
1. [Introduction to Ansible](#introduction-to-ansible)
2. [Ansible Installation and Configuration](#ansible-installation-and-configuration)
3. [Inventory Management](#inventory-management)
4. [Ad-Hoc Commands](#ad-hoc-commands)
5. [Playbooks](#playbooks)
6. [Variables](#variables)
7. [Facts](#facts)
8. [Task Control](#task-control)
9. [Handlers](#handlers)
10. [Templates](#templates)
11. [Roles](#roles)
12. [Ansible Vault](#ansible-vault)
13. [Troubleshooting](#troubleshooting)
14. [Practice Questions](#practice-questions)

---

## Introduction to Ansible

### What is Ansible?
Ansible is an open-source automation tool for:
- Configuration management
- Application deployment
- Task automation
- IT orchestration

### Key Features
- **Agentless**: No need to install agents on managed nodes
- **Idempotent**: Safe to run multiple times
- **Simple**: Uses YAML syntax
- **Push-based**: Control node pushes configurations to managed nodes

### Architecture Components
1. **Control Node**: Machine where Ansible is installed
2. **Managed Nodes**: Target machines managed by Ansible
3. **Inventory**: List of managed nodes
4. **Modules**: Units of code executed by Ansible
5. **Playbooks**: YAML files containing automation tasks

---

## Ansible Installation and Configuration

### Installation (RHEL/CentOS)
```bash
# Enable EPEL repository
sudo dnf install epel-release -y

# Install Ansible
sudo dnf install ansible -y

# Verify installation
ansible --version
```

### Configuration File Hierarchy
Ansible searches for configuration in this order:
1. `ANSIBLE_CONFIG` environment variable
2. `./ansible.cfg` (in current directory)
3. `~/.ansible.cfg` (in home directory)
4. `/etc/ansible/ansible.cfg` (global)

### Basic Configuration (/etc/ansible/ansible.cfg)
```ini
[defaults]
inventory = /etc/ansible/hosts
remote_user = ansible
ask_pass = false
host_key_checking = false
forks = 5
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400

[privilege_escalation]
become = true
become_method = sudo
become_user = root
become_ask_pass = false
```

### Important Configuration Parameters
- **inventory**: Default inventory file location
- **remote_user**: Default SSH user
- **ask_pass**: Prompt for SSH password
- **host_key_checking**: Verify SSH host keys
- **forks**: Number of parallel processes
- **become**: Enable privilege escalation
- **roles_path**: Path to roles directory

---

## Inventory Management

### Static Inventory

#### INI Format (/etc/ansible/hosts)
```ini
# Individual hosts
web1.example.com
web2.example.com

# Group of hosts
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com
db2.example.com

# Group with ranges
[webservers]
web[01:10].example.com

# Host with variables
[webservers]
web1.example.com ansible_host=192.168.1.10 ansible_port=2222

# Group variables
[webservers:vars]
http_port=80
max_clients=200

# Parent groups
[production:children]
webservers
dbservers
```

#### YAML Format
```yaml
all:
  hosts:
    web1.example.com:
    web2.example.com:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
      vars:
        http_port: 80
    dbservers:
      hosts:
        db1.example.com:
        db2.example.com:
```

### Dynamic Inventory
```bash
# List all hosts
ansible-inventory --list

# View inventory graph
ansible-inventory --graph

# Use custom inventory
ansible -i inventory.yml all --list-hosts
```

### Host and Group Variables

#### host_vars/web1.example.com.yml
```yaml
---
ansible_host: 192.168.1.10
http_port: 8080
```

#### group_vars/webservers.yml
```yaml
---
http_port: 80
max_clients: 200
document_root: /var/www/html
```

---

## Ad-Hoc Commands

### Syntax
```bash
ansible <host-pattern> -m <module> -a "<module arguments>"
```

### Common Ad-Hoc Commands

#### Ping all hosts
```bash
ansible all -m ping
```

#### Run shell command
```bash
ansible webservers -m command -a "uptime"
ansible webservers -m shell -a "ps aux | grep httpd"
```

#### Copy files
```bash
ansible webservers -m copy -a "src=/etc/hosts dest=/tmp/hosts"
```

#### Install packages
```bash
ansible webservers -m yum -a "name=httpd state=present"
ansible webservers -m dnf -a "name=nginx state=latest"
```

#### Manage services
```bash
ansible webservers -m service -a "name=httpd state=started enabled=yes"
```

#### Create users
```bash
ansible all -m user -a "name=john state=present"
```

#### Gather facts
```bash
ansible all -m setup
ansible all -m setup -a "filter=ansible_distribution*"
```

---

## Playbooks

### Basic Playbook Structure
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: present
    
    - name: Start Apache service
      service:
        name: httpd
        state: started
        enabled: yes
    
    - name: Copy index.html
      copy:
        src: files/index.html
        dest: /var/www/html/index.html
        owner: apache
        group: apache
        mode: '0644'
```

### Running Playbooks
```bash
# Run playbook
ansible-playbook site.yml

# Check syntax
ansible-playbook site.yml --syntax-check

# Dry run (check mode)
ansible-playbook site.yml --check

# Run with specific inventory
ansible-playbook -i inventory.yml site.yml

# Limit to specific hosts
ansible-playbook site.yml --limit webservers

# Start at specific task
ansible-playbook site.yml --start-at-task="Install Apache"

# Use tags
ansible-playbook site.yml --tags "configuration"
ansible-playbook site.yml --skip-tags "packages"
```

### Multiple Plays
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: present

- name: Configure database servers
  hosts: dbservers
  become: yes
  tasks:
    - name: Install MariaDB
      yum:
        name: mariadb-server
        state: present
```

---

## Variables

### Defining Variables

#### In Playbook
```yaml
---
- name: Variable example
  hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  
  tasks:
    - name: Display variables
      debug:
        msg: "HTTP port is {{ http_port }}"
```

#### In External File
```yaml
---
- name: Use external variables
  hosts: webservers
  vars_files:
    - vars/web_vars.yml
  
  tasks:
    - name: Install package
      yum:
        name: "{{ package_name }}"
        state: present
```

#### vars/web_vars.yml
```yaml
---
package_name: httpd
http_port: 80
document_root: /var/www/html
```

### Variable Precedence (Lowest to Highest)
1. Role defaults
2. Inventory file or script group vars
3. Inventory group_vars/all
4. Playbook group_vars/all
5. Inventory group_vars/*
6. Playbook group_vars/*
7. Inventory file or script host vars
8. Inventory host_vars/*
9. Playbook host_vars/*
10. Host facts
11. Play vars
12. Play vars_prompt
13. Play vars_files
14. Role vars
15. Block vars
16. Task vars
17. Extra vars (-e command line)

### Registering Variables
```yaml
---
- name: Register variable example
  hosts: webservers
  tasks:
    - name: Get service status
      command: systemctl status httpd
      register: httpd_status
      ignore_errors: yes
    
    - name: Display output
      debug:
        var: httpd_status.stdout_lines
    
    - name: Show return code
      debug:
        msg: "Return code: {{ httpd_status.rc }}"
```

### Magic Variables
- `hostvars`: Variables for all hosts
- `groups`: All groups in inventory
- `group_names`: Groups current host belongs to
- `inventory_hostname`: Current host name
- `ansible_play_hosts`: All hosts in current play
- `ansible_version`: Ansible version information

```yaml
---
- name: Magic variables example
  hosts: all
  tasks:
    - name: Display inventory hostname
      debug:
        msg: "Current host: {{ inventory_hostname }}"
    
    - name: Show all webservers
      debug:
        msg: "Webservers: {{ groups['webservers'] }}"
```

---

## Facts

### Gathering Facts
```yaml
---
- name: Facts example
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: Display OS family
      debug:
        msg: "OS: {{ ansible_facts['os_family'] }}"
    
    - name: Display IP address
      debug:
        msg: "IP: {{ ansible_facts['default_ipv4']['address'] }}"
```

### Common Facts
- `ansible_facts['distribution']`: OS distribution (RedHat, CentOS, Ubuntu)
- `ansible_facts['distribution_version']`: OS version
- `ansible_facts['hostname']`: Short hostname
- `ansible_facts['fqdn']`: Fully qualified domain name
- `ansible_facts['default_ipv4']['address']`: Primary IP address
- `ansible_facts['memtotal_mb']`: Total memory in MB
- `ansible_facts['processor_cores']`: CPU cores
- `ansible_facts['devices']`: Storage devices

### Custom Facts
Create custom facts in `/etc/ansible/facts.d/custom.fact`:
```ini
[general]
environment=production
datacenter=dc1
```

Or in JSON format:
```json
{
  "general": {
    "environment": "production",
    "datacenter": "dc1"
  }
}
```

Access custom facts:
```yaml
---
- name: Custom facts
  hosts: all
  tasks:
    - name: Display custom fact
      debug:
        msg: "Environment: {{ ansible_facts['ansible_local']['custom']['general']['environment'] }}"
```

### Disabling Fact Gathering
```yaml
---
- name: No facts needed
  hosts: all
  gather_facts: no
  
  tasks:
    - name: Simple task
      debug:
        msg: "This doesn't need facts"
```

---

## Task Control

### Conditionals (when)

#### Basic Conditionals
```yaml
---
- name: Conditional example
  hosts: all
  tasks:
    - name: Install Apache on RedHat
      yum:
        name: httpd
        state: present
      when: ansible_facts['os_family'] == "RedHat"
    
    - name: Install Apache on Debian
      apt:
        name: apache2
        state: present
      when: ansible_facts['os_family'] == "Debian"
```

#### Multiple Conditions
```yaml
---
- name: Multiple conditions
  hosts: all
  tasks:
    - name: Install on RedHat 8
      yum:
        name: httpd
        state: present
      when:
        - ansible_facts['os_family'] == "RedHat"
        - ansible_facts['distribution_major_version'] == "8"
```

#### Using Registered Variables
```yaml
---
- name: Conditional with register
  hosts: webservers
  tasks:
    - name: Check if file exists
      stat:
        path: /etc/httpd/conf/httpd.conf
      register: httpd_conf
    
    - name: Backup config if exists
      copy:
        src: /etc/httpd/conf/httpd.conf
        dest: /etc/httpd/conf/httpd.conf.bak
        remote_src: yes
      when: httpd_conf.stat.exists
```

### Loops

#### Simple Loop
```yaml
---
- name: Loop example
  hosts: all
  tasks:
    - name: Install multiple packages
      yum:
        name: "{{ item }}"
        state: present
      loop:
        - httpd
        - mod_ssl
        - php
```

#### Loop with Dictionary
```yaml
---
- name: Create users
  hosts: all
  tasks:
    - name: Add users
      user:
        name: "{{ item.name }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { name: 'alice', groups: 'wheel' }
        - { name: 'bob', groups: 'users' }
        - { name: 'charlie', groups: 'developers' }
```

#### Loop with Register
```yaml
---
- name: Loop with register
  hosts: all
  tasks:
    - name: Check multiple services
      service:
        name: "{{ item }}"
        state: started
      loop:
        - httpd
        - firewalld
        - sshd
      register: service_results
    
    - name: Display results
      debug:
        var: service_results
```

### Blocks

#### Basic Block
```yaml
---
- name: Block example
  hosts: webservers
  tasks:
    - name: Configure web server
      block:
        - name: Install Apache
          yum:
            name: httpd
            state: present
        
        - name: Start Apache
          service:
            name: httpd
            state: started
      when: ansible_facts['os_family'] == "RedHat"
```

#### Block with Rescue and Always
```yaml
---
- name: Error handling with blocks
  hosts: all
  tasks:
    - name: Handle errors
      block:
        - name: Risky operation
          command: /usr/bin/risky-command
      rescue:
        - name: Handle error
          debug:
            msg: "An error occurred, running recovery"
        
        - name: Recovery action
          command: /usr/bin/recovery-command
      always:
        - name: Always runs
          debug:
            msg: "This runs no matter what"
```

### Tags
```yaml
---
- name: Tagged tasks
  hosts: all
  tasks:
    - name: Install packages
      yum:
        name: httpd
        state: present
      tags:
        - packages
        - installation
    
    - name: Configure service
      template:
        src: httpd.conf.j2
        dest: /etc/httpd/conf/httpd.conf
      tags:
        - configuration
    
    - name: Start service
      service:
        name: httpd
        state: started
      tags:
        - services
```

Run specific tags:
```bash
ansible-playbook site.yml --tags "packages,configuration"
ansible-playbook site.yml --skip-tags "services"
```

---

## Handlers

### Basic Handler
```yaml
---
- name: Handler example
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: present
    
    - name: Copy configuration
      copy:
        src: files/httpd.conf
        dest: /etc/httpd/conf/httpd.conf
      notify: restart apache
  
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
```

### Multiple Handlers
```yaml
---
- name: Multiple handlers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Update configuration
      template:
        src: httpd.conf.j2
        dest: /etc/httpd/conf/httpd.conf
      notify:
        - restart apache
        - check apache status
  
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
    
    - name: check apache status
      command: systemctl status httpd
      register: apache_status
    
    - name: display status
      debug:
        var: apache_status.stdout_lines
```

### Force Handler Execution
```yaml
---
- name: Force handlers
  hosts: webservers
  tasks:
    - name: Task that might fail
      command: /usr/bin/some-command
      notify: restart apache
    
    - name: Force handlers to run now
      meta: flush_handlers
    
    - name: Next task
      debug:
        msg: "Handlers have been run"
```

---

## Templates

### Jinja2 Template Basics

#### Simple Template (templates/index.html.j2)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>Welcome to {{ inventory_hostname }}</h1>
    <p>Server IP: {{ ansible_facts['default_ipv4']['address'] }}</p>
    <p>OS: {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}</p>
</body>
</html>
```

#### Using Template in Playbook
```yaml
---
- name: Template example
  hosts: webservers
  vars:
    page_title: "My Web Server"
  
  tasks:
    - name: Deploy index page
      template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html
        owner: apache
        group: apache
        mode: '0644'
```

### Advanced Template Features

#### Configuration Template (templates/httpd.conf.j2)
```apache
ServerRoot "/etc/httpd"
Listen {{ http_port }}

ServerAdmin {{ admin_email }}
ServerName {{ ansible_facts['fqdn'] }}

DocumentRoot "{{ document_root }}"

<Directory "{{ document_root }}">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>

# Loop through virtual hosts
{% for vhost in virtual_hosts %}
<VirtualHost *:{{ http_port }}>
    ServerName {{ vhost.name }}
    DocumentRoot {{ vhost.docroot }}
</VirtualHost>
{% endfor %}

# Conditional configuration
{% if ansible_facts['distribution_major_version'] == "8" %}
IncludeOptional conf.modules.d/*.conf
{% endif %}

MaxClients {{ max_clients }}
```

#### Playbook Using Advanced Template
```yaml
---
- name: Configure Apache with template
  hosts: webservers
  vars:
    http_port: 80
    admin_email: admin@example.com
    document_root: /var/www/html
    max_clients: 200
    virtual_hosts:
      - { name: 'www.example.com', docroot: '/var/www/example' }
      - { name: 'blog.example.com', docroot: '/var/www/blog' }
  
  tasks:
    - name: Deploy Apache configuration
      template:
        src: templates/httpd.conf.j2
        dest: /etc/httpd/conf/httpd.conf
        validate: '/usr/sbin/httpd -t -f %s'
      notify: restart apache
  
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
```

### Jinja2 Filters
```yaml
---
- name: Filter examples
  hosts: all
  vars:
    my_list: [1, 2, 3, 4, 5]
    my_string: "hello world"
  
  tasks:
    - name: Default value
      debug:
        msg: "{{ undefined_var | default('default value') }}"
    
    - name: Upper/Lower case
      debug:
        msg: "{{ my_string | upper }}"
    
    - name: Join list
      debug:
        msg: "{{ my_list | join(',') }}"
    
    - name: Get unique items
      debug:
        msg: "{{ [1, 2, 2, 3, 3, 4] | unique }}"
    
    - name: Math operations
      debug:
        msg: "{{ my_list | max }}"
```

---

## Roles

### Role Structure
```
roles/
└── webserver/
    ├── defaults/
    │   └── main.yml        # Default variables
    ├── files/              # Static files
    │   └── index.html
    ├── handlers/
    │   └── main.yml        # Handlers
    ├── meta/
    │   └── main.yml        # Role dependencies
    ├── tasks/
    │   └── main.yml        # Main tasks
    ├── templates/          # Jinja2 templates
    │   └── httpd.conf.j2
    ├── tests/
    │   ├── inventory
    │   └── test.yml
    └── vars/
        └── main.yml        # Role variables
```

### Creating a Role
```bash
# Initialize role structure
ansible-galaxy init webserver

# Create role in specific directory
ansible-galaxy init --init-path roles/ webserver
```

### Role Example

#### roles/webserver/defaults/main.yml
```yaml
---
http_port: 80
document_root: /var/www/html
max_clients: 200
```

#### roles/webserver/tasks/main.yml
```yaml
---
- name: Install Apache
  yum:
    name: httpd
    state: present

- name: Deploy configuration
  template:
    src: httpd.conf.j2
    dest: /etc/httpd/conf/httpd.conf
    validate: '/usr/sbin/httpd -t -f %s'
  notify: restart apache

- name: Create document root
  file:
    path: "{{ document_root }}"
    state: directory
    owner: apache
    group: apache
    mode: '0755'

- name: Deploy index page
  copy:
    src: index.html
    dest: "{{ document_root }}/index.html"
    owner: apache
    group: apache
    mode: '0644'

- name: Start and enable Apache
  service:
    name: httpd
    state: started
    enabled: yes

- name: Configure firewall
  firewalld:
    service: http
    permanent: yes
    state: enabled
    immediate: yes
```

#### roles/webserver/handlers/main.yml
```yaml
---
- name: restart apache
  service:
    name: httpd
    state: restarted

- name: reload apache
  service:
    name: httpd
    state: reloaded
```

#### roles/webserver/meta/main.yml
```yaml
---
dependencies:
  - role: common
  - role: firewall
```

### Using Roles in Playbook

#### Simple Role Usage
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  roles:
    - webserver
```

#### Role with Variables
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  roles:
    - role: webserver
      http_port: 8080
      max_clients: 500
```

#### Multiple Roles
```yaml
---
- name: Complete server setup
  hosts: webservers
  become: yes
  
  roles:
    - common
    - firewall
    - webserver
    - monitoring
```

#### Roles with Tasks
```yaml
---
- name: Mixed roles and tasks
  hosts: webservers
  become: yes
  
  pre_tasks:
    - name: Update system
      yum:
        name: '*'
        state: latest
  
  roles:
    - webserver
  
  post_tasks:
    - name: Send notification
      debug:
        msg: "Web server setup complete"
```

### Ansible Galaxy
```bash
# Search for roles
ansible-galaxy search apache

# Install role from Galaxy
ansible-galaxy install geerlingguy.apache

# Install from requirements file
ansible-galaxy install -r requirements.yml

# List installed roles
ansible-galaxy list

# Remove role
ansible-galaxy remove geerlingguy.apache
```

#### requirements.yml
```yaml
---
- src: geerlingguy.apache
  version: 3.1.4

- src: geerlingguy.mysql
  version: 3.3.0

- src: https://github.com/username/role-name
  name: custom-role
  version: master
```

---

## Ansible Vault

### Creating Encrypted Files

#### Create New Encrypted File
```bash
ansible-vault create secret.yml
```

#### Encrypt Existing File
```bash
ansible-vault encrypt vars/database.yml
```

#### Encrypt Multiple Files
```bash
ansible-vault encrypt vars/*.yml
```

### Viewing and Editing Encrypted Files

#### View Encrypted File
```bash
ansible-vault view secret.yml
```

#### Edit Encrypted File
```bash
ansible-vault edit secret.yml
```

### Decrypting Files

#### Decrypt File
```bash
ansible-vault decrypt secret.yml
```

### Changing Vault Password

#### Rekey Encrypted File
```bash
ansible-vault rekey secret.yml
```

### Using Vault in Playbooks

#### Encrypted Variables File (vault.yml)
```yaml
---
db_password: "SuperSecretPassword123!"
api_key: "1234567890abcdef"
```

#### Playbook Using Vaulted Variables
```yaml
---
- name: Deploy application
  hosts: dbservers
  vars_files:
    - vault.yml
  
  tasks:
    - name: Configure database
      mysql_db:
        name: myapp
        login_password: "{{ db_password }}"
        state: present
```

#### Run Playbook with Vault
```bash
# Prompt for password
ansible-playbook site.yml --ask-vault-pass

# Use password file
ansible-playbook site.yml --vault-password-file ~/.vault_pass

# Use script for password
ansible-playbook site.yml --vault-password-file vault-pass.sh
```

### Vault Password File

#### Create Password File
```bash
echo "MyVaultPassword123" > ~/.vault_pass
chmod 600 ~/.vault_pass
```

#### Configure in ansible.cfg
```ini
[defaults]
vault_password_file = ~/.vault_pass
```

### Multiple Vault IDs
```bash
# Create with vault ID
ansible-vault create --vault-id dev@prompt secret_dev.yml
ansible-vault create --vault-id prod@prompt secret_prod.yml

# Run with multiple vault IDs
ansible-playbook site.yml --vault-id dev@prompt --vault-id prod@prompt
```

### Encrypting Specific Variables

#### Encrypt Single Variable
```bash
ansible-vault encrypt_string 'secret_password' --name 'db_password'
```

Output:
```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653561323463353538376333363737353034623339343738653432306339366165386561
          3730393336373265383639306362376663323462323563620a626466623330313364373262333837
          62376661313033626139636132623263323932306463396232636361333066646233323635396332
          6233663866306665340a316434333761346462316233353731353064613562356130623339363564
          3764
```

Use in playbook:
```yaml
---
- name: Use encrypted variable
  hosts: all
  vars:
    db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653561323463353538376333363737353034623339343738653432306339366165386561
          3730393336373265383639306362376663323462323563620a626466623330313364373262333837
          62376661313033626139636132623263323932306463396232636361333066646233323635396332
          6233663866306665340a316434333761346462316233353731353064613562356130623339363564
          3764
  
  tasks:
    - name: Use password
      debug:
        msg: "Password is {{ db_password }}"
```

---

## Troubleshooting

### Debugging Playbooks

#### Debug Module
```yaml
---
- name: Debugging example
  hosts: all
  tasks:
    - name: Display variable
      debug:
        var: ansible_facts
    
    - name: Display message
      debug:
        msg: "The value is {{ my_variable }}"
    
    - name: Conditional debug
      debug:
        msg: "This is a production server"
      when: environment == "production"
```

### Verbosity Levels
```bash
# Basic output
ansible-playbook site.yml

# Verbose (-v)
ansible-playbook site.yml -v

# More verbose (-vv)
ansible-playbook site.yml -vv

# Very verbose (-vvv)
ansible-playbook site.yml -vvv

# Connection debugging (-vvvv)
ansible-playbook site.yml -vvvv
```

### Check Mode (Dry Run)
```bash
# Check what would change
ansible-playbook site.yml --check

# Check with diff
ansible-playbook site.yml --check --diff
```

### Step Mode
```bash
# Confirm each task
ansible-playbook site.yml --step
```

### Start at Task
```bash
# Start from specific task
ansible-playbook site.yml --start-at-task="Install Apache"
```

### Limit Execution
```bash
# Run on specific host
ansible-playbook site.yml --limit web1.example.com

# Run on specific group
ansible-playbook site.yml --limit webservers

# Exclude hosts
ansible-playbook site.yml --limit 'all:!dbservers'
```

### Common Issues and Solutions

#### SSH Connection Issues
```yaml
# Increase timeout
ansible_ssh_timeout: 30

# Use different SSH key
ansible_ssh_private_key_file: ~/.ssh/custom_key

# Disable host key checking
host_key_checking = false
```

#### Privilege Escalation Issues
```yaml
# Become specific user
become_user: root

# Use different become method
become_method: su

# Prompt for password
ansible-playbook site.yml --ask-become-pass
```

#### Module Errors
```yaml
# Ignore errors
- name: Task that might fail
  command: /usr/bin/risky-command
  ignore_errors: yes

# Handle errors
- name: Try something
  command: /usr/bin/command
  register: result
  failed_when: result.rc != 0 and result.rc != 2
```

### Logging
```ini
# ansible.cfg
[defaults]
log_path = /var/log/ansible.log
```

---

## Practice Questions

### Question 1: Basic Playbook
**Task**: Create a playbook that installs and starts the `httpd` service on all hosts in the `webservers` group.

<details>
<summary>Solution</summary>

```yaml
---
- name: Install and start Apache
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install httpd
      yum:
        name: httpd
        state: present
    
    - name: Start and enable httpd
      service:
        name: httpd
        state: started
        enabled: yes
```
</details>

### Question 2: Inventory Management
**Task**: Create an inventory file with:
- Two groups: `webservers` and `dbservers`
- `webservers` group contains `web1.example.com` and `web2.example.com`
- `dbservers` group contains `db1.example.com`
- Set `http_port` variable to `8080` for `webservers` group

<details>
<summary>Solution</summary>

```ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com

[webservers:vars]
http_port=8080
```
</details>

### Question 3: Variables and Facts
**Task**: Create a playbook that displays the hostname, IP address, and OS distribution of each host.

<details>
<summary>Solution</summary>

```yaml
---
- name: Display host information
  hosts: all
  gather_facts: yes
  
  tasks:
    - name: Show host details
      debug:
        msg: |
          Hostname: {{ ansible_facts['hostname'] }}
          IP Address: {{ ansible_facts['default_ipv4']['address'] }}
          OS: {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}
```
</details>

### Question 4: Conditionals
**Task**: Create a playbook that installs `httpd` on RedHat-based systems and `apache2` on Debian-based systems.

<details>
<summary>Solution</summary>

```yaml
---
- name: Install web server
  hosts: all
  become: yes
  
  tasks:
    - name: Install Apache on RedHat
      yum:
        name: httpd
        state: present
      when: ansible_facts['os_family'] == "RedHat"
    
    - name: Install Apache on Debian
      apt:
        name: apache2
        state: present
      when: ansible_facts['os_family'] == "Debian"
```
</details>

### Question 5: Loops
**Task**: Create a playbook that creates three users: `alice`, `bob`, and `charlie`.

<details>
<summary>Solution</summary>

```yaml
---
- name: Create multiple users
  hosts: all
  become: yes
  
  tasks:
    - name: Create users
      user:
        name: "{{ item }}"
        state: present
      loop:
        - alice
        - bob
        - charlie
```
</details>

### Question 6: Handlers
**Task**: Create a playbook that copies a configuration file and restarts the service only if the file changes.

<details>
<summary>Solution</summary>

```yaml
---
- name: Update configuration
  hosts: webservers
  become: yes
  
  tasks:
    - name: Copy httpd configuration
      copy:
        src: files/httpd.conf
        dest: /etc/httpd/conf/httpd.conf
        owner: root
        group: root
        mode: '0644'
      notify: restart httpd
  
  handlers:
    - name: restart httpd
      service:
        name: httpd
        state: restarted
```
</details>

### Question 7: Templates
**Task**: Create a template for `/etc/motd` that displays the hostname and IP address.

<details>
<summary>Solution</summary>

Template file (templates/motd.j2):
```
Welcome to {{ ansible_facts['hostname'] }}
IP Address: {{ ansible_facts['default_ipv4']['address'] }}
OS: {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}
```

Playbook:
```yaml
---
- name: Configure MOTD
  hosts: all
  become: yes
  
  tasks:
    - name: Deploy MOTD
      template:
        src: templates/motd.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: '0644'
```
</details>

### Question 8: Roles
**Task**: Create a role named `webserver` that installs httpd, starts the service, and opens port 80 in the firewall.

<details>
<summary>Solution</summary>

Create role structure:
```bash
ansible-galaxy init webserver
```

roles/webserver/tasks/main.yml:
```yaml
---
- name: Install Apache
  yum:
    name: httpd
    state: present

- name: Start Apache
  service:
    name: httpd
    state: started
    enabled: yes

- name: Configure firewall
  firewalld:
    service: http
    permanent: yes
    state: enabled
    immediate: yes
```

Use in playbook:
```yaml
---
- name: Setup web servers
  hosts: webservers
  become: yes
  
  roles:
    - webserver
```
</details>

### Question 9: Ansible Vault
**Task**: Create an encrypted file containing database credentials and use it in a playbook.

<details>
<summary>Solution</summary>

Create encrypted file:
```bash
ansible-vault create vault.yml
```

vault.yml content:
```yaml
---
db_user: admin
db_password: SecurePassword123!
```

Playbook:
```yaml
---
- name: Configure database
  hosts: dbservers
  become: yes
  vars_files:
    - vault.yml
  
  tasks:
    - name: Create database user
      mysql_user:
        name: "{{ db_user }}"
        password: "{{ db_password }}"
        priv: '*.*:ALL'
        state: present
```

Run playbook:
```bash
ansible-playbook site.yml --ask-vault-pass
```
</details>

### Question 10: Error Handling
**Task**: Create a playbook that attempts to stop a service, handles errors gracefully, and always displays a completion message.

<details>
<summary>Solution</summary>

```yaml
---
- name: Error handling example
  hosts: all
  become: yes
  
  tasks:
    - name: Service management
      block:
        - name: Stop service
          service:
            name: httpd
            state: stopped
      rescue:
        - name: Handle error
          debug:
            msg: "Service could not be stopped, it may not be installed"
      always:
        - name: Completion message
          debug:
            msg: "Task completed"
```
</details>

### Question 11: Complex Scenario
**Task**: Create a complete solution that:
1. Sets up a web server role
2. Uses templates for configuration
3. Creates a group of web servers in inventory
4. Uses variables for customization
5. Implements proper error handling

<details>
<summary>Solution</summary>

Inventory (inventory.ini):
```ini
[webservers]
web1.example.com http_port=80
web2.example.com http_port=8080

[webservers:vars]
document_root=/var/www/html
admin_email=admin@example.com
```

Template (roles/webserver/templates/httpd.conf.j2):
```apache
ServerRoot "/etc/httpd"
Listen {{ http_port }}
ServerAdmin {{ admin_email }}
DocumentRoot "{{ document_root }}"

<Directory "{{ document_root }}">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

Role tasks (roles/webserver/tasks/main.yml):
```yaml
---
- name: Install Apache
  yum:
    name: httpd
    state: present

- name: Deploy configuration
  template:
    src: httpd.conf.j2
    dest: /etc/httpd/conf/httpd.conf
    validate: '/usr/sbin/httpd -t -f %s'
  notify: restart httpd

- name: Start Apache
  service:
    name: httpd
    state: started
    enabled: yes

- name: Configure firewall
  firewalld:
    port: "{{ http_port }}/tcp"
    permanent: yes
    state: enabled
    immediate: yes
  ignore_errors: yes
```

Role handlers (roles/webserver/handlers/main.yml):
```yaml
---
- name: restart httpd
  service:
    name: httpd
    state: restarted
```

Main playbook (site.yml):
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  roles:
    - webserver
```

Run:
```bash
ansible-playbook -i inventory.ini site.yml
```
</details>

---

## RHCE Exam Tips

### Exam Format
- **Duration**: 3-4 hours
- **Format**: Hands-on, performance-based
- **Tasks**: 15-20 real-world scenarios
- **Passing Score**: 210/300 (70%)

### Key Areas to Focus On
1. ✅ Creating and running playbooks
2. ✅ Managing inventory (static and dynamic)
3. ✅ Using variables and facts
4. ✅ Implementing task control (loops, conditionals)
5. ✅ Using templates (Jinja2)
6. ✅ Creating and using roles
7. ✅ Working with Ansible Vault
8. ✅ Using Ansible Galaxy
9. ✅ Troubleshooting and debugging
10. ✅ Managing files and directories
11. ✅ Deploying services
12. ✅ Scheduling tasks with cron
13. ✅ Working with storage
14. ✅ Managing users and groups
15. ✅ Configuring network services

### Best Practices for Exam
1. **Read carefully**: Understand requirements before starting
2. **Use check mode**: Test with `--check` before applying
3. **Verify syntax**: Use `--syntax-check`
4. **Test incrementally**: Run and verify after each task
5. **Use documentation**: Ansible docs are allowed
6. **Manage time**: Don't spend too long on one question
7. **Use roles**: Organize complex tasks into roles
8. **Comment your code**: Make playbooks readable
9. **Handle errors**: Use proper error handling
10. **Verify results**: Test that services actually work

### Common Exam Tasks
- Install and configure packages
- Manage services (start, stop, enable)
- Create users and groups
- Configure firewall rules
- Set up NFS/SMB shares
- Deploy web applications
- Schedule cron jobs
- Work with LVM
- Configure SELinux
- Manage system security

### Time Management
- **Planning**: 15 minutes - Read all questions
- **Execution**: 2.5 hours - Complete tasks
- **Verification**: 30 minutes - Test and verify
- **Review**: 15 minutes - Check all requirements

### Resources
- **Official Docs**: docs.ansible.com
- **Man pages**: `ansible-doc <module>`
- **Examples**: Built into ansible-doc
- **Galaxy**: galaxy.ansible.com

---

## Additional Resources

### Useful Commands Reference
```bash
# Version information
ansible --version

# List hosts
ansible all --list-hosts
ansible webservers --list-hosts

# Test connectivity
ansible all -m ping

# Check syntax
ansible-playbook site.yml --syntax-check

# Dry run
ansible-playbook site.yml --check --diff

# Run with tags
ansible-playbook site.yml --tags "configuration"

# List tags
ansible-playbook site.yml --list-tags

# List tasks
ansible-playbook site.yml --list-tasks

# Module documentation
ansible-doc yum
ansible-doc -l | grep service

# Vault commands
ansible-vault create secret.yml
ansible-vault encrypt file.yml
ansible-vault decrypt file.yml
ansible-vault view secret.yml
ansible-vault edit secret.yml
```

### Common Modules
- **System**: user, group, service, systemd, cron
- **Packages**: yum, dnf, apt, package
- **Files**: copy, file, template, lineinfile, blockinfile
- **Network**: firewalld, selinux, uri
- **Storage**: lvg, lvol, filesystem, mount
- **Database**: mysql_db, mysql_user, postgresql_db
- **Cloud**: ec2, azure_rm, gcp

---

**Good luck with your RHCE exam preparation!** 🚀
