# AWS Certified Solutions Architect - Associate (SAA-C03)
## Exam Questions and Answers

*Last Updated: October 2025*

---

## Domain 1: Design Secure Architectures (30%)

### Q1: Multi-Region High Availability
**Question:** A company wants to deploy a web application across multiple AWS regions to ensure high availability and disaster recovery. The application uses an Application Load Balancer (ALB) and EC2 instances. What is the MOST cost-effective solution to route traffic to the nearest healthy region?

**A)** Use Amazon CloudFront with multiple origins pointing to ALBs in different regions  
**B)** Use AWS Global Accelerator with endpoints in multiple regions  
**C)** Use Route 53 with geolocation routing policy  
**D)** Deploy a Network Load Balancer in each region and use Route 53 failover routing

**Answer:** B

**Explanation:** AWS Global Accelerator provides static IP addresses that act as a fixed entry point to your application and routes traffic to optimal endpoints based on health, geography, and routing policies. It's more cost-effective than CloudFront for non-cacheable content and provides automatic failover. Route 53 alone doesn't provide the same level of traffic optimization and health checking at the edge.

---

### Q2: S3 Encryption at Rest
**Question:** A financial services company needs to store sensitive customer data in Amazon S3 with encryption at rest. The company's security policy requires that encryption keys be rotated automatically and that the company maintain full control over the key rotation schedule. Which solution meets these requirements?

**A)** Use S3 Server-Side Encryption with Amazon S3-Managed Keys (SSE-S3)  
**B)** Use S3 Server-Side Encryption with AWS KMS Keys (SSE-KMS) with automatic key rotation enabled  
**C)** Use S3 Server-Side Encryption with Customer-Provided Keys (SSE-C)  
**D)** Use client-side encryption with AWS KMS

**Answer:** B

**Explanation:** SSE-KMS with AWS KMS provides automatic key rotation (every year by default) and allows you to control the key rotation schedule through KMS key policies. SSE-S3 doesn't give you control over key rotation, and SSE-C requires you to manage the keys entirely yourself. Client-side encryption adds complexity.

---

### Q3: VPC Security with Network ACLs
**Question:** A solutions architect is designing a VPC with public and private subnets. The private subnet hosts a database that should only accept traffic from the application servers in the public subnet on port 3306. The database should not be able to initiate outbound connections to the internet. How should the solutions architect configure the Network ACL for the private subnet?

**A)** Inbound: Allow port 3306 from public subnet CIDR, Allow ephemeral ports from public subnet CIDR; Outbound: Allow ephemeral ports to public subnet CIDR  
**B)** Inbound: Allow all traffic from public subnet CIDR; Outbound: Allow all traffic to public subnet CIDR  
**C)** Inbound: Allow port 3306 from anywhere; Outbound: Deny all traffic  
**D)** Inbound: Allow port 3306 from public subnet CIDR; Outbound: Deny all traffic

**Answer:** A

**Explanation:** Network ACLs are stateless, so you must explicitly allow both inbound and outbound traffic. The database needs to accept connections on port 3306 (inbound) and respond using ephemeral ports (outbound). The application servers will use ephemeral ports for their side of the connection. Option D would prevent responses from the database.

---

### Q4: IAM Role for Cross-Account Access
**Question:** Company A needs to grant Company B's AWS account access to specific S3 buckets in Company A's account. Company B has hundreds of users who need this access. What is the MOST secure and scalable solution?

**A)** Create IAM users in Company A's account for each user in Company B  
**B)** Create an IAM role in Company A's account with appropriate permissions, and allow Company B's account to assume the role  
**C)** Share the root account credentials with Company B  
**D)** Create a single IAM user in Company A's account and share the credentials with all users in Company B

**Answer:** B

**Explanation:** Creating a cross-account IAM role is the best practice for granting access between AWS accounts. Users in Company B can assume the role using their own credentials (through STS AssumeRole), which provides better security, auditability, and scalability than sharing credentials or creating individual users.

---

## Domain 2: Design Resilient Architectures (26%)

### Q5: Auto Scaling and Load Balancing
**Question:** An application runs on EC2 instances behind an Application Load Balancer. The application experiences predictable traffic patterns with high load during business hours (9 AM - 5 PM) and low load at night. What is the MOST cost-effective Auto Scaling configuration?

