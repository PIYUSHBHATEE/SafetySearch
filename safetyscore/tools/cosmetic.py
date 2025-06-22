import httpx
from mcp.server.fastmcp import FastMCP
from ..api_client import ApiClient

# FDA Cosmetic API endpoints
COSMETIC_LABEL_API_URL = "https://api.fda.gov/cosmetics/label.json"
COSMETIC_INGREDIENT_API_URL = "https://api.fda.gov/cosmetics/ingredient.json"
COSMETIC_EVENT_API_URL = "https://api.fda.gov/cosmetics/event.json"
COSMETIC_RECALL_API_URL = "https://api.fda.gov/cosmetics/enforcement.json"

api_client = ApiClient()

def register_cosmetic_tools(mcp: FastMCP):
    @mcp.tool()
    async def search_cosmetics(query: str) -> str:
        """Search for cosmetic products by name or description"""
        search_query = f'product_name:"{query}" OR product_description:"{query}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(COSMETIC_LABEL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No cosmetic products found matching '{query}'."

        results = data.get("results", [])
        if not results:
            return f"No cosmetic products found matching '{query}'."

        formatted_results = []
        for cosmetic in results:
            product_name = cosmetic.get('product_name', 'N/A')
            manufacturer = cosmetic.get('manufacturer_name', 'N/A')
            product_type = cosmetic.get('product_type', 'N/A')
            
            formatted_results.append(
                f"- Product: {product_name}\n"
                f"  Manufacturer: {manufacturer}\n"
                f"  Type: {product_type}"
            )
        
        return f"Found {len(results)} cosmetic products matching '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def get_cosmetic_product_info(product_name: str) -> str:
        """Get detailed information about a cosmetic product"""
        search_query = f'product_name:"{product_name}"'
        
        params = {
            'search': search_query,
            'limit': 1
        }
        
        data, error = await api_client.make_request(COSMETIC_LABEL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No cosmetic product found with name '{product_name}'."

        results = data.get("results", [])
        if not results:
            return f"No cosmetic product found with name '{product_name}'."

        cosmetic = results[0]
        
        # Extract detailed information
        manufacturer = cosmetic.get('manufacturer_name', 'N/A')
        product_type = cosmetic.get('product_type', 'N/A')
        registration_number = cosmetic.get('registration_number', 'N/A')
        registration_date = cosmetic.get('registration_date', 'N/A')
        
        # Get additional details if available
        ingredients = cosmetic.get('ingredients', ['No ingredient information available'])
        ingredient_text = ingredients[0] if ingredients else 'No ingredient information available'
        
        return (
            f"Cosmetic Product Information for '{product_name}':\n\n"
            f"Manufacturer: {manufacturer}\n"
            f"Product Type: {product_type}\n"
            f"Registration Number: {registration_number}\n"
            f"Registration Date: {registration_date}\n\n"
            f"Ingredients:\n{ingredient_text[:500]}..."
        )

    @mcp.tool()
    async def get_cosmetic_ingredients(product_name: str) -> str:
        """Get ingredient information for a cosmetic product"""
        search_query = f'product_name:"{product_name}"'
        
        params = {
            'search': search_query,
            'limit': 1
        }
        
        data, error = await api_client.make_request(COSMETIC_LABEL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No cosmetic product found with name '{product_name}'."

        results = data.get("results", [])
        if not results:
            return f"No cosmetic product found with name '{product_name}'."

        cosmetic = results[0]
        ingredients = cosmetic.get('ingredients', [])
        
        if not ingredients:
            return f"No ingredient information available for '{product_name}'."

        # Format ingredients list
        ingredient_list = ingredients[0] if isinstance(ingredients[0], str) else ', '.join(ingredients)
        
        return (
            f"Ingredients for '{product_name}':\n\n"
            f"{ingredient_list}"
        )

    @mcp.tool()
    async def search_cosmetic_events(query: str) -> str:
        """Search for cosmetic adverse events and safety reports"""
        search_query = f'product_name:"{query}" OR event_type:"{query}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(COSMETIC_EVENT_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No cosmetic events found for '{query}'."

        results = data.get("results", [])
        if not results:
            return f"No cosmetic events found for '{query}'."

        formatted_results = []
        for event in results:
            product_name = event.get('product_name', 'N/A')
            event_type = event.get('event_type', 'N/A')
            event_date = event.get('event_date', 'N/A')
            description = event.get('event_description', 'N/A')
            
            formatted_results.append(
                f"- Product: {product_name}\n"
                f"  Event Type: {event_type}\n"
                f"  Date: {event_date}\n"
                f"  Description: {description[:200]}..."
            )
        
        return f"Found {len(results)} cosmetic events for '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def get_cosmetic_recalls() -> str:
        """Get recent cosmetic recalls and safety alerts"""
        params = {
            'limit': 10
        }
        
        data, error = await api_client.make_request(COSMETIC_RECALL_API_URL, params=params)
        if error:
            return error

        if not data:
            return "No recent cosmetic recalls found."

        results = data.get("results", [])
        if not results:
            return "No recent cosmetic recalls found."

        formatted_results = []
        for recall in results:
            product_name = recall.get('product_name', 'N/A')
            reason = recall.get('reason_for_recall', 'N/A')
            company = recall.get('recalling_firm', 'N/A')
            recall_date = recall.get('recall_date', 'N/A')
            
            formatted_results.append(
                f"- Product: {product_name}\n"
                f"  Reason: {reason}\n"
                f"  Company: {company}\n"
                f"  Recall Date: {recall_date}"
            )
        
        return f"Recent cosmetic recalls:\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def check_cosmetic_safety(product_name: str) -> str:
        """Check safety information for a cosmetic product"""
        # Search for the product in the label database
        search_query = f'product_name:"{product_name}"'
        
        params = {
            'search': search_query,
            'limit': 1
        }
        
        data, error = await api_client.make_request(COSMETIC_LABEL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No cosmetic product found with name '{product_name}'."

        results = data.get("results", [])
        if not results:
            return f"No cosmetic product found with name '{product_name}'."

        cosmetic = results[0]
        
        # Check for safety-related information
        safety_info = []
        
        # Check if product is registered
        if cosmetic.get('registration_number'):
            safety_info.append("✅ Product is registered with FDA")
        else:
            safety_info.append("⚠️ Product is not registered with FDA")
        
        # Check for ingredients
        ingredients = cosmetic.get('ingredients', [])
        if ingredients:
            safety_info.append(f"✅ Product has ingredient information ({len(ingredients)} ingredients listed)")
        else:
            safety_info.append("⚠️ No ingredient information available")
        
        # Check for warnings or safety notices
        warnings = cosmetic.get('warnings', [])
        if warnings:
            safety_info.append(f"⚠️ Product has safety warnings: {warnings[0][:200]}...")
        else:
            safety_info.append("✅ No specific safety warnings found")
        
        # Get basic product info
        manufacturer = cosmetic.get('manufacturer_name', 'N/A')
        product_type = cosmetic.get('product_type', 'N/A')
        
        return (
            f"Safety Assessment for '{product_name}':\n\n"
            f"Manufacturer: {manufacturer}\n"
            f"Product Type: {product_type}\n\n"
            f"Safety Information:\n" + "\n".join(safety_info) + "\n\n"
            f"Note: This assessment is based on available FDA data. "
            f"Always read product labels and consult with healthcare providers if you have concerns."
        ) 