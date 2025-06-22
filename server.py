from mcp.server.fastmcp import FastMCP
from safetyscore.tools.food import register_food_tools

# Create the MCP server
mcp = FastMCP("SafetySearch")

# Register all the tools from their respective modules
register_food_tools(mcp)

def main():
    """Main function to run the SafetySearch MCP server."""
    mcp.run()

if __name__ == "__main__":
    main() 