import os
from dotenv import load_dotenv

load_dotenv()

COMPOSIO_API_KEY = os.environ["COMPOSIO_API_KEY"]
COMPOSIO_ENTITY_ID = os.getenv("COMPOSIO_ENTITY_ID", "pg-test-d454bb55-01db-4dcf-93ac-fd014ef2f0a7")
DEFAULT_PROVIDERS = [p.strip() for p in os.getenv("DEFAULT_PROVIDERS", "gmail,outlook").split(",")]
MAX_EMAILS = int(os.getenv("MAX_EMAILS", "100"))