**A)** Use target tracking scaling with CPU utilization at 70%  
**B)** Use scheduled scaling to increase capacity before business hours and decrease after  
**C)** Use step scaling with CloudWatch alarms  
**D)** Use simple scaling with a single adjustment

**Answer:** B

**Explanation:** Since the traffic pattern is predictable, scheduled scaling is the most cost-effective solution. It proactively adds capacity before the load increases, ensuring resources are available when needed without waiting for CloudWatch alarms to trigger. Target tracking and step scaling are reactive and better for unpredictable patterns.

---

### Q6: RDS Multi-AZ and Read Replicas
**Question:** A company runs a MySQL database on Amazon RDS and needs to improve read performance while maintaining high availability. The application performs many read queries but few writes. What solution should the solutions architect recommend?

**A)** Enable Multi-AZ deployment only  
**B)** Create Read Replicas in the same region  
**C)** Enable Multi-AZ deployment and create Read Replicas  
**D)** Migrate to Amazon Aurora and enable Multi-AZ

**Answer:** C

**Explanation:** Multi-AZ provides high availability and automatic failover for the primary database, while Read Replicas improve read performance by distributing read traffic. Both should be implemented - Multi-AZ for availability and Read Replicas for performance. Option D (Aurora) is more expensive, though it would work.

---

### Q7: EBS Volume Types for Database
**Question:** A database application requires consistent low-latency performance with 50,000 IOPS. The database size is 2 TB and growing. Which EBS volume type should be used?

**A)** General Purpose SSD (gp3)  
**B)** Provisioned IOPS SSD (io2)  
**C)** Throughput Optimized HDD (st1)  
**D)** Cold HDD (sc1)

**Answer:** B

**Explanation:** Provisioned IOPS SSD (io2 or io2 Block Express) is designed for I/O-intensive workloads requiring sustained IOPS performance and low latency, making it ideal for databases. While gp3 can deliver up to 16,000 IOPS, it cannot reach 50,000 IOPS. HDD volumes are not suitable for low-latency requirements.

---

### Q8: DynamoDB Global Tables
**Question:** A mobile application serves users globally and requires single-digit millisecond read and write latency in multiple regions. The application needs eventual consistency across regions. Which AWS service combination should be used?

**A)** Amazon RDS with Read Replicas in multiple regions  
**B)** Amazon DynamoDB with Global Tables  
**C)** Amazon Aurora Global Database  
**D)** Amazon ElastiCache with cross-region replication

**Answer:** B

**Explanation:** DynamoDB Global Tables provide multi-region, fully replicated tables with fast local reads and writes in each region. They're specifically designed for globally distributed applications requiring low latency and eventual consistency. Aurora Global Database has higher replication latency (typically under 1 second), and RDS Read Replicas have even higher latency.

---

## Domain 3: Design High-Performing Architectures (24%)

### Q9: CloudFront and S3 for Static Website
**Question:** A company hosts a static website on Amazon S3 and wants to improve performance for global users while reducing S3 data transfer costs. What should the solutions architect recommend?

**A)** Enable S3 Transfer Acceleration  
**B)** Create an Amazon CloudFront distribution with the S3 bucket as the origin  
**C)** Use S3 Cross-Region Replication to multiple regions  
**D)** Enable S3 Intelligent-Tiering

**Answer:** B

**Explanation:** CloudFront is a CDN that caches content at edge locations worldwide, providing low-latency access for global users and reducing data transfer costs from S3. Transfer Acceleration is for faster uploads, not downloads. Cross-Region Replication would increase costs and complexity. Intelligent-Tiering is for storage cost optimization, not performance.

---

### Q10: Lambda and API Gateway
**Question:** A serverless application uses AWS Lambda functions behind Amazon API Gateway. The Lambda functions query a DynamoDB table. During peak hours, the API returns 5xx errors due to throttling. What is the MOST cost-effective solution to resolve this issue?

**A)** Increase Lambda concurrency limits  
**B)** Increase DynamoDB provisioned throughput  
**C)** Enable DynamoDB Auto Scaling  
**D)** Add an SQS queue between API Gateway and Lambda

**Answer:** C

**Explanation:** DynamoDB Auto Scaling automatically adjusts read and write capacity based on actual usage patterns, making it cost-effective for variable workloads. Manually increasing provisioned throughput (Option B) would work but is more expensive during off-peak hours. Increasing Lambda concurrency doesn't address the DynamoDB throttling issue. Adding SQS changes the architecture to asynchronous processing.

---

