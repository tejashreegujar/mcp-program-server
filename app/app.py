from prefect import flow, task
import streamlit as st
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

# -----------------------------
# MCP SERVER CONFIG
# -----------------------------
SERVERS = {
    "program-server": {
        "transport": "stdio",
        "command": "python",
        "args": ["D:\\Python\\mcp-program-server\\main.py"]
    }
}

st.set_page_config(page_title="MCP Tool App", layout="centered")
st.title("🧰 MCP Program Tool")

# -----------------------------
# INIT MCP CLIENT
# -----------------------------
if "initialized" not in st.session_state:
    try:
        client = MultiServerMCPClient(SERVERS)
        tools = asyncio.run(client.get_tools())

        st.session_state.tools = tools
        st.session_state.tool_map = {t.name: t for t in tools}

        st.success(f"✅ Tools loaded: {[t.name for t in tools]}")
        st.session_state.initialized = True

    except Exception as e:
        st.error(f"❌ MCP connection failed: {e}")
        st.stop()

# -----------------------------
# SIMPLE INPUT UI
# -----------------------------
program_id = st.text_input("Enter Program ID")

if st.button("Get Program Details"):
    if not program_id:
        st.warning("Please enter a Program ID")
    else:
        try:
            tool = st.session_state.tool_map.get("get_program_details")

            if not tool:
                st.error("❌ Tool not found")
            else:
                result = asyncio.run(
                    tool.ainvoke({"programId": program_id})
                )

                st.subheader("📄 Result")
                st.json(result)

        except Exception as e:
            st.error(f"❌ Error: {e}")