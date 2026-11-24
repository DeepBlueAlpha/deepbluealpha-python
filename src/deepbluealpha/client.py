"""Tiny client for Deep Blue Alpha's public Ethereum whale-flow data.

Talks to the public MCP endpoint (https://deepbluealpha.io/mcp) with plain JSON-RPC over HTTPS.
No API key, no extra dependencies (standard library only).

    from deepbluealpha import DeepBlueAlpha
    dba = DeepBlueAlpha()
    dba.token_whale_activity("LINK", timeframe="7d")

Every method returns a dict of structured data. Add ``as_text=True`` to get the short
human-readable summary the same tool returns (useful as an LLM tool result).
Data describes past on-chain moves by tracked whale wallets. It is not financial advice.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Optional

from . import __version__

DEFAULT_URL = "https://deepbluealpha.io/mcp"


class DeepBlueAlphaError(RuntimeError):
    """The request failed or the tool returned an error."""


class DeepBlueAlpha:
    def __init__(self, url: str = DEFAULT_URL, timeout: float = 20.0, client_name: str = "python"):
        self.url = url
        self.timeout = timeout
        self.user_agent = f"deepbluealpha-{client_name}/{__version__}"
        self._id = 0

    # ── low level ────────────────────────────────────────────────────────────
    def call(self, tool: str, arguments: Optional[dict] = None, as_text: bool = False) -> Any:
        """Call one tool by name. Returns structured data (dict) or the text summary."""
        self._id += 1
        body = json.dumps({"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                           "params": {"name": tool, "arguments": {k: v for k, v in (arguments or {}).items()
                                                                   if v is not None}}}).encode()
        req = urllib.request.Request(self.url, data=body, method="POST", headers={
            "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
            "User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                raw = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise DeepBlueAlphaError(f"HTTP {e.code} from Deep Blue Alpha") from e
        except urllib.error.URLError as e:
            raise DeepBlueAlphaError(f"could not reach Deep Blue Alpha: {e.reason}") from e
        data = json.loads(raw[raw.index("{"):])          # tolerates an SSE "data:" prefix
        if "error" in data:
            raise DeepBlueAlphaError(str(data["error"].get("message", data["error"])))
        res = data.get("result") or {}
        text = "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise DeepBlueAlphaError(text or "tool error")
        if as_text:
            return text
        return res.get("structuredContent") if res.get("structuredContent") is not None else {"text": text}

    def list_tools(self) -> list:
        self._id += 1
        body = json.dumps({"jsonrpc": "2.0", "id": self._id, "method": "tools/list"}).encode()
        req = urllib.request.Request(self.url, data=body, method="POST", headers={
            "Content-Type": "application/json", "Accept": "application/json", "User-Agent": self.user_agent})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            raw = r.read().decode("utf-8")
        return json.loads(raw[raw.index("{"):])["result"]["tools"]

    # ── one method per tool ──────────────────────────────────────────────────
    def token_whale_activity(self, symbol: str, timeframe: str = "24h", as_text: bool = False):
        """Tracked whale moves for one token over 24h, 7d or 30d."""
        return self.call("get_token_whale_activity", {"symbol": symbol, "timeframe": timeframe}, as_text)

    def top_whale_tokens(self, timeframe: str = "24h", limit: int = 10, as_text: bool = False):
        """Tokens with the most tracked whale volume in the last 1h or 24h."""
        return self.call("get_top_whale_tokens", {"timeframe": timeframe, "limit": limit}, as_text)

    def exchange_flow_leaders(self, direction: str = "withdrawn", timeframe: str = "7d", limit: int = 10,
                              as_text: bool = False):
        """Tokens whales moved most off ("withdrawn") or onto ("deposited") exchanges."""
        return self.call("get_exchange_flow_leaders",
                         {"direction": direction, "timeframe": timeframe, "limit": limit}, as_text)

    def recent_whale_moves(self, limit: int = 10, symbol: Optional[str] = None, min_usd: float = 100_000,
                           as_text: bool = False):
        """Latest large moves by tracked whale wallets, each labeled exchange or DEX."""
        return self.call("get_recent_whale_moves", {"limit": limit, "symbol": symbol, "min_usd": min_usd}, as_text)

    def whale_sentiment_index(self, as_text: bool = False):
        """Daily Whale Sentiment Index (0-100, also shown as Whale Fear & Greed)."""
        return self.call("get_whale_sentiment_index", {}, as_text)

    def daily_whale_report(self, as_text: bool = False):
        """Summary of the latest daily Ethereum whale report."""
        return self.call("get_daily_whale_report", {}, as_text)

    def platform_stats(self, as_text: bool = False):
        """How many wallets/tokens are tracked, plus 24h exchange-flow totals."""
        return self.call("get_platform_stats", {}, as_text)
