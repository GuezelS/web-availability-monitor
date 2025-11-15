"""
Analytics module for calculating uptime and performance metrics.
"""

from datetime import datetime, timedelta
from src.database import get_connection, close_connection


def calculate_uptime_percentage(hours=None, days=None, url=None):
    """
    Calculate uptime percentage for a time period.
    
    Args:
        hours (int): Calculate for last N hours
        days (int): Calculate for last N days
        url (str): Filter by specific URL (optional)
        
    Returns:
        float: Uptime percentage (0-100)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build query based on parameters
        query = "SELECT success FROM checks WHERE 1=1"
        params = []
        
        # Add time filter
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
            query += " AND timestamp >= ?"
            params.append(cutoff_str)
        elif days:
            cutoff = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
            query += " AND timestamp >= ?"
            params.append(cutoff_str)
        
        # Add URL filter
        if url:
            query += " AND url = ?"
            params.append(url)
        
        # Execute query
        cursor.execute(query, params)
        results = cursor.fetchall()
        close_connection(conn)
        
        # Calculate uptime
        if not results:
            return 0.0
        
        total_checks = len(results)
        successful_checks = sum(1 for row in results if row[0] == 1)
        
        uptime = (successful_checks / total_checks) * 100
        return round(uptime, 2)
        
    except Exception as e:
        print(f"❌ Error calculating uptime: {e}")
        if conn:
            close_connection(conn)
        return 0.0


def get_overall_uptime(url=None):
    """
    Get overall uptime percentage since monitoring started.
    
    Args:
        url (str): Filter by specific URL (optional)
        
    Returns:
        float: Overall uptime percentage
    """
    return calculate_uptime_percentage(url=url)


def get_uptime_last_24h(url=None):
    """
    Get uptime for last 24 hours.
    
    Args:
        url (str): Filter by specific URL (optional)
        
    Returns:
        float: Uptime percentage for last 24 hours
    """
    return calculate_uptime_percentage(hours=24, url=url)


def get_uptime_last_7d(url=None):
    """
    Get uptime for last 7 days.
    
    Args:
        url (str): Filter by specific URL (optional)
        
    Returns:
        float: Uptime percentage for last 7 days
    """
    return calculate_uptime_percentage(days=7, url=url)


def get_uptime_last_30d(url=None):
    """
    Get uptime for last 30 days.
    
    Args:
        url (str): Filter by specific URL (optional)
        
    Returns:
        float: Uptime percentage for last 30 days
    """
    return calculate_uptime_percentage(days=30, url=url)


def get_uptime_summary(url=None):
    """
    Get uptime summary for multiple time periods.
    
    Args:
        url (str): Filter by specific URL (optional)
        
    Returns:
        dict: Uptime percentages for different periods
    """
    return {
        'overall': get_overall_uptime(url),
        'last_24h': get_uptime_last_24h(url),
        'last_7d': get_uptime_last_7d(url),
        'last_30d': get_uptime_last_30d(url)
    }