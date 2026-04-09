from fastmcp import FastMCP
from dotenv import load_dotenv
from Tool.program_tool import program_tool

load_dotenv()

mcp = FastMCP("Program Server")

mcp.tool()(program_tool)

if __name__ == "__main__":
     mcp.run(transport="streamable_http", host="0.0.0.0", port=8000)