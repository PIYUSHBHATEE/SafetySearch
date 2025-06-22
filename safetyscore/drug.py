from mcp.server.fastmcp import FastMCP

def register_drug_tools(mcp: FastMCP):
    @mcp.tool()
    def search_drugs(query: str) -> str:
        """Search for drug information by name, active ingredient, or description"""
        return f"Searching drugs for: {query}"

    @mcp.tool()
    def get_drug_label(drug_name: str) -> str:
        """Get detailed drug labeling information including warnings and dosage"""
        return f"Getting drug label for: {drug_name}"

    @mcp.tool()
    def get_drug_approvals(year: int) -> str:
        """Get drug approvals for a specific year"""
        return f"Getting drug approvals for year: {year}"

    @mcp.tool()
    def check_drug_shortages() -> str:
        """Check current drug shortages and availability"""
        return "Checking current drug shortages"

    @mcp.tool()
    def search_drug_recalls(query: str) -> str:
        """Search for drug recalls by product name or company"""
        return f"Searching drug recalls for: {query}"

    @mcp.tool()
    def get_drug_adverse_events(drug_name: str) -> str:
        """Get adverse event reports for a specific drug"""
        return f"Getting adverse events for drug: {drug_name}"

    @mcp.tool()
    def check_drug_interactions(drug1: str, drug2: str) -> str:
        """Check potential interactions between two drugs"""
        return f"Checking interactions between {drug1} and {drug2}" 