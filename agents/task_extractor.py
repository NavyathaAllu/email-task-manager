import json
from typing import List, Dict, Optional
from utils.parser import EmailParser
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TaskExtractor:
    """Extract tasks and deadlines from email content."""
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize Task Extractor.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.parser = EmailParser()
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to config file
        
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def extract_from_email(self, email: Dict) -> List[Dict]:
        """
        Extract tasks from an email.
        
        Args:
            email: Email dictionary with subject and body
        
        Returns:
            List of extracted tasks
        """
        tasks = []
        
        # Combine subject and body for analysis
        full_text = f"{email.get('subject', '')}\n{email.get('body', '')}"
        
        # Extract task items
        task_keywords = self.config.get('task_keywords', [])
        raw_tasks = self.parser.extract_tasks(email.get('body', ''), task_keywords)
        
        for raw_task in raw_tasks:
            task = self._process_task(raw_task, full_text, email)
            if task:
                tasks.append(task)
        
        logger.info(f"Extracted {len(tasks)} tasks from email: {email.get('subject')}")
        return tasks
    
    def _process_task(self, raw_task: Dict, full_text: str, email: Dict) -> Optional[Dict]:
        """
        Process and enrich a raw task with deadline, priority, etc.
        
        Args:
            raw_task: Raw task data
            full_text: Full email text for context
            email: Original email data
        
        Returns:
            Processed task dictionary
        """
        task_text = raw_task.get('description', '')
        if not task_text:
            return None
        
        # Clean task text
        clean_text = self.parser.clean_task_text(task_text)
        
        # Extract deadline
        deadline = self.parser.extract_deadline(task_text) or self.parser.extract_deadline(full_text)
        
        # Extract priority
        priority = self.parser.extract_priority(task_text)
        
        # Create task object
        task = {
            'title': clean_text[:100],  # Limit to 100 characters
            'description': clean_text,
            'deadline': deadline,
            'priority': priority,
            'status': 'Todo',
            'email_source': f"{email.get('sender', '')} - {email.get('subject', '')}"
        }
        
        return task
    
    def validate_task(self, task: Dict) -> bool:
        """
        Validate a task before sending to Notion.
        
        Args:
            task: Task dictionary
        
        Returns:
            True if valid, False otherwise
        """
        # Must have a title
        if not task.get('title') or not task['title'].strip():
            return False
        
        # Title must be reasonable length
        if len(task['title']) > 200:
            return False
        
        return True
