"""
TheSeedAPI client for interacting with the API endpoints.
"""

import time
from functools import cached_property
from types import TracebackType
from typing import Any, Optional

import requests
import structlog
from typing_extensions import Self

from ..__version__ import __title__, __version__
from ..api.schemas import *


class Limiter:
    """
    A simple rate limiter to enforce a minimum interval between requests.

    Note that NamuWiki's soft rate limit is 1 request per second. Setting interval_seconds to 1.0 is recommended.
    """

    def __init__(self, interval_seconds: float) -> None:
        """
        Initialize the rate limiter.

        :param interval_seconds: The minimum interval between requests in seconds. Setting this to 0 disables rate limiting by not calling sleep at all.
        """
        self.interval = float(interval_seconds)
        if self.interval <= 0.0:
            self.acquire = lambda: None
        self.last = float("-inf")

    def acquire(self) -> None:
        """
        Acquire the limiter before making a request. This will block if necessary to enforce the rate limit.
        """
        now = time.monotonic()
        elapsed = now - self.last
        wait = self.interval - elapsed
        time.sleep(max(0.0, wait))
        self.last = time.monotonic()

    def __enter__(self) -> Self:
        self.acquire()
        return self

    def __exit__(self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        pass


class TheSeedAPIClient:
    """
    Client for interacting with TheSeedAPI endpoints.
    """

    def __init__(
        self,
        base_url: str,
        api_token: str,
        logger: Optional[structlog.stdlib.BoundLogger] = None,
        limiter: Optional[Limiter] = None,
    ) -> None:
        """
        Initialize TheSeedAPI with the API token and base URL.

        :param base_url: The base URL for the API endpoints.
        :param api_token: The API token string.
        :param session: An optional requests session to use for the API calls. Defaults to None (creates a new session).
        :param logger: An optional structlog logger. Defaults to None (creates a new logger).
        :param limiter: An optional rate limiter. Defaults to None (no limiter).
        """
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
        }
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.logger = logger if logger is not None else structlog.get_logger(__name__)
        self.limiter = limiter if limiter is not None else Limiter(0.0)

    @cached_property
    def user_agent(self) -> str:
        """
        Get the user agent string for the API client.

        :return: The user agent string.
        """
        return f"{requests.utils.default_user_agent()} {__title__}/{__version__}"

    def edit_get(self, document: str) -> EditGETResponse:
        """
        Fetch the content of the document.

        :param document: The document to fetch.
        :return response: A dictionary containing the document text, existence status, and edit token.
        """
        url = f"{self.base_url}/edit/{document}"
        with self.limiter, self.session.get(url) as response:
            response.raise_for_status()
            return EditGETResponse.model_validate(response.json())

    def edit_post(self, document: str, body: EditPOSTBody) -> EditPOSTResponse:
        """
        Edit the document with new text.

        :param document: The document to edit.
        :param body: A dictionary containing the new text, log message, and edit token.
        :return response: A dictionary containing the revision number of the edit.
        """
        url = f"{self.base_url}/edit/{document}"
        with self.limiter, self.session.post(url, json=body) as response:
            response.raise_for_status()
            return EditPOSTResponse.model_validate(response.json())

    def backlink(
        self,
        document: str,
        namespace: Optional[str] = None,
        flag: Optional[int] = None,
        fromm: Optional[str] = None,
        until: Optional[str] = None,
    ) -> BacklinkResponse:
        """
        Retrieve backlinks for the document.

        Note: The behavior when both fromm and until are not None is not well-defined.

        :param document: The document to retrieve backlinks for.
        :param namespace: The namespace of documents to query.
        :param flag: Filter on how document is linked to this document.
        :param fromm: Paginate from this document (inclusive). Note the double 'm' to avoid Python keyword conflict.
        :param until: Paginate until this document (inclusive).
        :return response: A dictionary containing the namespaces, backlinks, and from/to information.
        """
        url = f"{self.base_url}/backlink/{document}"
        params: dict[str, Any] = {
            "namespace": namespace,
            "flag": flag,
            "from": fromm,
            "until": until,
        }

        with self.limiter, self.session.get(url, params=params) as response:
            response.raise_for_status()
            return BacklinkResponse.model_validate(response.json())

    def discuss(self, document: str) -> list[DiscussResponse]:
        """
        Fetch discussions on the document.

        :param document: The document to fetch discussions for.
        :return response: A list of dictionaries containing the slug, topic, updated date, and status of the discussions.
        """
        url = f"{self.base_url}/discuss/{document}"
        with self.limiter, self.session.get(url) as response:
            response.raise_for_status()
            return [DiscussResponse.model_validate(item) for item in response.json()]

    def __del__(self) -> None:
        self.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        self.session.close()
