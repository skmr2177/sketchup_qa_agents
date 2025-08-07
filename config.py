import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_CONFIG = {
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "region_name": os.getenv("AWS_DEFAULT_REGION", "us-east-1")
}

# Bedrock Configuration
BEDROCK_CONFIG = {
    "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
    "max_tokens": 8000,
    "temperature": 0.4
}

# Batch Processing Configuration
BATCH_CONFIG = {
    "batch_size": 3,
    "rate_limit_delay": 2,  # seconds between API calls
    "max_retries": 3,
    "parallel_processing": False,  # Set True for parallel batches
    "max_workers": 2
}