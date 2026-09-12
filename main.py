import argparse
import getpass
import sys

from services.auth_manager import default_auth_manager
from services.category_service import add_category, list_categories
from services.transaction_service import add_transaction, list_transactions
from utils.decorators import admin_required


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

	commands.add_parser("list", help="List your transactions")

	category = commands.add_parser("add-category", help="Add an admin category")
	category.add_argument("name")
	commands.add_parser("list-categories", help="List admin categories")
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
		elif args.command == "add-category":
			result = add_category(args.name)
			if result is None:
				return 1
		elif args.command == "list-categories":
			result = list_categories()
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
