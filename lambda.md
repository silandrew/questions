# AWS Lambda - Complete Guide

## What is AWS Lambda?

AWS Lambda is a **serverless compute service** that lets you run code without provisioning or managing servers. You pay only for the compute time you consume - there's no charge when your code isn't running.

### Key Concepts

- **Event-Driven**: Lambda functions are triggered by events from AWS services or custom applications
- **Automatic Scaling**: Automatically scales from a few requests per day to thousands per second
- **Pay-per-Use**: You're charged based on the number of requests and compute time
- **Stateless**: Each invocation is independent (use external storage for state)
- **Multiple Runtime Support**: Python, Node.js, Java, Go, Ruby, .NET, and custom runtimes

### Lambda Pricing Model

- **Requests**: $0.20 per 1 million requests
- **Duration**: Charged per GB-second of compute time
- **Free Tier**: 1 million free requests and 400,000 GB-seconds per month

---

## Common Use Cases & Scenarios

### 1. **Real-Time File Processing**
**Scenario**: Automatically process images uploaded to S3

**Example**: Image thumbnail generation

```python
import json
import boto3
from PIL import Image
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download the image
    download_path = '/tmp/{}'.format(key)
    s3_client.download_file(bucket, key, download_path)
    
    # Create thumbnail
    with Image.open(download_path) as image:
        image.thumbnail((200, 200))
        thumbnail_path = '/tmp/thumbnail-{}'.format(key)
        image.save(thumbnail_path)
    
    # Upload thumbnail
    thumbnail_key = 'thumbnails/{}'.format(key)
    s3_client.upload_file(thumbnail_path, bucket, thumbnail_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Thumbnail created: {thumbnail_key}')
    }
```

**Trigger Configuration**:
- **Event Source**: S3 bucket
- **Event Type**: `s3:ObjectCreated:*`
- **Prefix**: `uploads/`

---

### 2. **API Backend (REST API)**
**Scenario**: Build a serverless REST API with API Gateway + Lambda

**Example**: User management API

```python
import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    # Route handling
    if http_method == 'GET' and path == '/users':
        return get_users()
    elif http_method == 'GET' and path.startswith('/users/'):
        user_id = path.split('/')[-1]
        return get_user(user_id)
    elif http_method == 'POST' and path == '/users':
        return create_user(json.loads(event['body']))
    elif http_method == 'DELETE' and path.startswith('/users/'):
        user_id = path.split('/')[-1]
        return delete_user(user_id)
    else:
        return response(404, {'error': 'Not found'})

def get_users():
    try:
        result = table.scan()
        return response(200, result['Items'])
    except Exception as e:
        return response(500, {'error': str(e)})

def get_user(user_id):
    try:
        result = table.get_item(Key={'userId': user_id})
        if 'Item' in result:
            return response(200, result['Item'])
        return response(404, {'error': 'User not found'})
    except Exception as e:
        return response(500, {'error': str(e)})

def create_user(user_data):
    try:
        user_id = str(uuid.uuid4())
        item = {
            'userId': user_id,
            'name': user_data['name'],
            'email': user_data['email']
        }
        table.put_item(Item=item)
        return response(201, item)
    except Exception as e:
        return response(500, {'error': str(e)})

def delete_user(user_id):
    try:
        table.delete_item(Key={'userId': user_id})
        return response(200, {'message': 'User deleted'})
    except Exception as e:
        return response(500, {'error': str(e)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
```

**API Gateway Configuration**:
```yaml
Resources:
  - Path: /users
    Methods: [GET, POST]
  - Path: /users/{userId}
    Methods: [GET, DELETE]
```

---

### 3. **Scheduled Tasks (Cron Jobs)**
**Scenario**: Daily database cleanup or report generation

**Example**: Clean up expired sessions from DynamoDB

```python
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Sessions')

def lambda_handler(event, context):
    # Calculate expiration time (24 hours ago)
    expiration_time = int((datetime.now() - timedelta(hours=24)).timestamp())
    
    # Scan for expired sessions
    response = table.scan(
        FilterExpression='expirationTime < :exp_time',
        ExpressionAttributeValues={':exp_time': expiration_time}
    )
    
    deleted_count = 0
    # Delete expired sessions
    for item in response['Items']:
        table.delete_item(Key={'sessionId': item['sessionId']})
        deleted_count += 1
    
    print(f"Deleted {deleted_count} expired sessions")
    
    return {
        'statusCode': 200,
        'body': f"Cleaned up {deleted_count} expired sessions"
    }
```

**EventBridge Rule (CloudWatch Events)**:
```json
{
  "schedule": "cron(0 2 * * ? *)",
  "description": "Run daily at 2 AM UTC"
}
```

---

### 4. **Stream Processing**
**Scenario**: Process real-time data from Kinesis or DynamoDB Streams

**Example**: Process e-commerce order events

