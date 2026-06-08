import asyncio
import logging
from botocore.exceptions import ClientError
from src.config import MAX_RETRIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_with_retry(semaphore: asyncio.Semaphore, coroutine_func, *args, **kwargs):
    """
    Executes a coroutine with a semaphore for concurrency control 
    and an exponential backoff retry mechanism for API throttling.
    """
    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                return await coroutine_func(*args, **kwargs)
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', '')
                if error_code in ['ThrottlingException', 'TooManyRequestsException']:
                    if attempt < MAX_RETRIES - 1:
                        sleep_time = 2 ** attempt  # 1s, 2s, 4s...
                        logger.warning(f"Rate limited by AWS. Retrying in {sleep_time} seconds (Attempt {attempt + 1}/{MAX_RETRIES})")
                        await asyncio.sleep(sleep_time)
                        continue
                # If it's not a throttling exception, or we ran out of retries, raise it
                logger.error(f"API Error after {attempt + 1} attempts: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
