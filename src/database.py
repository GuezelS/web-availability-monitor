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