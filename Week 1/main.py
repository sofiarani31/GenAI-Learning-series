# pip install boto3
# pip install python-dotenv

import json
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION", "ap-southeast-2"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

response = client.invoke_model(
    modelId=os.getenv("BEDROCK_MODEL_ID", "nvidia.nemotron-nano-3-30b"),
    contentType="application/json",
    accept="application/json",
    body=json.dumps(
        {
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
            "max_tokens": 512,
            "temperature": 0.5,
            "top_p": 0.9,
        }
    ),
)

print("--------------------------------")
print(response)
print("--------------------------------")
#print(response["body"].read())
print(json.loads(response["body"].read())["choices"][0]["message"]["content"])
