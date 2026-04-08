from fastmcp import FastMCP
from Tool.program_tool import get_program_details
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP("program-server")  # ✅ MUST be named 'mcp'

mcp.tool()(get_program_details)

if __name__ == "__main__":
    mcp.run()