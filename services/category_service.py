"""
services/category_service.py

Story 9: Manage Categories (admin only).
"""

from services.data_store import DataStore
from services.auth_manager import default_auth_manager
from utils.decorators import admin_required
from models.transaction import Category
from rich.console import Console
from rich.table import Table

console = Console()


_store = DataStore("categories.json")


@admin_required(default_auth_manager)
def add_category(name):
    """Add a new category."""
    user = default_auth_manager.get_current_user()
    records = _store.load()

    cat = Category(id=_store.next_id(records), user=user.username, name=name)
    records.append(cat.to_dict())
    _store.save(records)
    print(f"Added category #{cat.id}: {name}")
    return cat


@admin_required(default_auth_manager)
def list_categories():
    """List all categories."""
    records = _store.load()
    if not records:
        console.print("[yellow]No categories yet.[/yellow]")
        return []

    table = Table(title="Categories")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    for r in records:
        table.add_row(str(r["id"]), r["name"])
    console.print(table)
    return [Category.from_dict(r) for r in records]

@admin_required(default_auth_manager)
def edit_category(cat_id, name):
    """Rename a category."""
    records = _store.load()
    match = next((r for r in records if r["id"] == cat_id), None)
    if match is None:
        print(f"No category with id {cat_id}.")
        return None
    match["name"] = name
    _store.save(records)
    print(f"Updated category #{cat_id} to '{name}'.")
    return Category.from_dict(match)


@admin_required(default_auth_manager)
def delete_category(cat_id):
    """Delete a category."""
    records = _store.load()
    match = next((r for r in records if r["id"] == cat_id), None)
    if match is None:
        print(f"No category with id {cat_id}.")
        return False
    records = [r for r in records if r["id"] != cat_id]
    _store.save(records)
    print(f"Deleted category #{cat_id}.")
    return True