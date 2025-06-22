import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
from ..api_client import ApiClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Get API URLs from environment variables with fallbacks to the public defaults
RECALL_API_URL = os.getenv("FDA_RECALL_API_URL", "https://api.fda.gov/food/enforcement.json")
ADVERSE_EVENT_API_URL = os.getenv("FDA_ADVERSE_EVENT_API_URL", "https://api.fda.gov/food/event.json")

api_client = ApiClient()

def register_food_tools(mcp: FastMCP):
    @mcp.tool()
    async def search_recalls_by_product_description(query: str) -> str:
        """Searches for food recalls by matching a query against the product description with detailed analysis."""
        search_query = f'product_description:"{query}"'
        
        # Use params to let httpx handle URL encoding properly
        params = {
            'search': search_query,
            'limit': 10,
            'sort': 'recall_initiation_date:desc'
        }
        
        data, error = await api_client.make_request(RECALL_API_URL, params=params)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for '{query}'."

        # Build comprehensive report
        report_parts = []
        report_parts.append(f"🚨 **Food Recall Analysis for '{query}'**")
        report_parts.append("=" * 60)
        
        # Summary statistics
        total_recalls = len(results)
        class_i_recalls = sum(1 for r in results if r.get('classification') == 'Class I')
        class_ii_recalls = sum(1 for r in results if r.get('classification') == 'Class II')
        class_iii_recalls = sum(1 for r in results if r.get('classification') == 'Class III')
        
        report_parts.append(f"📊 **Recall Summary:**")
        report_parts.append(f"• Total recalls found: {total_recalls}")
        report_parts.append(f"• Class I (Most Serious): {class_i_recalls}")
        report_parts.append(f"• Class II (Moderate): {class_ii_recalls}")
        report_parts.append(f"• Class III (Least Serious): {class_iii_recalls}")
        
        # Detailed recall information
        report_parts.append(f"\n📋 **Detailed Recall Information:**")
        
        for i, recall in enumerate(results, 1):
            report_parts.append(f"\n**Recall #{i}:**")
            
            # Basic product info
            product = recall.get('product_description', 'N/A')
            report_parts.append(f"🏷️ Product: {product}")
            
            # Company and contact info
            company = recall.get('recalling_firm', 'N/A')
            report_parts.append(f"🏢 Company: {company}")
            
            # Classification and seriousness
            classification = recall.get('classification', 'N/A')
            report_parts.append(f"⚠️ Classification: {classification}")
            
            # Dates
            recall_date = recall.get('recall_initiation_date', 'N/A')
            termination_date = recall.get('recall_termination_date', 'N/A')
            report_parts.append(f"📅 Recall Date: {recall_date}")
            if termination_date != 'N/A':
                report_parts.append(f"📅 Termination Date: {termination_date}")
            
            # Reason and details
            reason = recall.get('reason_for_recall', 'N/A')
            report_parts.append(f"🔍 Reason: {reason}")
            
            # Distribution info
            distribution = recall.get('distribution_pattern', 'N/A')
            if distribution != 'N/A':
                report_parts.append(f"🌍 Distribution: {distribution}")
            
            # Code information
            code_info = recall.get('code_info', 'N/A')
            if code_info != 'N/A':
                report_parts.append(f"🔢 Product Codes: {code_info}")
            
            # Quantity affected
            quantity = recall.get('quantity_in_commerce', 'N/A')
            if quantity != 'N/A':
                report_parts.append(f"📦 Quantity Affected: {quantity}")
            
            # Contact information
            contact = recall.get('recalling_firm', 'N/A')
            if contact != 'N/A':
                report_parts.append(f"📞 Contact: {contact}")
        
        # Safety recommendations
        report_parts.append(f"\n🛡️ **Safety Recommendations:**")
        if class_i_recalls > 0:
            report_parts.append(f"• ⚠️ {class_i_recalls} Class I recalls detected - IMMEDIATE ACTION REQUIRED")
            report_parts.append(f"• Check if you have any of the affected products")
            report_parts.append(f"• Do not consume products with matching codes")
            report_parts.append(f"• Contact the company for refund/replacement")
        
        if class_ii_recalls > 0:
            report_parts.append(f"• ⚠️ {class_ii_recalls} Class II recalls - MODERATE RISK")
            report_parts.append(f"• Monitor for symptoms if consumed")
            report_parts.append(f"• Consider returning affected products")
        
        # Recent activity indicator
        recent_recalls = [r for r in results if r.get('recall_initiation_date', '') >= '20240101']
        if recent_recalls:
            report_parts.append(f"\n🆕 **Recent Activity:** {len(recent_recalls)} recalls in 2024")
        
        return "\n".join(report_parts)

    @mcp.tool()
    async def search_recalls_by_product_type(product_type: str) -> str:
        """Searches for recalls where the product description contains a product type with detailed analysis."""
        search_query = f'product_description:"{product_type}"'
        
        params = {
            'search': search_query,
            'limit': 10,
            'sort': 'recall_initiation_date:desc'
        }

        data, error = await api_client.make_request(RECALL_API_URL, params=params)
        if error:
            return error

        results = data.get("results", [])
        if not results:
            return f"No food recalls found for product type '{product_type}'."

        # Build comprehensive report
        report_parts = []
        report_parts.append(f"🚨 **Product Type Recall Analysis: '{product_type}'**")
        report_parts.append("=" * 60)
        
        # Summary statistics
        total_recalls = len(results)
        class_i_recalls = sum(1 for r in results if r.get('classification') == 'Class I')
        class_ii_recalls = sum(1 for r in results if r.get('classification') == 'Class II')
        class_iii_recalls = sum(1 for r in results if r.get('classification') == 'Class III')
        
        report_parts.append(f"📊 **Recall Summary for {product_type} Products:**")
        report_parts.append(f"• Total recalls found: {total_recalls}")
        report_parts.append(f"• Class I (Most Serious): {class_i_recalls}")
        report_parts.append(f"• Class II (Moderate): {class_ii_recalls}")
        report_parts.append(f"• Class III (Least Serious): {class_iii_recalls}")
        
        # Company analysis
        companies = {}
        for recall in results:
            company = recall.get('recalling_firm', 'Unknown')
            companies[company] = companies.get(company, 0) + 1
        
        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:3]
        report_parts.append(f"\n🏢 **Top Companies with Recalls:**")
        for company, count in top_companies:
            report_parts.append(f"• {company}: {count} recalls")
        
        # Detailed recall information
        report_parts.append(f"\n📋 **Detailed Recall Information:**")
        
        for i, recall in enumerate(results, 1):
            report_parts.append(f"\n**Recall #{i}:**")
            
            # Basic product info
            product = recall.get('product_description', 'N/A')
            report_parts.append(f"🏷️ Product: {product}")
            
            # Company and contact info
            company = recall.get('recalling_firm', 'N/A')
            report_parts.append(f"🏢 Company: {company}")
            
            # Classification and seriousness
            classification = recall.get('classification', 'N/A')
            report_parts.append(f"⚠️ Classification: {classification}")
            
            # Dates
            recall_date = recall.get('recall_initiation_date', 'N/A')
            termination_date = recall.get('recall_termination_date', 'N/A')
            report_parts.append(f"📅 Recall Date: {recall_date}")
            if termination_date != 'N/A':
                report_parts.append(f"📅 Termination Date: {termination_date}")
            
            # Reason and details
            reason = recall.get('reason_for_recall', 'N/A')
            report_parts.append(f"🔍 Reason: {reason}")
            
            # Distribution info
            distribution = recall.get('distribution_pattern', 'N/A')
            if distribution != 'N/A':
                report_parts.append(f"🌍 Distribution: {distribution}")
            
            # Code information
            code_info = recall.get('code_info', 'N/A')
            if code_info != 'N/A':
                report_parts.append(f"🔢 Product Codes: {code_info}")
            
            # Quantity affected
            quantity = recall.get('quantity_in_commerce', 'N/A')
            if quantity != 'N/A':
                report_parts.append(f"📦 Quantity Affected: {quantity}")
        
        # Safety recommendations
        report_parts.append(f"\n🛡️ **Safety Recommendations:**")
        if class_i_recalls > 0:
            report_parts.append(f"• ⚠️ {class_i_recalls} Class I recalls detected - HIGH RISK")
            report_parts.append(f"• Exercise caution when purchasing {product_type} products")
            report_parts.append(f"• Check product codes before consumption")
            report_parts.append(f"• Monitor for any safety alerts")
        
        if class_ii_recalls > 0:
            report_parts.append(f"• ⚠️ {class_ii_recalls} Class II recalls - MODERATE RISK")
            report_parts.append(f"• Be aware of potential issues with {product_type} products")
            report_parts.append(f"• Check expiration dates and storage conditions")
        
        # Trend analysis
        recent_recalls = [r for r in results if r.get('recall_initiation_date', '') >= '20240101']
        if recent_recalls:
            report_parts.append(f"\n📈 **Recent Trend:** {len(recent_recalls)} recalls in 2024")
            report_parts.append(f"• This indicates ongoing safety concerns with {product_type} products")
        
        return "\n".join(report_parts)

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
        """Gets detailed symptom analysis and adverse event information for a specific food product."""
        search_query = f'products.name_brand:"{product_name}"'
        
        # First, get symptom count summary
        count_params = {
            'search': search_query,
            'count': 'reactions.exact'
        }
        
        count_data, count_error = await api_client.make_request(ADVERSE_EVENT_API_URL, params=count_params)
        if count_error:
            return count_error

        count_results = count_data.get("results", [])
        
        # Then, get detailed case information
        detail_params = {
            'search': search_query,
            'limit': 10,
            'sort': 'date_created:desc'
        }
        
        detail_data, detail_error = await api_client.make_request(ADVERSE_EVENT_API_URL, params=detail_params)
        if detail_error:
            return detail_error

        detail_results = detail_data.get("results", [])
        
        if not count_results and not detail_results:
            return f"No reported symptoms or adverse events found for '{product_name}'."

        # Build comprehensive report
        report_parts = []
        
        # 1. Symptom Summary
        if count_results:
            report_parts.append(f"📊 **Symptom Summary for '{product_name}'**")
            report_parts.append("=" * 50)
            
            symptoms = []
            total_reports = sum(item['count'] for item in count_results)
            
            for item in count_results[:10]:  # Top 10 symptoms
                percentage = (item['count'] / total_reports * 100) if total_reports > 0 else 0
                symptoms.append(f"• {item['term']}: {item['count']} reports ({percentage:.1f}%)")
            
            report_parts.append(f"Total adverse event reports: {total_reports}")
            report_parts.append("\n**Most Common Symptoms:**")
            report_parts.extend(symptoms)
        
        # 2. Detailed Case Analysis
        if detail_results:
            report_parts.append(f"\n📋 **Recent Case Details**")
            report_parts.append("=" * 50)
            
            for i, case in enumerate(detail_results[:5], 1):  # Top 5 cases
                report_parts.append(f"\n**Case {i}:**")
                
                # Basic case info
                report_date = case.get('date_created', 'N/A')
                report_parts.append(f"📅 Report Date: {report_date}")
                
                # Patient demographics
                patient = case.get('patient', {})
                age = patient.get('patientonsetage', 'N/A')
                sex = patient.get('patientsex', 'N/A')
                if age != 'N/A' or sex != 'N/A':
                    report_parts.append(f"👤 Patient: {age} years old, {sex}")
                
                # Symptoms
                reactions = case.get('reactions', [])
                if reactions:
                    report_parts.append(f"🩺 Symptoms: {', '.join(reactions[:5])}")
                    if len(reactions) > 5:
                        report_parts.append(f"   ... and {len(reactions) - 5} more symptoms")
                
                # Outcomes
                outcomes = case.get('outcomes', [])
                if outcomes:
                    report_parts.append(f"📈 Outcomes: {', '.join(outcomes)}")
                
                # Seriousness
                serious = case.get('serious', [])
                if serious:
                    report_parts.append(f"⚠️ Serious: {', '.join(serious)}")
                
                # Product details
                products = case.get('products', [])
                if products:
                    product = products[0]
                    brand_name = product.get('name_brand', 'N/A')
                    generic_name = product.get('name_generic', 'N/A')
                    if brand_name != 'N/A' or generic_name != 'N/A':
                        report_parts.append(f"🏷️ Product: {brand_name} ({generic_name})")
        
        # 3. Safety Insights
        if count_results and detail_results:
            report_parts.append(f"\n🔍 **Safety Insights**")
            report_parts.append("=" * 50)
            
            # Calculate severity indicators
            serious_cases = sum(1 for case in detail_results if case.get('serious'))
            total_cases = len(detail_results)
            severity_rate = (serious_cases / total_cases * 100) if total_cases > 0 else 0
            
            report_parts.append(f"• Serious cases: {serious_cases}/{total_cases} ({severity_rate:.1f}%)")
            
            # Most common outcomes
            all_outcomes = []
            for case in detail_results:
                all_outcomes.extend(case.get('outcomes', []))
            
            if all_outcomes:
                outcome_counts = {}
                for outcome in all_outcomes:
                    outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
                
                top_outcomes = sorted(outcome_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                report_parts.append(f"• Most common outcomes: {', '.join([f'{outcome} ({count})' for outcome, count in top_outcomes])}")
            
            # Timeline analysis
            if detail_results:
                dates = [case.get('date_created') for case in detail_results if case.get('date_created')]
                if dates:
                    report_parts.append(f"• Recent reports: {len(dates)} cases in available data")
        
        return "\n".join(report_parts) 