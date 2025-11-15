"""
Scheduler module for automated website monitoring.
Runs checks at regular intervals.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import os
from dotenv import load_dotenv

from src.monitor import check_website
from src.database import init_database, save_check
from src.logger import setup_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger()

# Global scheduler instance
scheduler = None

def check_and_save():
    """
    Check website and save result to database.
    This function is called by the scheduler.
    """
    try:
        # Get URL from environment
        url = os.getenv('MONITOR_URL', 'https://example.com')
        timeout = int(os.getenv('TIMEOUT', 5))
        
        # Check website
        result = check_website(url, timeout=timeout)
        
        # Save to database
        row_id = save_check(result)
        
        if row_id:
            logger.info(f"💾 Saved check result to database (ID: {row_id})")
        
    except Exception as e:
        logger.error(f"❌ Error in scheduled check: {e}")


def start_monitoring():
    """
    Start the monitoring scheduler.
    Checks website at regular intervals.
    """
    global scheduler
    
    # Initialize database
    init_database()
    
    # Get configuration
    url = os.getenv('MONITOR_URL', 'https://example.com')
    interval = int(os.getenv('CHECK_INTERVAL', 30))
    
    logger.info(f"🏁 Starting monitoring for {url}")
    logger.info(f"⏳ Checking every {interval} seconds")
    
    # Create scheduler
    scheduler = BackgroundScheduler()
    
    # Add job
    scheduler.add_job(
        check_and_save,
        trigger=IntervalTrigger(seconds=interval),
        id='website_check',
        name='Website availability check',
        replace_existing=True
    )
    
    # Start scheduler
    scheduler.start()
    logger.info("✅ Scheduler started")
    
    # Run first check immediately
    check_and_save()


def stop_monitoring():
    """
    Stop the monitoring scheduler.
    """
    global scheduler
    
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("🛑 Scheduler stopped")
    else:
        logger.info("⚠️  Scheduler is not running")


def is_running():
    """
    Check if scheduler is running.
    
    Returns:
        bool: True if running, False otherwise
    """
    global scheduler
    return scheduler is not None and scheduler.running