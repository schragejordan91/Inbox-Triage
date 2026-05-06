from rich.console import Console
from rich.table import Table

from src.providers.base import EmailProvider
from src.rules import Action, Rule

console = Console()


def run_triage(
    provider: EmailProvider,
    rules: list[Rule],
    max_emails: int = 100,
    dry_run: bool = False,
) -> dict:
    console.print(f"[bold]Fetching up to {max_emails} emails...[/bold]")
    emails = provider.list_emails(max_results=max_emails)
    console.print(f"Found [cyan]{len(emails)}[/cyan] emails.")

    stats = {a: 0 for a in Action}
    stats["skipped"] = 0

    table = Table(title="Triage Results", show_lines=True)
    table.add_column("Subject", max_width=50)
    table.add_column("From", max_width=30)
    table.add_column("Rule")
    table.add_column("Action")

    for email in emails:
        matched_rule = next((r for r in rules if r.matches(email)), None)
        if not matched_rule:
            stats["skipped"] += 1
            continue

        action = matched_rule.action
        table.add_row(
            email.get("subject", "")[:50],
            email.get("from", "")[:30],
            matched_rule.name,
            f"[{'green' if action == Action.ARCHIVE else 'red' if action == Action.DELETE else 'yellow'}]{action.value}[/]",
        )

        if not dry_run:
            _apply_action(provider, email, matched_rule)

        stats[action] = stats.get(action, 0) + 1

    console.print(table)
    if dry_run:
        console.print("[yellow]Dry run — no changes made.[/yellow]")
    return stats


def _apply_action(provider: EmailProvider, email: dict, rule: Rule) -> None:
    email_id = email["id"]
    if rule.action == Action.ARCHIVE:
        provider.archive(email_id)
    elif rule.action == Action.DELETE:
        provider.delete(email_id)
    elif rule.action == Action.LABEL and rule.label:
        provider.add_label(email_id, rule.label)
