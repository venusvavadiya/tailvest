# tailvest

WIP

## Development Setup

### Backend:

In the project root, create and activate virtual env:
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
