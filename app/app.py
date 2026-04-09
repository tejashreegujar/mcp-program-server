import streamlit as st
import asyncio
import re
import json

from langchain_mcp_adapters.client import MultiServerMCPClient

# -----------------------------
# MCP CONFIG (FIX YOUR PATH)
# -----------------------------
#local
SERVERS = {
    "program-server": {
        "transport": "stdio",
        "command": r"D:\Python\mcp-program-server\venv\Scripts\python.exe",
        "args": [r"D:\Python\mcp-program-server\main.py"]
    }
}
#Production
# SERVERS = {
#     "program-server": {
#         "transport": "stdio",
#         "command": r"Python",
#         "args": [r"main.py"]
#     }
# }
st.set_page_config(page_title="Smart Program Chat", layout="centered")
st.title("🧠 Smart Program Chat")

# -----------------------------
# INIT SESSION STATE
# -----------------------------
if "init" not in st.session_state:
    try:
        client = MultiServerMCPClient(SERVERS)
        tools = asyncio.run(client.get_tools())

        st.session_state.tool_map = {t.name: t for t in tools}
        st.session_state.init = True

        st.success("✅ MCP Connected")

    except Exception as e:
        st.error(f"❌ MCP Failed: {e}")
        st.stop()

# -----------------------------
# CHAT MEMORY
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def extract_id(text):
    match = re.search(r"\d+", text)
    return match.group() if match else None


def get_last_program_id():
    for msg in reversed(st.session_state.history):
        match = re.search(r"\d+", str(msg["content"]))
        if match:
            return match.group()
    return None


def detect_action(text):
    text = text.lower()

    if "payout" in text:
        return "payout"
    elif "status" in text:
        return "status"
    elif "detail" in text or "program" in text:
        return "details"
    return "details"


# ✅ NEW: CLEAN MCP RESPONSE
def clean_response(result):
    try:
        # MCP returns list sometimes
        if isinstance(result, list) and len(result) > 0:
            item = result[0]

            if isinstance(item, dict) and "text" in item:
                parsed = json.loads(item["text"])

                # Handle API error
                if "statusCode" in parsed:
                    return {
                        "error": parsed.get("message"),
                        "details": parsed.get("details")
                    }

                return parsed

        return result

    except Exception:
        return result


# -----------------------------
# RENDER CHAT HISTORY
# -----------------------------
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], dict):
            st.json(msg["content"])
        else:
            st.write(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Ask: Get program 127 or Show payout")

if user_input:
    st.chat_message("user").write(user_input)

    st.session_state.history.append({
        "role": "user",
        "content": user_input
    })

    # -----------------------------
    # SMART LOGIC
    # -----------------------------
    program_id = extract_id(user_input)

    if not program_id:
        program_id = get_last_program_id()

    action = detect_action(user_input)

    if not program_id and action != "status":
        response = "❌ Please provide a program ID"

        st.chat_message("assistant").write(response)

        st.session_state.history.append({
            "role": "assistant",
            "content": response
        })

    else:
        try:
            tool = st.session_state.tool_map["program_tool"]

            raw_result = asyncio.run(
                tool.ainvoke({
                    "programId": program_id or "",
                    "action": action
                })
            )

            # ✅ CLEAN RESULT
            result = clean_response(raw_result)

            # -----------------------------
            # HANDLE API ERRORS NICELY
            # -----------------------------
            if isinstance(result, dict) and "error" in result:
                st.chat_message("assistant").error(f"❌ {result['error']}")
            else:
                with st.chat_message("assistant"):
                    st.json(result)

            # Save
            st.session_state.history.append({
                "role": "assistant",
                "content": result
            })

        except Exception as e:
            error_msg = f"❌ Error: {e}"

            st.chat_message("assistant").write(error_msg)

            st.session_state.history.append({
                "role": "assistant",
                "content": error_msg
            })