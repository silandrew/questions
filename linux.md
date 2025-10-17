# Linux Troubleshooting Guide

## Table of Contents
1. [General Troubleshooting Approach](#general-troubleshooting-approach)
2. [Essential Linux Troubleshooting Tools](#essential-linux-troubleshooting-tools)
3. [Application Without Logs](#application-without-logs)
4. [System Won't Boot](#system-wont-boot)
5. [System Calls](#system-calls)
6. [User Space vs Kernel Space](#user-space-vs-kernel-space)
7. [Common Scenarios and Solutions](#common-scenarios-and-solutions)

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

## Essential Linux Troubleshooting Tools

### System Information & Monitoring

#### **top** - Real-time Process Monitoring
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

#### **htop** - Enhanced Interactive Process Viewer
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
