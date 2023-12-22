_default:
  @just --list --list-prefix '  '

# Install poetry and pre-commit
init:
    pipx install poetry
    poetry config virtualenvs.in-project true
    pipx install pre-commit

# Install project dependencies
install:
    poetry install

# Run pre-commit
lint:
    pre-commit run -a

# Run tests
test:
    poetry run pytest
