import argparse
import getpass
import sys

from services.auth_manager import default_auth_manager
from services.category_service import add_category, list_categories
from services.transaction_service import add_transaction, list_transactions, show_transaction, edit_transaction, delete_transaction
from utils.decorators import admin_required
from services.budget_service import set_budget, list_budgets
from services.report_service import generate_report


def build_parser():
	parser = argparse.ArgumentParser(description="Personal Finance Tracker CLI")
	commands = parser.add_subparsers(dest="command", required=True)

	register = commands.add_parser("register", help="Create a user account")
	register.add_argument("username")

	login = commands.add_parser("login", help="Start a session")
	login.add_argument("username")

	commands.add_parser("logout", help="End the current session")
	commands.add_parser("whoami", help="Show the current session")
	commands.add_parser("admin-status", help="Run an admin-only command")

	add = commands.add_parser("add", help="Add a transaction")
	add.add_argument("amount", type=float)
	add.add_argument("category")
	add.add_argument("date")
	add.add_argument("--description", default="")

	show = commands.add_parser("show", help="Show a single transaction")
	show.add_argument("txn_id", type=int)

	edit = commands.add_parser("edit", help="Edit a transaction you own")
	edit.add_argument("txn_id", type=int)
	edit.add_argument("--amount", type=float)
	edit.add_argument("--category")
	edit.add_argument("--date")
	edit.add_argument("--description")

	delete = commands.add_parser("delete", help="Delete a transaction you own")
	delete.add_argument("txn_id", type=int)

	commands.add_parser("list", help="List your transactions")

	category = commands.add_parser("add-category", help="Add an admin category")
	category.add_argument("name")
	commands.add_parser("list-categories", help="List admin categories")

	budget = commands.add_parser("budget", help="Set a monthly budget for a category")
	budget.add_argument("category")
	budget.add_argument("limit", type=float)

	commands.add_parser("budgets", help="List your budgets")
	commands.add_parser("report", help="View spending summary and budget vs. actual")
	return parser


def main(argv=None):
	args = build_parser().parse_args(argv)
	try:
		if args.command == "register":
			password = getpass.getpass("Password: ")
			user = default_auth_manager.register(args.username, password)
			print(f"Registered '{user.username}'.")
		elif args.command == "login":
			password = getpass.getpass("Password: ")
			user = default_auth_manager.login(args.username, password)
			print(f"Logged in as '{user.username}'.")
		elif args.command == "logout":
			default_auth_manager.logout()
			print("Logged out.")
		elif args.command == "whoami":
			user = default_auth_manager.get_current_user()
			if user is None:
				print("You are not logged in.")
				return 1
			print(f"{user.username} ({user.role})")
		elif args.command == "admin-status":
			_admin_status()
		elif args.command == "add":
			add_transaction(args.amount, args.category, args.date, args.description)
		elif args.command == "list":
			list_transactions()
		elif args.command == "show":
			result = show_transaction(args.txn_id)
			if result is None:
				return 1
		elif args.command == "edit":
			result = edit_transaction(args.txn_id, args.amount, args.category, args.date, args.description)
			if result is None:
				return 1
		elif args.command == "delete":
			result = delete_transaction(args.txn_id)
			if not result:
				return 1
		elif args.command == "add-category":
			result = add_category(args.name)
			if result is None:
				return 1
		elif args.command == "list-categories":
			result = list_categories()
			if result is None:
				return 1
		elif args.command == "budget":
			result = set_budget(args.category, args.limit)
			if result is None:
				return 1
		elif args.command == "budgets":
			result = list_budgets()
			if result is None:
				return 1
		elif args.command == "report":
			result = generate_report()
			if result is None:
				return 1
	except ValueError as error:
		print(f"Error: {error}", file=sys.stderr)
		return 1
	return 0


@admin_required(default_auth_manager)
def _admin_status():
	print("Admin access granted.")


if __name__ == "__main__":
	raise SystemExit(main())
