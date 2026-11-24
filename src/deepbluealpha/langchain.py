"""LangChain tools for Deep Blue Alpha (pip install "deepbluealpha[langchain]").

    from deepbluealpha.langchain import get_tools
    tools = get_tools()          # 7 StructuredTools, ready for any LangChain / LangGraph agent
"""
from __future__ import annotations

from typing import Optional

try:
    from langchain_core.tools import StructuredTool
except ImportError as e:  # pragma: no cover
    raise ImportError('LangChain support needs: pip install "deepbluealpha[langchain]"') from e

from .client import DeepBlueAlpha
from .tooldefs import TOOLS, NOTE


def get_tools(client: Optional[DeepBlueAlpha] = None) -> list:
    """Return Deep Blue Alpha tools as LangChain StructuredTools (results are short text summaries)."""
    dba = client or DeepBlueAlpha(client_name="langchain")
    out = []
    for name, mcp_name, desc, schema in TOOLS:
        def _run(_mcp=mcp_name, **kwargs):
            return dba.call(_mcp, kwargs, as_text=True)
        out.append(StructuredTool.from_function(func=_run, name=name, description=f"{desc} {NOTE}",
                                                args_schema=schema))
    return out
