# Bash Scripting Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Syntax](#basic-syntax)
3. [Variables](#variables)
4. [Input/Output](#inputoutput)
5. [Conditional Statements](#conditional-statements)
6. [Loops](#loops)
7. [Functions](#functions)
8. [Arrays](#arrays)
9. [String Manipulation](#string-manipulation)
10. [File Operations](#file-operations)
11. [Command-Line Arguments](#command-line-arguments)
12. [Exit Status and Error Handling](#exit-status-and-error-handling)
13. [Regular Expressions](#regular-expressions)
14. [Advanced Topics](#advanced-topics)

---

## Introduction

Bash (Bourne Again Shell) is a command-line interpreter and scripting language widely used in Linux/Unix systems for automation, system administration, and task execution.

### Creating a Bash Script

```bash
#!/bin/bash
# This is a comment
echo "Hello, World!"
```

**Key Points:**
- `#!/bin/bash` - Shebang line, specifies the interpreter
- Make script executable: `chmod +x script.sh`
- Run script: `./script.sh` or `bash script.sh`

---

## Basic Syntax

### Comments

```bash
# Single-line comment

: '
Multi-line comment
This is a multi-line comment
using the : command
'
```

### Echo Command

```bash
#!/bin/bash

# Simple echo
echo "Hello, World!"

# Echo without newline
echo -n "No newline"

# Echo with escape sequences
echo -e "Line 1\nLine 2\tTabbed"

# Echo variable
NAME="John"
echo "Hello, $NAME"
```

---

## Variables

### Variable Declaration and Usage

```bash
#!/bin/bash

# Variable assignment (no spaces around =)
NAME="Alice"
AGE=25
PI=3.14159

# Using variables
echo "Name: $NAME"
echo "Age: $AGE"
echo "Name: ${NAME}"  # Explicit syntax

# Read-only variables
readonly DATABASE="production_db"
# DATABASE="test_db"  # This would cause an error

# Unsetting variables
unset AGE
```

### Special Variables

```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
echo "Exit status of last command: $?"
echo "Process ID: $$"
echo "Last background process ID: $!"
```

### Environment Variables

```bash
#!/bin/bash

# Display environment variables
echo "Home directory: $HOME"
echo "Current user: $USER"
echo "Current path: $PATH"

# Setting environment variables
export MY_VAR="some value"

# Making variable available to child processes
export DATABASE_URL="postgresql://localhost/mydb"
```

### Command Substitution

```bash
#!/bin/bash

# Using backticks (old style)
CURRENT_DATE=`date`
echo "Date: $CURRENT_DATE"

# Using $() (preferred)
CURRENT_DATE=$(date +%Y-%m-%d)
echo "Date: $CURRENT_DATE"

# Nested command substitution
FILES_COUNT=$(ls -l $(pwd) | wc -l)
echo "Files count: $FILES_COUNT"
```

---

## Input/Output

### Reading User Input

```bash
#!/bin/bash

# Simple read
echo "Enter your name:"
read NAME
echo "Hello, $NAME!"

# Read with prompt
read -p "Enter your age: " AGE
echo "You are $AGE years old"

# Read password (silent input)
read -sp "Enter password: " PASSWORD
echo
echo "Password received"

# Read multiple values
read -p "Enter first and last name: " FIRST LAST
echo "First: $FIRST, Last: $LAST"

# Read with timeout
if read -t 5 -p "Enter something (5 sec): " INPUT; then
    echo "You entered: $INPUT"
else
    echo "Timeout!"
fi

# Read from file
while read line; do
    echo "Line: $line"
done < input.txt
```

### Redirections

```bash
#!/bin/bash

# Output redirection
echo "Hello" > output.txt          # Overwrite
echo "World" >> output.txt         # Append

# Input redirection
while read line; do
    echo $line
done < input.txt

# Error redirection
command 2> error.log               # Redirect stderr
command > output.log 2>&1          # Redirect stdout and stderr
command &> all_output.log          # Redirect all output (bash 4+)

# Here document
cat << EOF > file.txt
Line 1
Line 2
Variable: $VAR
EOF

# Here string
grep "pattern" <<< "string to search"
```

---

## Conditional Statements

### If-Else Statements

```bash
#!/bin/bash

# Simple if
if [ "$1" == "hello" ]; then
    echo "Hello to you too!"
fi

# If-else
if [ $# -eq 0 ]; then
    echo "No arguments provided"
else
    echo "Arguments provided: $@"
fi

# If-elif-else
read -p "Enter a number: " NUM
if [ $NUM -lt 0 ]; then
    echo "Negative number"
elif [ $NUM -eq 0 ]; then
    echo "Zero"
else
    echo "Positive number"
fi

# Using [[ ]] (more advanced)
if [[ $NUM -gt 0 && $NUM -lt 100 ]]; then
    echo "Number between 0 and 100"
fi
```

### Comparison Operators

```bash
#!/bin/bash

# Numeric comparisons
# -eq  equal to
# -ne  not equal to
# -lt  less than
# -le  less than or equal to
# -gt  greater than
# -ge  greater than or equal to

if [ $AGE -ge 18 ]; then
    echo "Adult"
fi

# String comparisons
# =    equal to
# !=   not equal to
# -z   string is empty
# -n   string is not empty
# <    less than (alphabetically)
# >    greater than (alphabetically)

if [ "$NAME" = "admin" ]; then
    echo "Welcome, admin!"
fi

if [ -z "$VAR" ]; then
    echo "Variable is empty"
fi

# File test operators
# -e   file exists
# -f   file exists and is regular file
# -d   directory exists
# -r   file is readable
# -w   file is writable
# -x   file is executable
# -s   file exists and not empty

if [ -f "config.txt" ]; then
    echo "Config file exists"
fi

if [ -d "/var/log" ]; then
    echo "Log directory exists"
fi
```

### Case Statements

```bash
#!/bin/bash

read -p "Enter a command (start/stop/restart): " CMD

case $CMD in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    *)
        echo "Unknown command: $CMD"
        ;;
esac

# Pattern matching in case
case $FILENAME in
    *.txt)
        echo "Text file"
        ;;
    *.jpg|*.png)
        echo "Image file"
        ;;
    *)
        echo "Unknown file type"
        ;;
esac
```

---

## Loops

### For Loop

```bash
#!/bin/bash

# Iterate over list
for item in apple banana cherry; do
    echo "Fruit: $item"
done

# Iterate over numbers
for i in {1..5}; do
    echo "Number: $i"
done

# C-style for loop
for ((i=0; i<5; i++)); do
    echo "Counter: $i"
done

# Iterate over files
for file in *.txt; do
    echo "Processing: $file"
done

# Iterate over command output
for user in $(cat /etc/passwd | cut -d: -f1); do
    echo "User: $user"
done

# Iterate with step
for i in {0..10..2}; do
    echo "Even: $i"
done
```

### While Loop

```bash
#!/bin/bash

# Simple while loop
counter=1
while [ $counter -le 5 ]; do
    echo "Count: $counter"
    ((counter++))
done

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# Infinite loop
while true; do
    echo "Running..."
    sleep 1
done

# While with condition
while [ ! -f "ready.txt" ]; do
    echo "Waiting for ready.txt..."
    sleep 2
done
```

### Until Loop

```bash
#!/bin/bash

# Until loop (opposite of while)
counter=1
until [ $counter -gt 5 ]; do
    echo "Count: $counter"
    ((counter++))
done

# Practical example
until ping -c 1 google.com &> /dev/null; do
    echo "Waiting for network..."
    sleep 5
done
echo "Network is up!"
```

### Loop Control

```bash
#!/bin/bash

# Break - exit loop
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break
    fi
    echo $i
done

# Continue - skip iteration
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        continue
    fi
    echo $i
done

# Nested loops with break
for i in {1..3}; do
    for j in {1..3}; do
        if [ $j -eq 2 ]; then
            break
        fi
        echo "i=$i, j=$j"
    done
done
```

---

## Functions

### Function Declaration and Usage

```bash
#!/bin/bash

# Simple function
greet() {
    echo "Hello, World!"
}

# Call function
greet

# Function with parameters
greet_person() {
    echo "Hello, $1!"
}

greet_person "Alice"
greet_person "Bob"

# Function with return value
add_numbers() {
    local result=$(($1 + $2))
    echo $result
}

sum=$(add_numbers 5 3)
echo "Sum: $sum"

# Function with return status
check_file() {
    if [ -f "$1" ]; then
        return 0  # Success
    else
        return 1  # Failure
    fi
}

if check_file "config.txt"; then
    echo "File exists"
else
    echo "File not found"
fi
```

### Local Variables in Functions

```bash
#!/bin/bash

GLOBAL_VAR="I am global"

my_function() {
    local LOCAL_VAR="I am local"
    GLOBAL_VAR="Modified global"
    echo "Inside function: $LOCAL_VAR"
}

my_function
echo "Outside function: $GLOBAL_VAR"
# echo "Outside function: $LOCAL_VAR"  # This would be empty
```

### Function Examples

```bash
#!/bin/bash

# Validate IP address
validate_ip() {
    local ip=$1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo "Valid IP"
        return 0
    else
        echo "Invalid IP"
        return 1
    fi
}

# Backup function
backup_file() {
    local file=$1
    local backup_dir="./backups"
    
    if [ ! -d "$backup_dir" ]; then
        mkdir -p "$backup_dir"
    fi
    
    cp "$file" "$backup_dir/${file}.$(date +%Y%m%d_%H%M%S).bak"
    echo "Backup created"
}

# Usage
validate_ip "192.168.1.1"
backup_file "important.txt"
```

---

## Arrays

### Indexed Arrays

```bash
#!/bin/bash

# Array declaration
fruits=("apple" "banana" "cherry")

# Another way to declare
declare -a numbers
numbers=(1 2 3 4 5)

# Access elements
echo "First fruit: ${fruits[0]}"
echo "Second fruit: ${fruits[1]}"

# All elements
echo "All fruits: ${fruits[@]}"
echo "All fruits: ${fruits[*]}"

# Array length
echo "Number of fruits: ${#fruits[@]}"

# Add element
fruits+=("date")
fruits[4]="elderberry"

# Iterate over array
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# Iterate with index
for i in "${!fruits[@]}"; do
    echo "Index $i: ${fruits[$i]}"
done

# Slice array
echo "Slice: ${fruits[@]:1:2}"  # Elements from index 1, length 2

# Remove element
unset fruits[1]
```

### Associative Arrays (Bash 4+)

```bash
#!/bin/bash

# Declare associative array
declare -A user_ages

# Assign values
user_ages[Alice]=25
user_ages[Bob]=30
user_ages[Charlie]=35

# Access values
echo "Alice's age: ${user_ages[Alice]}"

# All keys
echo "Users: ${!user_ages[@]}"

# All values
echo "Ages: ${user_ages[@]}"

# Iterate over associative array
for user in "${!user_ages[@]}"; do
    echo "$user is ${user_ages[$user]} years old"
done

# Check if key exists
if [ -v user_ages[Alice] ]; then
    echo "Alice exists in array"
fi
```

### Array Operations

```bash
#!/bin/bash

# Array from string
IFS=',' read -ra items <<< "item1,item2,item3"
echo "Items: ${items[@]}"

# Array from command output
files=($(ls *.txt))

# Merge arrays
array1=(1 2 3)
array2=(4 5 6)
merged=("${array1[@]}" "${array2[@]}")
echo "Merged: ${merged[@]}"

# Sort array
sorted=($(printf '%s\n' "${fruits[@]}" | sort))
echo "Sorted: ${sorted[@]}"
```

---

## String Manipulation

### String Operations

```bash
#!/bin/bash

text="Hello World"

# String length
echo "Length: ${#text}"

# Substring extraction
echo "Substring: ${text:0:5}"     # "Hello"
echo "Substring: ${text:6}"       # "World"
echo "Substring: ${text: -5}"     # "World" (space before -)

# String replacement
echo "${text/World/Universe}"     # Replace first occurrence
echo "${text//o/0}"               # Replace all occurrences

# Substring removal
filename="document.txt"
echo "${filename%.txt}"           # Remove .txt from end
echo "${filename#*.}"             # Remove up to first dot

path="/home/user/documents/file.txt"
echo "${path##*/}"                # Get filename
echo "${path%/*}"                 # Get directory

# Case conversion (Bash 4+)
echo "${text^^}"                  # HELLO WORLD (uppercase)
echo "${text,,}"                  # hello world (lowercase)
echo "${text^}"                   # Hello World (capitalize first)
```

### String Comparison

```bash
#!/bin/bash

str1="hello"
str2="world"

# Equality
if [ "$str1" = "$str2" ]; then
    echo "Strings are equal"
else
    echo "Strings are different"
fi

# Check if string contains substring
if [[ "$str1" == *"ell"* ]]; then
    echo "String contains 'ell'"
fi

# String starts with
if [[ "$str1" == "hel"* ]]; then
    echo "String starts with 'hel'"
fi

# String ends with
if [[ "$str1" == *"lo" ]]; then
    echo "String ends with 'lo'"
fi

# Empty string check
if [ -z "$empty_var" ]; then
    echo "String is empty"
fi

# Non-empty string check
if [ -n "$str1" ]; then
    echo "String is not empty"
fi
```

### String Concatenation

```bash
#!/bin/bash

# Simple concatenation
first="Hello"
second="World"
greeting="$first $second"
echo "$greeting"

# Concatenation with +=
message="Hello"
message+=" "
message+="World"
echo "$message"

# Concatenation in loop
result=""
for i in {1..5}; do
    result+="$i "
done
echo "Result: $result"
```

---

## File Operations

### Reading Files

```bash
#!/bin/bash

# Read entire file
file_content=$(cat file.txt)
echo "$file_content"

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# Read with line numbers
line_num=1
while IFS= read -r line; do
    echo "$line_num: $line"
    ((line_num++))
done < file.txt

# Read specific lines
sed -n '5,10p' file.txt           # Lines 5 to 10
head -n 20 file.txt               # First 20 lines
tail -n 10 file.txt               # Last 10 lines
```

### Writing Files

```bash
#!/bin/bash

# Overwrite file
echo "New content" > file.txt

# Append to file
echo "Additional line" >> file.txt

# Write multiple lines
cat > file.txt << EOF
Line 1
Line 2
Line 3
EOF

# Write array to file
array=("line1" "line2" "line3")
printf "%s\n" "${array[@]}" > file.txt
```

### File Tests

```bash
#!/bin/bash

file="test.txt"
dir="test_dir"

# File existence
if [ -e "$file" ]; then
    echo "File exists"
fi

# Regular file
if [ -f "$file" ]; then
    echo "Regular file"
fi

# Directory
if [ -d "$dir" ]; then
    echo "Directory exists"
fi

# Readable
if [ -r "$file" ]; then
    echo "File is readable"
fi

# Writable
if [ -w "$file" ]; then
    echo "File is writable"
fi

# Executable
if [ -x "$file" ]; then
    echo "File is executable"
fi

# Empty file
if [ -s "$file" ]; then
    echo "File is not empty"
else
    echo "File is empty"
fi

# Symbolic link
if [ -L "$file" ]; then
    echo "File is a symbolic link"
fi

# Compare file modification times
if [ "$file1" -nt "$file2" ]; then
    echo "file1 is newer than file2"
fi

if [ "$file1" -ot "$file2" ]; then
    echo "file1 is older than file2"
fi
```

### File Manipulation

```bash
#!/bin/bash

# Create file
touch newfile.txt

# Create directory
mkdir new_directory
mkdir -p path/to/nested/directory

# Copy files
cp source.txt destination.txt
cp -r source_dir/ destination_dir/

# Move/Rename files
mv oldname.txt newname.txt
mv file.txt /new/location/

# Delete files
rm file.txt
rm -f file.txt              # Force delete
rm -r directory/            # Delete directory recursively
rm -rf directory/           # Force delete directory

# Find files
find . -name "*.txt"
find . -type f -mtime -7    # Files modified in last 7 days
find . -type f -size +1M    # Files larger than 1MB
```

---

## Command-Line Arguments

### Argument Processing

```bash
#!/bin/bash

# Basic arguments
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"

# Check if arguments provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <arg1> <arg2>"
    exit 1
fi

# Shift arguments
echo "First arg: $1"
shift
echo "After shift, first arg: $1"
```

### Argument Parsing with getopts

```bash
#!/bin/bash

# Parse options
while getopts "u:p:h" opt; do
    case $opt in
        u)
            username="$OPTARG"
            ;;
        p)
            password="$OPTARG"
            ;;
        h)
            echo "Usage: $0 -u username -p password"
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument"
            exit 1
            ;;
    esac
done

echo "Username: $username"
echo "Password: $password"
```

### Advanced Argument Processing

```bash
#!/bin/bash

# Process long and short options
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--username)
            USERNAME="$2"
            shift 2
            ;;
        -p|--password)
            PASSWORD="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "  -u, --username    Username"
            echo "  -p, --password    Password"
            echo "  -v, --verbose     Verbose mode"
            echo "  -h, --help        Show help"
            exit 0
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

# Restore positional parameters
set -- "${POSITIONAL[@]}"

echo "Username: $USERNAME"
echo "Password: $PASSWORD"
echo "Verbose: $VERBOSE"
echo "Remaining args: $@"
```

---

## Exit Status and Error Handling

### Exit Codes

```bash
#!/bin/bash

# Exit with status code
exit 0    # Success
exit 1    # General error

# Check exit status
command
if [ $? -eq 0 ]; then
    echo "Command succeeded"
else
    echo "Command failed"
fi

# Short-circuit evaluation
command1 && command2    # Run command2 only if command1 succeeds
command1 || command2    # Run command2 only if command1 fails

# Practical example
mkdir /tmp/test && cd /tmp/test && touch file.txt
```

### Error Handling

```bash
#!/bin/bash

# Exit on error
set -e

# Exit on undefined variable
set -u

# Pipeline error handling
set -o pipefail

# Combination
set -euo pipefail

# Error handling function
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Usage
[ -f "config.txt" ] || error_exit "Config file not found"

# Trap errors
trap 'echo "Error on line $LINENO"' ERR

# Cleanup on exit
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}
trap cleanup EXIT
```

### Try-Catch Style Error Handling

```bash
#!/bin/bash

# Define error handler
handle_error() {
    echo "Error occurred in function: ${FUNCNAME[1]}"
    echo "Line: ${BASH_LINENO[0]}"
    exit 1
}

# Set error trap
trap handle_error ERR

# Function that might fail
risky_operation() {
    # Some operation
    false  # This will trigger error
}

# Main execution
set -e
risky_operation
echo "This won't execute if error occurs"
```

---

## Regular Expressions

### Pattern Matching

```bash
#!/bin/bash

# Using =~ operator (regex match)
email="user@example.com"

if [[ $email =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "Valid email"
else
    echo "Invalid email"
fi

# Extract matched groups
if [[ $email =~ ^(.+)@(.+)$ ]]; then
    username="${BASH_REMATCH[1]}"
    domain="${BASH_REMATCH[2]}"
    echo "Username: $username"
    echo "Domain: $domain"
fi

# IP address validation
ip="192.168.1.1"
if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    echo "Valid IP format"
fi

# Phone number matching
phone="123-456-7890"
if [[ $phone =~ ^[0-9]{3}-[0-9]{3}-[0-9]{4}$ ]]; then
    echo "Valid phone format"
fi
```

### Using grep with Regex

```bash
#!/bin/bash

# Basic grep
grep "pattern" file.txt

# Case-insensitive search
grep -i "pattern" file.txt

# Show line numbers
grep -n "pattern" file.txt

# Invert match (lines that don't match)
grep -v "pattern" file.txt

# Extended regex
grep -E "pattern1|pattern2" file.txt

# Recursive search
grep -r "pattern" /path/to/directory/

# Count matches
grep -c "pattern" file.txt

# Show only matched part
grep -o "pattern" file.txt

# Multiple patterns
grep -e "pattern1" -e "pattern2" file.txt
```

### Using sed for Pattern Replacement

```bash
#!/bin/bash

# Basic replacement
sed 's/old/new/' file.txt

# Replace all occurrences (global)
sed 's/old/new/g' file.txt

# In-place editing
sed -i 's/old/new/g' file.txt

# Delete lines matching pattern
sed '/pattern/d' file.txt

# Print only matching lines
sed -n '/pattern/p' file.txt

# Replace on specific lines
sed '5s/old/new/' file.txt       # Line 5
sed '5,10s/old/new/' file.txt    # Lines 5-10

# Multiple commands
sed -e 's/old1/new1/g' -e 's/old2/new2/g' file.txt

# Use different delimiter
sed 's|/old/path|/new/path|g' file.txt
```

---

## Advanced Topics

### Process Management

```bash
#!/bin/bash

# Run in background
command &

# Get process ID of last background job
echo "PID: $!"

# Wait for background jobs
wait

# Parallel execution
for i in {1..5}; do
    (sleep $i; echo "Job $i done") &
done
wait
echo "All jobs completed"

# Process substitution
diff <(ls dir1) <(ls dir2)

# Command grouping
{ command1; command2; } > output.txt
```

### Signal Handling

```bash
#!/bin/bash

# Trap signals
cleanup() {
    echo "Cleaning up..."
    # Cleanup code here
    exit 0
}

trap cleanup SIGINT SIGTERM

# Ignore signal
trap '' SIGINT

# Reset trap
trap - SIGINT

# Example: Handle Ctrl+C gracefully
while true; do
    echo "Running... (Press Ctrl+C to stop)"
    sleep 1
done
```

### Debugging

```bash
#!/bin/bash

# Enable debug mode
set -x    # Print commands and arguments
set -v    # Print shell input lines

# Disable debug mode
set +x
set +v

# Debug specific section
set -x
# Commands to debug
set +x

# Conditional debugging
DEBUG=1
debug_echo() {
    if [ "$DEBUG" = "1" ]; then
        echo "[DEBUG] $@"
    fi
}

debug_echo "This is a debug message"
```

### Performance and Optimization

```bash
#!/bin/bash

# Measure execution time
start_time=$(date +%s)
# Your commands here
end_time=$(date +%s)
echo "Execution time: $((end_time - start_time)) seconds"

# Using time command
time {
    # Commands to measure
    for i in {1..1000}; do
        echo $i > /dev/null
    done
}

# Efficient file processing
# Bad: spawning subprocess for each line
while read line; do
    echo $line | grep pattern
done < file.txt

# Good: using built-in features
while read line; do
    [[ $line =~ pattern ]] && echo $line
done < file.txt
```

### Here Documents and Here Strings

```bash
#!/bin/bash

# Here document
cat << EOF
This is a multi-line
text block with
variable expansion: $USER
EOF

# Here document without expansion
cat << 'EOF'
This $USER won't be expanded
EOF

# Here document to file
cat << EOF > output.txt
Line 1
Line 2
EOF

# Here string
grep "pattern" <<< "search this string"

# Variable from here document
read -r -d '' VAR << EOF
Multi-line
variable
content
EOF
```

### Subshells and Command Groups

```bash
#!/bin/bash

# Subshell - runs in separate process
(cd /tmp; ls; pwd)
echo "Current dir: $(pwd)"    # Original directory

# Command group - runs in current shell
{ cd /tmp; ls; pwd; }
echo "Current dir: $(pwd)"    # Changed directory

# Export variables from subshell (doesn't work)
(export VAR="value")
echo "$VAR"    # Empty

# Export in command group (works)
{ export VAR="value"; }
echo "$VAR"    # "value"
```

### One-Liners and Practical Examples

```bash
# Find and delete old files
find /path -type f -mtime +30 -delete

# Find largest files
find /path -type f -exec du -h {} + | sort -rh | head -10

# Count lines in all files
find . -name "*.txt" -exec wc -l {} + | awk '{sum+=$1} END {print sum}'

# Replace string in multiple files
find . -name "*.txt" -exec sed -i 's/old/new/g' {} +

# Monitor log file in real-time
tail -f /var/log/syslog | grep --line-buffered "ERROR"

# Check if port is open
timeout 1 bash -c "</dev/tcp/localhost/8080" && echo "Port open" || echo "Port closed"

# Generate random password
openssl rand -base64 12

# Bulk rename files
for file in *.txt; do mv "$file" "${file%.txt}.backup"; done

# Create directory structure
mkdir -p project/{src,bin,lib,docs}

# Archive and compress
tar -czf archive.tar.gz /path/to/directory/

# Network operations
curl -o output.html https://example.com
wget https://example.com/file.zip

# System information
echo "Disk usage:"; df -h
echo "Memory usage:"; free -h
echo "CPU info:"; lscpu

# Process monitoring
ps aux | grep process_name
top -b -n 1 | head -20
```

### Best Practices

```bash
#!/bin/bash

# 1. Always use shebang
#!/bin/bash

# 2. Use strict mode
set -euo pipefail

# 3. Quote variables
echo "$variable"
echo "${array[@]}"

# 4. Use meaningful variable names
user_name="John"    # Good
un="John"           # Bad

# 5. Use functions for reusable code
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# 6. Check command existence
if ! command -v python3 &> /dev/null; then
    echo "python3 is not installed"
    exit 1
fi

# 7. Use local variables in functions
my_function() {
    local temp_var="value"
    # ...
}

# 8. Validate input
if [ $# -ne 2 ]; then
    echo "Usage: $0 <arg1> <arg2>"
    exit 1
fi

# 9. Use arrays for lists
files=("file1.txt" "file2.txt" "file3.txt")
for file in "${files[@]}"; do
    echo "$file"
done

# 10. Avoid parsing ls output
# Bad
for file in $(ls *.txt); do
    echo "$file"
done

# Good
for file in *.txt; do
    [ -e "$file" ] || continue
    echo "$file"
done
```

---

## Summary

This guide covers essential bash scripting concepts with practical examples. Key takeaways:

1. **Variables**: Use proper quoting and understand scope
2. **Conditionals**: Master test operators and comparison methods
3. **Loops**: Choose appropriate loop type for your needs
4. **Functions**: Write modular, reusable code
5. **Arrays**: Use indexed and associative arrays effectively
6. **String Manipulation**: Leverage built-in string operations
7. **Error Handling**: Implement proper error checking and exit codes
8. **Best Practices**: Write clean, maintainable scripts

Practice these concepts to become proficient in bash scripting!
