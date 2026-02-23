# Publishing `pynamubot` to PyPI

## 1. Build and validate locally

```bash
uv build
```

Optional checks:

```bash
uvx twine check dist/*
```

## 2. Create the PyPI project

1. Create an account on <https://pypi.org/>.
2. If `pynamubot` is not already taken, your first upload will create the project.

## 3. Recommended: GitHub trusted publishing

This repository includes `.github/workflows/publish-pypi.yml`.

1. Push this repository to GitHub.
2. In PyPI, open your project settings and add a trusted publisher:
   - Owner: your GitHub org/user
   - Repository: this repo name
   - Workflow: `publish-pypi.yml`
   - Environment: `pypi`
3. In GitHub repo settings, create an environment named `pypi`.
4. Create a GitHub Release; the workflow will build and publish automatically.

## 4. Manual upload (fallback)

```bash
uvx twine upload dist/*
```
