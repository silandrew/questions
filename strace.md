# Trace a simple command
strace ls

# Trace a command with arguments
strace ls -la /etc

# Attach to a running process by PID
strace -p 1234

# Attach to a running process by name
strace -p $(pgrep nginx)

# Follow fork/exec - trace child processes
strace -f ./my-program

# Follow forks and show PID for each line
strace -ff -o trace ./my-program
# Creates trace.PID files for each process
```

---

### **Common strace Options**

```bash
# -e trace=SYSCALL - Filter specific system calls
strace -e trace=open,openat ls          # Only show open calls
strace -e trace=read,write cat file.txt  # Only read/write calls

# -e trace=SET - Filter by system call category
strace -e trace=file ls                  # All file operations
strace -e trace=network curl google.com  # All network operations
strace -e trace=process ./script.sh      # Process management
strace -e trace=memory ./program         # Memory operations
strace -e trace=signal ./program         # Signal-related calls

# -c - Count time, calls, and errors for each syscall
strace -c ls /etc
# Shows summary statistics at the end

# -T - Show time spent in each syscall
strace -T ls
# Example: open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3 <0.000023>

# -tt - Timestamps with microseconds
strace -tt ls
# Example: 14:23:45.123456 open("/etc/passwd", O_RDONLY) = 3

# -r - Relative timestamps (time between syscalls)
strace -r ls

# -o FILE - Output to a file instead of stderr
strace -o trace.log ls /etc

# -s SIZE - String size (default is 32 characters)
strace -s 512 cat /etc/passwd  # Show up to 512 chars of strings

# -y - Print file descriptor paths
strace -y cat /etc/hosts
# Shows paths like: read(3</etc/hosts>, "127.0.0.1...", 4096)

# -k - Print stack trace for each syscall (requires debug symbols)
strace -k ls

# -v - Verbose mode (unabbreviated output)
strace -v ls
```

---

### **Practical Examples and Use Cases**

#### **1. Find Which Files a Program Opens**
```bash
# See all files accessed by a program
strace -e trace=open,openat cat /etc/passwd 2>&1 | grep -E "open|openat"

# Better filtering
strace -e trace=openat ls 2>&1 | grep -v ENOENT

# Save to file for analysis
strace -e trace=openat -o files.log nginx -t
cat files.log | grep openat

# Real example - where does Python look for modules?
strace -e trace=openat python3 -c "import requests" 2>&1 | grep requests
```

#### **2. Debug "File Not Found" Errors**
```bash
# Application says file not found - where is it looking?
strace -e trace=openat ./myapp 2>&1 | grep ENOENT

# Example output:
# openat(AT_FDCWD, "/etc/myapp/config.conf", O_RDONLY) = -1 ENOENT
# This shows the app is looking in /etc/myapp/ but file doesn't exist

# Find all failed file access attempts
strace -e trace=file ./program 2>&1 | grep -E "ENOENT|EACCES"
```

#### **3. Debug Permission Issues**
```bash
# See permission denied errors
strace -e trace=open,openat,access ./program 2>&1 | grep EACCES

# Example - why can't the app write?
strace ./myapp 2>&1 | grep -E "EACCES|Permission denied"

# Output might show:
# open("/var/log/myapp.log", O_WRONLY|O_CREAT, 0666) = -1 EACCES
```

#### **4. Attach to a Running Process**
```bash
# Find the process ID
ps aux | grep nginx

# Attach strace to see what it's doing
sudo strace -p 12345

# Attach and filter for specific calls
sudo strace -p 12345 -e trace=network

# Attach to all threads of a process
sudo strace -f -p 12345

# Example: Debug a hanging web server
sudo strace -p $(pgrep -f "gunicorn") -e trace=network,poll,select

# You might see it stuck on:
# poll([{fd=5, events=POLLIN}], 1, -1)  = ... (waiting forever)
```

#### **5. Trace Network Connections**
```bash
# See all network system calls
strace -e trace=network curl https://google.com 2>&1

# Focus on connection attempts
strace -e trace=connect,socket curl https://example.com 2>&1

# Example output:
# socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) = 3
# connect(3, {sa_family=AF_INET, sin_port=htons(443), 
#         sin_addr=inet_addr("93.184.216.34")}, 16) = 0

# Debug DNS resolution
strace -e trace=network host google.com 2>&1 | grep connect

# See what a service is listening on
sudo strace -e trace=network -p $(pgrep sshd | head -1) 2>&1
```

#### **6. Performance Analysis**
```bash
# Summary of syscall counts and time
strace -c ls /usr/bin

# Example output:
# % time     seconds  usecs/call     calls    errors syscall
# ------ ----------- ----------- --------- --------- ----------------
#  45.23    0.000123          12        10           read
#  32.15    0.000087           8        11           open
#  12.45    0.000034           3        11           close
# ...

# Time spent in each call
strace -T ls /etc 2>&1 | grep "<"

# Find the slowest syscalls
strace -T ./myprogram 2>&1 | sort -k2 -rn | head -20

