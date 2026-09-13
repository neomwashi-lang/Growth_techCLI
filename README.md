# Growth_techCLI

**Team**
1. Neo Mwashi
2. Ryan Ng'ang'a
3. Emmanuel Wema

## Personal Finance Tracker — CLI Application

A command-line tool for tracking income, expenses, categories, and budgets,
with role-based access separating regular users from admins.

## Project structure

    Growth_techCLI/
    ├── main.py                    # CLI entry point (argparse) — wired end to end
    ├── models/
    │   ├── user.py                # User class: hashing, serialization
    │   ├── transaction.py         # Transaction and Category classes
    │   └── budget.py              # Budget class
    ├── services/
    │   ├── data_store.py          # Generic JSON load/save/next_id
    │   ├── auth_manager.py        # register(), login(), logout(), get_current_user()
    │   ├── transaction_service.py # Stories 3-6: add/list/show/edit/delete transactions
    │   ├── category_service.py    # Story 9: admin-only category management
    │   ├── budget_service.py      # Story 7: set/list budgets
    │   └── report_service.py      # Story 8: spending summary / budget vs. actual
    ├── utils/
    │   └── decorators.py          # @login_required, @admin_required
    ├── scripts/
    │   └── create_admin.py        # Standalone script to bootstrap an admin account
    ├── tests/                     # pytest suite — 67 tests, all passing
    ├── data/                      # JSON persistence
    ├── requirements.txt
    └── pytest.ini

## Setup

    git clone <repo-url>
    cd Growth_techCLI
    python -m venv venv
    # Windows:
    .\venv\Scripts\Activate.ps1
    # macOS/Linux:
    source venv/bin/activate

    pip install -r requirements.txt

## Running the tests

    python -m pytest -v

67 passed. Coverage: password hashing/serialization (`User`), generic file
persistence (`DataStore`), full auth lifecycle with session expiry
(`AuthManager`), access-control decorators, transaction CRUD with ownership
checks, admin-only category management, budget create/update, and
spending-summary reporting with over-budget flagging.

## Creating an admin account

Admin accounts are not created through normal registration —
`AuthManager.register()` always assigns the `"user"` role, and there is no
CLI command or self-promotion path to become an admin. Run:

    python scripts/create_admin.py

You'll be prompted for a username and password; the account is created
directly with `role="admin"`.

## Using the CLI

    # Account and session
    python main.py register <username>
    python main.py login <username>
    python main.py whoami
    python main.py logout

    # Transactions
    python main.py add <amount> <category> <date> --description "<text>"
    python main.py list
    python main.py show <id>
    python main.py edit <id> --amount <new_amount>
    python main.py delete <id>

    # Budgets and reporting
    python main.py budget <category> <limit>
    python main.py budgets
    python main.py report

    # Admin only
    python main.py admin-status
    python main.py add-category <name>
    python main.py list-categories

Example session:

    python main.py register neo
    python main.py login neo
    python main.py add -50 Groceries 2026-09-13 --description "Weekly shop"
    python main.py budget Groceries 40
    python main.py report

## Design at a glance

- **Roles:** `User.role` is `"user"` or `"admin"`, checked by
  `@admin_required` — not separate `AdminUser`/`RegularUser` subclasses.
  (Considered `Person → User` inheritance for the assignment's OOP
  guidance; see Known gaps.)
- **Storage:** no database — one JSON file per entity under `data/`, and
  `DataStore` is the only class that reads or writes those files directly.
  Every model converts itself to/from a plain dict via
  `to_dict()`/`from_dict()`. Budgets are stored as flat records filtered
  by `(user, category, month)` rather than a composite dictionary key,
  keeping the same pattern used for transactions and categories.
- **Ownership:** transactions and budgets are only visible/editable by the
  user who created them, enforced in their respective services and tested
  against a second "wrong owner" account.
- **Git:** all work happens on feature branches, merged into `secBranch`
  only through a reviewed pull request.

## Authentication strategy

- Registration stores only a PBKDF2-HMAC-SHA256 digest and a unique random
  salt in `data/users.json`; plaintext passwords are never persisted or
  logged.
- Login derives the digest again from the stored salt and compares it
  using a constant-time digest comparison (`hmac.compare_digest`), which
  avoids leaking timing information about a partially-correct password.
- A successful login writes a short-lived session (user id, username,
  role, and an 8-hour expiry) to `data/session.json`. Expired sessions are
  detected and cleared automatically on the next command.
- CLI commands use `@login_required` and `@admin_required` from
  `utils/decorators.py`, keeping authentication and authorization out of
  the command implementations themselves.

## Git workflow

- `secBranch` is the shared integration branch. Work happens on feature
  branches (e.g. `feature/auth`, `feature/transactions`, `feature/budgets`),
  merged into `secBranch` through a reviewed pull request.
- Commits use short, imperative messages describing what changed and why.

## Known gaps

- Decision pending: `Person → User` inheritance for additional OOP rubric
  credit — current design keeps role as a plain attribute on `User`.

## Team

All ten user stories (registration, login, transaction CRUD, budgets,
reporting, admin-only categories, and role-based access) are implemented,
tested, and wired into a working CLI. See git history and pull requests
for the individual contributions and the bugs found and fixed along the way.