### Q11: EFS vs EBS vs S3
**Question:** An application running on multiple EC2 instances needs to share file storage with concurrent read/write access. The storage must be mountable as a file system. Which storage solution should be used?

**A)** Amazon EBS with Multi-Attach enabled  
**B)** Amazon EFS  
**C)** Amazon S3 with S3FS  
**D)** Amazon FSx for Windows File Server

**Answer:** B

**Explanation:** Amazon EFS (Elastic File System) is designed for shared file storage that can be concurrently accessed by multiple EC2 instances. EBS Multi-Attach is limited to specific instance types and use cases. S3 is object storage, not a file system (S3FS has performance limitations). FSx for Windows is for Windows-based workloads.

---

### Q12: ElastiCache for Session Management
**Question:** A web application uses EC2 instances in an Auto Scaling group. Users report that they are logged out when the application scales. How can the solutions architect ensure session persistence?

**A)** Enable sticky sessions on the Application Load Balancer  
**B)** Store session data in Amazon ElastiCache  
**C)** Use larger EC2 instances to reduce scaling frequency  
**D)** Store session data on EBS volumes

**Answer:** B

**Explanation:** Storing session data in ElastiCache (Redis or Memcached) provides a centralized, high-performance session store that persists across instance scaling. Sticky sessions only route users to the same instance but don't solve the problem when instances are terminated. EBS volumes are not shared across instances.

---

## Domain 4: Design Cost-Optimized Architectures (20%)

### Q13: S3 Storage Classes
**Question:** A company needs to store application logs for compliance. Logs must be retained for 7 years but are rarely accessed after 90 days. If accessed, retrieval within 12 hours is acceptable. What is the MOST cost-effective storage strategy?

**A)** Store all logs in S3 Standard  
**B)** Store logs in S3 Standard, then transition to S3 Glacier after 90 days  
**C)** Store logs in S3 Standard-IA, then transition to S3 Glacier Deep Archive after 90 days  
**D)** Store logs directly in S3 Glacier Deep Archive

**Answer:** C

**Explanation:** S3 Standard-IA (Infrequent Access) is cost-effective for the first 90 days when logs might be accessed occasionally. After 90 days, S3 Glacier Deep Archive provides the lowest storage cost for long-term archival with retrieval times of 12 hours, which meets the requirement. Option D doesn't account for potential access in the first 90 days.

---

### Q14: Reserved Instances vs Savings Plans
**Question:** A company runs a steady-state workload on EC2 instances (t3.large) for 24/7 operations. The company wants to reduce costs and is planning to use the same instance type for the next 3 years. What is the MOST cost-effective option?

**A)** Purchase Standard Reserved Instances for 3 years with all upfront payment  
**B)** Purchase Compute Savings Plans for 3 years with all upfront payment  
**C)** Use Spot Instances with Spot Fleet  
**D)** Purchase Convertible Reserved Instances for 3 years with no upfront payment

**Answer:** A

**Explanation:** For a known, steady-state workload with a specific instance type, Standard Reserved Instances with all upfront payment provide the maximum discount (up to 72%). Compute Savings Plans offer flexibility but slightly less discount. Spot Instances are not suitable for 24/7 steady-state workloads. Convertible RIs with no upfront payment offer less discount than Standard RIs with all upfront.

---

### Q15: Lambda vs EC2 Cost Optimization
**Question:** A batch processing job runs once per day, processes data for 15 minutes, and requires 4 GB of memory. The job is currently running on a t3.medium EC2 instance (24/7). How can costs be reduced?

**A)** Use a Reserved Instance for the t3.medium  
**B)** Migrate the job to AWS Lambda  
**C)** Use a smaller instance type like t3.small  
**D)** Use EC2 Spot Instances

**Answer:** B

**Explanation:** Lambda is ideal for short-duration, infrequent workloads. You only pay for actual execution time (15 minutes per day) rather than running an EC2 instance 24/7. Lambda supports up to 10 GB of memory, so 4 GB is well within limits. This would provide significant cost savings compared to any EC2 option.

---

### Q16: RDS Cost Optimization
**Question:** A development team uses an RDS MySQL database during business hours (8 AM - 6 PM, Monday-Friday). The database is not used outside these hours. What is the MOST cost-effective solution?

**A)** Use Reserved Instances for the RDS database  
**B)** Create automated snapshots and delete/recreate the database instance daily  
**C)** Use Amazon Aurora Serverless  
**D)** Downsize the instance type during off-hours