# Analyze a specific slow operation
strace -T -e trace=read,write dd if=/dev/zero of=/tmp/test bs=1M count=100
```

#### **7. Debug Configuration File Loading**
```bash
# Where does nginx look for config?
strace -e trace=openat nginx -t 2>&1 | grep "\.conf"

# Output shows:
# openat(AT_FDCWD, "/etc/nginx/nginx.conf", O_RDONLY) = 3
# openat(AT_FDCWD, "/etc/nginx/mime.types", O_RDONLY) = 4

# What environment variables does a program read?
strace -e trace=access,open bash -c "echo \$PATH" 2>&1 | grep bashrc

# Find which Python config files are used
strace -e trace=openat python3 2>&1 | grep -E "\.py|pth|site-packages"
```

#### **8. Debug Library Loading Issues**
```bash
# See which shared libraries are loaded
strace -e trace=openat ./myapp 2>&1 | grep "\.so"

# Example output:
# openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY) = 3
# openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY) = 3

# Debug missing library
strace ./program 2>&1 | grep -E "\.so.*ENOENT"

# Compare with ldd output
ldd ./program
strace -e trace=openat ./program 2>&1 | grep "\.so"
```

#### **9. Monitor File Writes**
```bash
# See all files written by a program
strace -e trace=write,writev,pwrite ./program 2>&1

# Monitor log files being written
sudo strace -p $(pgrep rsyslogd) -e trace=write

# See what gets written to specific file descriptor
strace -e write=1,2 ./program  # stdout and stderr

# Example: where does app write its data?
strace -e trace=openat,write ./dataprocessor 2>&1 | grep -A2 "O_WRONLY\|O_RDWR"
```

#### **10. Debug Database Connection Issues**
```bash
# Trace PostgreSQL client connection
strace -e trace=network psql -h localhost -U postgres 2>&1

# Example shows:
# socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) = 3
# connect(3, {sa_family=AF_INET, sin_port=htons(5432), 
#         sin_addr=inet_addr("127.0.0.1")}, 16) = 0

# Debug MySQL connection
strace -e trace=network,file mysql -h localhost -u root 2>&1 | grep -E "connect|socket|/var/lib/mysql"

# See if app connects to Redis
strace -e trace=network ./myapp 2>&1 | grep 6379
```

#### **11. Analyze Child Processes**
```bash
# Follow all child processes created by a shell script
strace -f -e trace=process ./deploy.sh

# Track what each child process does
strace -ff -o trace_output ./parent_program
# Creates: trace_output.12345, trace_output.12346, etc.

# See all exec calls
strace -f -e trace=execve ./script.sh 2>&1

# Example output:
# execve("/bin/bash", ["bash", "script.sh"], ...) = 0
# execve("/usr/bin/ls", ["ls", "-la"], ...) = 0
```

#### **12. Debug System Call Errors**
```bash
# See all errors with details
strace ./program 2>&1 | grep -E "= -1"

# Common errors:
# ENOENT  - No such file or directory
# EACCES  - Permission denied
# EAGAIN  - Resource temporarily unavailable
# ECONNREFUSED - Connection refused
# ETIMEDOUT - Connection timed out

# Find specific error type
strace -e trace=all ./program 2>&1 | grep ECONNREFUSED

# Count errors by type
strace -c ./program 2>&1
```

#### **13. Monitor Process Waiting/Blocking**
```bash
# See what process is waiting on
sudo strace -p 12345 -e trace=poll,select,epoll_wait

# Example - stuck process might show:
# poll([{fd=3, events=POLLIN}], 1, -1) = ... (blocked here)

# See all blocking calls
sudo strace -p 12345 -e trace=select,poll,epoll_wait,futex,nanosleep

# Find why process is slow
sudo strace -T -p 12345 2>&1 | grep -E "<[0-9]\.[0-9]{3,}"
```

#### **14. Trace Environment Variables**
```bash
# See environment variable access
strace -e trace=access,getenv env 2>&1

# See what env vars a program reads
strace -v -e trace=execve ./program 2>&1 | grep -A100 execve

# Monitor environment in shell scripts
strace -e trace=execve -s 1000 bash -c 'echo $HOME'
```

#### **15. Advanced Filtering and Analysis**
```bash
# Exclude specific syscalls
strace -e trace=all -e \!read,write ./program

# Combine multiple filters
strace -e trace=file,network,process ./program 2>&1

# Filter by error code
strace ./program 2>&1 | grep "= -1"

# Filter by return value
strace ./program 2>&1 | grep "= 0"  # Successful calls

# Time-based filtering
strace -T ./program 2>&1 | awk '$NF ~ />0\.1/ {print}'  # Calls taking >0.1s

# Save and analyze later
strace -o trace.log -s 1000 -tt -T ./program
grep -E "open|connect" trace.log
```

---

### **Understanding strace Output**

```bash
# Basic format:
# syscall(arguments) = return_value [optional_error]

