# Email to Notion Task Manager

An intelligent agent that automatically extracts tasks from your Gmail emails and creates them in Notion with deadlines.

## Features

- 📧 Connect to Gmail and read emails
- 🤖 AI-powered task extraction from email content
- 📝 Automatically create tasks in Notion database
- ⏰ Extract and set deadlines
- 🔄 Schedule periodic checks
- 🔐 Secure credential management

## Prerequisites

- Python 3.8+
- Gmail account with app password enabled
- Notion account and database
- API credentials (Gmail & Notion)

## Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/NavyathaAllu/email-task-manager.git
cd email-task-manager
pip install -r requirements.txt
```

### 2. Gmail Setup

1. Enable [2-Step Verification](https://myaccount.google.com/security) on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Save your email and app password

### 3. Notion Setup

1. Create a new Notion database or use an existing one
2. [Create a Notion Integration](https://www.notion.so/my-integrations)
3. Get your `NOTION_API_KEY`
4. Share your database with the integration
5. Get your database ID from the database URL: `https://notion.so/{DATABASE_ID}?v=...`

### 4. Environment Configuration

Create a `.env` file in the root directory:

```
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id
```

## Usage

### Run Once

```bash
python main.py
```

### Schedule Daily Checks

```bash
# Linux/Mac: Add to crontab
crontab -e
# Add this line (runs daily at 9 AM):
0 9 * * * cd /path/to/email-task-manager && python main.py

# Windows: Use Task Scheduler or run:
python scheduler.py
```

## Configuration

Edit `config.json` to customize:

```json
{
  "email_check_limit": 10,
  "extract_unread_only": true,
  "task_extraction_prompt": "Extract tasks from this email...",
  "notion_properties": {
    "title": "Task Name",
    "deadline": "Deadline",
    "status": "Status",
    "priority": "Priority"
  }
}
```

## Project Structure

```
email-task-manager/
├── main.py                 # Entry point
├── config.json            # Configuration file
├── requirements.txt       # Dependencies
├── .env.example          # Environment variables template
├── agents/
│   ├── gmail_agent.py    # Gmail connection & email retrieval
│   ├── task_extractor.py # AI task extraction logic
│   └── notion_agent.py   # Notion database operations
└── utils/
    ├── parser.py         # Email parsing utilities
    └── logger.py         # Logging setup
```

## How It Works

1. **Gmail Agent** → Connects to Gmail and retrieves unread emails
2. **Task Extractor** → Uses AI to identify tasks and deadlines from email content
3. **Notion Agent** → Creates tasks in your Notion database
4. **Scheduler** → Runs the process on a schedule

## Example Email Format

The agent can extract tasks from emails like:

```
Subject: Project Updates

Hi,
Please complete the following tasks:
1. Review the design document by Friday
2. Send the report by next Tuesday
3. Meeting preparation before March 15

Thanks
```

**Result in Notion:**
| Task Name | Deadline | Status |
|-----------|----------|--------|
| Review the design document | Friday | Todo |
| Send the report | next Tuesday | Todo |
| Meeting preparation | March 15 | Todo |

## Troubleshooting

### "Authentication failed"
- Check your Gmail app password is correct
- Ensure 2-Step Verification is enabled

### "Tasks not being created"
- Verify the database ID is correct
- Ensure the integration has access to the database
- Check the email content contains clear task descriptions

### "Deadline parsing issues"
- Use clear date formats (e.g., "March 15", "next Friday")
- The agent learns from examples

## Security Notes

- ⚠️ Never commit `.env` file to Git
- Use app-specific passwords, not your main password
- Rotate API keys periodically
- Keep credentials in environment variables only

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Support

For issues or questions, open an issue in the repository.
