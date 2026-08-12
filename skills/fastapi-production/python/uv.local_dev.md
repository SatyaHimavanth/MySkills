# uv — Local Development

## Rules
- Use `uv run` for project commands.
- Use `uv sync` to synchronize the environment.
- Use dependency groups for testing/linting/development tooling.
- Use extras for optional application capabilities.
- Keep `.python-version` aligned with the supported project Python range.

## Discovery
```bash
python --version
uv --version
uv python list
```
