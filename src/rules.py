from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Action(str, Enum):
    ARCHIVE = "archive"
    DELETE = "delete"
    LABEL = "label"
    SKIP = "skip"


@dataclass
class Rule:
    name: str
    conditions: list[Callable[[dict], bool]]
    action: Action
    label: str | None = None  # used when action == LABEL

    def matches(self, email: dict) -> bool:
        return all(c(email) for c in self.conditions)


# --- condition helpers ---

def has_label(label: str) -> Callable[[dict], bool]:
    def check(email: dict) -> bool:
        return label.lower() in [l.lower() for l in email.get("labels", [])]
    return check


def from_domain(domain: str) -> Callable[[dict], bool]:
    def check(email: dict) -> bool:
        sender = email.get("from", "")
        return domain.lower() in sender.lower()
    return check


def older_than_days(days: int) -> Callable[[dict], bool]:
    from datetime import datetime, timezone, timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    def check(email: dict) -> bool:
        date_str = email.get("date")
        if not date_str:
            return False
        try:
            # ISO 8601 (Composio / Outlook format)
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return date < cutoff
        except ValueError:
            pass
        try:
            # RFC 2822 fallback
            from email.utils import parsedate_to_datetime
            date = parsedate_to_datetime(date_str)
            return date < cutoff
        except Exception:
            return False
    return check


def subject_contains(keyword: str) -> Callable[[dict], bool]:
    def check(email: dict) -> bool:
        return keyword.lower() in email.get("subject", "").lower()
    return check


# --- default rules (edit these to match your preferences) ---
# Gmail system label IDs: CATEGORY_PROMOTIONS, CATEGORY_SOCIAL, SPAM, INBOX, UNREAD
# Outlook uses categories[] which are user-defined strings

DEFAULT_RULES: list[Rule] = [
    Rule(
        name="Archive old Gmail promotions",
        conditions=[has_label("CATEGORY_PROMOTIONS"), older_than_days(7)],
        action=Action.ARCHIVE,
    ),
    Rule(
        name="Archive old Gmail updates",
        conditions=[has_label("CATEGORY_UPDATES"), older_than_days(14)],
        action=Action.ARCHIVE,
    ),
    Rule(
        name="Archive old Gmail social",
        conditions=[has_label("CATEGORY_SOCIAL"), older_than_days(14)],
        action=Action.ARCHIVE,
    ),
    Rule(
        name="Delete Gmail spam",
        conditions=[has_label("SPAM")],
        action=Action.DELETE,
    ),
    Rule(
        name="Archive newsletters older than 30 days",
        conditions=[subject_contains("newsletter"), older_than_days(30)],
        action=Action.ARCHIVE,
    ),
    Rule(
        name="Archive unsubscribe emails older than 30 days",
        conditions=[subject_contains("unsubscribe"), older_than_days(30)],
        action=Action.ARCHIVE,
    ),
]