```python
import json
import boto3
import base64

sns_client = boto3.client('sns')
TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:OrderNotifications'

def lambda_handler(event, context):
    for record in event['Records']:
        # Decode Kinesis data
        payload = base64.b64decode(record['kinesis']['data'])
        order = json.loads(payload)
        
        # Process order
        process_order(order)
    
    return {'statusCode': 200, 'body': 'Processed {} records'.format(len(event['Records']))}

def process_order(order):
    order_id = order['orderId']
    customer_email = order['customerEmail']
    total_amount = order['totalAmount']
    
    # Business logic
    if total_amount > 1000:
        # Send notification for large orders
        message = f"Large order received: ${total_amount}"
        sns_client.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"Large Order Alert - {order_id}",
            Message=message
        )
    
    # Log order details
    print(f"Processed order {order_id} for {customer_email}")
```

---

### 5. **Chatbot Backend**
**Scenario**: Slack or Teams bot integration

**Example**: Slack command handler

```python
import json
import boto3
import os
from urllib.parse import parse_qs

def lambda_handler(event, context):
    # Parse Slack request
    body = parse_qs(event['body'])
    command = body['command'][0]
    text = body['text'][0] if 'text' in body else ''
    user_name = body['user_name'][0]
    
    # Handle different commands
    if command == '/weather':
        response_text = get_weather(text)
    elif command == '/joke':
        response_text = get_joke()
    elif command == '/status':
        response_text = get_system_status()
    else:
        response_text = "Unknown command"
    
    # Slack response format
    return {
        'statusCode': 200,
        'body': json.dumps({
            'response_type': 'in_channel',
            'text': response_text
        })
    }

def get_weather(location):
    # Integration with weather API
    return f"Weather in {location}: Sunny, 75°F"

def get_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!"
    ]
    import random
    return random.choice(jokes)

def get_system_status():
    # Check system health
    return "All systems operational ✅"
```

---

### 6. **ETL Pipeline**
**Scenario**: Extract, Transform, Load data processing

**Example**: Process CSV files and load into database

```python
import json
import boto3
import csv
from io import StringIO

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SalesData')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download CSV file
    csv_obj = s3_client.get_object(Bucket=bucket, Key=key)
    csv_content = csv_obj['Body'].read().decode('utf-8')
    
    # Parse CSV
    csv_reader = csv.DictReader(StringIO(csv_content))
    
    processed_count = 0
    with table.batch_writer() as batch:
        for row in csv_reader:
            # Transform data
            transformed_row = {
                'salesId': row['id'],
                'date': row['date'],
                'amount': float(row['amount']),
                'region': row['region'].upper(),
                'product': row['product']
            }
            
            # Load into DynamoDB
            batch.put_item(Item=transformed_row)
            processed_count += 1
    
    return {
        'statusCode': 200,
        'body': f'Processed {processed_count} records from {key}'
    }
```

---

### 7. **Authentication & Authorization**
**Scenario**: Custom authorizer for API Gateway

**Example**: JWT token validator

```python
import json
import jwt
import os

SECRET_KEY = os.environ['JWT_SECRET']

def lambda_handler(event, context):
    token = event['authorizationToken'].replace('Bearer ', '')
    method_arn = event['methodArn']
    
    try:
        # Verify JWT token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['sub']
        
        # Generate policy
        return generate_policy(user_id, 'Allow', method_arn)
    except jwt.ExpiredSignatureError:
        return generate_policy('user', 'Deny', method_arn)
    except jwt.InvalidTokenError:
        return generate_policy('user', 'Deny', method_arn)

def generate_policy(principal_id, effect, resource):
    auth_response = {
        'principalId': principal_id
    }
    
    if effect and resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
        auth_response['policyDocument'] = policy_document
    
    return auth_response
```

---

### 8. **Serverless Web Scraper**
**Scenario**: Periodic web scraping and data collection

**Example**: Monitor product prices

```python
import json
import boto3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductPrices')
sns_client = boto3.client('sns')

PRODUCTS = [
    {'name': 'iPhone 15', 'url': 'https://example.com/iphone15'},
    {'name': 'Galaxy S24', 'url': 'https://example.com/galaxy-s24'}
]

def lambda_handler(event, context):
    results = []
    
    for product in PRODUCTS:
        price = scrape_price(product['url'])
        
        # Store in database
        item = {
            'productName': product['name'],
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'url': product['url']
        }
        table.put_item(Item=item)
        
        # Check for price drop
        check_price_drop(product['name'], price)
        
        results.append(item)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }

def scrape_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find('span', class_='price')
    price = float(price_element.text.replace('$', '').replace(',', ''))
    return price

def check_price_drop(product_name, current_price):
    # Query last price
    response = table.query(
        KeyConditionExpression='productName = :name',
        ExpressionAttributeValues={':name': product_name},
        ScanIndexForward=False,
        Limit=2
    )
    
    if len(response['Items']) > 1:
        last_price = response['Items'][1]['price']
        if current_price < last_price * 0.9:  # 10% drop
            sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:123456789012:PriceAlerts',
                Subject=f'Price Drop Alert: {product_name}',
                Message=f'{product_name} price dropped from ${last_price} to ${current_price}'
            )
```

