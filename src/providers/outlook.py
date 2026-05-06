from composio_openai import ComposioToolSet, Action
from src.providers.base import EmailProvider


class OutlookProvider(EmailProvider):
    def __init__(self, api_key: str, entity_id: str = "default"):
        self.toolset = ComposioToolSet(api_key=api_key, entity_id=entity_id)

    def list_emails(self, max_results: int = 100) -> list[dict]:
        result = self.toolset.execute_action(
            action=Action.OUTLOOK_LIST_MESSAGES,
            params={"top": max_results, "folder": "inbox"},
        )
        messages = (result.get("data") or {}).get("value", [])
        return [
            {
                "id": m["id"],
                "subject": m.get("subject", ""),
                "from": (m.get("from") or {}).get("emailAddress", {}).get("address", ""),
                "date": m.get("receivedDateTime", ""),
                "labels": m.get("categories", []),
                "is_read": m.get("isRead", False),
            }
            for m in messages
        ]

    def archive(self, email_id: str) -> None:
        self.toolset.execute_action(
            action=Action.OUTLOOK_MOVE_MESSAGE,
            params={"message_id": email_id, "destination_folder": "archive"},
        )

    def delete(self, email_id: str) -> None:
        self.toolset.execute_action(
            action=Action.OUTLOOK_DELETE_MESSAGE,
            params={"message_id": email_id},
        )

    def add_label(self, email_id: str, label: str) -> None:
        self.toolset.execute_action(
            action=Action.OUTLOOK_UPDATE_MESSAGE,
            params={"message_id": email_id, "categories": [label]},
        )
