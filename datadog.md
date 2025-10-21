# Datadog Log Parsing, Patterns, and Query Guide

## Table of Contents
1. [Parser Overview](#parser-overview)
2. [Parser Conditions and Matchers](#parser-conditions-and-matchers)
3. [Filter Rules](#filter-rules)
4. [Creating Patterns (Grok Parser)](#creating-patterns-grok-parser)
5. [Pattern Examples](#pattern-examples)
6. [Variables for Log Search](#variables-for-log-search)
7. [Variables for Dashboards](#variables-for-dashboards)
8. [Best Practices](#best-practices)

---

## Parser Overview

### What is a Log Parser?

A **log parser** in Datadog extracts structured data from raw log messages. It transforms unstructured text into queryable attributes.

**Example:**
```
# Raw Log
"User john.doe logged in from 192.168.1.100 at 2025-10-19 10:30:45"

# After Parsing
{
  "user": "john.doe",
  "ip_address": "192.168.1.100",
  "timestamp": "2025-10-19 10:30:45",
  "action": "logged in"
}
```

### Types of Parsers

1. **Grok Parser**: Pattern-based parsing using Grok syntax
2. **JSON Parser**: Parses JSON-formatted logs
3. **Key-Value Parser**: Extracts key=value pairs
4. **Regex Parser**: Custom regular expressions
5. **Date Remapper**: Extracts and standardizes timestamps
6. **Service Remapper**: Maps service names
7. **Status Remapper**: Maps log severity levels

---

## Parser Conditions and Matchers

### Condition Syntax

Parsers only process logs that match specific conditions. Use conditions to apply parsers selectively.

**Condition Operators:**
- `AND`: All conditions must match
- `OR`: At least one condition must match
- `NOT`: Negation

### Matcher Types

#### 1. **Source Matcher**
Match logs from specific sources:

```
source:nginx
source:(nginx OR apache)
source:kubernetes AND service:api
```

#### 2. **Service Matcher**
Match specific services:

```
service:web-app
service:(frontend OR backend)
NOT service:test-*
```

#### 3. **Tag Matcher**
Match based on tags:

```
env:production
env:prod AND region:us-east-1
team:platform OR team:sre
```

#### 4. **Attribute Matcher**
Match specific attributes:

```
@http.status_code:500
@user.role:admin
@error.type:NullPointerException
```

#### 5. **Full-Text Matcher**
Match text in the log message:

```
*error*
*failed* OR *exception*
"connection timeout"
```

### Example Conditions

```yaml
# Match production errors only
env:production AND status:error

# Match specific application logs
source:application AND service:payment-api

# Match logs with specific patterns
*Exception* OR *Error* OR *Failed*

# Complex condition
(env:prod OR env:staging) AND service:api-* AND @http.status_code:[400 TO 599]
```

---

## Filter Rules

### Exclusion Filters

Exclude logs you don't want to ingest or index.

**Examples:**

```yaml
# Exclude health checks
source:nginx AND @http.url_details.path:/health

# Exclude debug logs in production
env:production AND status:debug

# Exclude specific IPs
@network.client.ip:(10.0.0.* OR 192.168.*.*)

# Exclude noisy services
service:monitoring-agent
```

### Inclusion Filters

Only include logs matching criteria (implicit - logs not matching are excluded).

```yaml
# Only include errors and warnings
status:(error OR warn)

# Only include production
env:production

# Only include specific services
service:(api OR web OR worker)
```

### Filter Priority

1. **Exclusion filters** run first (drop unwanted logs)
2. **Parsers** process remaining logs
3. **Indexes** receive parsed logs

---

## Creating Patterns (Grok Parser)

### Grok Syntax Basics

Grok patterns use this syntax:
```
%{PATTERN_NAME:attribute_name:data_type}
```

**Components:**
- `PATTERN_NAME`: Predefined or custom pattern
- `attribute_name`: Field name in parsed log
- `data_type`: Optional (string, integer, double, boolean)

### Built-in Grok Patterns

Common patterns available in Datadog:

```grok
# Numbers
%{INT}           # Integer
%{NUMBER}        # Integer or float
%{POSINT}        # Positive integer

# Network
%{IP}            # IPv4 or IPv6
%{IPV4}          # IPv4 address
%{IPV6}          # IPv6 address
%{HOSTNAME}      # Hostname
%{MAC}           # MAC address

# Strings
%{WORD}          # Single word (alphanumeric + _)
%{NOTSPACE}      # Non-whitespace characters
%{DATA}          # Any character (non-greedy)
%{GREEDYDATA}    # Any character (greedy)
%{QUOTEDSTRING}  # Quoted string

# Date/Time
%{DATE}          # Date
%{TIME}          # Time
%{TIMESTAMP_ISO8601}  # ISO8601 timestamp

# HTTP
%{HTTPMETHOD}    # GET, POST, etc.
%{URIPATH}       # URI path
%{URIPARAM}      # URI parameters

# Logs
%{LOGLEVEL}      # Log levels (INFO, ERROR, etc.)
%{SYSLOGBASE}    # Syslog format
```

### Creating Custom Patterns

#### Step 1: Identify Log Format

```
Example Log:
[2025-10-19 10:30:45] INFO user=john.doe ip=192.168.1.100 action=login duration=250ms
```

#### Step 2: Write Grok Pattern

```grok
\[%{TIMESTAMP_ISO8601:timestamp}\] %{LOGLEVEL:log_level} user=%{NOTSPACE:user.name} ip=%{IP:network.client.ip} action=%{WORD:action} duration=%{NUMBER:duration:integer}ms
```

**Breakdown:**
- `\[...\]`: Literal brackets (escaped)
- `%{TIMESTAMP_ISO8601:timestamp}`: Extract timestamp
- `%{LOGLEVEL:log_level}`: Extract log level (INFO, ERROR, etc.)
- `%{NOTSPACE:user.name}`: Extract username
- `%{IP:network.client.ip}`: Extract IP address
- `%{WORD:action}`: Extract action
- `%{NUMBER:duration:integer}`: Extract duration as integer

#### Step 3: Configure in Datadog

**Via UI:**
1. Navigate to **Logs → Configuration → Pipelines**
2. Select or create pipeline
3. Add **Grok Parser** processor
4. Set condition matcher
5. Add parsing rules

**Example Configuration:**

```yaml
# Parser Name: Application Log Parser

# Sample Log:
[2025-10-19 10:30:45] INFO user=john.doe ip=192.168.1.100 action=login duration=250ms

# Parsing Rule:
Rule Name: Parse Application Logs
Pattern: \[%{TIMESTAMP_ISO8601:timestamp}\] %{LOGLEVEL:log_level} user=%{NOTSPACE:user.name} ip=%{IP:network.client.ip} action=%{WORD:action} duration=%{NUMBER:duration:integer}ms

# Advanced Settings:
- Extract from: message
- Helper Rules: (optional custom patterns)
```

---

## Pattern Examples

### 1. Apache/Nginx Access Logs

**Log Format:**
```
192.168.1.100 - - [19/Oct/2025:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0"
```

**Grok Pattern:**
```grok
%{IP:network.client.ip} - - \[%{HTTPDATE:timestamp}\] "%{WORD:http.method} %{URIPATH:http.url_details.path}(?:%{URIPARAM:http.url_details.query})? HTTP/%{NUMBER:http.version}" %{INT:http.status_code:integer} %{INT:network.bytes_written:integer} "%{DATA:http.referer}" "%{DATA:http.useragent}"
```

### 2. Java Application Logs

**Log Format:**
```
2025-10-19 10:30:45,123 [http-nio-8080-exec-10] ERROR com.example.UserService - Failed to fetch user: NullPointerException at line 42
```

**Grok Pattern:**
```grok
%{TIMESTAMP_ISO8601:timestamp} \[%{DATA:thread.name}\] %{LOGLEVEL:log_level} %{DATA:logger.name} - %{GREEDYDATA:message}
```

### 3. Docker Container Logs

**Log Format:**
```
2025-10-19T10:30:45.123456Z container_name=web-app-1 container_id=abc123 message="Processing request for /api/users"
```

**Grok Pattern:**
```grok
%{TIMESTAMP_ISO8601:timestamp} container_name=%{NOTSPACE:container.name} container_id=%{NOTSPACE:container.id} message="%{GREEDYDATA:message}"
```

### 4. AWS ALB Logs

**Log Format:**
```
http 2025-10-19T10:30:45.123456Z app/my-alb/50dc6c495c0c9188 192.168.1.100:54321 10.0.0.1:80 0.001 0.002 0.000 200 200 1234 567 "GET https://example.com:443/api/users HTTP/1.1" "Mozilla/5.0"
```

**Grok Pattern:**
```grok
%{NOTSPACE:http.protocol} %{TIMESTAMP_ISO8601:timestamp} %{NOTSPACE:elb.name} %{IP:network.client.ip}:%{INT:network.client.port:integer} %{IP:network.destination.ip}:%{INT:network.destination.port:integer} %{NUMBER:http.request_processing_time:double} %{NUMBER:http.target_processing_time:double} %{NUMBER:http.response_processing_time:double} %{INT:http.status_code:integer} %{INT:http.backend_status_code:integer} %{INT:network.bytes_read:integer} %{INT:network.bytes_written:integer} "%{WORD:http.method} %{DATA:http.url} HTTP/%{NUMBER:http.version}" "%{DATA:http.useragent}"
```

### 5. JSON Logs (Alternative to JSON Parser)

**Log Format:**
```
{"timestamp":"2025-10-19T10:30:45Z","level":"ERROR","service":"api","user":"john.doe","message":"Database connection failed"}
```

**Grok Pattern:**
```grok
\{"timestamp":"%{TIMESTAMP_ISO8601:timestamp}","level":"%{LOGLEVEL:log_level}","service":"%{WORD:service}","user":"%{DATA:user.name}","message":"%{DATA:message}"\}
```

**Note:** For JSON logs, use the **JSON Parser** instead of Grok for better performance.

### 6. Custom Application Pattern with Helper Rules

**Log Format:**
```
[APP-12345] 2025-10-19 10:30:45 | USER: john.doe | ACTION: CREATE_ORDER | ORDER_ID: ORD-98765 | AMOUNT: $123.45
```

**Helper Rules:**
```grok
# Define custom patterns
APP_ID APP-[0-9]{5}
ORDER_ID ORD-[0-9]{5}
MONEY_AMOUNT \$[0-9]+\.[0-9]{2}
```

**Main Pattern:**
```grok
\[%{APP_ID:app.id}\] %{TIMESTAMP_ISO8601:timestamp} \| USER: %{NOTSPACE:user.name} \| ACTION: %{WORD:action} \| ORDER_ID: %{ORDER_ID:order.id} \| AMOUNT: %{MONEY_AMOUNT:order.amount}
```

---

## Variables for Log Search

### Creating Saved Views with Variables

Variables allow dynamic filtering in log searches.

### 1. Using Facets as Variables

**Example: Filter by Environment**

```yaml
# Create facet: env
# Values: production, staging, development

# Query with variable:
env:$env
```

**In Datadog UI:**
- Saved View: "Errors by Environment"
- Query: `status:error env:$env`
- User selects environment from dropdown

### 2. Template Variables in URLs

Share log queries with dynamic filters:

```
https://app.datadoghq.com/logs?query=status:error%20env:{{env}}&from_ts={{start_time}}&to_ts={{end_time}}
```

### 3. Common Search Patterns

#### Search by Time Range
```
# Last 15 minutes of errors
status:error

# Specific time range (use UI time picker)
status:error
```

#### Search by Attributes
```
# Find specific user's logs
@user.name:john.doe

# Find errors for specific endpoint
@http.url_details.path:/api/users AND status:error

# Find slow requests
@duration:>5000
```

#### Search by Tags
```
# Production errors
env:production status:error

# Specific service and version
service:api version:2.1.3

# Multiple tags
env:prod AND region:us-east-1 AND team:platform
```

#### Wildcard Searches
```
# Any exception
*Exception*

# Specific error pattern
*ConnectionTimeout* OR *SocketException*

# User pattern
@user.name:john.*
```

#### Range Searches
```
# HTTP status codes
@http.status_code:[400 TO 599]

# Duration in milliseconds
@duration:[1000 TO *]

# Numeric ranges
@error.count:>=5
```

### 4. Creating Reusable Queries

**Saved View Structure:**

```yaml
Name: "Production API Errors"
Query: "service:api env:production status:error"
Columns:
  - timestamp
  - service
  - @http.status_code
  - @http.url_details.path
  - message
Filters:
  - env:production
  - status:error
  - service:api
```

**With Variables:**

```yaml
Name: "Service Errors by Environment"
Query: "service:$service env:$env status:error"
Variables:
  - name: service
    type: facet
    facet: service
  - name: env
    type: facet
    facet: env
```

---

## Variables for Dashboards

### Dashboard Template Variables

Template variables allow users to dynamically filter dashboard data.

### 1. Creating Template Variables

**Variable Types:**

#### a) Facet/Tag Variable
```yaml
Variable Name: env
Source: Tag or Facet
Tag/Facet Key: env
Default Value: production
Available Values: production, staging, development
```

#### b) Log Query Variable
```yaml
Variable Name: service
Source: Log Query
Query: service:*
Field: service
Default Value: api
```

#### c) Custom List Variable
```yaml
Variable Name: region
Source: Custom List
Values: us-east-1, us-west-2, eu-west-1
Default Value: us-east-1
```

### 2. Using Variables in Dashboard Widgets

#### Log Stream Widget
```yaml
Widget: Log Stream
Query: env:$env service:$service status:error
Columns: [@timestamp, service, @http.status_code, message]
```

#### Timeseries Widget
```yaml
Widget: Timeseries
Query: env:$env service:$service
Metrics: count(*)
Group by: @http.status_code
```

#### Top List Widget
```yaml
Widget: Top List
Query: env:$env status:error
Count by: @error.type
Limit: 10
```

#### Table Widget
```yaml
Widget: Table
Query: env:$env service:$service
Columns:
  - service
  - count(*) as "Error Count"
  - avg(@duration) as "Avg Duration"
Group by: service
```

### 3. Multi-Select Variables

Allow selecting multiple values:

```yaml
Variable Name: services
Type: Multi-Select
Source: Facet
Facet: service
Default: [api, web, worker]

# Usage in query:
service:$services.value
```

### 4. Dependent Variables

Create cascading filters:

```yaml
# Parent variable
Variable 1:
  Name: env
  Source: Facet
  Facet: env

# Child variable (depends on env)
Variable 2:
  Name: service
  Source: Log Query
  Query: env:$env service:*
  Field: service
```

### 5. Complete Dashboard Example

```yaml
Dashboard: "Application Monitoring"

Template Variables:
  1. Environment:
     - Name: env
     - Type: Facet
     - Facet: env
     - Default: production
     - Multi-select: No

  2. Service:
     - Name: service
     - Type: Log Query
     - Query: env:$env service:*
     - Field: service
     - Default: *
     - Multi-select: Yes

  3. Time Range:
     - Name: time_range
     - Type: Custom List
     - Values: [1h, 4h, 24h, 7d]
     - Default: 4h

Widgets:
  1. Error Rate:
     Type: Timeseries
     Query: env:$env service:$service.value status:error
     Formula: count(*) / total_requests * 100

  2. Top Errors:
     Type: Top List
     Query: env:$env service:$service.value status:error
     Group by: @error.type
     Limit: 10

  3. Error Logs:
     Type: Log Stream
     Query: env:$env service:$service.value status:error
     Columns: [@timestamp, service, @error.type, message]

  4. P95 Latency:
     Type: Query Value
     Query: env:$env service:$service.value
     Metric: p95(@duration)

  5. Request Distribution:
     Type: Pie Chart
     Query: env:$env service:$service.value
     Group by: @http.status_code
```

### 6. Variable Syntax in Queries

```yaml
# Single value variable
env:$env

# Multi-value variable (OR condition)
service:$services.value

# All values selected
service:*

# Variable with wildcard
@user.name:$username*

# Multiple variables
env:$env AND service:$service AND region:$region

# Variable in metric
avg:@duration{env:$env,service:$service}
```

---

## Best Practices

### Parser Best Practices

1. **Use Specific Conditions**
   ```
   ✅ source:nginx AND env:production
   ❌ *
   ```

2. **Order Parsers by Specificity**
   - Most specific parsers first
   - Generic parsers last
   - Use pipeline ordering

3. **Test with Sample Logs**
   - Use the parser test feature
   - Verify all fields extract correctly
   - Check data types

4. **Use Helper Rules for Reusability**
   ```grok
   # Define once, use everywhere
   ORDER_ID ORD-[0-9]{5}
   USER_ID USR-[0-9]{8}
   ```

5. **Name Attributes Consistently**
   ```
   ✅ user.name, user.email, user.id
   ❌ username, userEmail, userId
   ```

6. **Use Standard Attribute Names**
   - `@http.status_code` (not `@status` or `@code`)
   - `@network.client.ip` (not `@ip` or `@client_ip`)
   - `@duration` (not `@response_time` or `@latency`)

### Query Best Practices

1. **Use Facets for Common Filters**
   - Create facets for frequently searched attributes
   - Facets improve query performance

2. **Leverage Saved Views**
   - Save common queries
   - Share with team
   - Reduce query errors

3. **Use Indexed Fields**
   - Query indexed fields when possible
   - Non-indexed queries are slower

4. **Optimize Wildcards**
   ```
   ✅ service:api-* (prefix wildcard)
   ❌ *-service-* (middle wildcard - slower)
   ```

### Dashboard Best Practices

1. **Limit Variables**
   - 3-5 variables per dashboard
   - Too many variables confuse users

2. **Set Sensible Defaults**
   - Default to production environment
   - Default to recent time range
   - Default to most important services

3. **Group Related Widgets**
   - Use sections/groups
   - Logical flow (overview → details)

4. **Use Consistent Time Ranges**
   - Sync time across widgets
   - Use global time picker

5. **Add Context**
   - Widget titles describe what's shown
   - Use notes/markdown for documentation
   - Add links to runbooks

### Performance Best Practices

1. **Exclude Noisy Logs Early**
   - Use exclusion filters
   - Save on ingestion costs

2. **Index Strategically**
   - Don't index everything
   - Index logs needed for investigation
   - Use retention filters

3. **Use Sampling for High-Volume**
   - Sample debug logs (10%)
   - Keep all errors (100%)

4. **Optimize Parsing**
   - Parse only what you need
   - Avoid overly complex patterns
   - Use JSON parser for JSON logs

---

## Advanced Techniques

### Multi-Line Log Parsing

For logs spanning multiple lines (stack traces):

```yaml
# Pattern for start of new log entry
Start Pattern: ^\[%{TIMESTAMP_ISO8601}

# Aggregate following lines until next log starts
```

### Conditional Parsing

Apply different patterns based on content:

```grok
# If log contains "ERROR"
%{LOGLEVEL:log_level:regex("ERROR")} %{GREEDYDATA:error_details}

# If log contains "INFO"
%{LOGLEVEL:log_level:regex("INFO")} %{GREEDYDATA:info_message}
```

### Nested Attribute Extraction

Extract nested JSON fields:

```yaml
# Original: {"user": {"profile": {"name": "John"}}}
# Extracted as: user.profile.name = "John"
```

### Date Parsing and Remapping

Extract and remap timestamps:

```yaml
Date Remapper:
  Source: @timestamp_field
  Target: @timestamp
  Format: yyyy-MM-dd HH:mm:ss
  Timezone: UTC
```

---

## Troubleshooting

### Common Issues

1. **Parser Not Matching Logs**
   - Check condition matcher
   - Verify sample log format
   - Test pattern in parser tester

2. **Incorrect Field Extraction**
   - Pattern too greedy/specific
   - Check escape characters
   - Verify data types

3. **Performance Issues**
   - Too many parsers in pipeline
   - Complex regex patterns
   - Missing exclusion filters

4. **Variables Not Working**
   - Check variable scope
   - Verify facet exists
   - Check query syntax

### Testing Tools

1. **Grok Parser Tester**
   - Test patterns before deploying
   - Validate field extraction
   - Check data types

2. **Log Explorer**
   - Test queries live
   - Verify facets exist
   - Check attribute names

3. **Pipeline Testing**
   - Use sample logs
   - Verify parsing order
   - Check processor output

---

## Examples Summary

### Quick Reference: Common Patterns

```grok
# IP Address
%{IP:network.client.ip}

# Timestamp
%{TIMESTAMP_ISO8601:timestamp}

# HTTP Status
%{INT:http.status_code:integer}

# Duration/Latency
%{NUMBER:duration:double}ms

# User/Username
%{NOTSPACE:user.name}

# URL Path
%{URIPATH:http.url_details.path}

# Log Level
%{LOGLEVEL:log_level}

# Any text (non-greedy)
%{DATA:field_name}

# Any text (greedy - use at end)
%{GREEDYDATA:message}
```

### Quick Reference: Query Syntax

```
# Exact match
service:api

# OR condition
status:(error OR warn)

# AND condition
env:prod AND service:api

# NOT condition
NOT status:debug

# Wildcard
service:api-*

# Range
@http.status_code:[400 TO 599]

# Exists
@user.id:*

# Comparison
@duration:>1000

# Phrase search
"database connection failed"
```

---

## Additional Resources

### Datadog Documentation
- [Log Pipeline Documentation](https://docs.datadoghq.com/logs/log_configuration/pipelines/)
- [Grok Parser Documentation](https://docs.datadoghq.com/logs/log_configuration/parsing/)
- [Log Search Syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/)
- [Template Variables](https://docs.datadoghq.com/dashboards/template_variables/)

### External Resources
- [Grok Pattern Library](https://github.com/elastic/logstash/blob/main/patterns/grok-patterns)
- [Regex Testing](https://regex101.com/)
- [Grok Debugger](https://grokdebug.herokuapp.com/)

---

**Document Version:** 1.0  
**Last Updated:** October 19, 2025  
**Author:** DevOps Team
