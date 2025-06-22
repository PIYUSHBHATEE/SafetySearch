<p align="center">
  <img src="./SafetySearch-logo.png" alt="SafetySearch Logo" width="200">
</p>

# SafetySearch

> Search. Scan. Stay Safe.

A comprehensive Model Context Protocol (MCP) server that provides access to FDA (Food and Drug Administration) data across two major categories: **Food** and **Cosmetic** safety information.

## 🎯 What This Server Provides

This MCP server offers **19 tools** to access product safety data, helping users:
- Check product recalls and safety alerts across FDA categories
- Monitor food safety issues and recall trends
- Review cosmetic safety reports and ingredient information
- Compare FDA-regulated products across categories
- Analyze safety trends and company information
- Get comprehensive cross-category safety insights

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip or uv package manager

### Installation

1. **Clone or download the project:**
   ```bash
   git clone https://github.com/surabhya/SafetySearch.git
   cd SafetySearch
   ```

2. **Install dependencies:**
   ```bash
   # Using pip
   pip install "mcp[cli]>=1.0.0" httpx>=0.24.0 pydantic>=2.0.0
   
   # Or using uv (recommended)
   uv add "mcp[cli]>=1.0.0" httpx>=0.24.0 pydantic>=2.0.0
   ```

## 🔧 Usage

### Using uv (Recommended)

> **Note:**
> If you have previously installed `mcp` in another project, or if you encounter errors like `Failed to spawn: mcp ... No such file or directory`, run:
> ```bash
> uv remove mcp
> uv add "mcp[cli]>=1.0.0"
> ```
> This ensures the `mcp` binary is correctly linked to your current environment.

#### Start the MCP Inspector (Development Mode)
Test and validate the server using the MCP Inspector:
```bash
uv run mcp dev server.py
```

#### Start the Server Directly
Run the server directly for testing:
```bash
uv run python server.py
```

#### Install in Claude Desktop (Production)
Install the server in Claude Desktop for production use:
```bash
uv run mcp install server.py
```

## 🛠️ Available Tools

### Food Safety Tools (9 tools) ✅

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_recalls_by_product_description` | Searches for food recalls by matching a query against the product description. | `query: str` |
| `search_recalls_by_product_type` | Searches for recalls where the product description contains a product type (e.g., 'Bakery'). | `product_type: str` |
| `search_recalls_by_specific_product` | Checks for any ongoing recalls for a single, specific food product. | `product_name: str` |
| `search_recalls_by_classification` | Searches for food recalls by a specific classification (e.g., 'Class I'). | `classification: str` |
| `search_recalls_by_code_info` | Searches for food recalls by code info (lot codes, batch numbers, etc.). | `code_info: str` |
| `search_recalls_by_date` | Searches for food recalls initiated in the last N days. | `days: int` (default: 30) |
| `get_recall_trends_by_reason` | Analyzes the most common reasons for food recalls in the last 90 days. | None |
| `search_adverse_events_by_product` | Searches for adverse event reports related to a specific food product. | `product_name: str` |
| `get_symptom_summary_for_product` | Gets a list of reported symptoms (reactions) for a specific food product. | `product_name: str` |

### Cosmetic Safety Tools (6 tools) ✅

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_cosmetics` | Search for cosmetic products by name or description | `query: str` |
| `get_cosmetic_product_info` | Get detailed information about a cosmetic product | `product_name: str` |
| `get_cosmetic_ingredients` | Get ingredient information for a cosmetic product | `product_name: str` |
| `search_cosmetic_events` | Search for cosmetic adverse events and safety reports | `query: str` |
| `get_cosmetic_recalls` | Get recent cosmetic recalls and safety alerts | None |
| `check_cosmetic_safety` | Check safety information for a cosmetic product | `product_name: str` |