---

## Lambda Configuration Best Practices

### 1. **Environment Variables**
Store configuration outside code:

```python
import os

DATABASE_URL = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')
```

### 2. **Memory & Timeout Settings**
- **Memory**: 128 MB to 10,240 MB (more memory = more CPU)
- **Timeout**: Up to 15 minutes (900 seconds)
- **Tip**: Start with 512 MB and adjust based on CloudWatch metrics

### 3. **Cold Start Optimization**
```python
# Initialize outside handler (reused across invocations)
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def lambda_handler(event, context):
    # Handler code here
    pass
```

### 4. **Error Handling**
```python
import traceback

def lambda_handler(event, context):
    try:
        # Your code
        result = process_data(event)
        return {'statusCode': 200, 'body': json.dumps(result)}
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        return {'statusCode': 400, 'body': json.dumps({'error': str(e)})}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        return {'statusCode': 500, 'body': json.dumps({'error': 'Internal server error'})}
```

### 5. **Logging with Context**
```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Request ID: {context.request_id}")
    logger.info(f"Memory limit: {context.memory_limit_in_mb} MB")
    logger.info(f"Time remaining: {context.get_remaining_time_in_millis()} ms")
    
    # Your code here
```

---

## Lambda Layers

Share code and dependencies across multiple functions:

**Example Layer Structure**:
```
python/
  lib/
    python3.9/
      site-packages/
        requests/
        boto3/
```

**Using Layers**:
```python
# No need to include in deployment package
import requests
import custom_module  # From your custom layer

def lambda_handler(event, context):
    response = requests.get('https://api.example.com')
    return custom_module.process(response.json())
```

---

## Integration Patterns

### Lambda with SQS (Queue Processing)
```python
def lambda_handler(event, context):
    for record in event['Records']:
        message_body = record['body']
        message_id = record['messageId']
        
        try:
            process_message(message_body)
        except Exception as e:
            # Message will return to queue
            print(f"Failed to process {message_id}: {str(e)}")
            raise
    
    return {'statusCode': 200}
```

### Lambda with SNS (Pub/Sub)
```python
def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = record['Sns']['Message']
        subject = record['Sns']['Subject']
        
        print(f"Received: {subject}")
        process_notification(sns_message)
```

### Lambda with Step Functions (Orchestration)
```python
def lambda_handler(event, context):
    # Step 1: Validation
    if 'orderId' not in event:
        return {'status': 'ERROR', 'message': 'Missing orderId'}
    
    # Step 2: Processing
    result = process_order(event['orderId'])
    
    # Return data for next step
    return {
        'status': 'SUCCESS',
        'orderId': event['orderId'],
        'result': result
    }
```

---

## Monitoring & Debugging

### CloudWatch Metrics to Monitor:
- **Invocations**: Number of times function is invoked
- **Duration**: Execution time
- **Errors**: Number of errors
- **Throttles**: Number of throttled requests
- **ConcurrentExecutions**: Concurrent invocations

### X-Ray Tracing:
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    with xray_recorder.capture('process_order'):
        result = process_order(event)
    return result
```

---

## Deployment Methods

### 1. **AWS Console**: Manual upload
### 2. **AWS CLI**:
```bash
# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip
```

### 3. **SAM (Serverless Application Model)**:
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.9
      CodeUri: ./src
      Events:
        Api:
          Type: Api
          Properties:
            Path: /users
            Method: get
```

### 4. **Terraform**:
```hcl
resource "aws_lambda_function" "my_function" {
  filename      = "function.zip"
  function_name = "my-function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  
  environment {
    variables = {
      TABLE_NAME = "MyTable"
    }
  }
}
```

---

## Security Best Practices

1. **Use least privilege IAM roles**
2. **Store secrets in AWS Secrets Manager or Parameter Store**
3. **Enable VPC for database access**
4. **Use environment variables for configuration**
5. **Enable CloudTrail logging**
6. **Regularly update runtime versions**

---

## Common Pitfalls & Solutions

| Problem | Solution |
|---------|----------|
| Cold starts | Use provisioned concurrency, optimize package size |
| Timeout errors | Increase timeout, optimize code, use async processing |
| Memory errors | Increase memory allocation |
| Concurrent execution limits | Request limit increase, use throttling |
| Large deployment packages | Use Lambda Layers, remove unnecessary dependencies |
| Database connection issues | Use connection pooling, RDS Proxy |

---

## Conclusion

AWS Lambda is a powerful tool for building scalable, event-driven applications. The key is to:
- Keep functions small and focused (single responsibility)
- Optimize cold starts
- Monitor performance with CloudWatch
- Use appropriate memory/timeout settings
- Implement proper error handling and logging

Start small, test thoroughly, and scale as needed!
