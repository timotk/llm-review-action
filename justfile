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

# Make v1 release
release:
    git tag -d v1 && git push origin :refs/tags/v1
    git tag -a -m "Release v1" v1 && git push --follow-tags
