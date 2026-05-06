from composio_openai import ComposioToolSet, Action
from src.providers.base import EmailProvider


class GmailProvider(EmailProvider):
    def __init__(self, api_key: str, entity_id: str = "default"):
        self.toolset = ComposioToolSet(api_key=api_key, entity_id=entity_id)

    def list_emails(self, max_results: int = 100) -> list[dict]:
        result = self.toolset.execute_action(
            action=Action.GMAIL_LIST_THREADS,
            params={"max_results": max_results, "include_spam_trash": True},
        )
        threads = (result.get("data") or {}).get("threads", [])
        emails = []
        for t in threads:
            detail = self.toolset.execute_action(
                action=Action.GMAIL_GET_THREAD,
                params={"thread_id": t["id"]},
            )
            messages = (detail.get("data") or {}).get("messages", [])
            if messages:
                msg = messages[0]
                headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
                emails.append({
                    "id": msg["id"],
                    "thread_id": t["id"],
                    "subject": headers.get("Subject", ""),
                    "from": headers.get("From", ""),
                    "date": headers.get("Date", ""),
                    "labels": msg.get("labelIds", []),
                })
        return emails

    def archive(self, email_id: str) -> None:
        self.toolset.execute_action(
            action=Action.GMAIL_MODIFY_MESSAGE_LABELS,
            params={"message_id": email_id, "remove_label_ids": ["INBOX"]},
        )

    def delete(self, email_id: str) -> None:
        self.toolset.execute_action(
            action=Action.GMAIL_TRASH_MESSAGE,
            params={"message_id": email_id},
        )

    def add_label(self, email_id: str, label: str) -> None:
        self.toolset.execute_action(
            action=Action.GMAIL_MODIFY_MESSAGE_LABELS,
            params={"message_id": email_id, "add_label_ids": [label]},
        )
