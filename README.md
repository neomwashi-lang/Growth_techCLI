# Growth_techCLI

**Team**
1. Neo Mwashi
2. Ryan Ng'ang'a
3. Emmanuel Wema

## Personal Finance Tracker — CLI Application

A command-line tool for tracking income, expenses, categories, and budgets,
with role-based access separating regular users from admins.

Task 1 (Define the Problem) is complete — see the user stories on our
[Trello board]. This README now reflects real, working code, not stubs —
the authentication foundation (Stories 1, 2, and 10) is implemented and
tested. Transaction, category, and budget features (Stories 3–9) are in
progress.

## Project structure
Growth_techCLI/
├── main.py # CLI entry point (argparse) — in progress
├── models/
│ └── user.py # User class: hashing, serialization
├── services/
│ ├── data_store.py # Generic JSON load/save/next_id, reused by every model
│ └── auth_manager.py # register(), login(), logout(), get_current_user()
├── utils/
│ └── decorators.py # @login_required, @admin_required
├── scripts/
│ └── create_admin.py # Standalone script to bootstrap an admin account
├── tests/ # pytest suite — 23 tests, all passing
├── data/ # JSON persistence (users.json, session.json, ...)
├── requirements.txt
└── pytest.ini


## Setup

```bash
git clone <repo-url>
cd Growth_techCLI
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## Running the tests

```bash
python -m pytest -v
```

Should show 23 passed. Test coverage so far: password hashing and
serialization (`User`), generic file persistence (`DataStore`), the full
registration/login/logout/session lifecycle (`AuthManager`), and both
access-control decorators (`login_required`, `admin_required`).

## Creating an admin account

Admin accounts are **not** created through normal registration —
`AuthManager.register()` always assigns the `"user"` role, and there is no
CLI command or self-promotion path to become an admin. This is intentional:
admin status is only granted by someone with direct file access to the
project, running:

```bash
python scripts/create_admin.py
```

You'll be prompted for a username and password; the account is created
directly with `role="admin"`.

## Design at a glance

- **Roles:** `User` has a single `role` field (`"user"` or `"admin"`),
  checked by the `@admin_required` decorator — not separate `AdminUser`/
  `RegularUser` subclasses. (We considered a `Person → User` inheritance
  chain per the assignment's OOP guidance; current design keeps role as
  an attribute for simplicity. Open to revisiting before submission.)
- **Storage:** no database — one JSON file per entity under `data/`, and
  `DataStore` is the only class that reads or writes those files directly.
  Every model (`User`, and soon `Transaction`/`Category`/`Budget`) converts
  itself to/from a plain dict via `to_dict()`/`from_dict()`.
- **Passwords:** hashed with `pbkdf2_hmac` and a random salt before ever
  touching disk — plaintext passwords are never stored.
- **Sessions:** `login()` writes `data/session.json`, so a session persists
  across separate CLI invocations (matching real CLI tools like `git`,
  rather than requiring one long-running interactive process). `logout()`
  clears it.
- **Access control:** `@login_required` and `@admin_required` (in
  `utils/decorators.py`) wrap command functions. Both print a message and
  return without running the command if the check fails, rather than
  raising an exception — the CLI keeps running either way.
- **Git:** `main` and `secBranch` stay protected; all work happens on
  feature branches, merged into `secBranch` only through a reviewed PR.

## Known gaps / in progress

- Transaction, category, and budget commands (Stories 3–9) — not yet built
- `main.py`'s argparse subcommands are not yet wired to the auth layer
- Decision pending: whether to introduce `Person → User` inheritance for
  the OOP rubric credit

## Next step

Wire `main.py`'s subcommands (`register`, `login`, `logout`, `add`,
`list`, `report`, etc.) to the classes and decorators above, per Task 3.