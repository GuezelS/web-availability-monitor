"""
Main entry point for the website monitoring tool.
Run this script to start continuous monitoring.
"""

import time
import signal
import sys
from src.scheduler import start_monitoring, stop_monitoring
from src.logger import setup_logger

# Initialize logger
logger = setup_logger()

# Flag for graceful shutdown
running = True


def signal_handler(sig, frame):
    """
    Handle Ctrl+C gracefully.
    """
    global running
    logger.info("\n🛑 Shutdown signal received...")
    running = False
    stop_monitoring()
    logger.info("👋 Monitoring stopped. Goodbye!")
    sys.exit(0)


def main():
    """
    Main function to start monitoring.
    """
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("=" * 50)
    logger.info("🌐 Website Availability Monitor")
    logger.info("=" * 50)
    logger.info("")
    
    # Start monitoring
    start_monitoring()
    
    logger.info("")
    logger.info("📊 Monitoring is now running...")
    logger.info("⌨️  Press Ctrl+C to stop")
    logger.info("")
    
    # Keep running until interrupted
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 Keyboard interrupt received...")
        stop_monitoring()
        logger.info("👋 Monitoring stopped. Goodbye!")


if __name__ == '__main__':
    main()