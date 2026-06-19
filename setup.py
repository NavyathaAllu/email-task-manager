#!/usr/bin/env python3
"""
Setup instructions for Email to Notion Task Manager.

Provides step-by-step guidance for initial configuration.
"""

import os
import sys
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)

def check_dependencies():
    """
    Check if all required dependencies are installed.
    """
    logger.info("Checking dependencies...")
    
    required_packages = [
        'google',
        'notion_client',
        'dotenv',
        'dateutil',
        'schedule'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"  ✓ {package}")
        except ImportError:
            logger.warning(f"  ✗ {package}")
            missing.append(package)
    
    if missing:
        logger.error(f"Missing packages: {', '.join(missing)}")
        logger.error("Run: pip install -r requirements.txt")
        return False
    
    logger.info("All dependencies installed!\n")
    return True

def check_configuration():
    """
    Check if configuration files exist.
    """
    logger.info("Checking configuration files...")
    
    files_to_check = [
        '.env',
        'config.json'
    ]
    
    missing = []
    for file in files_to_check:
        if os.path.exists(file):
            logger.info(f"  ✓ {file}")
        else:
            logger.warning(f"  ✗ {file}")
            missing.append(file)
    
    if missing:
        logger.warning(f"Missing configuration files: {', '.join(missing)}")
        logger.warning("See .env.example and config.json for templates")
        return False
    
    logger.info("Configuration files found!\n")
    return True

def create_directories():
    """
    Create necessary directories.
    """
    logger.info("Creating necessary directories...")
    
    directories = ['logs', 'cache', 'data']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"  ✓ {directory}/")
    
    logger.info("Directories created!\n")

def setup_instructions():
    """
    Print setup instructions.
    """
    print("\n" + "="*60)
    print("EMAIL TO NOTION TASK MANAGER - SETUP GUIDE")
    print("="*60 + "\n")
    
    print("STEP 1: Install Dependencies")
    print("-" * 60)
    print("pip install -r requirements.txt\n")
    
    print("STEP 2: Configure Gmail")
    print("-" * 60)
    print("1. Enable 2-Step Verification: https://myaccount.google.com/security")
    print("2. Generate App Password: https://myaccount.google.com/apppasswords")
    print("3. Save your email and app password\n")
    
    print("STEP 3: Configure Notion")
    print("-" * 60)
    print("1. Create/Find your Notion database")
    print("2. Create a Notion Integration: https://www.notion.so/my-integrations")
    print("3. Get your NOTION_API_KEY")
    print("4. Share database with the integration")
    print("5. Get NOTION_DATABASE_ID from the database URL\n")
    
    print("STEP 4: Environment Configuration")
    print("-" * 60)
    print("1. Copy .env.example to .env")
    print("   cp .env.example .env")
    print("2. Edit .env and add your credentials:")
    print("   GMAIL_EMAIL=your-email@gmail.com")
    print("   GMAIL_APP_PASSWORD=your-app-password")
    print("   NOTION_API_KEY=your-notion-api-key")
    print("   NOTION_DATABASE_ID=your-database-id\n")
    
    print("STEP 5: Test the Agent")
    print("-" * 60)
    print("Run once to test:")
    print("   python main.py\n")
    
    print("STEP 6: Schedule Periodic Checks")
    print("-" * 60)
    print("Option A - Run Scheduler (keeps running in background):")
    print("   python scheduler.py\n")
    print("Option B - Use Cron (Linux/Mac):")
    print("   crontab -e")
    print("   # Add line to check every hour:")
    print("   0 * * * * cd /path/to/email-task-manager && python main.py\n")
    print("Option C - Use Task Scheduler (Windows):")
    print("   1. Open Task Scheduler")
    print("   2. Create Basic Task")
    print("   3. Set trigger and action to run: python main.py\n")
    
    print("="*60)
    print("Setup complete! You're ready to go!")
    print("="*60 + "\n")

if __name__ == "__main__":
    create_directories()
    check_dependencies()
    check_configuration()
    setup_instructions()