**Answer:** C

**Explanation:** Aurora Serverless automatically starts up, scales capacity, and shuts down based on application demand. You only pay for database capacity when it's in use, making it perfect for intermittent workloads. Option B is operationally complex and has data inconsistency risks. Reserved Instances don't help when the database isn't needed. Downsizing still incurs costs during off-hours.

---

## Additional Important Topics

### Q17: AWS Organizations and Service Control Policies
**Question:** A company with multiple AWS accounts wants to prevent any account from disabling CloudTrail logging. What should the solutions architect implement?

**A)** Create an IAM policy in each account that denies cloudtrail:StopLogging  
**B)** Use AWS Organizations and create a Service Control Policy (SCP) that denies cloudtrail:StopLogging  
**C)** Enable CloudTrail at the organization level with read-only access  
**D)** Use AWS Config rules to detect and remediate CloudTrail disablement

**Answer:** B

**Explanation:** Service Control Policies (SCPs) in AWS Organizations provide centralized control over permissions across all accounts in an organization. An SCP denying cloudtrail:StopLogging will prevent any user or role in member accounts from stopping CloudTrail, even if they have administrator permissions. This is more effective and centralized than managing IAM policies in each account.

---

### Q18: AWS Transit Gateway
**Question:** A company has 15 VPCs that need to communicate with each other and with on-premises networks via AWS Direct Connect. What is the MOST scalable and manageable solution?

**A)** Set up VPC peering connections between all VPCs  
**B)** Use AWS Transit Gateway to connect all VPCs and Direct Connect Gateway  
**C)** Use VPN connections from each VPC to on-premises  
**D)** Create a hub-and-spoke topology with one central VPC

**Answer:** B

**Explanation:** AWS Transit Gateway acts as a cloud router that simplifies network topology by enabling all VPCs and on-premises networks to connect through a single gateway. VPC peering would require 105 peering connections (n*(n-1)/2) which is not scalable. Transit Gateway is specifically designed for this scenario and supports up to 5,000 VPCs.

---

### Q19: AWS PrivateLink
**Question:** Company A wants to provide access to their SaaS application running in their VPC to customers' VPCs without exposing the traffic to the internet. What AWS service should be used?

**A)** VPC Peering  
**B)** AWS PrivateLink  
**C)** AWS Direct Connect  
**D)** Internet Gateway with security groups

**Answer:** B

**Explanation:** AWS PrivateLink provides private connectivity between VPCs and services without requiring internet gateways, NAT, VPC peering, or VPN connections. It's specifically designed for securely sharing services across accounts and is the standard solution for SaaS providers to offer services to customers privately.

---

### Q20: AWS Backup and Disaster Recovery
**Question:** A company needs to implement a disaster recovery strategy with an RTO of 4 hours and RPO of 1 hour for their production application running on EC2 and RDS. What DR strategy should be used?

**A)** Backup and Restore  
**B)** Pilot Light  
**C)** Warm Standby  
**D)** Multi-Site Active-Active

**Answer:** C

**Explanation:** Warm Standby maintains a scaled-down but fully functional version of the production environment in another region. This can typically achieve RTO of 1-4 hours and RPO of minutes to hours. Backup and Restore typically has RTO of hours to days. Pilot Light has minimal resources running (longer RTO). Multi-Site Active-Active is expensive and overkill for 4-hour RTO.

---

### Q21: Amazon EventBridge
**Question:** An application needs to perform specific actions when an EC2 instance state changes (e.g., stopping, terminating). What is the MOST efficient serverless solution?

**A)** Use CloudWatch Events to trigger a Lambda function  
**B)** Use Amazon EventBridge to trigger a Lambda function  
**C)** Poll EC2 API every minute using a Lambda function  
**D)** Use AWS Config to detect state changes

**Answer:** B

**Explanation:** Amazon EventBridge (evolution of CloudWatch Events) is designed for event-driven architectures. It can detect EC2 state changes and trigger Lambda functions in real-time without polling. While CloudWatch Events would also work (Option A), EventBridge is the modern recommended service with more features. Polling is inefficient and costly.

---

### Q22: AWS Systems Manager Parameter Store vs Secrets Manager
**Question:** An application needs to store database passwords, API keys, and application configuration parameters. The passwords must be rotated automatically every 90 days. What is the BEST solution?

