"""
services/report_service.py

Story 8: View Spending Summary / Budget vs. Actual.

Transaction.amount is stored as a signed number elsewhere in this codebase
(positive = income, negative = expense) — this report follows that same
convention rather than introducing a separate "type" field.
"""

from services.data_store import DataStore
from services.auth_manager import default_auth_manager
from services.budget_service import current_month
from utils.decorators import login_required
from rich.console import Console
console = Console()

_txn_store = DataStore("transactions.json")
_budget_store = DataStore("budgets.json")


@login_required(default_auth_manager)
def generate_report(month=None):
    user = default_auth_manager.get_current_user()
    month = month or current_month()

    txns = [t for t in _txn_store.load() if t["user"] == user.username and t["date"].startswith(month)]
    budgets = {b["category"]: b["limit"] for b in _budget_store.load() if b["user"] == user.username and b["month"] == month}

    income = sum(t["amount"] for t in txns if t["amount"] > 0)
    expenses = sum(t["amount"] for t in txns if t["amount"] < 0)

    by_category = {}
    for t in txns:
        by_category.setdefault(t["category"], 0)
        by_category[t["category"]] += t["amount"]

    console.print(f"[bold]Report for {month}[/bold]")
    console.print(f"[green]Total income:   {income:.2f}[/green]")
    console.print(f"[red]Total expenses: {expenses:.2f}[/red]")
    console.print("By category:")

    over_budget = []
    if not by_category:
        console.print("  [yellow]No transactions this month.[/yellow]")

    for category, total in by_category.items():
        spent = -total if total < 0 else total
        line = f"  {category:<15} {total:>10.2f}"
        if category in budgets:
            limit = budgets[category]
            line += f"   (budget {limit:.2f})"
            if spent > limit:
                line += "  [bold red]⚠ OVER BUDGET[/bold red]"
                over_budget.append(category)
        console.print(line)

    return {"income": income,
            "expenses": expenses, 
            "by_category": by_category, "over_budget": over_budget
            }