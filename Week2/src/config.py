import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

MAX_CONCURRENT_REQUESTS = int(
    os.getenv("MAX_CONCURRENT_REQUESTS", 3)
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", 3)
)