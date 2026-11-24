"""Shared tool definitions used by the LangChain and AgentKit adapters."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class TokenActivityInput(BaseModel):
    symbol: str = Field(description="Token symbol, e.g. ETH, LINK, PEPE")
    timeframe: Literal["24h", "7d", "30d"] = Field("24h", description="Window to summarise")


class TopTokensInput(BaseModel):
    timeframe: Literal["1h", "24h"] = Field("24h", description="Window")
    limit: int = Field(10, ge=1, le=10, description="How many tokens (max 10)")


class FlowLeadersInput(BaseModel):
    direction: Literal["withdrawn", "deposited"] = Field(
        "withdrawn", description="withdrawn = net off exchanges; deposited = net onto exchanges")
    timeframe: Literal["24h", "7d"] = Field("7d", description="Window")
    limit: int = Field(10, ge=1, le=10, description="How many tokens (max 10)")


class RecentMovesInput(BaseModel):
    limit: int = Field(10, ge=1, le=15, description="How many moves (max 15)")
    symbol: Optional[str] = Field(None, description="Optional token symbol filter")
    min_usd: float = Field(100_000, ge=0, description="Smallest move to include, in USD")


class NoInput(BaseModel):
    pass


# (name, mcp tool, description, input model)
TOOLS = [
    ("dba_token_whale_activity", "get_token_whale_activity",
     "Tracked Ethereum whale moves for one token over 24h, 7d or 30d: value withdrawn from and deposited to "
     "exchanges, DEX swaps, net flow, accumulation-side share, whale wallet count and the largest move.",
     TokenActivityInput),
    ("dba_top_whale_tokens", "get_top_whale_tokens",
     "Ethereum tokens with the most tracked whale volume in the last 1h or 24h, with net flow for each.",
     TopTokensInput),
    ("dba_exchange_flow_leaders", "get_exchange_flow_leaders",
     "Ethereum tokens with the largest net tracked-whale flow off exchanges (withdrawn) or onto exchanges "
     "(deposited) over 24h or 7d.", FlowLeadersInput),
    ("dba_recent_whale_moves", "get_recent_whale_moves",
     "The latest large moves by tracked Ethereum whale wallets, each labeled exchange withdrawal, exchange "
     "deposit or DEX swap, optionally filtered to one token.", RecentMovesInput),
    ("dba_whale_sentiment_index", "get_whale_sentiment_index",
     "Deep Blue Alpha's daily Whale Sentiment Index (0-100, shown as Whale Fear & Greed) with its flow mix "
     "and recent history.", NoInput),
    ("dba_daily_whale_report", "get_daily_whale_report",
     "Summary of the latest daily Ethereum whale report: tracked volume, top tokens and notable moves.", NoInput),
    ("dba_platform_stats", "get_platform_stats",
     "How many whale wallets and tokens Deep Blue Alpha tracks, plus 24h exchange-flow totals.", NoInput),
]

NOTE = "Data describes past on-chain moves by tracked whale wallets. It is not financial advice."
