"""Deep Blue Alpha — Ethereum whale-flow data for Python, LangChain and Coinbase AgentKit agents."""
__version__ = "0.1.0"

from .client import DeepBlueAlpha, DeepBlueAlphaError, DEFAULT_URL  # noqa: E402

__all__ = ["DeepBlueAlpha", "DeepBlueAlphaError", "DEFAULT_URL", "__version__"]
