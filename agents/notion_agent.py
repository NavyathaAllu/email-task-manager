from typing import List, Dict, Optional
from notion_client import Client
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)

class NotionAgent:
    """Agent for creating and managing tasks in Notion database."""
    
    def __init__(self, api_key: str, database_id: str):
        """
        Initialize Notion Agent.
        
        Args:
            api_key: Notion API key
            database_id: Notion database ID
        """
        self.client = Client(auth=api_key)
        self.database_id = database_id
        self._validate_connection()
    
    def _validate_connection(self):
        """
        Validate connection to Notion database.
        """
        try:
            db = self.client.databases.retrieve(self.database_id)
            logger.info(f"Connected to Notion database: {db.get('title', 'Unknown')}")
        except Exception as e:
            logger.error(f"Failed to connect to Notion database: {str(e)}")
            raise
    
    def create_task(self, task: Dict) -> Optional[str]:
        """
        Create a new task in Notion database.
        
        Args:
            task: Task dictionary with title, description, deadline, priority, etc.
        
        Returns:
            Page ID if successful, None otherwise
        """
        try:
            properties = self._build_properties(task)
            
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            page_id = response.get('id')
            logger.info(f"Created Notion task: {task['title']} (ID: {page_id})")
            return page_id
        
        except Exception as e:
            logger.error(f"Error creating Notion task: {str(e)}")
            return None
    
    def _build_properties(self, task: Dict) -> Dict:
        """
        Build Notion page properties from task data.
        
        Args:
            task: Task dictionary
        
        Returns:
            Notion properties dictionary
        """
        properties = {
            "Task Name": {
                "title": [{"text": {"content": task.get('title', 'Untitled Task')}}]
            }
        }
        
        # Add description if present
        if task.get('description'):
            properties["Description"] = {
                "rich_text": [{"text": {"content": task['description'][:2000]}}]
            }
        
        # Add deadline if present
        if task.get('deadline'):
            properties["Deadline"] = {
                "date": {"start": task['deadline']}
            }
        
        # Add priority if present
        if task.get('priority'):
            properties["Priority"] = {
                "select": {"name": task['priority']}
            }
        
        # Add status
        properties["Status"] = {
            "select": {"name": task.get('status', 'Todo')}
        }
        
        # Add email source if present
        if task.get('email_source'):
            properties["Email Source"] = {
                "rich_text": [{"text": {"content": task['email_source'][:500]}}]
            }
        
        return properties
    
    def task_exists(self, task_title: str) -> bool:
        """
        Check if a task with the same title already exists.
        
        Args:
            task_title: Task title to check
        
        Returns:
            True if task exists, False otherwise
        """
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Task Name",
                    "title": {"equals": task_title}
                }
            )
            return len(response.get('results', [])) > 0
        except Exception as e:
            logger.warning(f"Error checking if task exists: {str(e)}")
            return False
    
    def create_tasks_batch(self, tasks: List[Dict]) -> Dict:
        """
        Create multiple tasks in Notion.
        
        Args:
            tasks: List of task dictionaries
        
        Returns:
            Dictionary with success count and failed tasks
        """
        results = {
            'created': 0,
            'failed': 0,
            'skipped': 0,
            'failed_tasks': []
        }
        
        for task in tasks:
            try:
                # Check for duplicates
                if self.task_exists(task['title']):
                    logger.info(f"Task already exists: {task['title']} - Skipping")
                    results['skipped'] += 1
                    continue
                
                page_id = self.create_task(task)
                if page_id:
                    results['created'] += 1
                else:
                    results['failed'] += 1
                    results['failed_tasks'].append(task['title'])
            
            except Exception as e:
                logger.error(f"Error creating task {task.get('title')}: {str(e)}")
                results['failed'] += 1
                results['failed_tasks'].append(task['title'])
        
        logger.info(
            f"Batch creation complete: {results['created']} created, "
            f"{results['skipped']} skipped, {results['failed']} failed"
        )
        return results
