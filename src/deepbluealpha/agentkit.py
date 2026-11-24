"""Coinbase AgentKit action provider for Deep Blue Alpha (pip install "deepbluealpha[agentkit]").

    from coinbase_agentkit import AgentKit, AgentKitConfig
    from deepbluealpha.agentkit import deepbluealpha_action_provider

    agentkit = AgentKit(AgentKitConfig(wallet_provider=..., action_providers=[deepbluealpha_action_provider()]))

Read-only data actions; no wallet access, works on every network.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from coinbase_agentkit import ActionProvider, create_action
    from coinbase_agentkit.network import Network
except ImportError as e:  # pragma: no cover
    raise ImportError('AgentKit support needs: pip install "deepbluealpha[agentkit]"') from e

from .client import DeepBlueAlpha
from .tooldefs import (TOOLS, NOTE, TokenActivityInput, TopTokensInput, FlowLeadersInput,
                       RecentMovesInput, NoInput)

_DESC = {name: f"{desc} {NOTE}" for name, _mcp, desc, _s in TOOLS}


class DeepBlueAlphaActionProvider(ActionProvider):
    """Ethereum whale-flow data from Deep Blue Alpha."""

    def __init__(self, client: Optional[DeepBlueAlpha] = None):
        super().__init__("deepbluealpha", [])
        self.dba = client or DeepBlueAlpha(client_name="agentkit")

    def _run(self, tool: str, args: dict[str, Any]) -> str:
        try:
            return self.dba.call(tool, args, as_text=True)
        except Exception as e:   # agents get a readable error instead of a crash
            return f"Deep Blue Alpha request failed: {e}"

    @create_action(name="token_whale_activity", description=_DESC["dba_token_whale_activity"],
                   schema=TokenActivityInput)
    def token_whale_activity(self, args: dict[str, Any]) -> str:
        return self._run("get_token_whale_activity", args)

    @create_action(name="top_whale_tokens", description=_DESC["dba_top_whale_tokens"], schema=TopTokensInput)
    def top_whale_tokens(self, args: dict[str, Any]) -> str:
        return self._run("get_top_whale_tokens", args)

    @create_action(name="exchange_flow_leaders", description=_DESC["dba_exchange_flow_leaders"],
                   schema=FlowLeadersInput)
    def exchange_flow_leaders(self, args: dict[str, Any]) -> str:
        return self._run("get_exchange_flow_leaders", args)

    @create_action(name="recent_whale_moves", description=_DESC["dba_recent_whale_moves"], schema=RecentMovesInput)
    def recent_whale_moves(self, args: dict[str, Any]) -> str:
        return self._run("get_recent_whale_moves", args)

    @create_action(name="whale_sentiment_index", description=_DESC["dba_whale_sentiment_index"], schema=NoInput)
    def whale_sentiment_index(self, args: dict[str, Any]) -> str:
        return self._run("get_whale_sentiment_index", {})

    @create_action(name="daily_whale_report", description=_DESC["dba_daily_whale_report"], schema=NoInput)
    def daily_whale_report(self, args: dict[str, Any]) -> str:
        return self._run("get_daily_whale_report", {})

    @create_action(name="platform_stats", description=_DESC["dba_platform_stats"], schema=NoInput)
    def platform_stats(self, args: dict[str, Any]) -> str:
        return self._run("get_platform_stats", {})

    def supports_network(self, network: Network) -> bool:
        return True   # read-only data; no chain interaction


def deepbluealpha_action_provider(client: Optional[DeepBlueAlpha] = None) -> DeepBlueAlphaActionProvider:
    return DeepBlueAlphaActionProvider(client)
