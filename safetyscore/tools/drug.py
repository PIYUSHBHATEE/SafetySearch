import httpx
from mcp.server.fastmcp import FastMCP
from ..api_client import ApiClient

# FDA Drug API endpoints
DRUG_LABEL_API_URL = "https://api.fda.gov/drug/label.json"
DRUG_APPROVAL_API_URL = "https://api.fda.gov/drug/nda.json"
DRUG_SHORTAGE_API_URL = "https://api.fda.gov/drug/shortage.json"
DRUG_RECALL_API_URL = "https://api.fda.gov/drug/enforcement.json"
DRUG_ADVERSE_EVENT_API_URL = "https://api.fda.gov/drug/event.json"
DRUG_INTERACTION_API_URL = "https://api.fda.gov/drug/label.json"

api_client = ApiClient()

def register_drug_tools(mcp: FastMCP):
    @mcp.tool()
    async def search_drugs(query: str) -> str:
        """Search for drug information by name, active ingredient, or description"""
        search_query = f'openfda.generic_name:"{query}" OR openfda.brand_name:"{query}" OR openfda.substance_name:"{query}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(DRUG_LABEL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No drugs found matching '{query}'."

        results = data.get("results", [])
        if not results:
            return f"No drugs found matching '{query}'."

        formatted_results = []
        for drug in results:
            openfda = drug.get('openfda', {})
            generic_name = openfda.get('generic_name', ['N/A'])[0] if openfda.get('generic_name') else 'N/A'
            brand_name = openfda.get('brand_name', ['N/A'])[0] if openfda.get('brand_name') else 'N/A'
            manufacturer = openfda.get('manufacturer_name', ['N/A'])[0] if openfda.get('manufacturer_name') else 'N/A'
            
            formatted_results.append(
                f"- Generic Name: {generic_name}\n"
                f"  Brand Name: {brand_name}\n"
                f"  Manufacturer: {manufacturer}"
            )
        
        return f"Found {len(results)} drugs matching '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def get_drug_label(drug_name: str) -> str:
        """Get detailed drug labeling information including warnings and dosage"""
        search_query = f'openfda.generic_name:"{drug_name}" OR openfda.brand_name:"{drug_name}"'
        
        params = {
            'search': search_query,
            'limit': 1
        }
        
        data, error = await api_client.make_request(DRUG_LABEL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No drug label found for '{drug_name}'."

        results = data.get("results", [])
        if not results:
            return f"No drug label found for '{drug_name}'."

        drug = results[0]
        openfda = drug.get('openfda', {})
        
        # Extract key information
        generic_name = openfda.get('generic_name', ['N/A'])[0] if openfda.get('generic_name') else 'N/A'
        brand_name = openfda.get('brand_name', ['N/A'])[0] if openfda.get('brand_name') else 'N/A'
        manufacturer = openfda.get('manufacturer_name', ['N/A'])[0] if openfda.get('manufacturer_name') else 'N/A'
        
        # Get warnings and dosage info
        warnings = drug.get('warnings', ['No warnings available'])[0] if drug.get('warnings') else 'No warnings available'
        dosage = drug.get('dosage_and_administration', ['No dosage info available'])[0] if drug.get('dosage_and_administration') else 'No dosage info available'
        
        return (
            f"Drug Label for '{drug_name}':\n\n"
            f"Generic Name: {generic_name}\n"
            f"Brand Name: {brand_name}\n"
            f"Manufacturer: {manufacturer}\n\n"
            f"Warnings:\n{warnings[:500]}...\n\n"
            f"Dosage Information:\n{dosage[:500]}..."
        )

    @mcp.tool()
    async def get_drug_approvals(year: int) -> str:
        """Get drug approvals for a specific year"""
        search_query = f'action_date:{year}*'
        
        params = {
            'search': search_query,
            'limit': 10
        }
        
        data, error = await api_client.make_request(DRUG_APPROVAL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No drug approvals found for year {year}."

        results = data.get("results", [])
        if not results:
            return f"No drug approvals found for year {year}."

        formatted_results = []
        for approval in results:
            applicant = approval.get('applicant', 'N/A')
            product_name = approval.get('product_name', 'N/A')
            action_date = approval.get('action_date', 'N/A')
            
            formatted_results.append(
                f"- Product: {product_name}\n"
                f"  Applicant: {applicant}\n"
                f"  Approval Date: {action_date}"
            )
        
        return f"Found {len(results)} drug approvals for {year}:\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def check_drug_shortages() -> str:
        """Check current drug shortages and availability"""
        params = {
            'limit': 10
        }
        
        data, error = await api_client.make_request(DRUG_SHORTAGE_API_URL, params=params)
        if error:
            return error

        if not data:
            return "No current drug shortages found."

        results = data.get("results", [])
        if not results:
            return "No current drug shortages found."

        formatted_results = []
        for shortage in results:
            drug_name = shortage.get('drug_name', 'N/A')
            status = shortage.get('status', 'N/A')
            reason = shortage.get('reason', 'N/A')
            
            formatted_results.append(
                f"- Drug: {drug_name}\n"
                f"  Status: {status}\n"
                f"  Reason: {reason}"
            )
        
        return f"Current drug shortages:\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def search_drug_recalls(query: str) -> str:
        """Search for drug recalls by product name or company"""
        search_query = f'product_description:"{query}" OR recalling_firm:"{query}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(DRUG_RECALL_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No drug recalls found for '{query}'."

        results = data.get("results", [])
        if not results:
            return f"No drug recalls found for '{query}'."

        formatted_results = []
        for recall in results:
            product = recall.get('product_description', 'N/A')
            reason = recall.get('reason_for_recall', 'N/A')
            company = recall.get('recalling_firm', 'N/A')
            classification = recall.get('classification', 'N/A')
            
            formatted_results.append(
                f"- Product: {product}\n"
                f"  Reason: {reason}\n"
                f"  Company: {company}\n"
                f"  Classification: {classification}"
            )
        
        return f"Found {len(results)} drug recalls for '{query}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def get_drug_adverse_events(drug_name: str) -> str:
        """Get adverse event reports for a specific drug"""
        search_query = f'patient.drug.medicinalproduct:"{drug_name}" OR patient.drug.openfda.generic_name:"{drug_name}"'
        
        params = {
            'search': search_query,
            'limit': 5
        }
        
        data, error = await api_client.make_request(DRUG_ADVERSE_EVENT_API_URL, params=params)
        if error:
            return error

        if not data:
            return f"No adverse events found for drug '{drug_name}'."

        results = data.get("results", [])
        if not results:
            return f"No adverse events found for drug '{drug_name}'."

        formatted_results = []
        for event in results:
            patient = event.get('patient', {})
            drugs = patient.get('drug', [])
            
            if drugs:
                drug_info = drugs[0]
                product = drug_info.get('medicinalproduct', 'N/A')
                reactions = patient.get('reaction', [])
                reaction_text = ', '.join(reactions[:3]) if reactions else 'No reactions listed'
                
                formatted_results.append(
                    f"- Product: {product}\n"
                    f"  Reactions: {reaction_text}"
                )
        
        return f"Found {len(results)} adverse events for '{drug_name}':\n\n" + "\n\n".join(formatted_results)

    @mcp.tool()
    async def check_drug_interactions(drug1: str, drug2: str) -> str:
        """Check potential interactions between two drugs"""
        # Search for drug1's label
        search_query1 = f'openfda.generic_name:"{drug1}" OR openfda.brand_name:"{drug1}"'
        
        params1 = {
            'search': search_query1,
            'limit': 1
        }
        
        data1, error1 = await api_client.make_request(DRUG_LABEL_API_URL, params=params1)
        if error1:
            return f"Error searching for {drug1}: {error1}"

        if not data1:
            return f"No information found for drug '{drug1}'."

        results1 = data1.get("results", [])
        if not results1:
            return f"No information found for drug '{drug1}'."

        # Search for drug2's label
        search_query2 = f'openfda.generic_name:"{drug2}" OR openfda.brand_name:"{drug2}"'
        
        params2 = {
            'search': search_query2,
            'limit': 1
        }
        
        data2, error2 = await api_client.make_request(DRUG_LABEL_API_URL, params=params2)
        if error2:
            return f"Error searching for {drug2}: {error2}"

        if not data2:
            return f"No information found for drug '{drug2}'."

        results2 = data2.get("results", [])
        if not results2:
            return f"No information found for drug '{drug2}'."

        # Get drug interaction information
        drug1_info = results1[0]
        drug2_info = results2[0]
        
        interactions1 = drug1_info.get('drug_interactions', ['No interaction data available'])[0] if drug1_info.get('drug_interactions') else 'No interaction data available'
        interactions2 = drug2_info.get('drug_interactions', ['No interaction data available'])[0] if drug2_info.get('drug_interactions') else 'No interaction data available'
        
        openfda1 = drug1_info.get('openfda', {})
        openfda2 = drug2_info.get('openfda', {})
        
        generic1 = openfda1.get('generic_name', ['N/A'])[0] if openfda1.get('generic_name') else 'N/A'
        generic2 = openfda2.get('generic_name', ['N/A'])[0] if openfda2.get('generic_name') else 'N/A'
        
        return (
            f"Drug Interaction Analysis:\n\n"
            f"Drug 1: {generic1}\n"
            f"Drug 2: {generic2}\n\n"
            f"Interaction Information for {generic1}:\n{interactions1[:300]}...\n\n"
            f"Interaction Information for {generic2}:\n{interactions2[:300]}...\n\n"
            f"Note: Always consult with a healthcare provider before combining medications."
        ) 