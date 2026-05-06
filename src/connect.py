"""CLI helper to connect Gmail or Outlook via Composio OAuth."""
import sys
from composio_openai import ComposioToolSet, App
from src.config import COMPOSIO_API_KEY


def connect(provider: str) -> None:
    toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
    app_map = {"gmail": App.GMAIL, "outlook": App.OUTLOOK}
    app = app_map.get(provider.lower())
    if not app:
        print(f"Unknown provider '{provider}'. Choose: gmail, outlook")
        sys.exit(1)

    print(f"Opening browser to connect {provider.title()} via Composio OAuth...")
    entity = toolset.get_entity(id="default")
    request = entity.initiate_connection(app)
    print(f"\nVisit this URL to authorize:\n  {request.redirectUrl}")
    print("\nWaiting for connection to complete...")
    request.wait_until_active(timeout=120)
    print(f"{provider.title()} connected successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.connect <gmail|outlook>")
        sys.exit(1)
    connect(sys.argv[1])
