"""
Logging configuration with colored output.
"""

import logging
import colorlog


def setup_logger():
    """
    Configure colored logging for the application.
    
    Returns:
        logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('monitor')
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler()
    
    # Create colored formatter
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(levelname)s]%(reset)s %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger