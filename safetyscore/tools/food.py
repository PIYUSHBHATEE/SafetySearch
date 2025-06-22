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
        search_query = f'product_description:"{query}"'
        
        # Use params to let httpx handle URL encoding properly
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(RECALL_API_URL, params=params)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for '{query}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found {len(results)} food recalls for '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_product_type(product_type: str) -> str:
        """Searches for recalls where the product description contains a product type (e.g., 'Bakery')."""
        search_query = f'product_description:"{product_type}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }

        data, error = await api_client.make_request(RECALL_API_URL, params=params)
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
        search_query = f'product_description:"{product_name}"'
        
        # Use params to let httpx handle URL encoding properly
        params = {
            'search': search_query,
            'limit': 1
        }
        
        data, error = await api_client.make_request(RECALL_API_URL, params=params)
        if error:
            return error

        if data.get("results"):
            recall = data["results"][0]
            reason = recall.get('reason_for_recall', 'N/A')
            company = recall.get('recalling_firm', 'N/A')
            return f"Found a recall for '{product_name}': Reason - {reason}, Company - {company}."
        else:
            return f"No recalls found for '{product_name}'."

    @mcp.tool()
    async def search_recalls_by_classification(classification: str) -> str:
        """Searches for food recalls by a specific classification (e.g., 'Class I')."""
        search_query = f'classification:"{classification}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(RECALL_API_URL, params=params)
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
    async def search_recalls_by_code_info(code_info: str) -> str:
        """Searches for food recalls by a specific code info (lot codes, batch numbers, etc.)."""
        # Clean the code info to remove any extra characters and ensure proper encoding
        search_query = f'code_info:"{code_info}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(RECALL_API_URL, params=params)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found containing code info '{code_info}'."

        formatted_results = [
            (
                f"- Product: {r.get('product_description', 'N/A')}\n"
                f"  Reason: {r.get('reason_for_recall', 'N/A')}\n"
                f"  Company: {r.get('recalling_firm', 'N/A')}\n"
                f"  Classification: {r.get('classification', 'N/A')}\n"
                f"  Code Info: {r.get('code_info', 'N/A')}"
            )
            for r in results
        ]
        
        return f"Found recalls containing code info '{code_info}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_recalls_by_date(days: int = 30) -> str:
        """Searches for food recalls initiated in the last N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_date_str = start_date.strftime('%Y%m%d')
        end_date_str = end_date.strftime('%Y%m%d')

        search_query = f"recall_initiation_date:[{start_date_str} TO {end_date_str}]"
        
        params = {
            'search': search_query,
            'sort': 'recall_initiation_date:desc',
            'limit': 10
        }

        data, error = await api_client.make_request(RECALL_API_URL, params=params)
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
    async def search_adverse_events_by_product(product_name: str) -> str:
        """Searches for adverse event reports related to a specific food product."""
        search_query = f'products.name_brand:"{product_name}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(ADVERSE_EVENT_API_URL, params=params)
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
        
        params = {
            'search': search_query,
            'count': 'reactions.exact'
        }
        
        data, error = await api_client.make_request(ADVERSE_EVENT_API_URL, params=params)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No reported symptoms found for '{product_name}'."

        symptoms = [f"- {item['term']} ({item['count']} reports)" for item in results]
        
        return f"Reported symptoms for '{product_name}':\n" + "\n".join(symptoms) 