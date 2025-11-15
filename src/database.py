"""
Database module for storing website check results.
"""

import sqlite3
import os
from datetime import datetime


# Database file path
DB_PATH = 'data/monitoring.db'


def init_database():
    """
    Initialize database and create tables if they don't exist.
    """
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Connect to database (creates file if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create checks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            success INTEGER NOT NULL,
            error TEXT,
            retries INTEGER DEFAULT 0
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_url_timestamp 
        ON checks(url, timestamp)
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized at {DB_PATH}")


def get_connection():
    """
    Get database connection.
    
    Returns:
        sqlite3.Connection: Database connection
    """
    return sqlite3.connect(DB_PATH)


def close_connection(conn):
    """
    Close database connection.
    
    Args:
        conn: Database connection to close
    """
    if conn:
        conn.close()


def save_check(check_result):
    """
    Save a check result to the database.
    
    Args:
        check_result (dict): Check result from check_website()
            Expected keys: url, timestamp, status_code, response_time,
                          success, error, retries
    
    Returns:
        int: ID of inserted row, or None if failed
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Convert timestamp to string if datetime object
        timestamp = check_result['timestamp']
        if isinstance(timestamp, datetime):
            timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert success boolean to integer (SQLite stores as 0/1)
        success = 1 if check_result['success'] else 0
        
        # Insert check result
        cursor.execute('''
            INSERT INTO checks (
                url, timestamp, status_code, response_time,
                success, error, retries
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            check_result['url'],
            timestamp,
            check_result.get('status_code'),
            check_result.get('response_time'),
            success,
            check_result.get('error'),
            check_result.get('retries', 0)
        ))
        
        conn.commit()
        row_id = cursor.lastrowid
        close_connection(conn)
        
        return row_id
        
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        if conn:
            close_connection(conn)
        return None        