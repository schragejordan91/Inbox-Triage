from composio_client import Composio
from src.providers.base import EmailProvider
from src.config import COMPOSIO_ENTITY_ID


class OutlookProvider(EmailProvider):
    def __init__(self, api_key: str):
        self.client = Composio(api_key=api_key)

    def _exec(self, slug: str, **args) -> dict:
        result = self.client.tools.execute(
            slug,
            entity_id=COMPOSIO_ENTITY_ID,
            arguments=args,
        )
        return result.model_dump().get("data") or {}

    def list_emails(self, max_results: int = 100) -> list[dict]:
        data = self._exec(
            "OUTLOOK_OUTLOOK_LIST_MESSAGES",
            folder_id="inbox",
            top=max_results,
        )
        messages = (data.get("response_data") or {}).get("value") or []
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
        self._exec(
            "OUTLOOK_OUTLOOK_MOVE_MESSAGE",
            message_id=email_id,
            destination_folder_id="archive",
        )

    def delete(self, email_id: str) -> None:
        # Move to Deleted Items folder
        self._exec(
            "OUTLOOK_OUTLOOK_MOVE_MESSAGE",
            message_id=email_id,
            destination_folder_id="deleteditems",
        )

    def add_label(self, email_id: str, label: str) -> None:
        self._exec(
            "OUTLOOK_OUTLOOK_UPDATE_EMAIL",
            message_id=email_id,
            categories=[label],
        )
