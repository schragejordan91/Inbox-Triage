import os
from dotenv import load_dotenv

load_dotenv()

COMPOSIO_API_KEY = os.environ["COMPOSIO_API_KEY"]
DEFAULT_PROVIDERS = [p.strip() for p in os.getenv("DEFAULT_PROVIDERS", "gmail,outlook").split(",")]
MAX_EMAILS = int(os.getenv("MAX_EMAILS", "100"))
