from mcp.server.fastmcp import FastMCP
from safetyscore.tools.food import register_food_tools
from safetyscore.tools.drug import register_drug_tools
from safetyscore.tools.cosmetic import register_cosmetic_tools
from safetyscore.tools.common import register_common_tools

# Create the MCP server
mcp = FastMCP("SafetySearch")

# Register all the tools from their respective modules
register_food_tools(mcp)
register_drug_tools(mcp)
register_cosmetic_tools(mcp)
register_common_tools(mcp)

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run()) 