# Publishing to PyPI

This guide covers how to build and publish the Dremio CLI to PyPI.

## Prerequisites

```bash
pip install build twine
```

## Build Distribution

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source and wheel distributions
python -m build
```

This creates:
- `dist/dremio-cli-1.0.0.tar.gz` - Source distribution
- `dist/dremio_cli-1.0.0-py3-none-any.whl` - Wheel distribution

## Test Distribution Locally

```bash
# Install from local wheel
pip install dist/dremio_cli-1.0.0-py3-none-any.whl

# Test installation
dremio --version
dremio --help
```

## Upload to Test PyPI (Optional)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ dremio-cli
```

## Upload to PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

You'll be prompted for your PyPI credentials or API token.

## Using API Token

Create an API token at https://pypi.org/manage/account/token/

```bash
# Set token in ~/.pypirc
cat > ~/.pypirc <<EOF
[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE
EOF

chmod 600 ~/.pypirc
```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## Version Bumping

Update version in `pyproject.toml`:

```toml
[project]
version = "1.0.1"  # Increment version
```

## Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md
- [ ] Run tests: `pytest`
- [ ] Build distribution: `python -m build`
- [ ] Test locally: `pip install dist/*.whl`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Create GitHub release
- [ ] Verify installation: `pip install dremio-cli`

## Post-Publication

After publishing, users can install with:

```bash
pip install dremio-cli
```

## Troubleshooting

### Build Fails

```bash
# Check pyproject.toml syntax
python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"

# Verify package structure
python -m build --sdist --wheel --outdir dist/ .
```

### Upload Fails

```bash
# Check distribution
twine check dist/*

# Verify credentials
twine upload --repository testpypi dist/*
```