# Examples:
open("/etc/passwd", O_RDONLY) = 3
# - syscall: open
# - arguments: file path, flags
# - return: file descriptor 3 (success)

open("/nofile", O_RDONLY) = -1 ENOENT (No such file or directory)
# - syscall: open
# - return: -1 (error)
# - error: ENOENT with description

read(3, "root:x:0:0:root:/root:/bin/bash\n", 4096) = 32
# - syscall: read
# - arguments: fd 3, buffer showing data read, buffer size 4096
# - return: 32 bytes actually read

connect(3, {sa_family=AF_INET, sin_port=htons(80), sin_addr=inet_addr("1.2.3.4")}, 16) = 0
# - syscall: connect
# - arguments: socket fd, address structure
# - return: 0 (success)

# With -T option:
open("/etc/hosts", O_RDONLY) = 3 <0.000015>
#                                  ^^^^^^^^ time in seconds

# With -tt option:
14:23:45.123456 open("/etc/passwd", O_RDONLY) = 3
# Absolute timestamp

# With -r option:
     0.000000 execve("./program", ...)
     0.000123 open("/etc/passwd", ...)
     0.000045 read(3, ...)
# Relative time since previous call
```

---

### **Common System Call Categories**

```bash
# File operations
-e trace=file
# Includes: open, openat, stat, fstat, lstat, access, chmod, chown, 
#           unlink, rename, mkdir, rmdir, readlink, truncate

# Process management  
-e trace=process
# Includes: fork, vfork, clone, execve, exit, wait, waitpid, kill

# Network operations
-e trace=network
# Includes: socket, connect, bind, listen, accept, send, recv, 
#           sendto, recvfrom, shutdown, getsockopt, setsockopt

# IPC (Inter-Process Communication)
-e trace=ipc
# Includes: shmget, shmat, shmdt, semget, semop, msgget, msgsnd, msgrcv

# Signals
-e trace=signal
# Includes: kill, sigaction, sigprocmask, sigreturn, rt_sigaction

# Descriptor operations
-e trace=desc
# Includes: read, write, close, dup, dup2, fcntl, ioctl

# Memory operations
-e trace=memory
# Includes: mmap, munmap, mprotect, brk, sbrk
```

---

### **Real-World Troubleshooting Scenarios**

#### **Scenario 1: Application Won't Start**
```bash
# Problem: App fails to start with no clear error message
strace ./myapp 2>&1 | tail -20

# Look for the last syscalls before exit
# Common issues revealed:
# - Missing configuration file
# - Library not found
# - Permission denied on socket/port
# - Missing directory for PID file
```

#### **Scenario 2: Slow Application Startup**
```bash
# Find what's taking time
strace -T -c ./myapp

# Look for high time percentages
# Common culprits:
# - DNS lookups (connect to DNS server)
# - Slow disk reads
# - Network timeouts
# - Database connection delays
```

#### **Scenario 3: Application Hangs**
```bash
# Attach to hanging process
sudo strace -p $(pgrep myapp)

# Common hang causes:
# - Waiting on network: connect(), recv()
# - Waiting on file lock: flock(), fcntl()
# - Waiting on semaphore: sem_wait()
# - Blocking on read: read(), select(), poll()
```

#### **Scenario 4: Configuration Not Loading**
```bash
# Find where app looks for config
strace -e trace=openat ./myapp 2>&1 | grep config

# Common findings:
# - App looks in wrong directory
# - File exists but has wrong permissions
# - App looks for file with different name/extension
```

---

### **Performance Tips**

```bash
# 1. Use specific filters to reduce noise
strace -e trace=network curl google.com  # Not -e trace=all

# 2. Output to file for large traces
strace -o output.log -e trace=file find /

# 3. Use -c for quick overview
strace -c ./program  # Summary statistics only

# 4. Attach to running process carefully (can slow it down)
sudo strace -p 1234  # Use specific filters when possible

# 5. For multi-threaded apps, use -f carefully
strace -f ./multithreaded  # Can generate massive output
```

---

### **Alternatives and Related Tools**

```bash
# ltrace - Trace library calls instead of system calls
ltrace ./program

# perf - More advanced performance analysis
perf trace ./program

# ftrace - Kernel-level tracing
# bpftrace - Modern eBPF-based tracing
# SystemTap - Powerful but complex tracing framework
```

---

### **Common Use Cases Summary**

| **Problem** | **strace Command** |
|-------------|-------------------|
| Find config files | `strace -e trace=openat ./app 2>&1 \| grep conf` |
| Debug permissions | `strace ./app 2>&1 \| grep EACCES` |
| Find missing files | `strace -e trace=openat ./app 2>&1 \| grep ENOENT` |
| Network debugging | `strace -e trace=network ./app` |
| Performance analysis | `strace -c ./app` |
| Attach to running | `sudo strace -p PID` |
| Follow child processes | `strace -f ./app` |
| Save to file | `strace -o trace.log ./app` |
| Time per syscall | `strace -T ./app` |
| Library loading | `strace -e trace=openat ./app 2>&1 \| grep "\.so"` |