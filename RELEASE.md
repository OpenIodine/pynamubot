# Manual Release (uv/uvx)

Use this flow to manage versions and publish manually.

## 1. Bump version

Choose one:

```bash
uv version --bump patch --frozen
uv version --bump minor --frozen
uv version --bump major --frozen
```

## 2. Build distributions

```bash
uv build
```

## 3. Validate distributions

```bash
uvx twine check dist/*
```

## 4. Upload to PyPI

```bash
uvx twine upload dist/*
```

## 5. (Optional) Commit and tag release

```bash
git add pyproject.toml
git commit -m "chore(release): v$(uv version --short)"
git tag "v$(uv version --short)"
git push origin HEAD --tags
```