### Cross-Category Tools (4 tools) ✅

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_fda_products` | Search across all FDA categories (food, cosmetic) | `category: str`, `query: str` |
| `get_fda_company_info` | Get information about a company across all FDA categories | `company_name: str` |
| `compare_fda_products` | Compare two FDA-regulated products | `product1: str`, `product2: str` |
| `get_fda_statistics` | Get FDA statistics and data for a specific category | `category: str` |

## 📋 Example Usage

### Food Safety Tools
*   **Search for recalls of "ice cream"**
    ```
    food.search_recalls_by_product_description(query="ice cream")
    ```

*   **Find recalls for "Bakery" products**
    ```
    food.search_recalls_by_product_type(product_type="Bakery")
    ```

*   **Check for recalls on "Ben & Jerry's Chocolate Fudge Brownie"**
    ```
    food.search_recalls_by_specific_product(product_name="Ben & Jerry's Chocolate Fudge Brownie")
    ```

*   **Find recalls with classification "Class I"**
    ```
    food.search_recalls_by_classification(classification="Class I")
    ```

*   **Search for a recall with code info "222268"**
    ```
    food.search_recalls_by_code_info(code_info="222268")
    ```

*   **Get all recalls from the last 14 days**
    ```
    food.search_recalls_by_date(days=14)
    ```

*   **Get top 5 reasons for recalls in the last 90 days**
    ```
    food.get_recall_trends_by_reason()
    ```

*   **Find adverse events for "Cheerios"**
    ```
    food.search_adverse_events_by_product(product_name="Cheerios")
    ```

*   **Get a summary of symptoms reported for "Lucky Charms"**
    ```
    food.get_symptom_summary_for_product(product_name="Lucky Charms")
    ```

### Cosmetic Safety Tools
*   **Search for cosmetic products**
    ```
    cosmetic.search_cosmetics(query="lotion")
    ```

*   **Get detailed cosmetic product information**
    ```
    cosmetic.get_cosmetic_product_info(product_name="shampoo")
    ```

*   **Get cosmetic ingredients**
    ```
    cosmetic.get_cosmetic_ingredients(product_name="cream")
    ```

*   **Search for cosmetic adverse events**
    ```
    cosmetic.search_cosmetic_events(query="skin")
    ```

*   **Get recent cosmetic recalls**
    ```
    cosmetic.get_cosmetic_recalls()
    ```

*   **Check cosmetic safety**
    ```
    cosmetic.check_cosmetic_safety(product_name="lotion")
    ```

### Cross-Category Tools 
*   **Search across all FDA categories**
    ```
    common.search_fda_products(category="food", query="ice cream")
    common.search_fda_products(category="cosmetic", query="lotion")
    ```

*   **Get company information across categories**
    ```
    common.get_fda_company_info(company_name="Johnson")
    ```

*   **Compare products across categories**
    ```
    common.compare_fda_products(product1="ice cream", product2="lotion")
    ```

*   **Get statistics for specific categories**
    ```
    common.get_fda_statistics(category="food")
    common.get_fda_statistics(category="cosmetic")
    ```

## 🧪 Running Tests

To verify that all tools work as expected, you can run the provided test suites:

### Prerequisites
- Ensure you have installed all dependencies (see Installation section above)

### Run All Test Suites

From the project root directory, run:

```bash
# Test Food Tools
uv run python test_safetyscore/test_tools/test_food_tools.py

# Test Cosmetic Tools
uv run python test_safetyscore/test_tools/test_cosmetic_tools.py

# Test Common Tools
uv run python test_safetyscore/test_tools/test_common_tools.py
```

## 📊 API Endpoints Used

### Food Safety
- **Enforcement API**: `https://api.fda.gov/food/enforcement.json`
- **Adverse Events API**: `https://api.fda.gov/food/event.json`

### Cosmetic Safety
- **Label API**: `https://api.fda.gov/cosmetics/label.json`
- **Ingredient API**: `https://api.fda.gov/cosmetics/ingredient.json`
- **Event API**: `https://api.fda.gov/cosmetics/event.json`
- **Enforcement API**: `https://api.fda.gov/cosmetics/enforcement.json`

---

**SafetySearch** - Making FDA safety data accessible to everyone through the power of MCP.