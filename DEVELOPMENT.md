# Mailfeed Development

## Setup

Install in development mode:

```bash
cd apps/mailfeed
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Building

Build wheel and source distribution:

```bash
python -m build
```

This creates:
- `dist/mailfeed-0.1.0-py3-none-any.whl` (wheel)
- `dist/mailfeed-0.1.0.tar.gz` (source distribution)

## Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=mailfeed --cov-report=html
```

## Code Quality

Format code:

```bash
black src/
```

Lint:

```bash
flake8 src/
```

Type check:

```bash
mypy src/
```

## Publishing

To PyPI:

```bash
python -m build
python -m twine upload dist/*
```

To private repository or local installation:

```bash
pip install dist/mailfeed-0.1.0-py3-none-any.whl
```

## Using in Other Projects

After building, install in nibbler:

```bash
cd apps/nibbler
pip install ../mailfeed/dist/mailfeed-0.1.0-py3-none-any.whl
```

Or add to requirements.txt:

```
../mailfeed/dist/mailfeed-0.1.0-py3-none-any.whl
```

Or reference from Git:

```
mailfeed @ git+https://github.com/randallhunt/orangeshovel.git@main#subdirectory=apps/mailfeed
```
