import os
import boto3
from otenv import load_dotenv
import json
load_dotenv()

aws_region = os.getenv("AWS_REGION")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_bearer_token_bedrock = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
model_id = os.getenv("BEDROCK_MODEL_ID")
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)




#call the bedrock client 
response = bedrock_client.invoke_model(
    modelId=model_id,
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9,
    }),
)

# Parse the response
result = json.loads(response["body"].read())
model_reply = result["choices"][0]["message"]["content"]
print(model_reply)
