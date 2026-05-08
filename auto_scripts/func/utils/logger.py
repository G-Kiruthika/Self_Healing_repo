"""Logging utility for test framework."""

import logging
import yaml
from pathlib import Path
from datetime import datetime


def setup_logger(name=__name__):
    """Set up and return a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    # Load config
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    logging_config = config.get('logging', {})
    log_level = logging_config.get('level', 'INFO')
    log_file = logging_config.get('log_file', 'logs/test_execution.log')
    
    # Create logs directory if it doesn't exist
    log_path = Path(__file__).parent.parent / log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
