from mcp.server.fastmcp import FastMCP
from safetyscore.tools.food import register_food_tools
from safetyscore.tools.cosmetic import register_cosmetic_tools
from safetyscore.tools.common import register_common_tools

# Create the MCP server
mcp = FastMCP("SafetySearch")

# Register all the tools from their respective modules
register_food_tools(mcp)
register_cosmetic_tools(mcp)
register_common_tools(mcp)

def main():
    """Main function to run the SafetySearch MCP server."""
    mcp.run()

if __name__ == "__main__":
    main() 