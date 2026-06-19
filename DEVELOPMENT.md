# Email to Notion Task Manager - Development Guide

## Architecture

The agent follows a modular architecture:

```
┌─────────────┐
│   Gmail     │ → Retrieve unread emails
│   Agent     │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  Task Extractor  │ → Parse emails for tasks
│  & Parser        │   Extract deadlines & priorities
└──────┬───────────┘
       │
       ↓
┌─────────────────┐
│  Notion Agent   │ → Create tasks in Notion
│                 │   Handle duplicates
└─────────────────┘
```

## File Structure

```
.
├── main.py                 # Entry point
├── scheduler.py            # Scheduled execution
├── setup.py               # Setup guide
├── config.json            # Configuration
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── agents/
│   ├── __init__.py
│   ├── gmail_agent.py    # Gmail integration
│   ├── task_extractor.py # Task extraction logic
│   └── notion_agent.py   # Notion integration
├── utils/
│   ├── logger.py         # Logging setup
│   └── parser.py         # Email parsing
└── logs/                 # Log files
```

## Extending the Agent

### Adding Custom Task Extraction Rules

Edit `config.json` to add new task keywords or date patterns:

```json
{
  "task_keywords": [
    "task",
    "action item",
    "your_custom_keyword"
  ]
}
```

### Using OpenAI for Smarter Extraction

```python
# In task_extractor.py
import openai

def extract_with_ai(self, email_body: str) -> List[Dict]:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Extract tasks from the following email."
            },
            {"role": "user", "content": email_body}
        ]
    )
    # Parse response...
```

## Testing

```bash
# Test Gmail connection
python -c "from agents.gmail_agent import GmailAgent; g = GmailAgent('your@email.com')"

# Test Notion connection
python -c "from agents.notion_agent import NotionAgent; n = NotionAgent('key', 'db_id')"

# Test task extraction
python -c "from agents.task_extractor import TaskExtractor; t = TaskExtractor()"
```

## Debugging

Check logs in `logs/app.log` for detailed execution information.

### Common Issues

**Gmail Authentication Failed**
- Ensure 2-Step Verification is enabled
- Verify app password is correct (not your main password)
- Check email address matches your Gmail account

**Notion Tasks Not Created**
- Verify database ID (remove hyphens if present)
- Ensure integration has database access
- Check that property names match your database schema

**Tasks Not Extracted**
- Check that email contains task keywords from config.json
- Verify email body is plain text (not HTML-only)
- Add custom keywords to config.json if needed

## Future Enhancements

- [ ] Web UI for configuration
- [ ] Task priority based on sender
- [ ] Attachment handling
- [ ] Integration with Slack/Discord notifications
- [ ] Machine learning for better task detection
- [ ] Support for multiple email accounts
- [ ] Recurring task detection
- [ ] Task completion tracking
