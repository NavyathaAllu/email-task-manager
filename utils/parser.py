import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Tuple, Optional

class EmailParser:
    """Parse and extract task information from email content."""
    
    @staticmethod
    def extract_tasks(email_body: str, task_keywords: List[str]) -> List[Dict[str, str]]:
        """
        Extract potential tasks from email body.
        
        Args:
            email_body: Email content text
            task_keywords: Keywords to identify tasks
        
        Returns:
            List of extracted tasks with descriptions
        """
        tasks = []
        lines = email_body.split('\n')
        
        # Pattern for numbered/bulleted lists
        list_pattern = r'^\s*[-•*]\s+(.+)$|^\s*\d+\.\s+(.+)$'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches list format
            match = re.match(list_pattern, line)
            if match:
                task_text = match.group(1) or match.group(2)
                
                # Check if line contains task keywords
                if any(keyword.lower() in task_text.lower() for keyword in task_keywords):
                    tasks.append({'description': task_text})
            else:
                # Check for task keywords in any line
                if any(keyword.lower() in line.lower() for keyword in task_keywords):
                    tasks.append({'description': line})
        
        return tasks
    
    @staticmethod
    def extract_deadline(text: str) -> Optional[str]:
        """
        Extract deadline from text.
        
        Args:
            text: Text containing deadline information
        
        Returns:
            Parsed deadline date as string, or None
        """
        # Common date patterns
        patterns = [
            r'(by|until|before|due)\s+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(by|until|before|due)\s+([A-Za-z]+day)',
            r'(by|until|before|due)\s+(next\s+[A-Za-z]+)',
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(2) if match.lastindex >= 2 else match.group(0)
                try:
                    parsed_date = date_parser.parse(date_str, fuzzy=True)
                    return parsed_date.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
        
        # Check for relative dates
        relative_patterns = {
            r'\btoday\b': 0,
            r'\btomorrow\b': 1,
            r'\bnext\s+(?:week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b': 7,
            r'\bnext\s+month\b': 30,
        }
        
        for pattern, days in relative_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                deadline = datetime.now() + timedelta(days=days)
                return deadline.strftime('%Y-%m-%d')
        
        return None
    
    @staticmethod
    def extract_priority(text: str) -> str:
        """
        Extract priority level from text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Priority level: 'High', 'Medium', or 'Low'
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['urgent', 'asap', 'high', 'critical', 'important', '!!', 'important!']):
            return 'High'
        elif any(word in text_lower for word in ['medium', 'moderate']):
            return 'Medium'
        
        return 'Low'
    
    @staticmethod
    def clean_task_text(text: str) -> str:
        """
        Clean and normalize task text.
        
        Args:
            text: Raw task text
        
        Returns:
            Cleaned task text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common prefixes
        text = re.sub(r'^[-•*]\s+', '', text)
        text = re.sub(r'^\d+\.\s+', '', text)
        
        # Remove markdown formatting
        text = re.sub(r'[*_~`]', '', text)
        
        return text
