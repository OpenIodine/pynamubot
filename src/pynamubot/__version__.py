from importlib.metadata import PackageNotFoundError, version

__title__ = "pynamubot"
__description__ = "Python client library for TheSeed-based wiki APIs such as NamuWiki."
__author__ = "Iodine at NamuWiki"
__license__ = "MIT"
__copyright__ = "Copyright Iodine at NamuWiki"

try:
    __version__ = version(__title__)
except PackageNotFoundError:
    __version__ = "0.0.0"
