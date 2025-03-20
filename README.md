# AWS Lambda Function for Invoking Anthropic Claude 3.5 Sonnet

This README provides a guide on using an AWS Lambda function to invoke the Anthropic Claude 3.5 Sonnet model using AWS Bedrock Runtime, setting up the necessary IAM role with the appropriate permissions, configuring an API Gateway to manage the requests, and invoking the deployed API using different programming languages.

## Benefits of Using Lambda to Invoke Bedrock Model

Using AWS Lambda to invoke the Bedrock model offers several advantages:

- **Scalability**: Automatically scales based on the request volume without needing to manage the underlying server resources.
- **Cost-Effective**: You pay only for the compute time you consume, making it cost-effective for applications with varying usage patterns.
- **Performance**: Reduces latency by executing requests closer to the data source and end-users, utilizing AWS's optimized networking and global presence.
- **Integration**: Easily integrates with other AWS services such as Amazon API Gateway and AWS IAM, providing a robust and secure environment for deploying applications.
- **Serverless**: Eliminates the need to manage servers, thereby simplifying deployment and management of applications that need to process complex requests like those made to Bedrock Runtime.

## Lambda Function Code

The Lambda function is written in Python and is designed to handle both text-based and image-based inputs for processing with the Anthropic Claude 3.5 Sonnet model.

```python
# Import necessary libraries
import json
import botocore.session

# Initialize AWS Bedrock Runtime client using botocore
session = botocore.session.get_session()
bedrock_runtime = session.create_client("bedrock-runtime", region_name="us-east-1")

# Specify the Model ID
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

def lambda_handler(event, context):
    # Process incoming requests and handle them accordingly
    # Detailed implementation as provided above
    pass
```

## Setting Up IAM Role with Inline Policy

To allow the Lambda function to invoke the Bedrock model, you must configure an IAM role with appropriate permissions. Here is an example of an inline policy that grants full access to the Bedrock Runtime:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock-runtime:*",
            "Resource": "*"
        }
    ]
}
```

Name this policy `BedrockFullAccess` and attach it to the IAM role assigned to your Lambda function.

## Configuring API Gateway

To set up an API Gateway to handle requests to your Lambda function:

1. **Create a New API**:
   - Go to the API Gateway console and select **Create API**.
   - Choose **REST API** and follow the prompts to create a new REST API.

2. **Define New Resource and Methods**:
   - Create a new resource under your API, typically using '/' as the root.
   - Add a POST method to this resource and connect it to your Lambda function.

3. **Deploy the API**:
   - Create a new stage, e.g., `prod`, and deploy your API to this stage.
   - Note the Invoke URL provided after deployment.

4. **Test Your API**:
   - Use tools like `curl`, Postman, or any HTTP client to make requests to the deployed API endpoint.

## Invoking the API

Here are examples of how to invoke the API using different programming languages and tools:

### Curl

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Enter your text or base64 image data here"}'
```

### Python

```python
import requests

url = "https://your-api-id.execute-api.region.amazonaws.com/prod"
payload = {"prompt": "Enter your text or base64 image data here"}
response = requests.post(url, json=payload)
print(response.text)
```

### Node.js

```javascript
const axios = require('axios');

const url = "https://your-api-id.execute-api.region.amazonaws.com/prod";
const data = {
  prompt: "Enter your text or base64 image data here"
};

axios.post(url, data)
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

### TypeScript

```typescript
import axios from 'axios';

const url: string = "https://your-api-id.execute-api.region.amazonaws.com/prod";
const data: { prompt: string } = { prompt: "Enter your text or base64 image data here" };

axios.post(url, data)
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

## Conclusion

By following this guide, you can effectively set up a serverless application to invoke complex AI models hosted on AWS Bedrock using Lambda and manage requests through API Gateway, all within a secure and scalable environment.
