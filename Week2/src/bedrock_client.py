import json
import boto3
import asyncio
from botocore.exceptions import ClientError
from src.config import AWS_REGION, BEDROCK_MODEL_ID

# Initialize the Bedrock Runtime client
# boto3 will automatically pick up AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from environment variables
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=AWS_REGION
)

async def extract_data_with_bedrock(prompt_text: str) -> str:
    """
    Sends the prompt to AWS Bedrock asynchronously and returns the raw response string.
    We use the Converse API as it standardizes inputs across different model providers.
    """
    def _make_api_call():
        try:
            response = bedrock_runtime.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt_text}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": 2048,
                    "temperature": 0.0, # We want deterministic, factual extraction
                    "topP": 0.9,
                }
            )
            # Extract the generated text from the response
            return response['output']['message']['content'][0]['text']
        except ClientError as e:
            print(f"AWS Bedrock API Error: {e}")
            raise

    # Since boto3 is synchronous, we run the API call in an asyncio thread
    # so it doesn't block other tasks when we process multiple records.
    return await asyncio.to_thread(_make_api_call)
