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

def detect_outages(hours=24, url=None):
    """
    Detect outages (consecutive failed checks).
    
    Args:
        hours (int): Look back N hours (default 24)
        url (str): Filter by URL (optional)
        
    Returns:
        list: List of outage dictionaries
    """
    try:
        conn = get_connection()
        conn.row_factory = lambda cursor, row: {
            'id': row[0],
            'timestamp': row[1],
            'success': row[2]
        }
        cursor = conn.cursor()
        
        # Get checks for time period
        query = "SELECT id, timestamp, success FROM checks WHERE 1=1"
        params = []
        
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
            query += " AND timestamp >= ?"
            params.append(cutoff_str)
        
        if url:
            query += " AND url = ?"
            params.append(url)
        
        query += " ORDER BY timestamp ASC"
        
        cursor.execute(query, params)
        checks = cursor.fetchall()
        close_connection(conn)
        
        # Detect outages
        outages = []
        current_outage = None
        
        for check in checks:
            if check['success'] == 0:  # Failed check
                if current_outage is None:
                    # Start new outage
                    current_outage = {
                        'start': check['timestamp'],
                        'end': check['timestamp'],
                        'checks_failed': 1
                    }
                else:
                    # Continue current outage
                    current_outage['end'] = check['timestamp']
                    current_outage['checks_failed'] += 1
            else:  # Successful check
                if current_outage is not None:
                    # End current outage
                    current_outage['duration_minutes'] = calculate_duration_minutes(
                        current_outage['start'],
                        current_outage['end']
                    )
                    outages.append(current_outage)
                    current_outage = None
        
        # Handle ongoing outage
        if current_outage is not None:
            current_outage['duration_minutes'] = calculate_duration_minutes(
                current_outage['start'],
                current_outage['end']
            )
            current_outage['ongoing'] = True
            outages.append(current_outage)
        
        return outages
        
    except Exception as e:
        print(f"❌ Error detecting outages: {e}")
        if conn:
            close_connection(conn)
        return []


def calculate_duration_minutes(start_str, end_str):
    """
    Calculate duration between two timestamps in minutes.
    
    Args:
        start_str (str): Start timestamp
        end_str (str): End timestamp
        
    Returns:
        int: Duration in minutes
    """
    try:
        start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0


def get_outage_summary(hours=24, url=None):
    """
    Get summary of outages.
    
    Args:
        hours (int): Look back N hours
        url (str): Filter by URL (optional)
        
    Returns:
        dict: Outage statistics
    """
    outages = detect_outages(hours=hours, url=url)
    
    if not outages:
        return {
            'total_outages': 0,
            'total_downtime_minutes': 0,
            'longest_outage_minutes': 0,
            'outages': []
        }
    
    total_downtime = sum(o['duration_minutes'] for o in outages)
    longest_outage = max(o['duration_minutes'] for o in outages)
    
    return {
        'total_outages': len(outages),
        'total_downtime_minutes': total_downtime,
        'longest_outage_minutes': longest_outage,
        'outages': outages
    }

