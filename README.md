# tailvest

WIP

## Development Setup

### Backend:

In the project root, create and activate the virtual env:
```
uv venv
source .venv/bin/activate
```

Install dependencies:
```
uv sync
```

To run the FastAPI server:
```
fastapi dev main.py
```

To run ruff:
```
uv run ruff check --fix
uv run ruff format
```

### Frontend:

Switch to the `/frontend` directory.

Install dependencies:
```
pnpm install
```

To run the frontend:
```
pnpm dev
```

Once running, visit http://localhost:5173 to view the app.
