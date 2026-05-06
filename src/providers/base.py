from abc import ABC, abstractmethod


class EmailProvider(ABC):
    """Shared interface for Gmail and Outlook providers."""

    @abstractmethod
    def list_emails(self, max_results: int = 100) -> list[dict]:
        ...

    @abstractmethod
    def archive(self, email_id: str) -> None:
        ...

    @abstractmethod
    def delete(self, email_id: str) -> None:
        ...

    @abstractmethod
    def add_label(self, email_id: str, label: str) -> None:
        ...
