# pip-docs Mini Runners

This repository powers the Pip Install Python Components docs site. To make it easier to test an individual page without installing the full dependency set, each standalone Dash demo lives in its own “runner” folder with a minimal `requirements.txt`.

## Available runners

| Runner | Description | Command |
| --- | --- | --- |
| `runners/full_calendar` | Dash FullCalendar showcase (interactive builder, advanced workflows, API modal demo) | `python runners/full_calendar/run.py` |

## Running a runner

1. Create/activate a virtual environment (recommended):
   ```bash
   cd pip-docs
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install only the deps needed for the runner you want to test:
   ```bash
   pip install -r runners/full_calendar/requirements.txt
   ```
3. Start the Dash app:
   ```bash
   python runners/full_calendar/run.py
   ```
   The app listens on `http://127.0.0.1:8059` by default.

Each runner automatically adds the repo root to `PYTHONPATH` and reuses the shared `assets/` directory, so the demos behave the same way they do inside the full docs build.

## Adding a new runner

1. Create `runners/<feature-name>/run.py` and add a minimal `requirements.txt`.
2. In `run.py`, import `Path`/`sys`, push the repo root onto `sys.path`, and point Dash at `assets_folder=.../assets`.
3. Document the runner in the table above so contributors know how to start it.

This pattern keeps the install footprint tiny when you only need to verify one page, while preserving the standard docs structure (Markdown pages, components, data helpers, shared assets, etc.).
