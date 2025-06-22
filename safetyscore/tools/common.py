import httpx
from mcp.server.fastmcp import FastMCP
from ..api_client import ApiClient

# FDA API endpoints for cross-category searches
FOOD_API_URL = "https://api.fda.gov/food/enforcement.json"
DRUG_API_URL = "https://api.fda.gov/drug/enforcement.json"
COSMETIC_API_URL = "https://api.fda.gov/cosmetics/enforcement.json"

api_client = ApiClient()

def register_common_tools(mcp: FastMCP):
    @mcp.tool()
    async def search_fda_products(category: str, query: str) -> str:
        """Search across all FDA categories (food, drug, cosmetic)"""
        category = category.lower()
        
        if category not in ['food', 'drug', 'cosmetic']:
            return "Invalid category. Please use 'food', 'drug', or 'cosmetic'."
        
        # Select appropriate API endpoint
        if category == 'food':
            api_url = FOOD_API_URL
            search_field = 'product_description'
        elif category == 'drug':
            api_url = DRUG_API_URL
            search_field = 'product_description'
        else:  # cosmetic
            api_url = COSMETIC_API_URL
            search_field = 'product_name'
        
        search_query = f'{search_field}:"{query}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(api_url, params=params)
        if error:
            return error

        if not data:
            return f"No {category} products found matching '{query}'."

        results = data.get("results", [])
        if not results:
            return f"No {category} products found matching '{query}'."

        formatted_results = []
        for product in results:
            if category == 'food':
                product_name = product.get('product_description', 'N/A')
                reason = product.get('reason_for_recall', 'N/A')
                company = product.get('recalling_firm', 'N/A')
                classification = product.get('classification', 'N/A')
                
                formatted_results.append(
                    f"- Product: {product_name}\n"
                    f"  Reason: {reason}\n"
                    f"  Company: {company}\n"
                    f"  Classification: {classification}"
                )
            elif category == 'drug':
                product_name = product.get('product_description', 'N/A')
                reason = product.get('reason_for_recall', 'N/A')
                company = product.get('recalling_firm', 'N/A')
                classification = product.get('classification', 'N/A')
                
                formatted_results.append(
                    f"- Product: {product_name}\n"
                    f"  Reason: {reason}\n"
                    f"  Company: {company}\n"
                    f"  Classification: {classification}"
                )
            else:  # cosmetic
                product_name = product.get('product_name', 'N/A')
                reason = product.get('reason_for_recall', 'N/A')
                company = product.get('recalling_firm', 'N/A')
                recall_date = product.get('recall_date', 'N/A')
                
                formatted_results.append(
                    f"- Product: {product_name}\n"
                    f"  Reason: {reason}\n"
                    f"  Company: {company}\n"
                    f"  Recall Date: {recall_date}"
                )
        
        return f"Found {len(results)} {category} products matching '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def get_fda_company_info(company_name: str) -> str:
        """Get information about a company across all FDA categories"""
        results = {}
        
        # Search across all three categories
        categories = [
            ('food', FOOD_API_URL),
            ('drug', DRUG_API_URL),
            ('cosmetic', COSMETIC_API_URL)
        ]
        
        for category, api_url in categories:
            search_query = f'recalling_firm:"{company_name}"'
            
            params = {
                'search': search_query,
                'limit': 3
            }
            
            data, error = await api_client.make_request(api_url, params=params)
            if not error and data:
                category_results = data.get("results", [])
                if category_results:
                    results[category] = category_results
        
        if not results:
            return f"No FDA records found for company '{company_name}'."
        
        # Format the results
        formatted_output = [f"FDA Records for '{company_name}':\n"]
        
        for category, category_results in results.items():
            formatted_output.append(f"\n{category.upper()} Category ({len(category_results)} records):")
            
            for record in category_results:
                if category == 'food':
                    product = record.get('product_description', 'N/A')
                    reason = record.get('reason_for_recall', 'N/A')
                    date = record.get('recall_initiation_date', 'N/A')
                elif category == 'drug':
                    product = record.get('product_description', 'N/A')
                    reason = record.get('reason_for_recall', 'N/A')
                    date = record.get('recall_initiation_date', 'N/A')
                else:  # cosmetic
                    product = record.get('product_name', 'N/A')
                    reason = record.get('reason_for_recall', 'N/A')
                    date = record.get('recall_date', 'N/A')
                
                formatted_output.append(
                    f"  - Product: {product}\n"
                    f"    Reason: {reason}\n"
                    f"    Date: {date}"
                )
        
        return "\n".join(formatted_output)

    @mcp.tool()
    async def compare_fda_products(product1: str, product2: str) -> str:
        """Compare two FDA-regulated products"""
        # Search for both products across all categories
        categories = [
            ('food', FOOD_API_URL, 'product_description'),
            ('drug', DRUG_API_URL, 'product_description'),
            ('cosmetic', COSMETIC_API_URL, 'product_name')
        ]
        
        product1_info = {}
        product2_info = {}
        
        # Search for product1
        for category, api_url, search_field in categories:
            search_query = f'{search_field}:"{product1}"'
            
            params = {
                'search': search_query,
                'limit': 1
            }
            
            data, error = await api_client.make_request(api_url, params=params)
            if not error and data:
                results = data.get("results", [])
                if results:
                    product1_info[category] = results[0]
        
        # Search for product2
        for category, api_url, search_field in categories:
            search_query = f'{search_field}:"{product2}"'
            
            params = {
                'search': search_query,
                'limit': 1
            }
            
            data, error = await api_client.make_request(api_url, params=params)
            if not error and data:
                results = data.get("results", [])
                if results:
                    product2_info[category] = results[0]
        
        # Format comparison
        comparison = [f"FDA Product Comparison:\n"]
        comparison.append(f"Product 1: {product1}")
        comparison.append(f"Product 2: {product2}\n")
        
        # Compare by category
        all_categories = set(product1_info.keys()) | set(product2_info.keys())
        
        for category in all_categories:
            comparison.append(f"{category.upper()} Category:")
            
            if category in product1_info and category in product2_info:
                # Both products found in this category
                p1 = product1_info[category]
                p2 = product2_info[category]
                
                if category == 'food':
                    p1_name = p1.get('product_description', 'N/A')
                    p1_reason = p1.get('reason_for_recall', 'N/A')
                    p1_company = p1.get('recalling_firm', 'N/A')
                    
                    p2_name = p2.get('product_description', 'N/A')
                    p2_reason = p2.get('reason_for_recall', 'N/A')
                    p2_company = p2.get('recalling_firm', 'N/A')
                elif category == 'drug':
                    p1_name = p1.get('product_description', 'N/A')
                    p1_reason = p1.get('reason_for_recall', 'N/A')
                    p1_company = p1.get('recalling_firm', 'N/A')
                    
                    p2_name = p2.get('product_description', 'N/A')
                    p2_reason = p2.get('reason_for_recall', 'N/A')
                    p2_company = p2.get('recalling_firm', 'N/A')
                else:  # cosmetic
                    p1_name = p1.get('product_name', 'N/A')
                    p1_reason = p1.get('reason_for_recall', 'N/A')
                    p1_company = p1.get('recalling_firm', 'N/A')
                    
                    p2_name = p2.get('product_name', 'N/A')
                    p2_reason = p2.get('reason_for_recall', 'N/A')
                    p2_company = p2.get('recalling_firm', 'N/A')
                
                comparison.append(f"  Product 1: {p1_name} (Company: {p1_company})")
                comparison.append(f"  Product 2: {p2_name} (Company: {p2_company})")
                
                if p1_reason != 'N/A' or p2_reason != 'N/A':
                    comparison.append(f"  Recall Reasons:")
                    if p1_reason != 'N/A':
                        comparison.append(f"    Product 1: {p1_reason}")
                    if p2_reason != 'N/A':
                        comparison.append(f"    Product 2: {p2_reason}")
            
            elif category in product1_info:
                comparison.append(f"  Product 1: Found in FDA database")
                comparison.append(f"  Product 2: Not found in this category")
            
            elif category in product2_info:
                comparison.append(f"  Product 1: Not found in this category")
                comparison.append(f"  Product 2: Found in FDA database")
            
            comparison.append("")
        
        if not product1_info and not product2_info:
            return f"Neither '{product1}' nor '{product2}' found in FDA databases."
        
        return "\n".join(comparison)

    @mcp.tool()
    async def get_fda_statistics(category: str) -> str:
        """Get FDA statistics and data for a specific category"""
        category = category.lower()
        
        if category not in ['food', 'drug', 'cosmetic']:
            return "Invalid category. Please use 'food', 'drug', or 'cosmetic'."
        
        # Get recent data for statistics
        if category == 'food':
            api_url = FOOD_API_URL
        elif category == 'drug':
            api_url = DRUG_API_URL
        else:  # cosmetic
            api_url = COSMETIC_API_URL
        
        # Get recent records for analysis
        params = {
            'limit': 100
        }
        
        data, error = await api_client.make_request(api_url, params=params)
        if error:
            return error

        if not data:
            return f"No {category} data available for statistics."

        results = data.get("results", [])
        if not results:
            return f"No {category} data available for statistics."

        # Analyze the data
        total_records = len(results)
        
        # Count by classification (for food and drug)
        classifications = {}
        companies = {}
        
        for record in results:
            if category in ['food', 'drug']:
                classification = record.get('classification', 'Unknown')
                classifications[classification] = classifications.get(classification, 0) + 1
            
            company = record.get('recalling_firm', 'Unknown')
            companies[company] = companies.get(company, 0) + 1
        
        # Format statistics
        stats = [f"FDA {category.upper()} Statistics (Recent Data):\n"]
        stats.append(f"Total Records Analyzed: {total_records}")
        
        if classifications:
            stats.append(f"\nClassifications:")
            for classification, count in sorted(classifications.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_records) * 100
                stats.append(f"  {classification}: {count} ({percentage:.1f}%)")
        
        stats.append(f"\nTop Companies by Recall Count:")
        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]
        for company, count in top_companies:
            percentage = (count / total_records) * 100
            stats.append(f"  {company}: {count} ({percentage:.1f}%)")
        
        return "\n".join(stats) 