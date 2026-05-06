import click
from rich.console import Console

from src.config import COMPOSIO_API_KEY, DEFAULT_PROVIDERS, MAX_EMAILS
from src.rules import DEFAULT_RULES
from src.triage import run_triage

console = Console()


@click.command()
@click.option("--provider", "-p", multiple=True, help="gmail, outlook, or both (default: from .env)")
@click.option("--dry-run", is_flag=True, default=False, help="Preview actions without applying them")
@click.option("--max-emails", default=None, type=int, help="Max emails to process per provider")
def main(provider: tuple, dry_run: bool, max_emails: int | None) -> None:
    providers = list(provider) or DEFAULT_PROVIDERS
    limit = max_emails or MAX_EMAILS

    for p in providers:
        console.rule(f"[bold blue]{p.title()} Triage[/bold blue]")
        email_provider = _get_provider(p)
        if email_provider is None:
            console.print(f"[red]Unknown provider '{p}'. Skipping.[/red]")
            continue
        stats = run_triage(email_provider, DEFAULT_RULES, max_emails=limit, dry_run=dry_run)
        console.print(f"[bold]Stats:[/bold] {stats}")


def _get_provider(name: str):
    if name.lower() == "gmail":
        from src.providers.gmail import GmailProvider
        return GmailProvider(api_key=COMPOSIO_API_KEY)
    if name.lower() == "outlook":
        from src.providers.outlook import OutlookProvider
        return OutlookProvider(api_key=COMPOSIO_API_KEY)
    return None


if __name__ == "__main__":
    main()
