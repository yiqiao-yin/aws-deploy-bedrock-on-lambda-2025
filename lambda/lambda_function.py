import json
import botocore.session

# Initialize AWS Bedrock Runtime client using botocore
session = botocore.session.get_session()
bedrock_runtime = session.create_client("bedrock-runtime", region_name="us-east-1")

# Model ID for Anthropic Claude 3.5 Sonnet
MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

def lambda_handler(event, context):
    """
    AWS Lambda function to invoke Anthropic Claude 3.5 Sonnet model.
    Supports both text-based and image-based inputs.
    """

    try:
        # DEBUG: Print event to check incoming request
        print("Received event:", json.dumps(event, indent=2))

        # Handle missing payload
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing request body."})
            }

        # Extract request body (handling API Gateway string-wrapped JSON)
        try:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON format."})
            }

        # Extract input parameters
        prompt = body.get("prompt")
        image_data = body.get("image")  # Base64-encoded image (if provided)
        max_tokens = body.get("max_tokens", 2000)
        temperature = body.get("temperature", 1)
        top_k = body.get("top_k", 250)
        top_p = body.get("top_p", 0.999)

        # Construct message list based on input type
        messages = []

        if image_data:
            # Properly format the image payload for Claude 3.5 Sonnet
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "data": image_data,  # Bedrock expects base64 data as-is, no decoding
                            "media_type": "image/jpeg"  # Adjust based on actual image type
                        }
                    },
                    {
                        "type": "text",
                        "text": "Read the text in the image and summarize it."
                    }
                ]
            })
        elif prompt:
            # If no image, process as text-only
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            })
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Either 'prompt' or 'image' must be provided."})
            }

        # Construct the Bedrock API request body
        model_body = json.dumps({
            "messages": messages,
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "stop_sequences": []
        })

        kwargs = {
            "modelId": MODEL_ID,
            "contentType": "application/json",
            "accept": "application/json",
            "body": model_body
        }

        try:
            # Invoke the Bedrock model
            response = bedrock_runtime.invoke_model(**kwargs)
            response_json = json.loads(response["body"].read().decode("utf-8"))

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Bedrock Model Response",
                    "parameters_used": {
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p
                    },
                    "model_response": response_json
                }, indent=2)
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Model invocation failed", "details": str(e)})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Unexpected error", "details": str(e)})
        }