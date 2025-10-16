# Scripts

Utility scripts for project setup and task automation.

## Available Scripts

### setup.sh
Complete setup script for the project:
- Installs UV package manager (if not already installed)
- Creates virtual environment
- Installs all dependencies
- Validates environment setup

**Usage**:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### tasks.py
Task runner for common development tasks using UV:
- `demo` - Run demo examples
- `test` - Run tests (when implemented)
- `clean` - Clean build artifacts
- `sync` - Sync dependencies

**Usage**:
```bash
# Run demo
uv run scripts/tasks.py demo

# Sync dependencies
uv run scripts/tasks.py sync
```

## Manual Commands

If you prefer to run commands directly:

```bash
# Install dependencies
uv sync

# Run demo
uv run examples/demo.py

# Run tests
uv run pytest

# Install test dependencies
uv sync --extra test
```

## More Information

- See [../docs/QUICK_REFERENCE.md](../docs/QUICK_REFERENCE.md) for all commands
- See [../README.md](../README.md) for quick start guide
