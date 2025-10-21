# Linux Troubleshooting Guide

## Quick Reference Table of Contents with Line Numbers

> **Note:** Click on any topic name to jump directly to that section in the document.

| **Topic** | **Line** | **Description** |
|-----------|----------|-----------------|
| **GENERAL** |
| [General Troubleshooting Approach](#general-troubleshooting-approach) | 15 | Systematic troubleshooting methodology |
| [Systematic Troubleshooting Method](#systematic-troubleshooting-method) | 17 | Step-by-step approach |
| **COMMAND FUNDAMENTALS** |
| [Linux Command Fundamentals](#linux-command-fundamentals) | 27 | Basic command structure and usage |
| [Command Structure](#command-structure) | 31 | How Linux commands are structured |
| [Common Command Options](#common-command-options) | 51 | Short vs long options |
| **FILE & DIRECTORY COMMANDS** |
| [File and Directory Commands](#file-and-directory-commands) | 91 | Core file management commands |
| [ls - List Directory](#ls---list-directory-contents) | 93 | List files and directories |
| [cd - Change Directory](#cd---change-directory) | 133 | Navigate directories |
| [pwd - Print Working Directory](#pwd---print-working-directory) | 150 | Show current location |
| [mkdir - Make Directory](#mkdir---make-directory) | 158 | Create directories |
| [rm - Remove Files/Directories](#rm---remove-filesdirectories) | 172 | Delete files/directories |
| [cp - Copy Files/Directories](#cp---copy-filesdirectories) | 200 | Copy operations |
| [mv - Move/Rename Files](#mv---moverename-files) | 224 | Move and rename |
| [touch - Create/Update Files](#touch---create-empty-file-or-update-timestamp) | 248 | Create empty files |
| [cat - Display File Contents](#cat---concatenate-and-display-files) | 259 | Concatenate and view files |
| [less - View Files Paginated](#less---view-file-contents-paginated) | 276 | View files with pagination |
| [head - Display First Lines](#head---display-first-lines) | 297 | View file beginning |
| [tail - Display Last Lines](#tail---display-last-lines) | 308 | View file ending, follow logs |
| **TEXT PROCESSING** |
| [Text Processing Commands](#text-processing-commands) | 326 | Text manipulation tools |
| [grep - Search Text](#grep---search-text-patterns) | 328 | Pattern matching and search |
| [sed - Stream Editor](#sed---stream-editor) | 367 | Text transformation |
| [awk - Pattern Processing](#awk---pattern-scanning-and-processing) | 402 | Advanced text processing |
| [sort - Sort Lines](#sort---sort-lines) | 439 | Sort file contents |
| [uniq - Remove Duplicates](#uniq---remove-duplicate-lines) | 457 | Find unique lines |
| [cut - Extract Columns](#cut---extract-columns) | 471 | Extract fields from text |
| [tr - Translate Characters](#tr---translate-or-delete-characters) | 485 | Character translation |
| [wc - Word Count](#wc---word-count) | 500 | Count lines, words, characters |
| **PERMISSIONS** |
| [File Permissions and Ownership](#file-permissions-and-ownership) | 518 | Permission management |
| [chmod - Change Permissions](#chmod---change-file-permissions) | 520 | Modify file permissions |
| [chown - Change Ownership](#chown---change-ownership) | 563 | Change file owner |
| [chgrp - Change Group](#chgrp---change-group) | 577 | Change file group |
| [umask - Default Permissions](#umask---set-default-permissions) | 584 | Set default permission mask |
| **PROCESS MANAGEMENT** |
| [Process Management Commands](#process-management-commands) | 599 | Process control |
| [ps - Process Status](#ps---process-status) | 601 | List processes |
| [kill - Send Signals](#kill---send-signal-to-process) | 621 | Terminate processes |
| [pkill/pgrep - Process by Name](#pkill--pgrep---process-management-by-name) | 644 | Find/kill by name |
| [jobs/fg/bg - Job Control](#jobs--fg--bg---job-control) | 656 | Background job management |
| **SYSTEM INFORMATION** |
| [System Information Commands](#system-information-commands) | 673 | System details |
| [uname - System Info](#uname---system-information) | 675 | Kernel and OS information |
| [hostname - System Name](#hostname---showset-hostname) | 687 | Show/set hostname |
| [uptime - System Uptime](#uptime---system-uptime) | 697 | System running time |
| [whoami/who/w - User Info](#whoami--who--w---user-information) | 705 | Current user information |
| [df - Disk Free Space](#df---disk-free-space) | 718 | Filesystem usage |
| [du - Disk Usage](#du---disk-usage) | 733 | Directory size |
| [free - Memory Usage](#free---memory-usage) | 748 | RAM and swap usage |
| **ARCHIVES** |
| [Archive and Compression](#archive-and-compression) | 762 | File compression tools |
| [tar - Archive Files](#tar---archive-files) | 764 | Create/extract archives |
| [gzip/gunzip - Compress](#gzip--gunzip---compress-files) | 799 | Gzip compression |
| [zip/unzip - ZIP Archives](#zip--unzip---zip-archives) | 812 | ZIP file handling |
| **INSTALLATION** |
| [Quick Installation Guide](#quick-installation-guide-for-common-tools) | 829 | Tool installation commands |
| [Red Hat/CentOS/Rocky/Alma](#red-hatcentosrockyalma-linux) | 833 | RHEL-based systems |
| [Ubuntu/Debian](#ubuntudebian) | 865 | Debian-based systems |
| [Python pip Tools](#using-python-pip-cross-platform) | 894 | Python-based utilities |
| [Built-in Tools](#built-in-tools-no-installation-required) | 901 | No installation needed |
| **TROUBLESHOOTING TOOLS** |
| [Essential Troubleshooting Tools](#essential-linux-troubleshooting-tools) | 912 | Advanced diagnostic tools |
| [System Information & Monitoring](#system-information--monitoring) | 914 | Monitoring section |
| [top - Process Monitor](#top---real-time-process-monitoring) | 916 | Real-time process viewer |
| [htop - Interactive Process Viewer](#htop---interactive-process-viewer) | ~940 | Enhanced top alternative |
| [vmstat - Virtual Memory Stats](#vmstat---virtual-memory-statistics) | ~970 | Memory/CPU statistics |
| [iostat - I/O Statistics](#iostat---io-statistics) | ~1000 | Disk I/O monitoring |
| [mpstat - CPU Statistics](#mpstat---multiprocessor-statistics) | ~1030 | Per-CPU statistics |
| [sar - System Activity Report](#sar---system-activity-reporter) | ~1060 | Historical system data |
| **NETWORK TOOLS** |
| [Network Troubleshooting](#network-troubleshooting) | ~1100 | Network diagnostics |
| [netstat - Network Statistics](#netstat---network-statistics) | ~1110 | Network connections |
| [ss - Socket Statistics](#ss---socket-statistics) | ~1140 | Modern netstat replacement |
| [ip - Network Configuration](#ip---network-configuration) | ~1170 | IP address management |
| [ping - Network Connectivity](#ping---test-network-connectivity) | ~1200 | Test connectivity |
| [traceroute - Route Tracing](#traceroute---trace-network-route) | ~1230 | Trace network path |
| [nslookup/dig - DNS Lookup](#nslookup--dig---dns-lookup) | ~1260 | DNS queries |
| [tcpdump - Packet Capture](#tcpdump---packet-capture) | ~1290 | Network packet analysis |
| **DISK & FILESYSTEM** |
| [Disk and Filesystem Tools](#disk-and-filesystem-tools) | ~1320 | Storage management |
| [lsblk - List Block Devices](#lsblk---list-block-devices) | ~1330 | View disk layout |
| [fdisk - Partition Manager](#fdisk---disk-partitioning) | ~1360 | Disk partitioning |
| [mount/umount - Mount Filesystems](#mount--umount---mount-filesystems) | ~1390 | Mount/unmount operations |
| [fsck - Filesystem Check](#fsck---filesystem-check) | ~1420 | Repair filesystems |
| [lsof - List Open Files](#lsof---list-open-files) | ~1450 | Find open files |
| **ADVANCED DIAGNOSTICS** |
| [strace - System Call Tracer](#strace---system-call-tracer) | ~1489 | Trace system calls |
| [ltrace - Library Call Tracer](#ltrace---library-call-tracer) | ~1560 | Trace library calls |
| [perf - Performance Analysis](#perf---performance-analysis) | ~1590 | CPU profiling |
| [dmesg - Kernel Messages](#dmesg---kernel-ring-buffer) | ~1620 | View kernel logs |
| [journalctl - Systemd Logs](#journalctl---systemd-journal) | ~1650 | Query systemd journal |
| **LOG FILES** |
| [Log File Locations](#log-files-and-locations) | ~1700 | Important log paths |
| [System Logs](#system-logs) | ~1710 | /var/log/* files |
| [Application Logs](#application-logs) | ~1740 | App-specific logs |
| **PERFORMANCE** |
| [Performance Tuning](#performance-tuning-and-optimization) | ~1800 | Optimization techniques |
| [CPU Performance](#cpu-performance) | ~1810 | CPU optimization |
| [Memory Performance](#memory-performance) | ~1840 | RAM optimization |
| [Disk Performance](#disk-io-performance) | ~1870 | I/O optimization |
| [Network Performance](#network-performance) | ~1900 | Network tuning |
| **SECURITY** |
| [Security Tools](#security-and-access-control) | ~1950 | Security diagnostics |
| [SELinux Troubleshooting](#selinux-troubleshooting) | ~1960 | SELinux issues |
| [Firewall (iptables/firewalld)](#firewall-troubleshooting) | ~2000 | Firewall debugging |
| **BOOT & RECOVERY** |
| [System Won't Boot](#system-wont-boot) | ~2050 | Boot troubleshooting |
| [GRUB Issues](#grub-bootloader-issues) | ~2060 | Bootloader problems |
| [Recovery Mode](#recovery-mode) | ~2090 | Single user mode |
| [Rescue System](#rescue-system) | ~2120 | Emergency recovery |
| **SYSTEM CALLS** |
| [System Calls Overview](#system-calls) | ~2200 | Understanding syscalls |
| [Common System Calls](#common-system-calls) | ~2210 | Frequently used syscalls |
| [User Space vs Kernel Space](#user-space-vs-kernel-space) | ~2250 | OS architecture |
| **SCENARIOS** |
| [Common Scenarios and Solutions](#common-scenarios-and-solutions) | ~2300 | Real-world problems |
| [High CPU Usage](#high-cpu-usage) | ~2310 | CPU troubleshooting |
| [High Memory Usage](#high-memory-usage) | ~2350 | Memory issues |
| [Disk Full](#disk-full-issues) | ~2390 | Storage problems |
| [Network Issues](#network-connectivity-issues) | ~2430 | Connectivity problems |
| [Slow System](#slow-system-performance) | ~2470 | Performance issues |
| [Application Without Logs](#application-without-logs) | ~2510 | Debug apps with no logs |
| **SCRIPTS & AUTOMATION** |
| [Bash Scripting Basics](#bash-scripting-for-troubleshooting) | ~2600 | Shell script fundamentals |
| [Monitoring Scripts](#monitoring-scripts) | ~2650 | Automated monitoring |
| **BEST PRACTICES** |
| [Troubleshooting Best Practices](#troubleshooting-best-practices) | ~2750 | Tips and guidelines |
| [Documentation](#documentation-and-logging) | ~2760 | Keeping records |
| [Safety Precautions](#safety-precautions) | ~2780 | Avoiding disasters |

---

## Detailed Table of Contents
1. [General Troubleshooting Approach](#general-troubleshooting-approach)
2. [Linux Command Fundamentals](#linux-command-fundamentals)
3. [Essential Linux Troubleshooting Tools](#essential-linux-troubleshooting-tools)
4. [Application Without Logs](#application-without-logs)
5. [System Won't Boot](#system-wont-boot)
6. [System Calls](#system-calls)
7. [User Space vs Kernel Space](#user-space-vs-kernel-space)
8. [Common Scenarios and Solutions](#common-scenarios-and-solutions)

---

## General Troubleshooting Approach

### Systematic Troubleshooting Method
1. **Define the problem** - What exactly is failing?
2. **Gather information** - Logs, metrics, system state
3. **Identify what changed** - Recent updates, deployments, config changes
4. **Formulate hypothesis** - Based on symptoms and data
5. **Test hypothesis** - Make targeted changes
6. **Document findings** - For future reference

---

## Linux Command Fundamentals

Understanding Linux command structure and syntax is essential for effective troubleshooting and system administration.

### Command Structure

```bash
command [options] [arguments]
```

**Components:**
- **command**: The program or utility to execute
- **options/flags**: Modify command behavior (usually start with `-` or `--`)
- **arguments**: Input data (files, directories, values)

**Examples:**
```bash
ls -la /var/log              # Command: ls, Options: -la, Argument: /var/log
grep -r "error" /var/log     # Command: grep, Options: -r, Arguments: "error" /var/log
systemctl status nginx       # Command: systemctl, Argument: status, Argument: nginx
```

---

### Common Command Options

#### Short Options vs Long Options

```bash
# Short options (single dash, single character)
ls -l -a -h                  # Can be combined: ls -lah
ps -e -f                     # Can be combined: ps -ef

# Long options (double dash, full word)
ls --all --human-readable
docker --version
grep --recursive --ignore-case

# Some commands support both
tar -x -v -f file.tar        # Short: tar -xvf file.tar
tar --extract --verbose --file=file.tar  # Long

# Mixed usage
ls -la --color=auto
```

#### Common Option Patterns

| Option | Meaning | Example |
|--------|---------|---------|
| `-a, --all` | Show all (including hidden) | `ls -a` |
| `-r, -R, --recursive` | Recursive operation | `rm -r dir/` |
| `-v, --verbose` | Verbose output | `cp -v file1 file2` |
| `-f, --force` | Force operation | `rm -f file` |
| `-i, --interactive` | Interactive/prompt | `rm -i file` |
| `-h, --human-readable` | Human-readable sizes | `df -h` |
| `-n` | Numeric output | `netstat -n` |
| `-p` | Process/PID related | `ps -p 1234` |
| `-u` | User related | `ps -u username` |
| `-q, --quiet` | Quiet/silent | `grep -q pattern` |
| `-o, --output` | Output file | `gcc -o program` |

---

### File and Directory Commands

#### **ls** - List Directory Contents

```bash
# Basic usage
ls                           # List current directory
ls /path/to/dir             # List specific directory
ls file.txt                 # Check if file exists

# Common options
ls -l                       # Long format (permissions, size, date)
ls -a                       # Show hidden files (starting with .)
ls -h                       # Human-readable sizes (KB, MB, GB)
ls -t                       # Sort by modification time (newest first)
ls -r                       # Reverse order
ls -S                       # Sort by size (largest first)
ls -R                       # Recursive listing

# Combined options
ls -lah                     # Long, all files, human-readable
ls -ltr                     # Long, sorted by time, reversed (oldest first)
ls -lhS                     # Long, human-readable, sorted by size

# Advanced usage
ls -li                      # Show inode numbers
ls -ld /var/log            # List directory itself, not contents
ls *.txt                    # List only .txt files
ls -1                       # One file per line
ls --color=auto            # Colored output

# Output explanation (ls -l)
# -rw-r--r-- 1 user group 1234 Oct 19 10:30 file.txt
# │││││││││  │ │    │     │    │           └─ filename
# │││││││││  │ │    │     │    └─ modification date/time
# │││││││││  │ │    │     └─ size in bytes
# │││││││││  │ │    └─ group owner
# │││││││││  │ └─ user owner
# │││││││││  └─ number of hard links
# └─────────── permissions (type and rwx for user, group, others)
```

#### **cd** - Change Directory

```bash
cd /path/to/directory       # Absolute path
cd relative/path            # Relative path
cd ..                       # Parent directory
cd ../..                    # Two levels up
cd ~                        # Home directory
cd -                        # Previous directory
cd                          # Home directory (no argument)

# Useful shortcuts
cd ~username                # Another user's home directory
cd /                        # Root directory
pwd                         # Print working directory (where am I?)
```

#### **pwd** - Print Working Directory

```bash
pwd                         # Show current directory
pwd -P                      # Physical path (resolve symlinks)
pwd -L                      # Logical path (show symlink path)
```

#### **mkdir** - Make Directory

```bash
mkdir dirname               # Create single directory
mkdir -p path/to/nested/dir # Create nested directories (parent directories)
mkdir -m 755 dirname        # Set permissions during creation
mkdir -v dirname            # Verbose output
mkdir dir1 dir2 dir3        # Create multiple directories

# Examples
mkdir -p ~/projects/{python,java,golang}/src  # Create nested structure
mkdir -m 700 ~/.ssh         # Create with specific permissions
```

#### **rm** - Remove Files/Directories

```bash
# Remove files
rm file.txt                 # Remove single file
rm file1.txt file2.txt      # Remove multiple files
rm *.log                    # Remove all .log files

# Common options
rm -f file.txt              # Force (no prompt, ignore non-existent)
rm -i file.txt              # Interactive (prompt before each)
rm -v file.txt              # Verbose (show what's being deleted)

# Remove directories
rm -r directory             # Recursive (required for directories)
rm -rf directory            # Force recursive (DANGEROUS!)
rm -ri directory            # Interactive recursive (safer)

# Safer alternatives
rm -I *.txt                 # Prompt once before removing >3 files
trash file.txt              # Move to trash (if trash-cli installed)

# ⚠️ DANGEROUS COMMANDS (NEVER RUN THESE)
# rm -rf /                  # Delete everything (root required)
# rm -rf /*                 # Delete everything in root
# rm -rf ~                  # Delete entire home directory
```

#### **cp** - Copy Files/Directories

```bash
# Copy files
cp source.txt destination.txt           # Copy and rename
cp file.txt /path/to/destination/       # Copy to directory
cp file1.txt file2.txt /dest/           # Copy multiple files

# Common options
cp -r source_dir dest_dir               # Recursive (for directories)
cp -i file.txt dest.txt                 # Interactive (prompt before overwrite)
cp -v file.txt dest.txt                 # Verbose
cp -p file.txt dest.txt                 # Preserve attributes (permissions, timestamps)
cp -a source dest                       # Archive mode (-dpR, preserve everything)
cp -u source.txt dest.txt               # Update (copy only if newer)
cp -n source.txt dest.txt               # No clobber (don't overwrite)

# Advanced usage
cp -r src/ dest/                        # Copy directory contents
cp -r src dest                          # Copy directory itself
cp --backup=numbered file.txt dest/     # Create numbered backups
cp -L symlink dest                      # Follow symlinks (copy target)
```

#### **mv** - Move/Rename Files

```bash
# Rename file/directory
mv oldname.txt newname.txt              # Rename file
mv old_dir new_dir                      # Rename directory

# Move files
mv file.txt /path/to/destination/       # Move file
mv file1.txt file2.txt /dest/           # Move multiple files
mv *.log /var/log/                      # Move all .log files

# Common options
mv -i file.txt dest.txt                 # Interactive (prompt before overwrite)
mv -f file.txt dest.txt                 # Force (no prompt)
mv -v file.txt dest.txt                 # Verbose
mv -n file.txt dest.txt                 # No clobber (don't overwrite)
mv -u source.txt dest.txt               # Update (move only if newer)

# Examples
mv ~/Downloads/*.pdf ~/Documents/       # Move all PDFs
mv -t /destination/ file1 file2 file3   # Move to target directory
```

#### **touch** - Create Empty File or Update Timestamp

```bash
touch file.txt                          # Create empty file or update timestamp
touch file1.txt file2.txt               # Create multiple files
touch -c file.txt                       # Don't create file if doesn't exist
touch -t 202310191530.00 file.txt       # Set specific timestamp (YYYYMMDDhhmm.ss)
touch -r reference.txt new.txt          # Use timestamp from reference file
touch -d "2023-10-19 15:30" file.txt    # Set timestamp with date string
```

#### **cat** - Concatenate and Display Files

```bash
cat file.txt                            # Display file contents
cat file1.txt file2.txt                 # Display multiple files
cat > newfile.txt                       # Create file (Ctrl+D to save)
cat >> file.txt                         # Append to file
cat -n file.txt                         # Show line numbers
cat -b file.txt                         # Number non-empty lines only
cat -s file.txt                         # Squeeze multiple blank lines
cat -A file.txt                         # Show all characters (including special)

# Useful combinations
cat file.txt | grep "error"             # Display and search
cat /dev/null > file.txt                # Empty file contents
```

#### **less** - View File Contents (Paginated)

```bash
less file.txt                           # View file with pagination
less +F file.txt                        # Follow mode (like tail -f)
less -N file.txt                        # Show line numbers
less -S file.txt                        # No line wrapping

# Navigation keys inside less
# Space / f         - Next page
# b                 - Previous page
# /pattern          - Search forward
# ?pattern          - Search backward
# n                 - Next search result
# N                 - Previous search result
# g                 - Go to beginning
# G                 - Go to end
# q                 - Quit
# h                 - Help
```

#### **head** - Display First Lines

```bash
head file.txt                           # First 10 lines (default)
head -n 20 file.txt                     # First 20 lines
head -n 5 file.txt                      # First 5 lines
head -c 100 file.txt                    # First 100 bytes
head -n -5 file.txt                     # All except last 5 lines
head file1.txt file2.txt                # Multiple files
```

#### **tail** - Display Last Lines

```bash
tail file.txt                           # Last 10 lines (default)
tail -n 20 file.txt                     # Last 20 lines
tail -f file.txt                        # Follow mode (live updates)
tail -F file.txt                        # Follow with retry (if file rotated)
tail -n +10 file.txt                    # From line 10 to end
tail -c 100 file.txt                    # Last 100 bytes

# Real-time log monitoring
tail -f /var/log/syslog                 # Follow system log
tail -f /var/log/nginx/access.log       # Follow web server log
tail -f file.log | grep "ERROR"         # Follow and filter
```

---

### Text Processing Commands

#### **grep** - Search Text Patterns

```bash
# Basic usage
grep "pattern" file.txt                 # Search for pattern
grep "error" /var/log/syslog            # Search in log file
grep -i "error" file.txt                # Case-insensitive
grep -v "info" file.txt                 # Invert match (exclude lines)
grep -n "pattern" file.txt              # Show line numbers
grep -c "pattern" file.txt              # Count matching lines

# Recursive search
grep -r "pattern" /path/to/dir          # Recursive search in directory
grep -R "pattern" /path/to/dir          # Recursive with symlinks
grep -r "TODO" ~/projects/              # Find all TODOs in project

# Advanced options
grep -w "word" file.txt                 # Match whole word only
grep -x "exact line" file.txt           # Match exact line
grep -l "pattern" *.txt                 # List files with matches
grep -L "pattern" *.txt                 # List files without matches
grep -A 5 "pattern" file.txt            # Show 5 lines After match
grep -B 5 "pattern" file.txt            # Show 5 lines Before match
grep -C 5 "pattern" file.txt            # Show 5 lines Context (before+after)

# Regular expressions
grep "^start" file.txt                  # Lines starting with "start"
grep "end$" file.txt                    # Lines ending with "end"
grep "^$" file.txt                      # Empty lines
grep "[0-9]" file.txt                   # Lines containing numbers
grep -E "pattern1|pattern2" file.txt    # Extended regex (OR)
grep -P "\d{3}-\d{4}" file.txt          # Perl regex (phone numbers)

# Practical examples
grep -r "error" /var/log/ | grep -i "mysql"     # Find MySQL errors
grep -v "^#" /etc/ssh/sshd_config | grep -v "^$" # Show non-comment, non-empty lines
ps aux | grep nginx                              # Find nginx processes
```

#### **sed** - Stream Editor

```bash
# Substitution (find and replace)
sed 's/old/new/' file.txt               # Replace first occurrence per line
sed 's/old/new/g' file.txt              # Replace all occurrences (global)
sed 's/old/new/gi' file.txt             # Replace all (case-insensitive)
sed 's/old/new/2' file.txt              # Replace 2nd occurrence per line
sed -i 's/old/new/g' file.txt           # Edit file in-place
sed -i.bak 's/old/new/g' file.txt       # Edit with backup

# Delete lines
sed '5d' file.txt                       # Delete line 5
sed '5,10d' file.txt                    # Delete lines 5-10
sed '/pattern/d' file.txt               # Delete lines matching pattern
sed '/^$/d' file.txt                    # Delete empty lines
sed '/^#/d' file.txt                    # Delete comment lines

# Print specific lines
sed -n '10p' file.txt                   # Print line 10 only
sed -n '10,20p' file.txt                # Print lines 10-20
sed -n '/pattern/p' file.txt            # Print matching lines

# Insert and append
sed '5i\New line text' file.txt         # Insert before line 5
sed '5a\New line text' file.txt         # Append after line 5
sed '/pattern/a\New line' file.txt      # Append after matching line

# Practical examples
sed -i 's/127.0.0.1/192.168.1.1/g' config.txt   # Replace IP
sed 's/ *$//' file.txt                          # Remove trailing spaces
sed '/^#/d; /^$/d' config.txt                   # Remove comments and empty lines
sed -n '/START/,/END/p' file.txt                # Print between patterns
```

#### **awk** - Pattern Scanning and Processing

```bash
# Print columns
awk '{print $1}' file.txt               # Print 1st column
awk '{print $1, $3}' file.txt           # Print 1st and 3rd columns
awk '{print $NF}' file.txt              # Print last column
awk '{print $0}' file.txt               # Print entire line

# Field separator
awk -F: '{print $1}' /etc/passwd        # Use : as separator (usernames)
awk -F, '{print $2}' data.csv           # Parse CSV (2nd field)
awk 'BEGIN{FS=":"} {print $1}' /etc/passwd  # Alternative syntax

# Pattern matching
awk '/pattern/ {print $0}' file.txt     # Print lines matching pattern
awk '$3 > 100 {print $1}' file.txt      # Print if 3rd field > 100
awk 'NR==5 {print}' file.txt            # Print line 5
awk 'NR>=5 && NR<=10 {print}' file.txt  # Print lines 5-10

# Built-in variables
awk '{print NR, $0}' file.txt           # NR = line number
awk '{print NF}' file.txt               # NF = number of fields
awk 'END {print NR}' file.txt           # Print total line count

# Calculations
awk '{sum += $1} END {print sum}' file.txt          # Sum 1st column
awk '{sum += $1} END {print sum/NR}' file.txt       # Average
awk '$3 > 100 {count++} END {print count}' file.txt # Count lines

# Practical examples
ps aux | awk '{print $2, $11}'                      # Print PID and command
df -h | awk '$5+0 > 80 {print $0}'                  # Disks over 80% full
awk -F: '$3 >= 1000 {print $1}' /etc/passwd         # Regular users
netstat -an | awk '/ESTABLISHED/ {count++} END {print count}'  # Count connections
```

#### **sort** - Sort Lines

```bash
sort file.txt                           # Sort alphabetically
sort -r file.txt                        # Reverse sort
sort -n file.txt                        # Numeric sort
sort -h file.txt                        # Human-numeric sort (1K, 2M, 3G)
sort -u file.txt                        # Sort and remove duplicates
sort -k2 file.txt                       # Sort by 2nd field
sort -k2,2n -k1,1 file.txt              # Sort by 2nd field (numeric), then 1st
sort -t: -k3n /etc/passwd               # Sort by 3rd field, : separator

# Practical examples
du -sh * | sort -h                      # Sort directories by size
ps aux | sort -k3nr | head -10          # Top 10 CPU consumers
sort -u file.txt > sorted.txt           # Remove duplicates and save
```

#### **uniq** - Remove Duplicate Lines

```bash
uniq file.txt                           # Remove consecutive duplicates
uniq -c file.txt                        # Count occurrences
uniq -d file.txt                        # Show only duplicates
uniq -u file.txt                        # Show only unique lines
uniq -i file.txt                        # Case-insensitive

# Note: Must sort first for all duplicates
sort file.txt | uniq                    # Remove all duplicates
sort file.txt | uniq -c | sort -nr      # Count and sort by frequency
```

#### **cut** - Extract Columns

```bash
cut -d: -f1 /etc/passwd                 # 1st field, : delimiter
cut -d: -f1,3 /etc/passwd               # 1st and 3rd fields
cut -d: -f1-3 /etc/passwd               # Fields 1 through 3
cut -c1-10 file.txt                     # Characters 1-10
cut -c1,5,10 file.txt                   # Characters 1, 5, and 10

# Practical examples
cat /etc/passwd | cut -d: -f1           # Extract usernames
echo "192.168.1.100" | cut -d. -f1-3    # Get network portion (192.168.1)
```

#### **tr** - Translate or Delete Characters

```bash
tr 'a-z' 'A-Z' < file.txt               # Lowercase to uppercase
tr 'A-Z' 'a-z' < file.txt               # Uppercase to lowercase
tr -d '0-9' < file.txt                  # Delete all digits
tr -s ' ' < file.txt                    # Squeeze repeated spaces
tr ' ' '_' < file.txt                   # Replace spaces with underscores
tr -d '\r' < dos.txt > unix.txt         # Convert DOS to Unix (remove \r)

# Practical examples
echo "hello world" | tr 'a-z' 'A-Z'     # HELLO WORLD
cat file.txt | tr -s '\n'               # Remove blank lines
```

#### **wc** - Word Count

```bash
wc file.txt                             # Lines, words, bytes
wc -l file.txt                          # Count lines only
wc -w file.txt                          # Count words only
wc -c file.txt                          # Count bytes
wc -m file.txt                          # Count characters
wc -L file.txt                          # Longest line length

# Practical examples
ls | wc -l                              # Count files in directory
ps aux | wc -l                          # Count running processes
grep "error" /var/log/syslog | wc -l    # Count error lines
```

---

### File Permissions and Ownership

#### **chmod** - Change File Permissions

```bash
# Numeric mode (octal)
chmod 755 file.txt                      # rwxr-xr-x
chmod 644 file.txt                      # rw-r--r--
chmod 600 file.txt                      # rw-------
chmod 777 file.txt                      # rwxrwxrwx (dangerous!)
chmod 000 file.txt                      # --------- (no permissions)

# Recursive
chmod -R 755 directory/                 # Apply to directory and contents

# Symbolic mode
chmod u+x file.txt                      # Add execute for user
chmod g-w file.txt                      # Remove write for group
chmod o+r file.txt                      # Add read for others
chmod a+x file.txt                      # Add execute for all
chmod u=rwx,g=rx,o=r file.txt          # Set specific permissions

# Permission numbers
# 4 = read (r)
# 2 = write (w)
# 1 = execute (x)
# 0 = no permission (-)
#
# 7 = 4+2+1 = rwx
# 6 = 4+2   = rw-
# 5 = 4+1   = r-x
# 4 = 4     = r--
# 3 = 2+1   = -wx
# 2 = 2     = -w-
# 1 = 1     = --x
# 0 = 0     = ---

# Common patterns
chmod 755 script.sh                     # Executable script
chmod 644 document.txt                  # Regular file
chmod 600 ~/.ssh/id_rsa                 # Private key
chmod 700 ~/.ssh                        # SSH directory
chmod 1777 /tmp                         # Sticky bit
```

#### **chown** - Change Ownership

```bash
chown user file.txt                     # Change owner
chown user:group file.txt               # Change owner and group
chown :group file.txt                   # Change group only
chown -R user:group directory/          # Recursive

# Practical examples
sudo chown root:root /etc/config        # Change to root
sudo chown www-data:www-data /var/www/  # Web server ownership
sudo chown -R $USER:$USER ~/project/    # Take ownership
```

#### **chgrp** - Change Group

```bash
chgrp group file.txt                    # Change group
chgrp -R group directory/               # Recursive
```

#### **umask** - Set Default Permissions

```bash
umask                                   # Show current umask
umask 022                               # Set umask (common: files 644, dirs 755)
umask 077                               # Restrictive (files 600, dirs 700)

# How umask works:
# Files: 666 - umask = default permissions
# Dirs:  777 - umask = default permissions
# umask 022: files=644 (666-022), dirs=755 (777-022)
```

---

### Process Management Commands

#### **ps** - Process Status

```bash
ps                                      # Show processes in current shell
ps aux                                  # All processes, detailed (BSD style)
ps -ef                                  # All processes (System V style)
ps -u username                          # Processes by user
ps -p 1234                              # Process by PID
ps -C nginx                             # Processes by command name

# Output filtering
ps aux | grep nginx                     # Find nginx processes
ps aux --sort=-%cpu | head              # Top CPU consumers
ps aux --sort=-%mem | head              # Top memory consumers

# Custom output
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head
ps -eo user,pid,ppid,cmd                # Specific columns
```

#### **kill** - Send Signal to Process

```bash
kill PID                                # Send TERM signal (graceful)
kill -9 PID                             # Send KILL signal (force)
kill -15 PID                            # Send TERM (same as no option)
kill -HUP PID                           # Reload configuration
kill -STOP PID                          # Pause process
kill -CONT PID                          # Resume process

# Kill by name
killall nginx                           # Kill all nginx processes
pkill -f "python script.py"             # Kill by pattern

# Common signals
# 1  HUP     - Hang up (reload config)
# 2  INT     - Interrupt (Ctrl+C)
# 9  KILL    - Force kill (cannot be caught)
# 15 TERM    - Terminate gracefully (default)
# 18 CONT    - Continue
# 19 STOP    - Stop (pause)
```

#### **pkill / pgrep** - Process Management by Name

```bash
pgrep nginx                             # Find PIDs by name
pgrep -u username                       # Find PIDs by user
pgrep -f "python script.py"             # Find by full command line

pkill nginx                             # Kill processes by name
pkill -9 -u username                    # Force kill user's processes
pkill -HUP nginx                        # Send HUP to nginx
```

#### **jobs / fg / bg** - Job Control

```bash
jobs                                    # List background jobs
fg                                      # Bring recent job to foreground
fg %1                                   # Bring job 1 to foreground
bg                                      # Resume paused job in background
bg %2                                   # Resume job 2 in background

# Usage
command &                               # Start in background
Ctrl+Z                                  # Pause current job
fg                                      # Resume in foreground
```

---

### System Information Commands

#### **uname** - System Information

```bash
uname                                   # Kernel name (Linux)
uname -a                                # All information
uname -r                                # Kernel release (5.15.0-91-generic)
uname -m                                # Machine architecture (x86_64)
uname -n                                # Network node hostname
uname -s                                # Kernel name
uname -v                                # Kernel version with build date
```

#### **hostname** - Show/Set Hostname

```bash
hostname                                # Show hostname
hostname -f                             # FQDN (fully qualified domain name)
hostname -i                             # IP address
hostname -I                             # All IP addresses
sudo hostname newhostname               # Set hostname (temporary)
```

#### **uptime** - System Uptime

```bash
uptime                                  # Show uptime and load average
uptime -p                               # Pretty format (up 5 days, 3 hours)
uptime -s                               # Since when (2024-10-14 08:30:00)
```

#### **whoami / who / w** - User Information

```bash
whoami                                  # Current username
who                                     # Who is logged in
who -b                                  # Last boot time
w                                       # Who is logged in + what they're doing
users                                   # List logged-in usernames
last                                    # Login history
last -n 10                              # Last 10 logins
last username                           # Specific user's logins
```

#### **df** - Disk Free Space

```bash
df                                      # Show disk space
df -h                                   # Human-readable (GB, MB)
df -T                                   # Show filesystem type
df -i                                   # Show inode usage
df /path                                # Check specific mount point
df -h --total                           # Show total at bottom

# Practical usage
df -h | grep -v "tmpfs"                 # Exclude temporary filesystems
df -h | awk '$5+0 > 80 {print}'        # Show filesystems over 80%
```

#### **du** - Disk Usage

```bash
du -sh directory/                       # Summary of directory size
du -h directory/                        # Sizes of all subdirectories
du -sh *                                # Size of each item in current dir
du -ah directory/                       # All files and directories
du -h --max-depth=1                     # One level deep only
du -ch directory/                       # Show grand total

# Find largest directories
du -sh * | sort -h                      # Sort by size
du -h | sort -h | tail -20              # Top 20 largest
```

#### **free** - Memory Usage

```bash
free                                    # Show memory in KB
free -h                                 # Human-readable
free -m                                 # Show in MB
free -g                                 # Show in GB
free -s 2                               # Update every 2 seconds
free -t                                 # Show total line
free -w                                 # Wide mode (split buffers/cache)
```

---

### Archive and Compression

#### **tar** - Archive Files

```bash
# Create archives
tar -cf archive.tar files/              # Create tar archive
tar -czf archive.tar.gz files/          # Create gzip compressed
tar -cjf archive.tar.bz2 files/         # Create bzip2 compressed
tar -cJf archive.tar.xz files/          # Create xz compressed

# Extract archives
tar -xf archive.tar                     # Extract tar
tar -xzf archive.tar.gz                 # Extract gzip
tar -xjf archive.tar.bz2                # Extract bzip2
tar -xJf archive.tar.xz                 # Extract xz

# List contents
tar -tf archive.tar                     # List files in archive
tar -tzf archive.tar.gz                 # List gzip archive

# Options explained
# c - create
# x - extract
# f - file (must be followed by filename)
# z - gzip compression
# j - bzip2 compression
# J - xz compression
# v - verbose (show progress)
# t - list contents

# Advanced usage
tar -czf backup.tar.gz --exclude='*.log' directory/
tar -xzf archive.tar.gz -C /destination/
tar -czf - directory/ | ssh user@host "cat > /backup/archive.tar.gz"
```

#### **gzip / gunzip** - Compress Files

```bash
gzip file.txt                           # Compress (creates file.txt.gz)
gzip -k file.txt                        # Keep original file
gzip -r directory/                      # Compress all files in directory
gunzip file.txt.gz                      # Decompress
gzip -d file.txt.gz                     # Decompress (same as gunzip)
gzip -l file.txt.gz                     # List compression info
gzip -1 file.txt                        # Fast compression
gzip -9 file.txt                        # Best compression
```

#### **zip / unzip** - ZIP Archives

```bash
zip archive.zip file1 file2             # Create zip
zip -r archive.zip directory/           # Recursive
unzip archive.zip                       # Extract
unzip -l archive.zip                    # List contents
unzip archive.zip -d /destination/      # Extract to specific directory
unzip -q archive.zip                    # Quiet mode
```

---

This comprehensive Linux command reference provides detailed explanations with practical examples for troubleshooting and system administration tasks.

---

## Quick Installation Guide for Common Tools

Most troubleshooting tools can be installed via package managers. Below is a quick reference:

### Red Hat/CentOS/Rocky/Alma Linux
```bash
# Essential performance monitoring tools (sysstat package)
sudo yum install sysstat -y         # RHEL 7 and earlier
sudo dnf install sysstat -y         # RHEL 8/9+
# Includes: iostat, sar, mpstat, pidstat, cifsiostat

# Enable EPEL repository (for additional tools)
sudo yum install epel-release -y    # RHEL 7
sudo dnf install epel-release -y    # RHEL 8/9+

# Process monitoring tools
sudo dnf install htop atop glances nmon -y

# I/O monitoring
sudo dnf install iotop -y

# Network tools
sudo dnf install tcpdump mtr iftop -y

# System tracing
sudo dnf install strace ltrace perf -y

# Resource statistics
sudo dnf install dstat -y           # RHEL 8 (deprecated in RHEL 9)
sudo dnf install pcp-system-tools -y  # RHEL 9+ (replacement for dstat)

# Enable sysstat for historical data collection
sudo systemctl enable sysstat
sudo systemctl start sysstat
```

### Ubuntu/Debian
```bash
# Update package list
sudo apt-get update

# Essential tools
sudo apt-get install -y \
    sysstat \
    htop \
    atop \
    glances \
    iotop \
    nmon \
    dstat \
    tcpdump \
    mtr \
    iftop \
    strace \
    ltrace \
    linux-tools-common \
    linux-tools-generic \
    linux-tools-$(uname -r)

# Enable sysstat
sudo sed -i 's/ENABLED="false"/ENABLED="true"/' /etc/default/sysstat
sudo systemctl enable sysstat
sudo systemctl start sysstat
```

### Using Python pip (Cross-platform)
```bash
# For Python-based tools
pip3 install glances
pip3 install 'glances[all]'  # With all optional dependencies
```

### Built-in Tools (No Installation Required)
The following tools are typically pre-installed on most Linux distributions:
- `top`, `ps`, `free`, `uptime`, `df`, `du`
- `vmstat`, `mpstat` (if procps package is installed)
- `lsof`, `ss`, `ip`, `ping`, `traceroute`
- `journalctl`, `dmesg`, `systemctl`
- `grep`, `awk`, `sed`, `tail`, `head`, `less`
- `netstat` (deprecated, use `ss` instead)

---

## Essential Linux Troubleshooting Tools

### System Information & Monitoring

#### **top** - Real-time Process Monitoring

**Built-in:** Yes (no installation required)

**Usage:**
```bash
top                    # Basic usage
top -u username        # Filter by user
top -p PID             # Monitor specific process
top -d 5               # Update every 5 seconds

# Interactive commands (while top is running):
# Press 'h' - Help
# Press '1' - Show individual CPU cores
# Press 'M' - Sort by memory usage
# Press 'P' - Sort by CPU usage
# Press 'k' - Kill a process
# Press 'r' - Renice a process
# Press 'W' - Save configuration
# Press 'z' - Color display
# Press 'c' - Show full command path
# Press 'f' - Select fields to display
```

**What it shows:**
- System uptime and load averages
- Task summary (total, running, sleeping, stopped, zombie)
- CPU usage (user, system, nice, idle, wait, hardware interrupts)
- Memory and swap usage
- Per-process CPU, memory, time, command

#### **top Command Field Descriptions**

**Summary Area (Top Section)**

1. **First Line - System Information:**
```
top - 14:23:45 up 5 days, 3:21, 2 users, load average: 0.45, 0.32, 0.28
```
- `14:23:45` - Current time
- `up 5 days, 3:21` - System uptime (days, hours:minutes)
- `2 users` - Number of logged-in users
- `load average: 0.45, 0.32, 0.28` - System load averages for 1, 5, and 15 minutes
  - Values < 1.0 indicate low load
  - Values = number of CPUs indicate full utilization
  - Values > number of CPUs indicate system overload

2. **Second Line - Tasks/Processes:**
```
Tasks: 245 total, 1 running, 244 sleeping, 0 stopped, 0 zombie
```
- `total` - Total number of processes
- `running` - Processes currently executing on CPU
- `sleeping` - Processes waiting for resources (idle)
- `stopped` - Processes suspended (usually by Ctrl+Z)
- `zombie` - Dead processes waiting to be reaped by parent

3. **Third Line - CPU Usage:**
```
%Cpu(s): 12.5 us, 3.2 sy, 0.0 ni, 83.1 id, 1.2 wa, 0.0 hi, 0.0 si, 0.0 st
```
- `us` (user) - Time spent running user processes (normal priority)
- `sy` (system) - Time spent in kernel mode (system calls, kernel operations)
- `ni` (nice) - Time spent running niced (lower priority) user processes
- `id` (idle) - Time CPU is idle (higher is better if no work to do)
- `wa` (wait) - Time waiting for I/O to complete (high = I/O bottleneck)
- `hi` (hardware interrupts) - Time servicing hardware interrupts
- `si` (software interrupts) - Time servicing software interrupts
- `st` (steal time) - Time stolen by hypervisor (VM environments only)

**High wa% indicates:** Disk I/O bottleneck, slow storage, or network issues
**High sy% indicates:** Many system calls, kernel operations, or context switches
**High us% indicates:** CPU-intensive application workload

4. **Fourth Line - Physical Memory (RAM):**
```
MiB Mem: 16045.2 total, 8234.5 free, 5821.3 used, 1989.4 buff/cache
```
- `total` - Total physical RAM installed
- `free` - Completely unused memory
- `used` - Memory used by processes (excluding buffers/cache)
- `buff/cache` - Memory used for buffers and cache (can be reclaimed)
- **Available memory** = free + buff/cache (approximately)

5. **Fifth Line - Swap Memory:**
```
MiB Swap: 8192.0 total, 8190.0 free, 2.0 used, 14523.4 avail Mem
```
- `total` - Total swap space configured
- `free` - Unused swap space
- `used` - Swap space in use (high usage indicates memory pressure)
- `avail Mem` - Estimate of memory available for starting new applications

**Process List Area (Bottom Section)**

```
PID  USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
1234 root      20   0  162896  12456   8764 S   5.3   0.1   0:12.34 nginx
5678 www-data  20   0 1245678 456789  23456 R  98.5   2.8  15:23.45 php-fpm
```

**Column Definitions:**

- **PID** (Process ID)
  - Unique identifier for each process
  - Used to send signals (kill, stop, etc.)

- **USER**
  - Username of the process owner
  - Useful for identifying which user's processes are consuming resources

- **PR** (Priority)
  - Kernel scheduling priority
  - Values: 0-39 (lower = higher priority)
  - RT (Real-Time) indicates real-time scheduling

- **NI** (Nice Value)
  - User-space priority adjustment
  - Range: -20 (highest priority) to +19 (lowest priority)
  - Default is 0
  - Only root can set negative values

- **VIRT** (Virtual Memory)
  - Total virtual memory used by process
  - Includes: code, data, shared libraries, swapped pages
  - Not all of this is in physical RAM
  - Can be larger than total RAM

- **RES** (Resident Memory)
  - Actual physical RAM used by process (non-swapped)
  - This is the "real" memory usage
  - More important metric than VIRT
  - RES ≤ VIRT always

- **SHR** (Shared Memory)
  - Memory shared with other processes
  - Includes shared libraries and memory mappings
  - Counted in RES but can be used by multiple processes

- **S** (Process Status)
  - `R` - Running (currently executing on CPU)
  - `S` - Sleeping (waiting for event/resource)
  - `D` - Uninterruptible sleep (usually I/O wait)
  - `T` - Stopped (by job control signal)
  - `t` - Stopped by debugger
  - `Z` - Zombie (terminated but not reaped)
  - `I` - Idle kernel thread

- **%CPU** (CPU Usage)
  - Percentage of CPU time used since last update
  - Can exceed 100% on multi-core systems
  - 100% = fully utilizing one CPU core
  - 400% on quad-core = using all cores

- **%MEM** (Memory Usage)
  - Percentage of physical RAM (RES) used
  - Calculated as: (RES / Total RAM) × 100

- **TIME+** (CPU Time)
  - Total CPU time process has consumed
  - Format: minutes:seconds.hundredths
  - Cumulative since process started
  - Useful for finding long-running processes

- **COMMAND**
  - Process name or command line
  - Press `c` to toggle between name and full command path
  - Truncated if too long

**Additional Fields (press 'f' to select):**

- **PPID** - Parent Process ID
- **UID** - User ID number
- **GID** - Group ID number
- **TTY** - Controlling terminal
- **%MEM** - Memory usage percentage
- **WCHAN** - Kernel function where process is sleeping
- **Flags** - Task flags (technical, rarely useful)
- **DATA** - Data + Stack size
- **CODE** - Code size (text segment)
- **SWAP** - Swapped size
- **nMaj** - Major page faults
- **nMin** - Minor page faults
- **nDRT** - Dirty pages count

**Useful top Commands and Shortcuts:**

```bash
# Sort processes
top -o %CPU           # Sort by CPU (same as 'P' in interactive)
top -o %MEM           # Sort by memory (same as 'M' in interactive)
top -o TIME+          # Sort by cumulative time

# Filter processes
top -u username       # Show only user's processes
top -p 1234,5678      # Monitor specific PIDs

# Batch mode (for scripts)
top -b -n 1           # Run once and exit
top -b -n 1 > top.txt # Save output to file
top -b -n 10 -d 2     # 10 iterations, 2-second delay

# Show individual CPU cores
top                   # Then press '1'
# Shows: %Cpu0, %Cpu1, %Cpu2, etc.

# Highlight running processes
top                   # Then press 'z' for colors, 'x' for column highlight

# Show full command paths
top                   # Then press 'c'
```

**Interpreting top Output - Common Scenarios:**

1. **High Load Average** (> number of CPU cores)
   - System is overloaded
   - Processes waiting for CPU time
   - Look at running/waiting processes

2. **High %wa (iowait)**
   - Disk I/O bottleneck
   - Check with `iostat` or `iotop`
   - May need faster storage or I/O optimization

3. **Many Zombie Processes**
   - Parent process not reaping children
   - Usually indicates application bug
   - Find parent with `ps -ef | grep defunct`

4. **High Swap Usage**
   - System running out of RAM
   - Performance degradation (swap is slow)
   - Need to add RAM or reduce memory usage

5. **Process in 'D' State**
   - Uninterruptible sleep (usually I/O)
   - Cannot be killed until I/O completes
   - Check storage subsystem health

**Example Analysis:**

```
top - 15:30:24 up 10 days, 5:45, 3 users, load average: 8.42, 6.23, 4.15
Tasks: 312 total, 3 running, 308 sleeping, 0 stopped, 1 zombie
%Cpu(s): 45.2 us, 12.3 sy, 0.0 ni, 5.4 id, 35.1 wa, 0.2 hi, 1.8 si, 0.0 st
MiB Mem: 8192.0 total, 124.3 free, 7845.2 used, 222.5 buff/cache
MiB Swap: 4096.0 total, 1234.5 free, 2861.5 used, 89.7 avail Mem

PID  USER     PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
2345 postgres 20   0  2.5g    1.8g   1.2g D  85.3  22.5  125:34.21 postgres
```

**Analysis of this system:**
- ✗ Load average (8.42) much higher than typical for 4-core system = overloaded
- ✗ High iowait (35.1 wa) = severe I/O bottleneck
- ✗ Low idle time (5.4 id) = CPU constantly busy
- ✗ High memory usage (7.8GB/8GB) = memory pressure
- ✗ High swap usage (2.8GB) = system thrashing
- ✗ Postgres in 'D' state at 85% CPU = stuck in I/O operation
- ✗ 1 zombie process = application not cleaning up children
- **Problem:** Database doing heavy I/O, system out of memory, swapping heavily
- **Solution:** Add more RAM, optimize queries, improve storage I/O

#### **htop** - Enhanced Interactive Process Viewer

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install htop -y              # RHEL 7 and earlier
sudo dnf install htop -y              # RHEL 8/9+
sudo yum install epel-release -y      # Enable EPEL if needed, then install htop
sudo dnf install epel-release -y      # For RHEL 8/9

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install htop -y

# Fedora
sudo dnf install htop -y

# Verify installation
htop --version
which htop
```

**Usage:**
```bash
htop                   # Enhanced interface with colors
htop -u username       # Filter by user
htop -p PID1,PID2      # Monitor specific processes
htop -d 10             # Update delay (tenths of seconds)

# Features over top:
# - Color-coded display
# - Mouse support
# - Horizontal/vertical scrolling
# - Tree view of processes
# - Easy sorting (F6)
# - Easy kill (F9)
# - Easy nice (F8)
# - Shows all CPU cores by default
```

**Interactive keys:**
- `F1` - Help
- `F2` - Setup (customize display)
- `F3` - Search process
- `F4` - Filter processes
- `F5` - Tree view
- `F6` - Sort by column
- `F9` - Kill process
- `F10` - Quit
- `t` - Tree view toggle
- `u` - Filter by user
- `Space` - Tag process
- `U` - Untag all

#### **atop** - Advanced System & Process Monitor

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install atop -y              # RHEL 7 and earlier
sudo dnf install atop -y              # RHEL 8/9+
sudo yum install epel-release -y      # Enable EPEL if needed
sudo dnf install epel-release -y      # For RHEL 8/9

# Enable atop logging service
sudo systemctl enable atop
sudo systemctl start atop

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install atop -y

# Verify installation
atop -V
which atop
```

**Usage:**
```bash
atop                   # Real-time monitoring
atop -r /var/log/atop/atop_20251017  # Read log file
atop 5                 # 5-second intervals
atopsar               # System activity report

# Interactive commands:
# 'g' - Generic output (default)
# 'm' - Memory details
# 'd' - Disk details
# 'n' - Network details
# 'c' - Command line per process
# 'p' - Process activity
```

**Unique features:**
- Records system/process activity in logs
- Can replay historical data
- Shows disappeared processes
- Monitors disk I/O per process
- Network activity per process

#### **glances** - Cross-Platform System Monitoring

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install glances -y           # RHEL 7 and earlier
sudo dnf install glances -y           # RHEL 8/9+
sudo yum install epel-release -y      # Enable EPEL if needed
sudo dnf install epel-release -y      # For RHEL 8/9

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install glances -y

# Using Python pip (any distro)
pip3 install glances
# or
sudo pip3 install glances

# With additional features
pip3 install 'glances[all]'

# Verify installation
glances --version
which glances
```

**Usage:**
```bash
glances               # All-in-one monitoring
glances -t 2          # 2-second refresh
glances -1            # Display one line per CPU
glances --export-csv /tmp/glances.csv  # Export data
glances -w            # Web server mode (http://localhost:61208)

# Advanced features:
glances --disable-plugin network    # Disable specific plugin
glances --enable-plugin gpu         # Enable GPU monitoring
```

**What it monitors:**
- CPU, Memory, Swap, Load
- Network bandwidth
- Disk I/O
- File system space
- Sensors (temperature)
- Processes
- Docker containers
- Alerts for thresholds

#### **vmstat** - Virtual Memory Statistics
```bash
vmstat                # Display statistics
vmstat 2              # Update every 2 seconds
vmstat 2 10           # 10 updates at 2-second intervals
vmstat -s             # Memory statistics summary
vmstat -d             # Disk statistics
vmstat -p /dev/sda1   # Partition statistics

# Output columns explained:
# Procs:
#   r - processes waiting for run time
#   b - processes in uninterruptible sleep
# Memory:
#   swpd - virtual memory used
#   free - free memory
#   buff - memory used as buffers
#   cache - memory used as cache
# Swap:
#   si - memory swapped in from disk
#   bo - memory swapped out to disk
# IO:
#   bi - blocks received from block device
#   bo - blocks sent to block device
# System:
#   in - interrupts per second
#   cs - context switches per second
# CPU:
#   us - user time
#   sy - system time
#   id - idle time
#   wa - wait time
#   st - stolen time (virtual machines)
```

#### **iostat** - CPU and I/O Statistics

**Installation on Red Hat/CentOS/Rocky/Alma Linux:**
```bash
# iostat is part of the sysstat package
# Install sysstat package
sudo yum install sysstat -y          # RHEL 7 and earlier
sudo dnf install sysstat -y          # RHEL 8/9 and Fedora

# Enable and start the sysstat service (for data collection)
sudo systemctl enable sysstat
sudo systemctl start sysstat

# Verify installation
iostat -V                            # Check version
which iostat                         # Verify location (/usr/bin/iostat)

# On Ubuntu/Debian (for reference)
# sudo apt-get install sysstat -y
```

**Usage Examples:**
```bash
iostat                # Basic CPU and I/O stats
iostat -x             # Extended statistics
iostat -x 2           # Update every 2 seconds
iostat -p sda         # Per-partition stats for device
iostat -c             # CPU statistics only
iostat -d             # Disk statistics only
iostat -m             # Display in MB/s
iostat -k             # Display in KB/s
iostat -xz            # Extended, skip devices with no activity

# Key metrics to watch:
# %util - Percentage of time device was busy
# await - Average time for I/O requests (ms)
# svctm - Service time (deprecated)
# r/s   - Reads per second
# w/s   - Writes per second
# rkB/s - KB read per second
# wkB/s - KB written per second
# avgqu-sz - Average queue size

# High %util (>80%) indicates I/O bottleneck
# High await indicates slow disk or queue buildup
```

#### **iotop** - I/O Usage by Process

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install iotop -y             # RHEL 7 and earlier
sudo dnf install iotop -y             # RHEL 8/9+

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install iotop -y

# Verify installation
iotop --version
which iotop
```

**Usage:**
```bash
sudo iotop            # Requires root
iotop -o              # Only show processes doing I/O
iotop -a              # Accumulated I/O instead of bandwidth
iotop -p PID          # Monitor specific process
iotop -u user         # Filter by user
iotop -k              # Use kilobytes instead of human-readable
iotop -b              # Batch mode (non-interactive)
iotop -n 5            # Number of iterations in batch mode

# Interactive keys:
# Left/Right arrow - Change sort column
# r - Reverse sort order
# o - Toggle showing only processes with I/O
# p - Toggle showing processes vs threads
# a - Toggle accumulated mode
# q - Quit
```

**Shows per process:**
- Total disk read
- Total disk write
- Swap in percentage
- I/O priority
- Command

#### **lsof** - List Open Files
```bash
lsof                  # List all open files (huge output!)
lsof /path/to/file    # What's using this file?
lsof +D /directory    # What's using files in this directory?
lsof -u username      # Files opened by user
lsof -u ^username     # Files NOT opened by user
lsof -c processname   # Files opened by process
lsof -p PID           # Files opened by PID
lsof -i               # Network connections
lsof -i :80           # What's using port 80?
lsof -i TCP:22        # TCP connections on port 22
lsof -i UDP           # All UDP connections
lsof -i @192.168.1.1  # Connections to specific IP
lsof -t /path/to/file # Return only PIDs (useful for scripts)
lsof -n               # Don't resolve hostnames (faster)
lsof -P               # Don't resolve port names (faster)

# Combinations:
lsof -u username -i   # Network connections by user
lsof -a -u username -c ssh  # -a means AND operation
lsof -i -s TCP:LISTEN # All listening TCP ports
lsof +L1              # Find deleted files still open
lsof -i -n -P | grep ESTABLISHED  # All established connections

# Useful for:
# - Finding which process has a file locked
# - Finding deleted but open files (taking disk space)
# - Troubleshooting "device busy" errors
# - Finding network connections
# - Security auditing
```

#### **strace** - System Call Tracer

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install strace -y            # RHEL 7 and earlier
sudo dnf install strace -y            # RHEL 8/9+

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install strace -y

# Verify installation
strace -V
which strace
```

**Usage:**
```bash
strace command        # Trace a command
strace -p PID         # Attach to running process
strace -f command     # Follow child processes
strace -e open command # Trace only 'open' syscalls
strace -e trace=open,read,write command  # Multiple syscalls
strace -e trace=file command   # All file operations
strace -e trace=network command # All network operations
strace -e trace=process command # Process management calls
strace -c command     # Summary statistics
strace -T command     # Show time spent in each syscall
strace -tt command    # Timestamps with microseconds
strace -r command     # Relative timestamps
strace -o output.txt command  # Save to file
strace -s 512 command # String length (default 32)
strace -y command     # Print file descriptor paths
strace -k command     # Print stack trace

# Advanced usage:
strace -e trace=open -e signal=none command  # Ignore signals
strace -e inject=open:error=ENOENT command   # Fault injection
strace -p $(pgrep processname)  # Attach by name

# Common syscall categories:
# -e trace=file     - open, stat, chmod, unlink, etc.
# -e trace=process  - fork, exec, wait, exit, etc.
# -e trace=network  - socket, connect, send, recv, etc.
# -e trace=signal   - kill, sigaction, etc.
# -e trace=ipc      - shmget, semget, msgget, etc.
# -e trace=desc     - read, write, close, etc.
# -e trace=memory   - mmap, mprotect, brk, etc.

# Example outputs:
# open("/etc/hosts", O_RDONLY) = 3  (success, fd 3)
# open("/nofile", O_RDONLY) = -1 ENOENT (No such file)
# read(3, "data", 4096) = 4 (read 4 bytes)
```

**Use cases:**
- Debugging why an application can't find files
- Finding configuration files being read
- Debugging permission issues
- Performance analysis
- Understanding application behavior

#### **ltrace** - Library Call Tracer

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install ltrace -y            # RHEL 7 and earlier
sudo dnf install ltrace -y            # RHEL 8/9+

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ltrace -y

# Verify installation
ltrace -V
which ltrace
```

**Usage:**
```bash
ltrace command        # Trace library calls
ltrace -p PID         # Attach to running process
ltrace -f command     # Follow child processes
ltrace -c command     # Summary statistics
ltrace -T command     # Show time spent
ltrace -tt command    # Timestamps
ltrace -o output.txt command  # Save to file
ltrace -e function command    # Trace specific function
ltrace -e malloc+free command # Multiple functions
ltrace -S command     # Display system calls too

# Examples:
ltrace ls             # Trace library calls of ls
ltrace -e malloc ls   # Only malloc calls
ltrace -c ./myapp     # Statistics of library usage

# Shows calls like:
# malloc(64) = 0x55555555a2a0
# strlen("hello") = 5
# printf("Hello %s\n", "World") = 12
# free(0x55555555a2a0)
```

**Difference from strace:**
- `strace` traces kernel system calls
- `ltrace` traces user-space library function calls
- Often used together for complete picture

#### **perf** - Performance Analysis Tool

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install perf -y              # RHEL 7 and earlier
sudo dnf install perf -y              # RHEL 8/9+

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install linux-tools-common linux-tools-generic linux-tools-$(uname -r) -y

# Verify installation
perf --version
which perf

# Note: Kernel debug symbols may be needed for detailed analysis
# RHEL/CentOS: sudo debuginfo-install kernel
```

**Usage:**
```bash
perf top              # Real-time performance counter
perf stat command     # Performance statistics
perf record command   # Record performance data
perf report           # Analyze recorded data
perf list             # List available events

# Advanced usage:
perf top -p PID       # Profile specific process
perf stat -e cycles,instructions,cache-misses command
perf record -g command # Record with call graphs
perf record -F 99 -p PID -g -- sleep 30  # Profile for 30 sec
perf diff             # Compare two perf.data files

# CPU performance monitoring:
perf stat -e task-clock,cycles,instructions,cache-references,cache-misses ./app

# Record and analyze:
perf record -g ./myapp
perf report --stdio   # Text-based report
perf report --tui     # Terminal UI

# Flame graphs:
perf record -F 99 -a -g -- sleep 60
perf script | ./flamegraph.pl > flamegraph.svg
```

**What it monitors:**
- CPU cycles
- Cache hits/misses
- Branch predictions
- Page faults
- Context switches
- System calls
- Custom tracepoints

#### **sar** - System Activity Reporter

**Installation:**
```bash
# sar is part of the sysstat package
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install sysstat -y           # RHEL 7 and earlier
sudo dnf install sysstat -y           # RHEL 8/9+

# Enable and start data collection
sudo systemctl enable sysstat
sudo systemctl start sysstat

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install sysstat -y

# Enable data collection (edit /etc/default/sysstat)
sudo sed -i 's/ENABLED="false"/ENABLED="true"/' /etc/default/sysstat
sudo systemctl enable sysstat
sudo systemctl start sysstat

# Verify installation
sar -V
which sar

# Note: Historical data requires waiting for cron jobs to collect data
# Or manually run: sudo /usr/lib64/sa/sa1
```

**Usage:**
```bash
sar                   # Default report (CPU)
sar -u                # CPU utilization
sar -r                # Memory utilization
sar -b                # I/O and transfer rate
sar -d                # Block device statistics
sar -n DEV            # Network statistics
sar -q                # Queue length and load average
sar -w                # Context switches
sar -B                # Paging statistics

# Time-based queries:
sar -s 09:00:00       # Start time
sar -e 17:00:00       # End time
sar -f /var/log/sa/sa17  # Read specific file
sar -u 2 10           # 10 samples at 2-second intervals

# Historical analysis:
sar -u -f /var/log/sa/sa16  # Previous day data
sar -r -s 10:00:00 -e 12:00:00  # Memory from 10am to noon

# Network detailed:
sar -n DEV            # Network interface statistics
sar -n EDEV           # Network errors
sar -n TCP            # TCP statistics
sar -n SOCK           # Socket usage

# Useful combinations:
sar -A                # All reports
sar -u -r -b -n DEV   # CPU, Memory, I/O, Network
```

**Requires:** sysstat package and cron job for data collection

#### **dstat** - Versatile Resource Statistics

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install dstat -y             # RHEL 7 and earlier
sudo dnf install dstat -y             # RHEL 8 (deprecated, consider using pcp-dstat)

# For RHEL 9+ (dstat is deprecated, replaced by pcp)
sudo dnf install pcp-system-tools -y
# Use: pcp dstat

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install dstat -y

# Verify installation
dstat --version
which dstat
```

**Usage:**
```bash
dstat                 # Default output
dstat -cdngy          # CPU, Disk, Net, paging, system
dstat -a              # Show all stats
dstat --top-cpu       # Show most expensive CPU process
dstat --top-mem       # Show process using most memory
dstat --top-io        # Show process with most I/O
dstat -D sda,sdb      # Specific disks
dstat -N eth0         # Specific network interface
dstat --output file.csv  # Export to CSV

# Custom columns:
dstat -c -m -d -n     # CPU, Memory, Disk, Network
dstat --tcp --udp     # TCP and UDP stats
dstat --disk-util    # Disk utilization
dstat --freespace     # Free disk space

# Advanced:
dstat -t --top-cpu-adv --top-mem --top-io  # Comprehensive
dstat --integer       # No decimal points
dstat --nocolor       # Disable colors
```

**Advantages:**
- Combines vmstat, iostat, netstat functionality
- Easy to read columnar output
- Extensible with plugins
- CSV export for analysis

#### **nmon** - Performance Monitor

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install nmon -y              # RHEL 7 and earlier
sudo dnf install nmon -y              # RHEL 8/9+
sudo yum install epel-release -y      # Enable EPEL if needed
sudo dnf install epel-release -y      # For RHEL 8/9

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install nmon -y

# Verify installation
nmon -h
which nmon
```

**Usage:**
```bash
nmon                  # Interactive mode
nmon -f -s 2 -c 30    # Record 30 snapshots at 2-sec intervals
nmon -F filename      # Save to specific file
nmon -t               # Include top processes

# Interactive keys:
# c - CPU stats
# m - Memory stats
# d - Disk I/O
# n - Network
# t - Top processes
# r - Resources
# j - JFS filesystem stats
# k - Kernel stats
# l - Long-term averages
# V - Virtual memory
# h - Help
# q - Quit

# Analysis:
nmonchart file.nmon   # Generate HTML charts (requires nmonchart)
nmon2rrd file.nmon    # Convert to RRD format
```

**Use cases:**
- AIX and Linux performance monitoring
- Historical performance data collection
- Creating performance reports
- Capacity planning

### System Information & Monitoring
```bash
# System resource usage
top                    # Real-time process monitoring
htop                   # Enhanced version of top (needs installation)
atop                   # Advanced system & process monitor
glances                # Cross-platform monitoring tool

# CPU information
lscpu                  # Display CPU architecture info
mpstat                 # CPU usage statistics
cat /proc/cpuinfo      # Detailed CPU information

# Memory information
free -h                # Memory usage (human readable)
vmstat                 # Virtual memory statistics
cat /proc/meminfo      # Detailed memory information

# Disk usage and I/O
df -h                  # Disk space usage
du -sh /path/*         # Directory size
iostat                 # CPU and I/O statistics
iotop                  # I/O usage by process
lsblk                  # List block devices
```

### Process Management

#### **ps** - Process Status
```bash
# Common usage patterns
ps aux                 # BSD style - all processes, user-oriented
ps -ef                 # UNIX style - all processes, full format
ps -eF                 # Extra full format
ps -ely                # Long format with priority
ps axjf                # Process tree (forest)
ps -u username         # Processes by user
ps -C processname      # Processes by name
ps -p 1234             # Specific PID
ps --ppid 1234         # Children of specific parent

# Advanced options
ps aux --sort=-%cpu    # Sort by CPU (descending)
ps aux --sort=-%mem    # Sort by memory (descending)
ps aux --sort=-rss     # Sort by resident memory
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head
ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,comm  # Scheduling info
ps -eo pid,user,args --forest  # Tree view with full command

# Custom output
ps -eo pid,user,vsz,rss,stat,start,time,cmd
# pid    - Process ID
# user   - Owner
# vsz    - Virtual memory size (KB)
# rss    - Resident set size (actual RAM in KB)
# stat   - Process state
# start  - Start time
# time   - CPU time consumed
# cmd    - Command

# Process states (STAT column):
# R - Running or runnable
# S - Interruptible sleep (waiting for event)
# D - Uninterruptible sleep (usually I/O)
# T - Stopped (by job control signal)
# t - Stopped by debugger
# Z - Zombie (terminated but not reaped)
# X - Dead (should never be seen)
# < - High priority
# N - Low priority
# L - Has pages locked in memory
# s - Session leader
# l - Multi-threaded
# + - Foreground process group

# Watch processes in real-time
watch -n 1 'ps aux --sort=-%cpu | head -20'
```

#### **pgrep/pkill** - Process Grep/Kill
```bash
pgrep processname      # Find PIDs by name
pgrep -u username      # PIDs by user
pgrep -l processname   # Show PID and name
pgrep -f "full command line"  # Match full command
pgrep -n processname   # Newest matching process
pgrep -o processname   # Oldest matching process
pgrep -x exact_name    # Exact match only
pgrep -a processname   # Show full command line

# Advanced pgrep
pgrep -u username -l   # All processes by user with names
pgrep -g groupid       # By group ID
pgrep -s sessionid     # By session ID
pgrep -t tty           # By terminal

# pkill - Kill by name
pkill processname      # Kill all matching processes
pkill -9 processname   # Force kill (SIGKILL)
pkill -u username      # Kill all user's processes
pkill -TERM processname # Send SIGTERM
pkill -HUP processname  # Send SIGHUP (reload config)
pkill -f "pattern"     # Match full command line

# Safety with pkill
pkill -l processname   # List what would be killed (dry run)
pgrep -a processname && pkill processname  # Check then kill
```

#### **pstree** - Process Tree
```bash
pstree                 # Show process tree
pstree -p              # Show PIDs
pstree -u              # Show user transitions
pstree -a              # Show command line arguments
pstree -g              # Show process groups
pstree -h              # Highlight current process
pstree -H PID          # Highlight specific process
pstree -s PID          # Show parents of process
pstree -p username     # Tree for specific user
pstree -t              # Show threads
pstree -n              # Sort by PID
pstree -G              # Use VT100 line drawing characters
pstree -c              # Disable compaction

# Combined options
pstree -aup            # Full details with users and PIDs
pstree -p | grep processname  # Find process in tree

# Example output:
# systemd─┬─NetworkManager─┬─{NetworkManager}
#         │                 └─{NetworkManager}
#         ├─sshd─┬─sshd───bash───pstree
#         │      └─sshd───bash
```

#### **pidof** - Find PID of Running Program
```bash
pidof processname      # Get PID(s) of process
pidof -s processname   # Single PID (if multiple)
pidof -x scriptname    # Also find shell scripts
pidof -o %PPID processname  # Omit parent process

# Usage in scripts
kill $(pidof processname)
PID=$(pidof processname)
if pidof processname > /dev/null; then
    echo "Process is running"
fi
```

#### **kill/killall** - Terminate Processes
```bash
kill PID               # Send SIGTERM (15) - graceful
kill -9 PID            # Send SIGKILL (9) - force
kill -15 PID           # Same as kill PID
kill -TERM PID         # Same as kill PID
kill -HUP PID          # Hangup (reload config often)
kill -INT PID          # Interrupt (Ctrl+C)
kill -QUIT PID         # Quit (with core dump)
kill -STOP PID         # Stop process (pause)
kill -CONT PID         # Continue stopped process
kill -USR1 PID         # User-defined signal 1
kill -USR2 PID         # User-defined signal 2

# List signals
kill -l                # List all signals
kill -l 9              # Name of signal 9 (KILL)
kill -l TERM           # Number of SIGTERM (15)

# killall - by name
killall processname    # Kill all instances
killall -9 processname # Force kill all
killall -u username    # Kill all user's processes
killall -i processname # Interactive (ask before each)
killall -w processname # Wait for processes to die
killall -y 30m processname  # Only if younger than 30 min
killall -o 30m processname  # Only if older than 30 min

# Signal types and uses:
# SIGTERM (15) - Graceful shutdown (default)
# SIGKILL (9)  - Force kill (cannot be caught)
# SIGHUP (1)   - Reload configuration
# SIGINT (2)   - Interrupt from keyboard (Ctrl+C)
# SIGQUIT (3)  - Quit from keyboard (Ctrl+\)
# SIGSTOP (19) - Pause process
# SIGCONT (18) - Resume process
# SIGUSR1/2    - Application defined
```

#### **nice/renice** - Process Priority
```bash
# nice values: -20 (highest) to 19 (lowest)
# Default priority: 0

# Start with priority
nice -n 10 command     # Start with lower priority
nice -n -5 command     # Higher priority (requires root)
nice --adjustment=10 command  # Same as -n 10

# Change running process priority
renice 10 -p PID       # Set to priority 10
renice -5 -p PID       # Set to priority -5 (needs root)
renice 10 -u username  # All user's processes
renice 10 -g groupname # All group's processes

# Check current nice value
ps -eo pid,ni,cmd      # Show nice values
top                    # NI column shows nice value

# Example: Run backup with low priority
nice -n 19 tar czf backup.tar.gz /data

# Example: Boost database priority
sudo renice -10 -p $(pidof mysqld)
```

#### **nohup** - Run Command Immune to Hangups
```bash
nohup command &        # Run in background, ignore SIGHUP
nohup command > output.log 2>&1 &  # Redirect output
nohup long_running_script.sh &

# Output goes to nohup.out by default
# Check progress
tail -f nohup.out

# Find nohup processes
ps aux | grep -v grep | grep nohup
```

#### **/proc filesystem** - Process Information
```bash
# Process-specific directories: /proc/PID/

# Command line and environment
cat /proc/PID/cmdline  # Command with arguments (null-separated)
tr '\0' ' ' < /proc/PID/cmdline; echo  # Human-readable
cat /proc/PID/environ  # Environment variables
tr '\0' '\n' < /proc/PID/environ  # Readable environment

# Process status and stats
cat /proc/PID/status   # Comprehensive status
cat /proc/PID/stat     # Raw statistics
cat /proc/PID/statm    # Memory statistics
cat /proc/PID/io       # I/O statistics
cat /proc/PID/limits   # Resource limits

# Memory mapping
cat /proc/PID/maps     # Memory map
cat /proc/PID/smaps    # Detailed memory map
pmap PID               # User-friendly memory map

# File descriptors
ls -l /proc/PID/fd/    # Open file descriptors
ls -l /proc/PID/fd/ | wc -l  # Count open files
readlink /proc/PID/exe # Executable path
readlink /proc/PID/cwd # Current working directory

# Network
cat /proc/PID/net/tcp  # TCP connections
cat /proc/PID/net/udp  # UDP connections

# System-wide information
cat /proc/cpuinfo      # CPU information
cat /proc/meminfo      # Memory information
cat /proc/version      # Kernel version
cat /proc/uptime       # System uptime
cat /proc/loadavg      # Load average
cat /proc/sys/fs/file-nr  # Open file handles (system-wide)
cat /proc/sys/fs/file-max # Maximum file handles
```

#### **systemctl** - Service Management (systemd)
```bash
# Service operations
systemctl start service    # Start service
systemctl stop service     # Stop service
systemctl restart service  # Restart service
systemctl reload service   # Reload config without restart
systemctl status service   # Service status
systemctl enable service   # Enable at boot
systemctl disable service  # Disable at boot
systemctl is-active service   # Check if running
systemctl is-enabled service  # Check if enabled

# Information
systemctl list-units       # List loaded units
systemctl list-units --type=service  # Services only
systemctl list-units --failed  # Failed units
systemctl list-unit-files  # All unit files
systemctl list-dependencies service  # Dependencies
systemctl show service     # All properties

# System state
systemctl status           # System status
systemctl --failed         # Failed services
systemctl list-jobs        # Active jobs

# Advanced
systemctl cat service      # Show unit file
systemctl edit service     # Edit override
systemctl daemon-reload    # Reload systemd config
systemctl isolate multi-user.target  # Change target
systemctl get-default      # Default target
systemctl set-default multi-user.target  # Set default

# Masking (prevent service from starting)
systemctl mask service     # Prevent start
systemctl unmask service   # Allow start

# Resource management
systemctl show -p CPUShares service
systemctl set-property service CPUShares=512
systemd-cgtop             # Control group resource usage
```

### Network Troubleshooting

#### **ping** - Test Network Connectivity
```bash
ping host              # Basic ping
ping -c 4 host         # Send 4 packets then stop
ping -i 2 host         # 2-second interval
ping -s 1000 host      # Packet size 1000 bytes
ping -f host           # Flood ping (root only)
ping -I eth0 host      # Use specific interface
ping -w 10 host        # Timeout after 10 seconds
ping -q host           # Quiet output (summary only)
ping -a host           # Audible ping
ping -4 host           # Force IPv4
ping -6 host           # Force IPv6

# Advanced usage
ping -c 1 -W 1 host    # Single packet, 1-sec timeout
ping -M do -s 1472 host # Path MTU discovery (don't fragment)
ping -R host           # Record route
ping -t 64 host        # Set TTL

# Parse output
# TTL - Time To Live (hops remaining)
# time - Round trip time
# Loss percentage indicates network issues
# TTL decreasing = packets taking different routes
```

**What to look for:**
- **0% packet loss** = Good connection
- **<5% packet loss** = Acceptable for most uses
- **>5% packet loss** = Network issues
- **High latency (>100ms)** = Slow network
- **Variable latency** = Network congestion

#### **traceroute/tracepath** - Trace Network Path
```bash
traceroute host        # Trace route to host
traceroute -n host     # No DNS resolution (faster)
traceroute -I host     # Use ICMP instead of UDP
traceroute -T host     # Use TCP SYN
traceroute -p 80 host  # Use specific port
traceroute -m 20 host  # Max 20 hops
traceroute -w 2 host   # Wait 2 seconds per hop
traceroute -q 1 host   # 1 query per hop (faster)

# tracepath (no root required)
tracepath host         # Similar to traceroute
tracepath -n host      # No DNS resolution
tracepath -b host      # Print both hostnames and IPs
tracepath -m 20 host   # Max hops

# Read output:
# 1  router.local (192.168.1.1)  1.234 ms
# 2  10.0.0.1  5.678 ms
# 3  * * *    (timeout/blocked)
# 4  endpoint  45.123 ms

# * * * means:
# - Firewall blocking
# - Router not sending ICMP replies
# - Packet loss at that hop
```

#### **mtr** - Network Diagnostic Tool
```bash
mtr host               # Interactive mode
mtr -r -c 100 host     # Report mode, 100 cycles
mtr -n host            # No DNS
mtr -b host            # Show both hostnames and IPs
mtr -o "LSD NBAW" host # Custom fields
mtr -i 2 host          # 2-second interval
mtr -s 1000 host       # Packet size
mtr --tcp -P 80 host   # TCP to port 80
mtr --udp host         # Use UDP
mtr -4 host            # IPv4 only
mtr -6 host            # IPv6 only

# Save to file
mtr -r -c 100 host > report.txt

# Fields explained:
# Loss%  - Packet loss percentage
# Snt    - Packets sent
# Last   - Last latency
# Avg    - Average latency
# Best   - Best latency
# Wrst   - Worst latency
# StDev  - Standard deviation

# Interactive keys:
# r - Reset statistics
# p - Pause
# d - Display mode
# n - Toggle DNS
# q - Quit
```

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install mtr -y               # RHEL 7 and earlier
sudo dnf install mtr -y               # RHEL 8/9+

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mtr -y

# Verify installation
mtr --version
which mtr
```

**Advantages over ping/traceroute:**
- Combines functionality of both
- Real-time statistics
- Shows packet loss per hop
- Identifies problematic routers

#### **netstat** - Network Statistics (legacy)
```bash
netstat -tuln          # TCP/UDP listening ports
netstat -tulpn         # Include program names (root)
netstat -an            # All connections, numeric
netstat -r             # Routing table
netstat -i             # Interface statistics
netstat -s             # Protocol statistics
netstat -c             # Continuous update
netstat -e             # Extended information

# Common combinations
netstat -tulpn | grep :80     # What's on port 80?
netstat -an | grep ESTABLISHED # Active connections
netstat -an | grep TIME_WAIT   # TIME_WAIT connections
netstat -tulpn | grep LISTEN   # All listening ports

# Connection states:
# LISTEN      - Waiting for connections
# ESTABLISHED - Active connection
# TIME_WAIT   - Waiting after close
# CLOSE_WAIT  - Remote closed, local not
# FIN_WAIT1   - Connection closing
# FIN_WAIT2   - Connection closed
# SYN_SENT    - Attempting connection
# SYN_RECV    - Received connection request
```

#### **ss** - Socket Statistics (modern replacement for netstat)
```bash
ss                     # All connections
ss -tuln               # TCP/UDP listening, numeric
ss -tulpn              # Include process info
ss -s                  # Summary statistics
ss -a                  # All sockets
ss -l                  # Listening sockets
ss -t                  # TCP only
ss -u                  # UDP only
ss -x                  # Unix sockets
ss -4                  # IPv4 only
ss -6                  # IPv6 only
ss -p                  # Show process
ss -n                  # Numeric (no DNS/service resolution)
ss -e                  # Extended info
ss -m                  # Memory usage
ss -i                  # TCP internal info

# Filtering
ss state established   # Only ESTABLISHED
ss state listening     # Only LISTENING
ss state time-wait     # Only TIME-WAIT
ss dst 192.168.1.1     # Connections to specific IP
ss dport = :80         # Connections on port 80
ss sport = :22         # Source port 22
ss '( dport = :80 or sport = :80 )'  # Port 80 either direction

# Common usage
ss -tulpn | grep :443  # HTTPS connections
ss -tn src :80         # TCP connections from port 80
ss -o state established '( dport = :ssh or sport = :ssh )'
ss -at '( dport = :443 or sport = :443 )'  # HTTPS connections

# Output with timers
ss -to                 # Show TCP timers
ss -e                  # Show detailed socket info

# Why ss instead of netstat:
# - Faster (especially with many connections)
# - More detailed information
# - Better filtering capabilities
# - Active development
```

#### **tcpdump** - Packet Capture and Analysis

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install tcpdump -y           # RHEL 7 and earlier
sudo dnf install tcpdump -y           # RHEL 8/9+

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tcpdump -y

# Verify installation
tcpdump --version
which tcpdump

# Note: Requires root/sudo privileges to capture packets
```

**Usage:**
```bash
# Basic capture
tcpdump                # Capture on default interface
tcpdump -i eth0        # Specific interface
tcpdump -i any         # All interfaces
tcpdump -n             # No DNS resolution
tcpdump -nn            # No DNS or port resolution
tcpdump -c 100         # Capture 100 packets
tcpdump -w file.pcap   # Write to file
tcpdump -r file.pcap   # Read from file
tcpdump -A             # ASCII output
tcpdump -X             # Hex and ASCII output
tcpdump -v             # Verbose
tcpdump -vv            # More verbose
tcpdump -vvv           # Very verbose

# Filters
tcpdump host 192.168.1.1          # Traffic to/from host
tcpdump src 192.168.1.1           # From source
tcpdump dst 192.168.1.1           # To destination
tcpdump net 192.168.1.0/24        # Network
tcpdump port 80                   # Port 80
tcpdump portrange 20-22           # Port range
tcpdump tcp                       # TCP only
tcpdump udp                       # UDP only
tcpdump icmp                      # ICMP only

# Protocol specific
tcpdump tcp port 80               # HTTP traffic
tcpdump tcp port 443              # HTTPS traffic
tcpdump udp port 53               # DNS queries
tcpdump tcp port 22               # SSH traffic

# Logical operators
tcpdump 'host 192.168.1.1 and port 80'
tcpdump 'src 192.168.1.1 or dst 192.168.1.1'
tcpdump 'tcp and not port 22'
tcpdump 'port 80 or port 443'

# Advanced filters
tcpdump 'tcp[tcpflags] & (tcp-syn) != 0'  # SYN packets
tcpdump 'tcp[tcpflags] & (tcp-rst) != 0'  # RST packets
tcpdump 'tcp[13] & 2 != 0'                # SYN packets (alt)
tcpdump 'greater 1000'                    # Packets > 1000 bytes
tcpdump 'less 100'                        # Packets < 100 bytes

# Real-world examples
tcpdump -i eth0 -nn 'port 80 and (tcp[tcpflags] & tcp-syn != 0)'
tcpdump -i any -nn -s0 -v port 53         # DNS debugging
tcpdump -i eth0 -nn -A 'port 80 and host 192.168.1.1'
tcpdump -i eth0 -w capture.pcap 'host 10.0.0.1 and port 443'

# Capture and analyze later
tcpdump -i eth0 -s 0 -w dump.pcap
tcpdump -r dump.pcap | less
tcpdump -r dump.pcap 'port 80'
```

**Common use cases:**
- Debug network connectivity issues
- Analyze application protocols
- Detect network attacks
- Troubleshoot DNS issues
- Monitor bandwidth usage

#### **nslookup/dig/host** - DNS Troubleshooting
```bash
# nslookup (interactive and non-interactive)
nslookup example.com              # Simple lookup
nslookup example.com 8.8.8.8      # Use specific DNS
nslookup -type=mx example.com     # Mail servers
nslookup -type=ns example.com     # Name servers
nslookup -type=txt example.com    # TXT records
nslookup -type=soa example.com    # SOA record
nslookup -type=any example.com    # All records
nslookup -debug example.com       # Debug mode

# dig (more detailed)
dig example.com                   # A record
dig example.com +short            # Brief output
dig example.com @8.8.8.8          # Use specific DNS
dig -x 8.8.8.8                    # Reverse lookup
dig example.com MX                # Mail servers
dig example.com NS                # Name servers
dig example.com TXT               # TXT records
dig example.com ANY               # All records
dig example.com +trace            # Trace delegation
dig example.com +noall +answer    # Only answers
dig example.com +stats            # Show statistics
dig -t AAAA example.com           # IPv6 address

# Advanced dig
dig @8.8.8.8 example.com +dnssec  # DNSSEC validation
dig +tcp example.com              # Force TCP
dig +nocmd +noall +answer example.com  # Clean output
dig +short example.com A example.org A  # Multiple queries

# host (simple interface)
host example.com                  # Basic lookup
host -t MX example.com            # Mail servers
host -t NS example.com            # Name servers
host -a example.com               # All records
host 8.8.8.8                      # Reverse lookup
host -v example.com               # Verbose

# DNS configuration
cat /etc/resolv.conf              # DNS servers
cat /etc/hosts                    # Local hosts file
cat /etc/nsswitch.conf            # Name resolution order

# Test DNS resolution
getent hosts example.com          # Use system resolver
getent ahosts example.com         # All addresses
```

**DNS troubleshooting workflow:**
1. Check `/etc/resolv.conf` for DNS servers
2. Test with `dig example.com` - if fails, DNS issue
3. Test with different DNS: `dig @8.8.8.8 example.com`
4. Use `+trace` to see delegation path
5. Check local hosts file: `/etc/hosts`

#### **ip** - Network Configuration (modern)
```bash
# Show/set IP addresses
ip addr                           # Show all addresses
ip addr show dev eth0             # Specific interface
ip addr add 192.168.1.10/24 dev eth0  # Add address
ip addr del 192.168.1.10/24 dev eth0  # Remove address
ip -br addr                       # Brief output
ip -4 addr                        # IPv4 only
ip -6 addr                        # IPv6 only

# Interface management
ip link                           # Show interfaces
ip link show dev eth0             # Specific interface
ip link set eth0 up               # Bring up
ip link set eth0 down             # Bring down
ip link set eth0 mtu 9000         # Set MTU
ip link set eth0 promisc on       # Promiscuous mode

# Routing
ip route                          # Show routing table
ip route show                     # Same as above
ip route get 8.8.8.8              # Route to specific IP
ip route add default via 192.168.1.1  # Add default gateway
ip route add 10.0.0.0/8 via 192.168.1.1  # Add route
ip route del 10.0.0.0/8           # Delete route
ip -6 route                       # IPv6 routes

# Neighbors (ARP table)
ip neigh                          # Show ARP cache
ip neigh show dev eth0            # Specific interface
ip neigh add 192.168.1.1 lladdr aa:bb:cc:dd:ee:ff dev eth0
ip neigh del 192.168.1.1 dev eth0 # Delete entry
ip neigh flush dev eth0           # Flush ARP cache

# Statistics
ip -s link                        # Interface statistics
ip -s -s link                     # More detailed stats
ip -stats neigh                   # Neighbor stats

# Multiple commands
ip addr show && ip route show
ip -br -c addr                    # Brief, colored output

# Monitor changes
ip monitor                        # Watch for changes
ip monitor all                    # All subsystems
ip monitor route                  # Route changes only
```

#### **curl/wget** - HTTP/HTTPS Testing
```bash
# curl - Advanced HTTP client
curl http://example.com           # GET request
curl -I http://example.com        # HEAD request (headers only)
curl -v http://example.com        # Verbose (see request/response)
curl -s http://example.com        # Silent mode
curl -o file.html http://example.com  # Save output
curl -O http://example.com/file.zip   # Save with original name
curl -L http://example.com        # Follow redirects
curl -k https://example.com       # Insecure (ignore SSL errors)
curl -x proxy:8080 http://example.com  # Use proxy

# HTTP methods
curl -X POST http://example.com   # POST request
curl -X PUT http://example.com    # PUT request
curl -X DELETE http://example.com # DELETE request

# Headers and data
curl -H "Content-Type: application/json" http://example.com
curl -H "Authorization: Bearer TOKEN" http://example.com
curl -d "key=value" http://example.com  # POST data
curl -d @file.json http://example.com   # POST from file
curl -F "file=@upload.txt" http://example.com  # File upload

# Authentication
curl -u username:password http://example.com
curl --basic -u user:pass http://example.com
curl --digest -u user:pass http://example.com

# SSL/TLS
curl -v https://example.com 2>&1 | grep -i "ssl\|tls"
curl --cacert ca.crt https://example.com
curl --cert client.crt --key client.key https://example.com

# Timing
curl -w "@curl-format.txt" -o /dev/null -s http://example.com
# curl-format.txt content:
# time_namelookup:  %{time_namelookup}\n
# time_connect:     %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer: %{time_pretransfer}\n
# time_redirect:    %{time_redirect}\n
# time_starttransfer: %{time_starttransfer}\n
# time_total:       %{time_total}\n

# Quick timing
curl -w "DNS: %{time_namelookup} Connect: %{time_connect} Total: %{time_total}\n" -o /dev/null -s http://example.com

# wget - File downloader
wget http://example.com/file.zip  # Download file
wget -O output.html http://example.com  # Save as
wget -c http://example.com/large.zip    # Continue download
wget -b http://example.com/file.zip     # Background
wget -q http://example.com              # Quiet mode
wget -r http://example.com              # Recursive
wget -np -r http://example.com/dir/     # No parent
wget --spider http://example.com        # Check if URL exists
wget --limit-rate=200k http://example.com  # Limit bandwidth
wget --tries=10 http://example.com      # Retry attempts
wget --timeout=30 http://example.com    # Timeout
```

#### **nc (netcat)** - TCP/UDP Swiss Army Knife
```bash
# Port scanning
nc -zv host 80                    # Test TCP port
nc -zvu host 53                   # Test UDP port
nc -zv host 20-80                 # Scan port range
nc -zv -w 2 host 22               # 2-second timeout

# Connect to service
nc host 80                        # Connect to port 80
# Then type: GET / HTTP/1.0
nc -v host 22                     # Verbose connection

# Listen mode (server)
nc -l 1234                        # Listen on port 1234
nc -l -p 1234                     # Explicit port
nc -l -k 1234                     # Keep listening after disconnect

# Transfer files
# On receiver:
nc -l 1234 > received_file
# On sender:
nc receiver_ip 1234 < file_to_send

# Chat/debug
# Server:
nc -l 1234
# Client:
nc server_ip 1234
# Type messages in either terminal

# UDP mode
nc -u host 53                     # UDP connection
nc -lu 1234                       # UDP listener

# Proxy/relay
nc -l 1234 | nc remote_host 80    # Simple proxy

# Execute command (DANGEROUS - security risk)
nc -l 1234 -e /bin/bash           # Remote shell (don't use!)

# Banner grabbing
echo "" | nc -v -w 2 host 22      # SSH banner
echo "GET / HTTP/1.0\r\n" | nc host 80  # HTTP banner
```

#### **iftop** - Network Bandwidth Monitor

**Installation:**
```bash
# Red Hat/CentOS/Rocky/Alma Linux
sudo yum install iftop -y             # RHEL 7 and earlier
sudo dnf install iftop -y             # RHEL 8/9+
sudo yum install epel-release -y      # Enable EPEL if needed
sudo dnf install epel-release -y      # For RHEL 8/9

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install iftop -y

# Verify installation
iftop -h
which iftop

# Note: Requires root/sudo privileges
```

**Usage:**
```bash
sudo iftop                        # Monitor default interface
sudo iftop -i eth0                # Specific interface
sudo iftop -n                     # No DNS resolution
sudo iftop -N                     # No port resolution
sudo iftop -P                     # Show ports
sudo iftop -B                     # Display in bytes
sudo iftop -f 'port 80'           # Filter traffic
sudo iftop -F 192.168.1.0/24      # Filter by network

# Interactive keys:
# n - Toggle DNS resolution
# N - Toggle port resolution
# t - Toggle display mode
# p - Show/hide ports
# P - Pause display
# j/k - Scroll display
# l - Display scale
# q - Quit

# BPF filter examples:
sudo iftop -f 'dst port 80'
sudo iftop -f 'src host 192.168.1.1'
```

#### **iperf3** - Network Performance Testing
```bash
# Server mode
iperf3 -s                         # Start server
iperf3 -s -p 5201                 # Specific port

# Client mode
iperf3 -c server_ip               # Test to server
iperf3 -c server_ip -t 60         # Test for 60 seconds
iperf3 -c server_ip -P 4          # 4 parallel streams
iperf3 -c server_ip -R            # Reverse (download test)
iperf3 -c server_ip -u            # UDP test
iperf3 -c server_ip -u -b 100M    # UDP with 100Mbps bandwidth
iperf3 -c server_ip -i 1          # 1-second intervals
iperf3 -c server_ip -J            # JSON output
iperf3 -c server_ip -w 256K       # Set TCP window size

# Bidirectional test
iperf3 -c server_ip --bidir

# Example output analysis:
# Bandwidth - Transfer speed achieved
# Retr - Retransmissions (packet loss indicator)
# Cwnd - Congestion window (TCP performance)
```

### Network Troubleshooting
```bash
# Network connectivity
ping <host>            # Test connectivity
traceroute <host>      # Trace network path
mtr <host>             # Combined ping & traceroute
telnet <host> <port>   # Test TCP connection
nc -zv <host> <port>   # Port scanning with netcat

# Network configuration
ip addr                # IP addresses
ip route               # Routing table
ss -tulpn              # Socket statistics (modern)
netstat -tulpn         # Network connections (legacy)
lsof -i                # Network connections by process
tcpdump -i eth0        # Packet capture

# DNS troubleshooting
nslookup <domain>      # DNS lookup
dig <domain>           # Detailed DNS query
host <domain>          # Simple DNS lookup
cat /etc/resolv.conf   # DNS configuration
```

### Log Analysis

#### **journalctl** - Systemd Journal Viewer
```bash
# Basic usage
journalctl                        # All logs (paged)
journalctl -f                     # Follow (like tail -f)
journalctl -r                     # Reverse order (newest first)
journalctl -n 50                  # Last 50 lines
journalctl --no-pager             # Don't page output

# Time-based filtering
journalctl --since "2025-10-01"   # Since date
journalctl --since "2 hours ago"
journalctl --since "10 minutes ago"
journalctl --since "2025-10-17 09:00:00"
journalctl --until "2025-10-17 17:00:00"
journalctl --since today
journalctl --since yesterday
journalctl --since "2 days ago" --until "1 day ago"

# Service-specific logs
journalctl -u nginx               # Specific service
journalctl -u nginx -u mysql      # Multiple services
journalctl -u nginx --since today
journalctl -u nginx -f            # Follow service logs
journalctl -u nginx -n 100        # Last 100 lines

# Priority filtering
journalctl -p err                 # Errors only
journalctl -p warning             # Warning and above
journalctl -p emerg..err          # Range (emerg to error)
# Priorities: emerg, alert, crit, err, warning, notice, info, debug

# Boot-related
journalctl -b                     # Current boot
journalctl -b -1                  # Previous boot
journalctl -b -2                  # 2 boots ago
journalctl --list-boots           # List all boots
journalctl -b <boot_id>           # Specific boot

# Kernel messages
journalctl -k                     # Kernel messages only
journalctl -k -b                  # Kernel from this boot
journalctl -k -p err              # Kernel errors

# Process/User filtering
journalctl _PID=1234              # By process ID
journalctl _UID=1000              # By user ID
journalctl _COMM=sshd             # By command name
journalctl /usr/bin/nginx         # By executable path

# Output formatting
journalctl -o verbose             # Verbose format
journalctl -o json                # JSON format
journalctl -o json-pretty         # Pretty JSON
journalctl -o cat                 # Just messages (no metadata)
journalctl -o short-iso           # ISO timestamps
journalctl -o short-precise       # Precise timestamps

# Advanced filtering
journalctl _TRANSPORT=kernel      # Kernel logs
journalctl _SYSTEMD_UNIT=nginx.service  # By unit
journalctl --disk-usage           # Journal disk usage
journalctl --verify               # Verify journal integrity

# Maintenance
journalctl --vacuum-time=2weeks   # Keep 2 weeks
journalctl --vacuum-size=500M     # Max 500MB
journalctl --rotate               # Rotate journals

# Export/analysis
journalctl -u nginx -o json > nginx.json
journalctl --since "1 hour ago" | grep -i error
journalctl -u mysql --no-pager | awk '/ERROR/ {print}'

# Real-world examples
journalctl -u nginx -p err --since today  # Today's nginx errors
journalctl -f | grep -i "fail\|error\|warn"  # Live error monitoring
journalctl _COMM=sshd --since "1 hour ago"   # Recent SSH activity
journalctl -u '*' --since "10 minutes ago" -p err  # All recent errors

# Persistent journals (edit /etc/systemd/journald.conf)
# Storage=persistent
sudo systemctl restart systemd-journald
```

#### **dmesg** - Kernel Ring Buffer
```bash
dmesg                             # All kernel messages
dmesg -T                          # Human-readable timestamps
dmesg -t                          # No timestamps
dmesg -H                          # Human-readable (paged, colored)
dmesg -w                          # Wait for new messages (follow)
dmesg -l err                      # Error messages only
dmesg -l warn                     # Warnings only
dmesg -l info                     # Info messages
dmesg -f daemon                   # Daemon messages
dmesg -c                          # Read and clear
dmesg -C                          # Clear only
dmesg -n 1                        # Set console log level
dmesg -s 1000000                  # Buffer size (bytes)

# Facility filters
dmesg -f kern                     # Kernel messages
dmesg -f user                     # User-level messages
dmesg -f mail                     # Mail system
dmesg -f daemon                   # System daemons

# Level filters (can combine with -l)
# emerg, alert, crit, err, warn, notice, info, debug

# Time-based
dmesg --since '1 hour ago'
dmesg --until '10 minutes ago'

# Combined filters
dmesg -T -l err,warn              # Errors and warnings with time
dmesg -H -l err -f kern           # Kernel errors, human-readable

# Useful searches
dmesg | grep -i error             # Find errors
dmesg | grep -i fail              # Find failures
dmesg | grep -i 'out of memory'   # OOM issues
dmesg | grep -i segfault          # Segmentation faults
dmesg | grep -i usb               # USB events
dmesg | grep -i eth0              # Network interface
dmesg | grep -i sda               # Disk issues
dmesg | grep -i temperature       # Temperature issues

# Monitor hardware
dmesg -T | grep -i 'hardware error'
dmesg -T | grep -i 'i/o error'
dmesg -T | grep -i 'firmware'

# Real-world examples
dmesg -T | tail -50               # Recent messages
dmesg -T | grep -E 'eth0|wlan0'   # Network interfaces
dmesg | grep -i -E 'error|fail|warn|critical'  # All issues
watch -n 1 'dmesg -T | tail -20'  # Live monitoring
```

#### **tail/head** - View Log Files
```bash
# tail - View end of file
tail /var/log/syslog              # Last 10 lines
tail -n 50 /var/log/syslog        # Last 50 lines
tail -f /var/log/syslog           # Follow (live updates)
tail -F /var/log/syslog           # Follow with retry (if rotated)
tail -n +1 file.log               # From line 1 (entire file)
tail -c 1024 file.log             # Last 1024 bytes
tail -q -f file1.log file2.log    # Multiple files, quiet

# head - View beginning of file
head /var/log/syslog              # First 10 lines
head -n 50 /var/log/syslog        # First 50 lines
head -c 1024 file.log             # First 1024 bytes

# Combined usage
tail -f /var/log/syslog | grep error  # Follow and filter
tail -n 100 /var/log/syslog | grep -i fail

# Multiple files
tail -f /var/log/{syslog,auth.log}
multitail /var/log/syslog /var/log/auth.log  # Split screen

# Rotate-safe following
tail -F /var/log/app.log          # Continue after logrotate
```

#### **grep/egrep/zgrep** - Search Logs
```bash
# Basic grep
grep "error" /var/log/syslog      # Find "error"
grep -i "error" /var/log/syslog   # Case-insensitive
grep -v "debug" /var/log/syslog   # Invert (exclude "debug")
grep -c "error" /var/log/syslog   # Count matches
grep -n "error" /var/log/syslog   # Show line numbers
grep -A 5 "error" /var/log/syslog # 5 lines after match
grep -B 5 "error" /var/log/syslog # 5 lines before match
grep -C 5 "error" /var/log/syslog # 5 lines before and after

# Recursive search
grep -r "error" /var/log/         # Search all files
grep -r -i "failed" /var/log/ --include="*.log"
grep -r "error" /var/log/ --exclude="*.gz"

# Extended regex (egrep or grep -E)
grep -E "error|fail|warn" /var/log/syslog
grep -E "ERROR: .* failed" /var/log/syslog
egrep "^[0-9]{4}-[0-9]{2}-[0-9]{2}" /var/log/syslog  # Date pattern

# Compressed files (zgrep)
zgrep "error" /var/log/syslog.1.gz
zgrep -i "fail" /var/log/*.gz

# Advanced patterns
grep -P "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" /var/log/access.log  # IP addresses
grep -oP "(?<=error: ).*" /var/log/syslog  # Extract after "error: "

# Multiple patterns
grep -e "error" -e "fail" -e "warn" /var/log/syslog
grep -f patterns.txt /var/log/syslog  # Patterns from file

# Performance
grep -F "exact.string" /var/log/huge.log  # Fixed string (faster)
LC_ALL=C grep "pattern" /var/log/huge.log # Faster for ASCII

# Real-world examples
grep -i "authentication failure" /var/log/auth.log
grep "Out of memory" /var/log/syslog
grep -E "refused|denied|invalid" /var/log/auth.log
grep "$(date +'%b %d')" /var/log/syslog  # Today's logs
grep "error" /var/log/*.log | wc -l      # Count errors across files
```

#### **awk** - Log Processing
```bash
# Print specific columns
awk '{print $1, $3}' /var/log/syslog    # Columns 1 and 3
awk '{print $NF}' /var/log/syslog       # Last column
awk '{print $1, $NF}' /var/log/syslog   # First and last

# Filter and print
awk '/error/ {print $0}' /var/log/syslog # Lines with "error"
awk '/error/ {print $1, $3}' /var/log/syslog
awk '$3 ~ /ERROR/ {print}' /var/log/syslog

# Conditions
awk '$3 == "ERROR" {print}' file.log
awk '$1 > 100 {print}' file.log
awk 'NF > 5 {print}' file.log           # More than 5 fields

# Count and statistics
awk '{count++} END {print count}' file.log  # Count lines
awk '{sum+=$1} END {print sum}' file.log    # Sum column 1
awk '{sum+=$1} END {print sum/NR}' file.log # Average

# Field separators
awk -F: '{print $1, $3}' /etc/passwd    # Use : as separator
awk -F',' '{print $2}' file.csv         # CSV file

# Real-world examples
awk '/Failed/ {print $1, $2, $11}' /var/log/auth.log  # Failed logins
awk '{print $4}' /var/log/apache2/access.log | sort | uniq -c  # Count by field
journalctl -u nginx | awk '/error/ {print $0}'
awk '$9 ~ /^5/ {print $7}' /var/log/nginx/access.log  # 5xx errors

# Complex example - analyze HTTP response codes
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# Calculate response time statistics
awk '{sum+=$NF; count++} END {print "Avg:", sum/count, "Total:", count}' response_times.log
```

#### **sed** - Stream Editor for Logs
```bash
# Print specific lines
sed -n '10p' file.log             # Line 10
sed -n '10,20p' file.log          # Lines 10-20
sed -n '$p' file.log              # Last line

# Pattern matching
sed -n '/error/p' file.log        # Print lines with "error"
sed -n '/error/,/success/p' file.log  # Range between patterns

# Substitution
sed 's/error/ERROR/' file.log     # Replace first occurrence
sed 's/error/ERROR/g' file.log    # Replace all occurrences
sed 's/error/ERROR/gi' file.log   # Case-insensitive replace
sed '1,10s/foo/bar/g' file.log    # Replace in lines 1-10

# Delete lines
sed '/debug/d' file.log           # Delete lines with "debug"
sed '1,10d' file.log              # Delete lines 1-10
sed '/^$/d' file.log              # Delete blank lines

# In-place editing
sed -i 's/old/new/g' file.log     # Edit file in-place
sed -i.bak 's/old/new/g' file.log # Keep backup

# Multiple commands
sed -e 's/foo/bar/' -e 's/old/new/' file.log
sed 's/foo/bar/; s/old/new/' file.log

# Real-world examples
sed -n '/2025-10-17/p' /var/log/syslog  # Extract specific date
sed -n '/ERROR/,/^$/p' file.log    # Extract error blocks
sed 's/^/[PREFIX] /' file.log      # Add prefix to each line
sed '/^#/d; /^$/d' config.log      # Remove comments and blanks
```

#### **Log File Locations**
```bash
# System logs
/var/log/syslog                   # System messages (Debian/Ubuntu)
/var/log/messages                 # System messages (RHEL/CentOS)
/var/log/kern.log                 # Kernel messages
/var/log/dmesg                    # Boot messages
/var/log/boot.log                 # Boot process

# Authentication
/var/log/auth.log                 # Authentication (Debian/Ubuntu)
/var/log/secure                   # Authentication (RHEL/CentOS)
/var/log/faillog                  # Failed login attempts
/var/log/lastlog                  # Last login info

# Application logs
/var/log/apache2/                 # Apache (Debian/Ubuntu)
/var/log/httpd/                   # Apache (RHEL/CentOS)
/var/log/nginx/                   # Nginx
/var/log/mysql/                   # MySQL
/var/log/postgresql/              # PostgreSQL

# System services
/var/log/cron                     # Cron jobs
/var/log/maillog                  # Mail server
/var/log/audit/audit.log          # Audit logs (auditd)

# Package management
/var/log/dpkg.log                 # Debian package management
/var/log/apt/                     # APT logs (Debian/Ubuntu)
/var/log/yum.log                  # YUM logs (RHEL/CentOS)

# Other important logs
/var/log/wtmp                     # Login records (binary - use last)
/var/log/btmp                     # Failed logins (binary - use lastb)
/var/log/utmp                     # Current logins (binary - use who)

# Journal location (systemd)
/var/log/journal/                 # Persistent journal
/run/log/journal/                 # Volatile journal
```

#### **Log Analysis Tools**

**last/lastb** - Login History
```bash
last                              # Login history
last -n 10                        # Last 10 logins
last username                     # Specific user
last -a                           # Show hostname in last column
last -d                           # Show IP instead of hostname
last -F                           # Full dates and times
last -i                           # Show IP addresses
last -x                           # Show shutdowns and run level
last reboot                       # Reboot history
lastb                             # Failed login attempts (root only)
lastb -a                          # Failed logins with hostname
```

**w/who** - Currently Logged In Users
```bash
w                                 # Who is logged in and what they're doing
who                               # Who is logged in
who -a                            # All information
who -b                            # Last boot time
who -q                            # Count of users
whoami                            # Current username
```

**logrotate** - Log Rotation Management
```bash
# Config file: /etc/logrotate.conf
# Service configs: /etc/logrotate.d/

# Test configuration
logrotate -d /etc/logrotate.conf  # Debug mode (dry-run)
logrotate -f /etc/logrotate.conf  # Force rotation
logrotate -v /etc/logrotate.conf  # Verbose

# Example logrotate config
# /var/log/myapp/*.log {
#     daily
#     rotate 7
#     compress
#     delaycompress
#     missingok
#     notifempty
#     create 0644 user group
#     postrotate
#         systemctl reload myapp
#     endscript
# }
```

### Log Analysis
```bash
# System logs
journalctl                    # Systemd journal (all logs)
journalctl -u <service>       # Logs for specific service
journalctl -f                 # Follow logs in real-time
journalctl --since "1 hour ago"
journalctl -p err             # Only error messages

# Traditional logs
tail -f /var/log/messages     # System messages
tail -f /var/log/syslog       # System log (Debian/Ubuntu)
tail -f /var/log/secure       # Authentication log (RHEL/CentOS)
tail -f /var/log/auth.log     # Authentication log (Debian/Ubuntu)
dmesg                         # Kernel ring buffer
dmesg -T                      # With timestamps

# Log searching
grep -r "error" /var/log/     # Search all logs
zgrep "pattern" /var/log/*.gz # Search compressed logs
```

### Performance Analysis
```bash
# System performance
uptime                 # System load average
sar                    # System activity reporter
perf                   # Performance analysis tool
strace -p <PID>        # Trace system calls of running process
ltrace -p <PID>        # Trace library calls

# Disk performance
hdparm -Tt /dev/sda    # Disk speed test
smartctl -a /dev/sda   # SMART disk health
```

---

## Application Without Logs

### Troubleshooting Applications That Don't Produce Logs

#### 1. **System Call Tracing**
```bash
# Trace system calls of the application
strace -o output.txt ./application
strace -p <PID>                    # Attach to running process
strace -f -p <PID>                 # Include child processes
strace -e open,read,write -p <PID> # Trace specific syscalls

# Advanced strace usage
strace -c ./application            # Summary statistics
strace -tt -T -p <PID>             # Timestamps and time spent
```

#### 2. **Library Call Tracing**
```bash
# Trace library calls
ltrace ./application
ltrace -p <PID>                    # Attach to running process
ltrace -c ./application            # Summary statistics
```

#### 3. **Process Monitoring**
```bash
# Monitor file access
lsof -p <PID>                      # Files opened by process
ls -l /proc/<PID>/fd/              # File descriptors
cat /proc/<PID>/maps               # Memory mappings

# Monitor process behavior
watch -n 1 'ps -p <PID> -o pid,ppid,cmd,%cpu,%mem,stat,start'
```

#### 4. **Network Activity**
```bash
# Monitor network connections
lsof -i -a -p <PID>                # Network connections
ss -p | grep <PID>                 # Socket information
tcpdump -i any -n -A 'host <IP>'   # Capture traffic
```

#### 5. **Application Output Redirection**
```bash
# Redirect stderr and stdout
./application > output.log 2>&1
./application 2>&1 | tee output.log

# Run with verbose/debug options
./application --verbose
./application --debug
export DEBUG=*                     # For Node.js apps
```

#### 6. **Debugging Tools**
```bash
# GDB debugger
gdb -p <PID>                       # Attach debugger
gdb ./application                  # Start with debugger

# In GDB
(gdb) bt                           # Backtrace
(gdb) info threads                 # Thread information
(gdb) thread apply all bt          # Backtrace all threads
```

#### 7. **Kernel Tracing**
```bash
# Ftrace
echo function > /sys/kernel/debug/tracing/current_tracer
cat /sys/kernel/debug/tracing/trace

# perf tool
perf record -p <PID> -g           # Record with call graph
perf report                        # Analyze recording
```

#### 8. **Audit System**
```bash
# Use auditd to track application behavior
auditctl -w /path/to/app -p x     # Watch execution
ausearch -x /path/to/app           # Search audit logs
```

---

## System Won't Boot

### Boot Troubleshooting Process

#### 1. **BIOS/UEFI Stage**
**Symptoms:** No POST, beeping, no display

**Troubleshooting:**
- Check hardware connections
- Remove unnecessary peripherals
- Reset BIOS settings
- Check boot order in BIOS
- Verify boot device is detected

#### 2. **Bootloader Stage (GRUB)**
**Symptoms:** "GRUB>" prompt, "error: no such partition"

**Troubleshooting:**
```bash
# Boot from rescue media
# Mount root partition
mkdir /mnt/root
mount /dev/sda1 /mnt/root
mount --bind /dev /mnt/root/dev
mount --bind /proc /mnt/root/proc
mount --bind /sys /mnt/root/sys
chroot /mnt/root

# Reinstall GRUB
grub2-install /dev/sda             # RHEL/CentOS
grub-install /dev/sda              # Debian/Ubuntu
update-grub                        # Regenerate config

# Fix GRUB configuration
vim /etc/default/grub
grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL/CentOS
update-grub                             # Debian/Ubuntu
```

#### 3. **Kernel Stage**
**Symptoms:** Kernel panic, initramfs errors

**Troubleshooting:**
```bash
# Boot into rescue mode
# At GRUB menu, press 'e' and add to kernel line:
systemd.unit=rescue.target
# or
init=/bin/bash

# Rebuild initramfs
dracut --force                     # RHEL/CentOS
update-initramfs -u                # Debian/Ubuntu

# Check kernel logs
dmesg | less
journalctl -xb                     # Boot logs
```

#### 4. **Init/Systemd Stage**
**Symptoms:** Boot hangs, specific service fails

**Troubleshooting:**
```bash
# Boot with systemd debug
systemd.log_level=debug
systemd.log_target=console

# Check failed services
systemctl --failed
systemctl status <service>
journalctl -xb -u <service>

# Boot to specific target
systemd.unit=multi-user.target     # No GUI
systemd.unit=emergency.target      # Minimal system
```

#### 5. **Filesystem Issues**
**Symptoms:** "Give root password for maintenance"

**Troubleshooting:**
```bash
# Check filesystems
fsck /dev/sda1                     # File system check
xfs_repair /dev/sda1               # For XFS filesystem

# Check /etc/fstab
cat /etc/fstab
blkid                              # Verify UUIDs match

# Mount in read-write mode
mount -o remount,rw /
```

#### 6. **Emergency Boot Options**

**GRUB Kernel Parameters:**
```bash
# Add to kernel line in GRUB (press 'e' at GRUB menu)
single                             # Single user mode
init=/bin/bash                     # Bash as init
rd.break                           # Break before mounting root
emergency                          # Emergency mode
rescue                             # Rescue mode
systemd.unit=rescue.target
noresume                           # Skip resume from hibernate
nomodeset                          # Disable graphics drivers
```

**Recovery from Emergency Shell:**
```bash
# When dropped to emergency shell
mount -o remount,rw /sysroot       # Remount root as writable
chroot /sysroot                    # Change root
mount -a                           # Mount all filesystems

# Fix and reboot
touch /.autorelabel                # For SELinux relabel
exit
reboot
```

---

## System Calls

### Understanding System Calls

**System calls** are the interface between user programs and the kernel. They allow applications to request services from the operating system.

### Common System Call Categories

#### 1. **Process Control**
```bash
fork()      # Create child process
exec()      # Execute program
exit()      # Terminate process
wait()      # Wait for child process
kill()      # Send signal to process
getpid()    # Get process ID
```

#### 2. **File Operations**
```bash
open()      # Open file
read()      # Read from file
write()     # Write to file
close()     # Close file descriptor
lseek()     # Reposition file offset
stat()      # Get file status
```

#### 3. **Device Management**
```bash
ioctl()     # Device-specific operations
read()      # Read from device
write()     # Write to device
```

#### 4. **Information Maintenance**
```bash
getpid()    # Process ID
time()      # Current time
gettimeofday() # Time with microseconds
uname()     # System information
```

#### 5. **Communication**
```bash
socket()    # Create socket
connect()   # Connect to socket
send()      # Send data
recv()      # Receive data
pipe()      # Create pipe
```

### Tracing System Calls

```bash
# Basic system call tracing
strace ls                          # Trace ls command
strace -c ls                       # Summary statistics

# Advanced options
strace -tt -T ls                   # With timestamps and duration
strace -e open,read,write ls       # Specific syscalls only
strace -f -p <PID>                 # Follow forks
strace -o output.txt -p <PID>      # Save to file

# System-wide tracing
perf trace                         # System-wide syscall tracing
perf trace -p <PID>                # Specific process
```

### System Call Flow
```
User Application
    ↓
    | System Call (e.g., read())
    ↓
User Space
=====================================
Kernel Space
    ↓
    | Context Switch
    ↓
Kernel System Call Handler
    ↓
    | Execute Privileged Operation
    ↓
    | Return Result
    ↓
User Space
    ↓
Application Continues
```

---

## User Space vs Kernel Space

### Memory Architecture

```
┌─────────────────────────────────────┐
│        User Space (Ring 3)          │  ← Applications run here
│  - User applications                │  ← Limited privileges
│  - Libraries                        │  ← Cannot access hardware directly
│  - User processes                   │  ← Protected memory
├─────────────────────────────────────┤
│     System Call Interface           │  ← Bridge between spaces
├─────────────────────────────────────┤
│       Kernel Space (Ring 0)         │  ← Operating system core
│  - Device drivers                   │  ← Full hardware access
│  - Kernel code                      │  ← Privileged operations
│  - System services                  │  ← Manages resources
└─────────────────────────────────────┘
```

### User Space

**Characteristics:**
- Applications and user processes run here
- Restricted access to hardware and memory
- Cannot execute privileged instructions
- Process isolation and protection
- If crashes, doesn't affect kernel

**Components:**
```bash
- Applications (browsers, editors, etc.)
- System utilities (ls, cat, grep, etc.)
- Libraries (libc, libssl, etc.)
- Shells (bash, zsh, etc.)
- Daemons (Apache, MySQL, etc.)
```

**Debugging User Space:**
```bash
# Process information
ps aux
top
pstree

# Library dependencies
ldd /bin/ls
ldconfig -p

# Memory maps
cat /proc/<PID>/maps
pmap <PID>

# Debug tools
gdb
valgrind
strace
```

### Kernel Space

**Characteristics:**
- Operating system core runs here
- Direct hardware access
- Can execute any CPU instruction
- Manages all system resources
- If crashes, entire system crashes (kernel panic)

**Components:**
```bash
- Process management
- Memory management
- File system
- Device drivers
- Network stack
- System calls
```

**Debugging Kernel Space:**
```bash
# Kernel messages
dmesg
dmesg -T                           # With timestamps
dmesg -l err,warn                  # Errors and warnings only

# Kernel logs
journalctl -k                      # Kernel messages
cat /var/log/kern.log              # Kernel log file

# Loaded kernel modules
lsmod                              # List modules
modinfo <module>                   # Module information
modprobe -r <module>               # Remove module
modprobe <module>                  # Load module

# Kernel parameters
sysctl -a                          # All kernel parameters
sysctl kernel.hostname             # Specific parameter
sysctl -w kernel.parameter=value   # Set parameter

# Kernel tracing
cat /sys/kernel/debug/tracing/available_tracers
echo function > /sys/kernel/debug/tracing/current_tracer

# Crash dumps
cat /proc/vmcore                   # Kernel crash dump
crash /var/crash/vmcore            # Analyze crash dump
```

### Context Switching

When switching between user and kernel space:
```bash
1. User process makes system call
2. CPU switches from Ring 3 (user) to Ring 0 (kernel)
3. Save user context (registers, stack pointer)
4. Execute kernel code
5. Restore user context
6. Return to user space (Ring 3)
```

**Monitoring Context Switches:**
```bash
vmstat 1                           # Context switches per second
pidstat -w 1                       # Per-process context switches
perf stat -e context-switches ls   # Count for specific command
```

---

## Common Scenarios and Solutions

### Scenario 1: High CPU Usage
```bash
# Identify the process
top                                # Real-time monitoring
ps aux --sort=-%cpu | head         # Top CPU consumers

# Investigate the process
strace -c -p <PID>                 # System call summary
perf top -p <PID>                  # Performance profiling
pstack <PID>                       # Stack trace
```

### Scenario 2: High Memory Usage
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head         # Top memory consumers

# Detailed analysis
pmap -x <PID>                      # Memory map
cat /proc/<PID>/smaps              # Detailed memory info
valgrind --leak-check=full ./app   # Memory leak detection
```

### Scenario 3: Disk Full
```bash
# Find large files
df -h                              # Disk usage
du -sh /*                          # Directory sizes
find / -type f -size +1G           # Files > 1GB
find /var/log -type f -mtime +30   # Old log files

# Clean up
journalctl --vacuum-size=100M      # Clean journal logs
rm -rf /tmp/*                      # Clean temporary files
yum clean all                      # Clean package cache (RHEL)
apt-get clean                      # Clean package cache (Debian)
```

### Scenario 4: Network Connection Issues
```bash
# Test connectivity
ping <host>
traceroute <host>
telnet <host> <port>

# Check configuration
ip addr
ip route
cat /etc/resolv.conf

# Check firewall
iptables -L -n
firewall-cmd --list-all
ufw status

# Check services
ss -tulpn | grep <port>
systemctl status <service>
```

### Scenario 5: Service Not Starting
```bash
# Check service status
systemctl status <service>
journalctl -xeu <service>

# Check configuration
<service> -t                       # Test config (nginx, apache)
<service> --configtest

# Check dependencies
systemctl list-dependencies <service>

# Check permissions
ls -l /path/to/service/files
ps aux | grep <service>
```

### Scenario 6: Permission Issues
```bash
# Check permissions
ls -la /path/to/file
getfacl /path/to/file              # ACL permissions

# Check SELinux (if enabled)
getenforce
ls -Z /path/to/file
ausearch -m AVC -ts recent

# Check AppArmor (if enabled)
aa-status
cat /var/log/audit/audit.log | grep DENIED
```

### Scenario 7: Slow System Performance
```bash
# System overview
uptime                             # Load average
vmstat 1 5                         # System statistics
iostat -x 1 5                      # I/O statistics
sar -u 1 5                         # CPU usage

# Identify bottleneck
top                                # Overall view
iotop                              # I/O bottleneck
iftop                              # Network bottleneck
atop                               # Advanced monitoring
```

---

## Best Practices

1. **Always check logs first** - Start with `journalctl` and `/var/log`
2. **Make incremental changes** - Change one thing at a time
3. **Document everything** - Keep notes of what you tried
4. **Have a rollback plan** - Be able to undo changes
5. **Use monitoring tools** - Set up proactive monitoring
6. **Test in non-production** - When possible
7. **Check recent changes** - Often the cause of issues
8. **Know your baselines** - Understand normal behavior
9. **Use version control** - For configuration files
10. **Keep backups** - Before making changes

---

## Quick Reference Commands

```bash
# System health check one-liner
uptime && free -h && df -h && top -bn1 | head -20

# Find what's using port
lsof -i :<port>
ss -tulpn | grep :<port>

# Find what's using file/directory
lsof +D /path/to/directory
fuser -v /path/to/file

# Kill all processes by name
pkill <process_name>
killall <process_name>

# Check if service is listening
nc -zv localhost <port>
timeout 1 bash -c 'cat < /dev/null > /dev/tcp/localhost/<port>'

# Monitor file changes
watch -n 1 'ls -lh /path/to/file'
tail -f /path/to/file

# Real-time log monitoring
journalctl -f
multitail /var/log/messages /var/log/secure

# System resource summary
dstat
nmon
```

---

## Additional Resources

- `man` pages - Built-in documentation
- `/usr/share/doc` - Package documentation
- Red Hat/CentOS: Knowledge Base
- Ubuntu: Official documentation
- ArchWiki - Excellent Linux resource
- Stack Overflow/Server Fault
- Linux Performance by Brendan Gregg

---

*Last Updated: October 2025*
