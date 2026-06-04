import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID")
AWS_PROFILE = os.getenv("AWS_PROFILE")

DEFAULT_TEMPERATURE = 0.3
DEFAULT_TOP_P = 0.9