**A)** Store all values in Systems Manager Parameter Store (SecureString)  
**B)** Store passwords in Secrets Manager and configuration in Parameter Store  
**C)** Store all values in Secrets Manager  
**D)** Store values encrypted in S3

**Answer:** B

**Explanation:** AWS Secrets Manager provides automatic rotation for secrets like database passwords and API keys, while Parameter Store is cost-effective for configuration parameters. Using both services optimally balances functionality and cost. Secrets Manager charges per secret, so storing non-secret configuration there is unnecessarily expensive.

---

### Q23: Amazon Kinesis Data Streams vs Kinesis Firehose
**Question:** A company needs to ingest real-time clickstream data, perform real-time analytics, and store the data in S3 for long-term analysis. What is the MOST appropriate solution?

**A)** Use Kinesis Data Streams with Lambda for analytics, then write to S3  
**B)** Use Kinesis Data Firehose to deliver directly to S3  
**C)** Use Kinesis Data Streams with Kinesis Data Analytics, then Firehose to S3  
**D)** Use SQS to buffer data, then Lambda to write to S3

**Answer:** C

**Explanation:** Kinesis Data Streams allows real-time processing and custom analytics using Kinesis Data Analytics (for SQL-based processing) or Lambda. Kinesis Data Firehose can then batch and deliver data to S3. Option B (Firehose alone) doesn't provide real-time analytics capabilities. Option A works but is more complex than using Data Analytics.

---

### Q24: AWS Shield and WAF
**Question:** A public-facing web application on EC2 behind an ALB experiences frequent DDoS attacks. The company needs protection against network and application layer attacks while maintaining a budget. What should be implemented?

**A)** Enable AWS Shield Standard only  
**B)** Enable AWS Shield Advanced  
**C)** Use AWS WAF with rate-based rules and AWS Shield Standard  
**D)** Use AWS Shield Advanced and AWS WAF with AWS Firewall Manager

**Answer:** C

**Explanation:** AWS Shield Standard is automatically enabled for all AWS customers at no additional cost and protects against common network layer DDoS attacks. AWS WAF provides application-layer protection with customizable rules, including rate-based rules to block excessive requests. Shield Advanced ($3,000/month) is expensive and not needed unless you require 24/7 DDoS Response Team support and cost protection.

---

### Q25: Amazon SNS vs SQS
**Question:** An e-commerce application needs to send order notifications to multiple systems: email to customer, update inventory, trigger shipping process, and log to analytics. Each system should receive the notification independently. What is the BEST architecture?

**A)** Use Amazon SQS with multiple consumers polling the same queue  
**B)** Use Amazon SNS with multiple SQS queues as subscribers (fan-out pattern)  
**C)** Use Amazon EventBridge with multiple targets  
**D)** Use Lambda to send notifications to each system sequentially

**Answer:** B

**Explanation:** The SNS fan-out pattern is the standard solution for sending messages to multiple independent subscribers. SNS publishes the message once, and each subscribed SQS queue receives a copy. This decouples the systems and allows each to process at their own rate. Option A (single SQS queue) would result in only one consumer receiving each message. Option C works but is more complex for this use case.

---

### Q26: AWS DataSync vs AWS Transfer Family
**Question:** A company needs to migrate 100 TB of data from an on-premises NFS server to Amazon EFS. The migration should be done efficiently with minimal impact on the production network. What service should be used?

**A)** AWS Transfer Family  
**B)** AWS DataSync  
**C)** AWS Snow Family  
**D)** AWS Direct Connect with rsync

**Answer:** B

**Explanation:** AWS DataSync is specifically designed for online data transfer between on-premises storage and AWS storage services (S3, EFS, FSx). It provides built-in data validation, encryption, and bandwidth throttling. AWS Transfer Family is for SFTP/FTP access to S3, not bulk migration. Snow Family is for offline transfers (typically 100+ TB or limited bandwidth). DataSync is the optimal choice for 100 TB online migration.

---

### Q27: Amazon Athena and S3 Data Partitioning
**Question:** A data analytics team queries terabytes of log data stored in S3 using Amazon Athena. Queries are expensive and slow. The logs are organized by date and most queries filter by date ranges. How can query performance and cost be improved?

**A)** Partition the data by date in S3 and use partitioned tables in Athena  
**B)** Convert data to Parquet format only  
**C)** Increase Athena query concurrency limit  
**D)** Use S3 Select instead of Athena

