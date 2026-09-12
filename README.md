# Growth_techCLI
# 1. Neo Mwashi
# 2. Ryan Ng'ang'a
# 3. Emmanuel Wema

# Personal Finance Tracker — CLI Application

Task 1 (Define the Problem) deliverable, expressed as Python instead of prose.
Nothing here executes real logic — every class/function is a stub. Real
behavior is built in Task 3 (Develop the Code).

## Files

| File | Proposal sections | What it holds |
|---|---|---|
| `proposal_1_3_overview.py` | 1–3 | Problem definition, target users, core feature list |
| `proposal_4_6_design.py` | 4–6 | Entities and planned classes (`User`, `AdminUser`, `RegularUser`, `Transaction`, `Category`, `Budget`), plus the `DataStore` class documenting the JSON storage plan |
| `proposal_7_8_strategy.py` | 7–8 | `AuthManager` and the `login_required`/`admin_required` decorator stubs for the authentication strategy, plus the Git workflow plan as a module-level string |

## Design at a glance

- **Roles:** `AdminUser` and `RegularUser` both extend `User` — shared account
  fields live once in the base class, role-specific behavior is added on top.
- **Storage:** no database — one JSON file per entity under `data/`, and only
  `DataStore` is allowed to touch those files directly.
- **Auth:** passwords are salted and hashed before they ever reach disk;
  a successful login opens a short session that the `@login_required` and
  `@admin_required` decorators check before running a command.
- **Git:** `main` stays protected; all work happens on `feature/<area>`
  branches, merged only through a reviewed pull request.

## Running the stubs

Each file can be run on its own to print the plan it documents:

```bash
python3 proposal_1_3_overview.py
python3 proposal_7_8_strategy.py
```

`proposal_4_6_design.py` is meant to be imported, not run directly — it just
defines the classes:

```bash
python3 -c "import proposal_4_6_design as m; print(m.User, m.DataStore)"
```

## Next step

Task 2 (Determine the Design) turns these stubs into an actual command
surface with `argparse`; Task 3 fills in the `NotImplementedError` bodies
with real logic.
