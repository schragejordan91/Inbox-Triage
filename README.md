# Inbox Triage

A Python app to automatically clean up and organize your Gmail and Outlook inboxes. Authenticated via [Composio](https://composio.dev).

## Features

- Connect Gmail and/or Outlook via Composio OAuth
- Define flexible triage rules: archive, label, delete, or move emails
- Run on-demand or on a schedule
- Dry-run mode to preview changes before applying them

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your COMPOSIO_API_KEY
```

Get your Composio API key at https://app.composio.dev/settings

### 3. Connect your email accounts

```bash
# Connect Gmail
python -m src.connect gmail

# Connect Outlook
python -m src.connect outlook
```

This opens a browser OAuth flow managed by Composio.

### 4. Run inbox triage

```bash
# Dry run (preview only, no changes)
python -m src.main --dry-run

# Apply rules to Gmail
python -m src.main --provider gmail

# Apply rules to Outlook
python -m src.main --provider outlook

# Apply to both
python -m src.main
```

## Triage Rules

Edit `src/rules.py` to customize your triage logic. Rules are evaluated in order and each email is matched against the first rule that applies.

Example rule:

```python
Rule(
    name="Archive newsletters",
    conditions=[has_label("Promotions"), older_than_days(7)],
    action=Action.ARCHIVE,
)
```

## Project Structure

```
src/
  main.py        # CLI entrypoint
  connect.py     # Composio OAuth connection helper
  config.py      # Settings loaded from .env
  rules.py       # User-defined triage rules
  triage.py      # Core triage engine
  providers/
    gmail.py     # Gmail-specific Composio actions
    outlook.py   # Outlook-specific Composio actions
    base.py      # Shared provider interface
```
