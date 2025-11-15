"""
Website availability monitoring module.
Checks if websites are up or down.
"""

import requests
from datetime import datetime


def check_website(url, timeout=5):
    """
    Check if a website is available.
    
    Args:
        url (str): Website URL to check
        timeout (int): Max seconds to wait for response
        
    Returns:
        dict: Check result with keys:
            - url: The URL checked
            - status_code: HTTP status (200, 404, etc.)
            - response_time: Time in seconds
            - success: True if up, False if down
            - timestamp: When check happened
            - error: Error message or None
    """
    try:
        # Record start time
        start_time = datetime.now()
        
        # Make HTTP request
        response = requests.get(url, timeout=timeout)
        
        # Record end time
        end_time = datetime.now()
        
        # Calculate duration
        response_time = (end_time - start_time).total_seconds()
        
        # Return success result
        return {
            'url': url,
            'status_code': response.status_code,
            'response_time': response_time,
            'success': response.ok,
            'timestamp': datetime.now(),
            'error': None
        }
        
    except requests.Timeout:
        # Website took too long
        return {
            'url': url,
            'status_code': None,
            'response_time': None,
            'success': False,
            'timestamp': datetime.now(),
            'error': f'Timeout - Website took longer than {timeout} seconds'
        }
        
    except requests.ConnectionError:
        # Cannot connect to website
        return {
            'url': url,
            'status_code': None,
            'response_time': None,
            'success': False,
            'timestamp': datetime.now(),
            'error': 'Connection failed - Cannot reach website'
        }
        
    except Exception as e:
        # Unexpected error
        return {
            'url': url,
            'status_code': None,
            'response_time': None,
            'success': False,
            'timestamp': datetime.now(),
            'error': f'Unexpected error: {str(e)}'
        }