#!/usr/bin/env python3
"""
Scheduler for Email to Notion Task Manager.

Runs the main task at regular intervals.
"""

import schedule
import time
import os
from dotenv import load_dotenv
from main import main
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

def scheduled_task():
    """
    Wrapper function for scheduled task execution.
    """
    logger.info("Starting scheduled task execution...")
    try:
        main()
    except Exception as e:
        logger.error(f"Scheduled task failed: {str(e)}", exc_info=True)
    logger.info("Scheduled task execution completed.\n")

def start_scheduler(check_interval_hours: int = 1):
    """
    Start the scheduler.
    
    Args:
        check_interval_hours: How often to check emails (in hours)
    """
    logger.info(f"Starting scheduler with {check_interval_hours} hour interval...")
    
    # Schedule the task
    schedule.every(check_interval_hours).hours.do(scheduled_task)
    
    logger.info(f"Scheduler started. Will check emails every {check_interval_hours} hour(s)")
    logger.info("Press Ctrl+C to stop.\n")
    
    # Keep scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute if a scheduled task is pending
    except KeyboardInterrupt:
        logger.info("\nScheduler stopped by user.")

if __name__ == "__main__":
    check_interval = int(os.getenv('CHECK_INTERVAL_HOURS', 1))
    start_scheduler(check_interval)
