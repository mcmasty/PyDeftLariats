# Publishing PyDeftLariats to PyPI

This document explains how to publish PyDeftLariats to PyPI using GitHub Actions with trusted publishing.

## Prerequisites

### Set Up Trusted Publishing on PyPI

Trusted publishing eliminates the need for API tokens by using OpenID Connect (OIDC) to verify your identity through GitHub Actions.

#### For Production PyPI:

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name**: `PyDeftLariats`
   - **Owner**: `mcmasty` (your GitHub username)
   - **Repository name**: `PyDeftLariats`
   - **Workflow name**: `publish-to-pypi.yml`
   - **Environment name**: `pypi`
4. Click "Add"

#### For TestPyPI (for testing):

1. Go to https://test.pypi.org/manage/account/publishing/
2. Follow the same steps as above but use environment name: `testpypi`

> **Note**: You only need to set up the pending publisher once. After the first successful publish, PyPI will remember the configuration.

## Publishing Methods

### Method 1: Automatic Publishing via GitHub Release (Recommended)

This is the easiest method and uses trusted publishing:

1. **Update the version** (see Version Management section below)

2. **Create a GitHub Release**:
   ```bash
   # Tag the release
   git tag v1.2.12
   git push origin v1.2.12
   
   # Or use GitHub CLI
   gh release create v1.2.12 --generate-notes
   ```

3. **The workflow automatically**:
   - Builds the package with uv
   - Publishes to PyPI using trusted publishing
   - Uploads distribution files to the GitHub release

### Method 2: Manual Test Publishing

To test publishing to TestPyPI before a real release:

1. Go to: https://github.com/mcmasty/PyDeftLariats/actions/workflows/publish-to-pypi.yml
2. Click "Run workflow"
3. Select "testpypi" from the dropdown
4. Click "Run workflow"

This will publish to https://test.pypi.org/project/PyDeftLariats/

### Method 3: Local Manual Publishing

If you need to publish locally (not recommended for production):

```bash
# Build the package
uv build

# Publish to TestPyPI
uv run twine upload --repository testpypi dist/*

# Publish to PyPI (production)
uv run twine upload dist/*
```

For local publishing, you'll need to set up API tokens in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # your PyPI token

[testpypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # your TestPyPI token
```

## Version Management

This project uses `bump-my-version` for version management.

### Current Version

Check current version:
```bash
cat VERSION
# or
grep __version__ src/deftlariat/__init__.py
```

### Bump Version

```bash
# Install dev dependencies
uv sync --all-extras

# Bump patch version (1.2.11 -> 1.2.12)
uv run bump-my-version bump patch

# Bump minor version (1.2.11 -> 1.3.0)
uv run bump-my-version bump minor

# Bump major version (1.2.11 -> 2.0.0)
uv run bump-my-version bump major
```

This automatically updates:
- `VERSION` file
- `src/deftlariat/__init__.py`
- `pyproject.toml` (need to add this - see below)
- Creates a git commit and tag

### Add pyproject.toml to bump-my-version

Currently, `bump-my-version` doesn't update `pyproject.toml`. Let's fix that in `.bumpversion.toml`.

## Pre-Publishing Checklist

Before publishing a new version:

- [ ] All tests pass: `uv run python -m unittest discover -s ./tests`
- [ ] Version is bumped: `uv run bump-my-version bump [patch|minor|major]`
- [ ] `HISTORY.rst` is updated with changes
- [ ] Changes are committed and pushed
- [ ] GitHub release is created with tag (e.g., `v1.2.12`)

## Testing the Package

After publishing to TestPyPI, test installation:

```bash
# Create a test environment
uv venv test-env
source test-env/bin/activate  # or test-env\Scripts\activate on Windows

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ PyDeftLariats

# Test the CLI
deft --help

# Deactivate and clean up
deactivate
rm -rf test-env
```

## Workflow Features

The automated workflow provides:

- ✅ **Trusted publishing** - No API tokens needed
- ✅ **TestPyPI support** - Test before production release
- ✅ **GitHub Release assets** - Distribution files attached to releases
- ✅ **SLSA provenance** - Supply chain security (via separate workflow)
- ✅ **Manual trigger** - Publish on demand for testing

## Troubleshooting

### Trusted Publishing Not Working

1. Verify the pending publisher is set up correctly on PyPI
2. Check that environment name matches (`pypi` or `testpypi`)
3. Ensure the workflow file name is exactly `publish-to-pypi.yml`
4. Verify repository owner and name match exactly

### Version Mismatch

If you see version mismatches:

```bash
# Check all version locations
cat VERSION
grep __version__ src/deftlariat/__init__.py
grep '^version' pyproject.toml
```

These should all match. Use `bump-my-version` to keep them in sync.

### Build Failures

If the build fails:

```bash
# Test locally
uv build

# Check for any uncommitted changes
git status

# Ensure pyproject.toml is valid
uv sync
```

## Resources

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions - pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
- [uv Documentation](https://docs.astral.sh/uv/)
- [bump-my-version Documentation](https://github.com/callowayproject/bump-my-version)