**Answer:** A

**Explanation:** Partitioning data in S3 by date (e.g., year=2025/month=10/day=17/) and using partitioned Athena tables allows queries to scan only relevant partitions, significantly reducing data scanned and cost. Converting to Parquet (Option B) also helps but partitioning has the most impact for date-filtered queries. Combining both (partitioning + Parquet format) is the best practice.

---

### Q28: AWS Service Catalog
**Question:** A company wants to enable developers to provision pre-approved AWS resources (EC2, RDS, VPC configurations) without granting them full AWS account permissions. What service should be used?

**A)** AWS Systems Manager  
**B)** AWS CloudFormation with IAM policies  
**C)** AWS Service Catalog  
**D)** AWS Control Tower

**Answer:** C

**Explanation:** AWS Service Catalog allows administrators to create and manage catalogs of approved IT services (defined as CloudFormation templates). Developers can then provision these resources without needing deep AWS knowledge or broad IAM permissions. Service Catalog enforces governance and compliance while enabling self-service.

---

### Q29: Amazon Route 53 Health Checks and Failover
**Question:** A company runs a web application in us-east-1 (primary) and eu-west-1 (secondary). Users should be routed to us-east-1 unless it becomes unhealthy. What Route 53 configuration should be used?

**A)** Weighted routing policy with 100% weight to us-east-1  
**B)** Failover routing policy with us-east-1 as primary and eu-west-1 as secondary, with health checks  
**C)** Geolocation routing policy  
**D)** Latency-based routing policy

**Answer:** B

**Explanation:** Failover routing policy is designed for active-passive configurations. With health checks on the primary endpoint (us-east-1), Route 53 automatically fails over to the secondary (eu-west-1) when the primary becomes unhealthy. Weighted routing doesn't provide automatic failover. Geolocation routes based on user location, not health. Latency-based routes to the lowest latency endpoint.

---

### Q30: Amazon CloudWatch Logs Insights vs Athena
**Question:** A company needs to analyze application logs stored in CloudWatch Logs to troubleshoot issues and identify patterns. The logs contain JSON-formatted entries. What is the MOST efficient solution for ad-hoc queries?

**A)** Export logs to S3 and query with Athena  
**B)** Use CloudWatch Logs Insights  
**C)** Stream logs to Elasticsearch and use Kibana  
**D)** Export logs to RDS and use SQL queries

**Answer:** B

**Explanation:** CloudWatch Logs Insights is purpose-built for querying CloudWatch Logs with a powerful query language that supports JSON parsing. It's the simplest and most cost-effective solution for ad-hoc log analysis. Exporting to S3/Athena adds latency and complexity. Elasticsearch is expensive and overcomplicated for ad-hoc queries. RDS is not designed for log analytics.

---

## Key Exam Tips

### Important Service Comparisons:
- **S3 vs EBS vs EFS:** S3 (object storage), EBS (block storage, single instance), EFS (shared file storage)
- **SNS vs SQS vs EventBridge:** SNS (pub/sub), SQS (queue), EventBridge (event bus for integrations)
- **Aurora vs RDS:** Aurora (better performance, higher cost), RDS (standard databases)
- **Application Load Balancer vs Network Load Balancer:** ALB (Layer 7, HTTP/HTTPS), NLB (Layer 4, TCP/UDP, static IPs)
- **CloudWatch vs CloudTrail:** CloudWatch (performance monitoring), CloudTrail (API call logging)

### Cost Optimization Strategies:
1. Right-size EC2 instances
2. Use appropriate storage classes (S3 lifecycle policies)
3. Reserved Instances / Savings Plans for steady workloads
4. Spot Instances for fault-tolerant workloads
5. Delete unused resources (EBS volumes, snapshots, EIPs)
6. Use AWS Cost Explorer and Trusted Advisor

### High Availability Design Patterns:
1. Multi-AZ deployments
2. Auto Scaling groups
3. Multiple Availability Zones
4. Cross-Region replication
5. Route 53 health checks and failover

### Security Best Practices:
1. Principle of least privilege (IAM)
2. Enable MFA for privileged accounts
3. Encrypt data at rest and in transit
4. Use VPC endpoints for AWS service access
5. Enable CloudTrail logging
6. Regular security audits with AWS Security Hub

---

*Note: These questions reflect common patterns and concepts tested in SAA-C03. Always review the latest AWS documentation and practice with official AWS practice exams.*
