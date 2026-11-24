# deepbluealpha

Ethereum whale-flow data for AI agents, from [Deep Blue Alpha](https://deepbluealpha.io). It tracks
20,000+ Ethereum whale wallets and labels every move for what it is: a DEX buy or sell, an exchange
withdrawal or an exchange deposit.

- **No API key.** Uses Deep Blue Alpha's free public data.
- **No required dependencies** for the plain client.
- Ready-made tools for **LangChain / LangGraph** and **Coinbase AgentKit**.

```bash
pip install "deepbluealpha @ git+https://github.com/DeepBlueAlpha/deepbluealpha-python"              # plain client
pip install "deepbluealpha[langchain] @ git+https://github.com/DeepBlueAlpha/deepbluealpha-python"   # + LangChain tools
pip install "deepbluealpha[agentkit] @ git+https://github.com/DeepBlueAlpha/deepbluealpha-python"    # + Coinbase AgentKit action provider
```

## Plain Python

```python
from deepbluealpha import DeepBlueAlpha

dba = DeepBlueAlpha()
dba.token_whale_activity("LINK", timeframe="7d")       # dict
dba.exchange_flow_leaders(direction="withdrawn")       # tokens whales pulled off exchanges
print(dba.whale_sentiment_index(as_text=True))         # short text summary
```

## LangChain / LangGraph

```python
from deepbluealpha.langchain import get_tools
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools=get_tools())
agent.invoke({"messages": [("user", "What have whales done with LINK this week?")]})
```

## Coinbase AgentKit

```python
from coinbase_agentkit import AgentKit, AgentKitConfig
from deepbluealpha.agentkit import deepbluealpha_action_provider

agentkit = AgentKit(AgentKitConfig(
    wallet_provider=wallet_provider,
    action_providers=[deepbluealpha_action_provider()],
))
```

## Tools

| Tool | What it returns |
|---|---|
| `token_whale_activity` | One token over 24h / 7d / 30d: withdrawn from and deposited to exchanges, DEX swaps, net flow, whale count, largest move |
| `top_whale_tokens` | Tokens with the most tracked whale volume (1h / 24h) |
| `exchange_flow_leaders` | Tokens whales moved most off or onto exchanges (24h / 7d) |
| `recent_whale_moves` | Latest large whale moves, each labeled exchange or DEX |
| `whale_sentiment_index` | Daily 0–100 Whale Sentiment Index (Whale Fear & Greed) |
| `daily_whale_report` | Latest daily whale report summary |
| `platform_stats` | Coverage and 24h exchange-flow totals |

Also available as an MCP server for Claude, ChatGPT, Cursor and other MCP clients:
`https://deepbluealpha.io/mcp`. Teams that need full history, webhooks or bulk files:
[deepbluealpha.io/business](https://deepbluealpha.io/business).

Data is CC-BY-4.0: credit "Deep Blue Alpha (deepbluealpha.io)". It describes past on-chain moves
by tracked whale wallets and is not financial advice.

MIT licensed.
