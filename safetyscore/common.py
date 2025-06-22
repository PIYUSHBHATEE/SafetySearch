from mcp.server.fastmcp import FastMCP

def register_common_tools(mcp: FastMCP):
    @mcp.tool()
    def search_fda_products(category: str, query: str) -> str:
        """Search across all FDA categories (food, drug, cosmetic)"""
        return f"Searching {category} products for: {query}"

    @mcp.tool()
    def get_fda_company_info(company_name: str) -> str:
        """Get information about a company across all FDA categories"""
        return f"Getting company info for: {company_name}"

    @mcp.tool()
    def compare_fda_products(product1: str, product2: str) -> str:
        """Compare two FDA-regulated products"""
        return f"Comparing products: {product1} vs {product2}"

    @mcp.tool()
    def get_fda_statistics(category: str) -> str:
        """Get FDA statistics and data for a specific category"""
        return f"Getting statistics for {category}" 