def get_performance_stats(hours=None, days=None, url=None):
    """
    Get performance statistics for response times.
    Separates count queries from response time statistics to handle failed checks properly.
    
    Args:
        hours (int): Last N hours (optional)
        days (int): Last N days (optional)
        url (str): Filter by URL (optional)
        
    Returns:
        dict: Performance statistics including:
            - total_checks (int): Total number of checks (successful + failed)
            - successful_checks (int): Number of successful checks
            - failed_checks (int): Number of failed checks
            - avg_response_time (float): Average response time in seconds (from successful checks only)
            - min_response_time (float): Minimum response time in seconds (from successful checks only)
            - max_response_time (float): Maximum response time in seconds (from successful checks only)
            - median_response_time (float): Median response time in seconds (from successful checks only)
            
    Note:
        Response time statistics (avg, min, max, median) are calculated only from successful checks
        where response_time is not NULL. Failed checks are counted in failed_checks but do not
        contribute to response time calculations.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build time and URL filters
        time_filter = ""
        params = []
        
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
            time_filter = " AND timestamp >= ?"
            params.append(cutoff_str)
        elif days:
            cutoff = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
            time_filter = " AND timestamp >= ?"
            params.append(cutoff_str)
        
        url_filter = ""
        if url:
            url_filter = " AND url = ?"
            params.append(url)
        
        # Query 1: Get total, successful, and failed counts (ALL checks)
        count_query = f"""
            SELECT 
                COUNT(*) as total_checks,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_checks,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_checks
            FROM checks
            WHERE 1=1{time_filter}{url_filter}
        """
        cursor.execute(count_query, params)
        count_result = cursor.fetchone()
        
        # Handle None result from count query
        if not count_result:
            total_checks = 0
            successful_checks = 0
            failed_checks = 0
        else:
            total_checks = count_result[0] or 0
            successful_checks = count_result[1] or 0
            failed_checks = count_result[2] or 0
        
        # Query 2: Get response time stats (ONLY successful checks)
        stats_query = f"""
            SELECT 
                AVG(response_time) as avg_response_time,
                MIN(response_time) as min_response_time,
                MAX(response_time) as max_response_time
            FROM checks
            WHERE success = 1 AND response_time IS NOT NULL{time_filter}{url_filter}
        """
        cursor.execute(stats_query, params)
        stats_result = cursor.fetchone()
        
        # Handle None result from stats query
        if not stats_result:
            avg = 0.0
            min_time = 0.0
            max_time = 0.0
        else:
            avg = stats_result[0] if stats_result[0] is not None else 0.0
            min_time = stats_result[1] if stats_result[1] is not None else 0.0
            max_time = stats_result[2] if stats_result[2] is not None else 0.0
        
        # Query 3: Get median (ONLY successful checks)
        median_query = f"""
            SELECT response_time FROM checks 
            WHERE success = 1 AND response_time IS NOT NULL{time_filter}{url_filter}
            ORDER BY response_time
        """
        cursor.execute(median_query, params)
        response_times = [row[0] for row in cursor.fetchall() if row and row[0] is not None]
        
        close_connection(conn)
        
        # Calculate median
        median = 0.0
        if response_times:
            n = len(response_times)
            if n % 2 == 0:
                median = (response_times[n//2 - 1] + response_times[n//2]) / 2
            else:
                median = response_times[n//2]
        
        return {
            'total_checks': total_checks,
            'successful_checks': successful_checks,
            'failed_checks': failed_checks,
            'avg_response_time': round(avg, 3),
            'min_response_time': round(min_time, 3),
            'max_response_time': round(max_time, 3),
            'median_response_time': round(median, 3)
        }
        
    except Exception as e:
        print(f"❌ Error getting performance stats: {e}")
        if conn:
            close_connection(conn)
        return {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'avg_response_time': 0.0,
            'min_response_time': 0.0,
            'max_response_time': 0.0,
            'median_response_time': 0.0
        }
        
    except Exception as e:
        print(f"❌ Error getting performance stats: {e}")
        if conn:
            close_connection(conn)
        return {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'avg_response_time': 0.0,
            'min_response_time': 0.0,
            'max_response_time': 0.0,
            'median_response_time': 0.0
        }
        

def get_complete_report(hours=24, url=None):
    """
    Get comprehensive monitoring report.
    Combines uptime, outages, and performance stats.
    
    Args:
        hours (int): Time period in hours
        url (str): Filter by URL (optional)
        
    Returns:
        dict: Complete monitoring report
    """
    return {
        'uptime': get_uptime_summary(url=url),
        'outages': get_outage_summary(hours=hours, url=url),
        'performance': get_performance_stats(hours=hours, url=url),
        'report_period_hours': hours,
        'report_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }