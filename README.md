# pynamubot

Python client library for TheSeed-based wiki APIs (for example, NamuWiki).

## Installation

```bash
pip install pynamubot
```

If you need Selenium-based utilities:

```bash
pip install "pynamubot[puppet]"
```

## Quick start

```python
from pynamubot.api import TheSeedAPIClient

client = TheSeedAPIClient(
    base_url="https://namu.wiki/api",
    api_token="YOUR_API_TOKEN",
)

response = client.edit_get("TestDocument")
print(response.exists, response.token)
```

## Requirements

- Python 3.9+
- A valid API token issued by the target wiki

## Reference

- TheSeed API docs: <https://doc.theseed.io/>
