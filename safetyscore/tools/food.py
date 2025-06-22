import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
from ..api_client import ApiClient

RECALL_API_URL = "https://api.fda.gov/food/enforcement.json"
ADVERSE_EVENT_API_URL = "https://api.fda.gov/food/event.json"
api_client = ApiClient()

def register_food_tools(mcp: FastMCP):
    @mcp.tool()
    async def search_recalls_by_product_description(query: str) -> str:
        """Searches for food recalls by matching a query against the product description."""
        search_query = f'product_description:"{query}"+AND+status:Ongoing'
        # Manually construct the full URL to avoid encoding issues
        full_url = f"{RECALL_API_URL}?search={search_query}&limit=5"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No ongoing food recalls found for '{query}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found {len(results)} ongoing food recalls for '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_product_type(product_type: str) -> str:
        """Searches for recalls where the product description contains a product type (e.g., 'Bakery')."""
        search_query = f'product_description:"{product_type}"'
        full_url = f"{RECALL_API_URL}?search={search_query}&limit=5"

        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for product type '{product_type}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found recalls for product type '{product_type}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_specific_product(product_name: str) -> str:
        """Checks for any ongoing recalls for a single, specific food product."""
        search_query = f'product_description:"{product_name}"+AND+status:Ongoing'
        full_url = f"{RECALL_API_URL}?search={search_query}&limit=1"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        if data.get("results"):
            recall = data["results"][0]
            reason = recall.get('reason_for_recall', 'N/A')
            company = recall.get('recalling_firm', 'N/A')
            return f"Found an ongoing recall for '{product_name}': Reason - {reason}, Company - {company}."
        else:
            return f"No ongoing recalls found for '{product_name}'."

    @mcp.tool()
    async def search_recalls_by_classification(classification: str) -> str:
        """Searches for food recalls by a specific classification (e.g., 'Class I')."""
        search_query = f'classification:"{classification}"'
        full_url = f"{RECALL_API_URL}?search={search_query}&limit=5"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for classification '{classification}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found recalls for classification '{classification}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_reason(reason: str) -> str:
        """Searches for food recalls by the reason for the recall (e.g., 'Salmonella')."""
        search_query = f'reason_for_recall:"{reason}"'
        full_url = f"{RECALL_API_URL}?search={search_query}&limit=5"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for reason '{reason}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found recalls for reason '{reason}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_code_info(lot_code: str) -> str:
        """Searches for food recalls by a specific lot code or other code info."""
        search_query = f'code_info:"{lot_code}"'
        full_url = f"{RECALL_API_URL}?search={search_query}&limit=5"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for lot code '{lot_code}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found recalls for lot code '{lot_code}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_date(days: int = 30) -> str:
        """Searches for food recalls initiated in the last N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_date_str = start_date.strftime('%Y%m%d')
        end_date_str = end_date.strftime('%Y%m%d')

        search_query = f"recall_initiation_date:[{start_date_str}+TO+{end_date_str}]"
        full_url = f"{RECALL_API_URL}?search={search_query}&sort=recall_initiation_date:desc&limit=10"

        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found in the last {days} days."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')} on {r.get('recall_initiation_date', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found {len(results)} food recalls in the last {days} days:\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_critical_safety_alerts() -> str:
        """Gets high-priority food safety alerts (recent Class I recalls)."""
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
        search_query = f'classification:"Class I"+AND+recall_initiation_date:[{seven_days_ago}+TO+{datetime.now().strftime("%Y%m%d")}]'
        full_url = f"{RECALL_API_URL}?search={search_query}&sort=recall_initiation_date:desc&limit=5"

        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error
            
        results = data.get("results", [])
        if not results:
            return "No critical food safety alerts (Class I recalls) found in the last 7 days."
        
        alerts = [f"- {r.get('product_description', 'N/A')} due to {r.get('reason_for_recall', 'N/A')}." for r in results]
        return "Recent critical food safety alerts:\n" + "\n".join(alerts)

    @mcp.tool()
    async def get_recall_trends_by_reason() -> str:
        """Analyzes the most common reasons for food recalls in the last 90 days."""
        ninety_days_ago = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
        search_query = f'recall_initiation_date:[{ninety_days_ago}+TO+{datetime.now().strftime("%Y%m%d")}]'
        full_url = f"{RECALL_API_URL}?search={search_query}&count=reason_for_recall.exact"

        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return "Could not find any recall trends in the last 90 days."

        trends = [f"- {item['term']}: {item['count']} recalls" for item in results[:5]] # Top 5 reasons
        return "Top food recall reasons in the last 90 days:\n" + "\n".join(trends)

    @mcp.tool()
    async def search_adverse_events_by_product(product_name: str) -> str:
        """Searches for adverse event reports related to a specific food product."""
        search_query = f'products.name_brand:"{product_name}"'
        full_url = f"{ADVERSE_EVENT_API_URL}?search={search_query}&limit=5"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No adverse event reports found for '{product_name}'."

        formatted_results = [
            (
                f"- Report Date: {r.get('date_created', 'N/A')}\n"
                f"  Symptoms: {', '.join(r.get('reactions', ['N/A']))}\n"
                f"  Outcome: {', '.join(r.get('outcomes', ['N/A']))}"
            )
            for r in results
        ]
        
        return f"Found {len(results)} adverse event reports for '{product_name}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def get_symptom_summary_for_product(product_name: str) -> str:
        """Gets a list of reported symptoms (reactions) for a specific food product."""
        search_query = f'products.name_brand:"{product_name}"'
        full_url = f"{ADVERSE_EVENT_API_URL}?search={search_query}&count=reactions.exact"
        
        data, error = await api_client.make_request(full_url, params=None)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No reported symptoms found for '{product_name}'."

        symptoms = [f"- {item['term']} ({item['count']} reports)" for item in results]
        
        return f"Reported symptoms for '{product_name}':\n" + "\n".join(symptoms) 