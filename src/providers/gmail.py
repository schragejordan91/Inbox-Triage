from composio_client import Composio
from src.providers.base import EmailProvider
from src.config import COMPOSIO_ENTITY_ID


class GmailProvider(EmailProvider):
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
            "GMAIL_FETCH_EMAILS",
            max_results=max_results,
            include_spam_trash=False,
        )
        messages = data.get("messages") or []
        return [
            {
                "id": m["messageId"],
                "thread_id": m.get("threadId", ""),
                "subject": m.get("subject", ""),
                "from": m.get("sender", ""),
                "date": m.get("messageTimestamp", ""),
                "labels": m.get("labelIds", []),
            }
            for m in messages
        ]

    def archive(self, email_id: str) -> None:
        self._exec(
            "GMAIL_ADD_LABEL_TO_EMAIL",
            message_id=email_id,
            remove_label_ids=["INBOX"],
        )

    def delete(self, email_id: str) -> None:
        self._exec("GMAIL_MOVE_TO_TRASH", message_id=email_id)

    def add_label(self, email_id: str, label: str) -> None:
        self._exec(
            "GMAIL_ADD_LABEL_TO_EMAIL",
            message_id=email_id,
            add_label_ids=[label],
        )
