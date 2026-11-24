"""Live smoke test against deepbluealpha.io (network required): python -m pytest tests -q"""
from deepbluealpha import DeepBlueAlpha


def test_client_all_tools():
    dba = DeepBlueAlpha(client_name="test")
    assert len(dba.list_tools()) >= 7
    assert dba.token_whale_activity("LINK", timeframe="7d")["symbol"] == "LINK"
    assert "tokens" in dba.top_whale_tokens(limit=3)
    assert "tokens" in dba.exchange_flow_leaders(limit=3)
    assert "moves" in dba.recent_whale_moves(limit=3)
    assert 0 <= dba.whale_sentiment_index()["score"] <= 100
    assert dba.platform_stats()["tracked_wallets"] > 1000
    assert "whale" in dba.daily_whale_report(as_text=True).lower()


def test_langchain_tools():
    from deepbluealpha.langchain import get_tools
    tools = {t.name: t for t in get_tools()}
    assert len(tools) == 7
    out = tools["dba_token_whale_activity"].invoke({"symbol": "ETH", "timeframe": "24h"})
    assert "ETH" in out and "not financial advice" in out.lower()
    assert tools["dba_whale_sentiment_index"].invoke({})
