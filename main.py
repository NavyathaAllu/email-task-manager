#!/usr/bin/env python3
"""
Main entry point for Email to Notion Task Manager.

This script connects to Gmail, extracts tasks from emails,
and creates them in a Notion database.
"""

import os
import sys
from dotenv import load_dotenv

from agents.gmail_agent import GmailAgent
from agents.task_extractor import TaskExtractor
from agents.notion_agent import NotionAgent
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

def main():
    """
    Main function to run the email to Notion task manager.
    """
    logger.info("Starting Email to Notion Task Manager...")
    
    # Load credentials from environment
    gmail_email = os.getenv('GMAIL_EMAIL')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    notion_api_key = os.getenv('NOTION_API_KEY')
    notion_database_id = os.getenv('NOTION_DATABASE_ID')
    email_check_limit = int(os.getenv('EMAIL_CHECK_LIMIT', 10))
    
    # Validate credentials
    if not all([gmail_email, gmail_app_password, notion_api_key, notion_database_id]):
        logger.error("Missing required environment variables. Please check .env file.")
        logger.error(f"Gmail Email: {'✓' if gmail_email else '✗'}")
        logger.error(f"Gmail App Password: {'✓' if gmail_app_password else '✗'}")
        logger.error(f"Notion API Key: {'✓' if notion_api_key else '✗'}")
        logger.error(f"Notion Database ID: {'✓' if notion_database_id else '✗'}")
        sys.exit(1)
    
    try:
        # Initialize agents
        logger.info("Initializing Gmail Agent...")
        gmail_agent = GmailAgent(gmail_email, gmail_app_password)
        
        logger.info("Initializing Task Extractor...")
        task_extractor = TaskExtractor('config.json')
        
        logger.info("Initializing Notion Agent...")
        notion_agent = NotionAgent(notion_api_key, notion_database_id)
        
        # Get unread emails
        logger.info(f"Retrieving up to {email_check_limit} unread emails...")
        emails = gmail_agent.get_unread_emails(limit=email_check_limit)
        
        if not emails:
            logger.info("No unread emails found.")
            return
        
        logger.info(f"Found {len(emails)} unread emails")
        
        # Extract tasks from emails
        all_tasks = []
        for email in emails:
            logger.info(f"Processing email: {email['subject']}")
            tasks = task_extractor.extract_from_email(email)
            
            # Validate tasks
            valid_tasks = [t for t in tasks if task_extractor.validate_task(t)]
            all_tasks.extend(valid_tasks)
            
            logger.info(f"  → Extracted {len(valid_tasks)} valid tasks")
        
        if not all_tasks:
            logger.info("No valid tasks extracted from emails.")
            return
        
        logger.info(f"Total tasks to create: {len(all_tasks)}")
        
        # Create tasks in Notion
        logger.info("Creating tasks in Notion...")
        results = notion_agent.create_tasks_batch(all_tasks)
        
        # Log results
        logger.info("\n" + "="*50)
        logger.info("TASK CREATION SUMMARY")
        logger.info("="*50)
        logger.info(f"✓ Created: {results['created']}")
        logger.info(f"⊘ Skipped (duplicates): {results['skipped']}")
        logger.info(f"✗ Failed: {results['failed']}")
        
        if results['failed_tasks']:
            logger.warning(f"Failed tasks: {', '.join(results['failed_tasks'])}")
        
        logger.info("="*50 + "\n")
        
        logger.info("Email to Notion Task Manager completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
