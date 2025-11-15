"""
Website availability monitoring module.
Checks if websites are up or down.
"""

import requests
from datetime import datetime
import time
from src.logger import setup_logger

# Initialize logger
logger = setup_logger()

def check_website(url, timeout=5, max_retries=3):
    """
    Check if a website is available.
    
    Args:
        url (str): Website URL to check
        timeout (int): Max seconds to wait for response
        max_retries (int): Number of retry attempts if failed

    Returns:
        dict: Check result with keys:
            - url: The URL checked
            - status_code: HTTP status (200, 404, etc.)
            - response_time: Time in seconds
            - success: True if up, False if down
            - timestamp: When check happened
            - error: Error message or None
            - retries: Number of retries needed
    """
    last_error = None

    logger.info(f"Checking {url}...")

    # Try multiple times
    for attempt in range(max_retries):
        try:
            # Record start time
            start_time = datetime.now()
            
            # Make HTTP request
            response = requests.get(url, timeout=timeout)
            
            # Record end time
            end_time = datetime.now()
            
            # Calculate duration
            response_time = (end_time - start_time).total_seconds()
            
            # Log success
            logger.info(f"✅ {url} is UP - {response.status_code} ({response_time:.3f}s)")

            # Return success result
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'success': response.ok,
                'timestamp': datetime.now(),
                'error': None,
                'retries': attempt
            }
        
        except requests.Timeout:
            last_error = f'Timeout - Website took longer than {timeout} seconds'
            logger.warning(f"⏱️  Attempt {attempt + 1} timed out")
        except requests.ConnectionError:
            last_error = 'Connection failed - Cannot reach website'
            logger.warning(f"🌐 Attempt {attempt + 1} connection failed")
        except Exception as e:
            last_error = f'Unexpected error: {str(e)}'
            logger.warning(f"⚠️  Attempt {attempt + 1} error: {e}")
        # If not last attempt, wait before retry
        if attempt < max_retries - 1:
            time.sleep(1)  # Wait 1 second before retry

    logger.error(f"❌ {url} is DOWN - {last_error}")
    
    # All retries failed - return failure
    return {
        'url': url,
        'status_code': None,
        'response_time': None,
        'success': False,
        'timestamp': datetime.now(),
        'error': last_error,
        'retries': max_retries
    }