<p align="center">
  <img src="./SafetySearch-logo.png" alt="SafetySearch Logo" width="200">
</p>

# SafetySearch

> Search. Scan. Stay Safe.

A comprehensive Model Context Protocol (MCP) server that provides access to FDA (Food and Drug Administration) data for **Food** safety information.

## 🎯 What This Server Provides

This MCP server offers **8 tools** to access product safety data, helping users:
- Check product recalls and safety alerts for food products
- Monitor food safety issues and recall trends
- Analyze safety trends and company information
- Get comprehensive food safety insights

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

### Food Safety Tools (8 tools) ✅

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_recalls_by_product_description` | Searches for food recalls with detailed analysis, safety insights, and comprehensive reporting. | `query: str` |
| `search_recalls_by_product_type` | Searches for recalls by product type with detailed analysis, company trends, and safety recommendations. | `product_type: str` |
| `search_recalls_by_specific_product` | Checks for recalls on specific products with detailed safety information and recommendations. | `product_name: str` |
| `search_recalls_by_classification` | Searches for recalls by classification with detailed analysis and risk assessment. | `classification: str` |
| `search_recalls_by_code_info` | Searches for recalls by code info with detailed product tracking and safety alerts. | `code_info: str` |
| `search_recalls_by_date` | Searches for recalls by date range with detailed timeline analysis and safety trends. | `days: int` (default: 30) |
| `search_adverse_events_by_product` | Searches for adverse events with detailed case analysis and safety insights. | `product_name: str` |
| `get_symptom_summary_for_product` | Gets detailed symptom analysis, case details, and safety insights for a specific food product. | `product_name: str` |

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

*   **Find adverse events for "Cheerios"**
    ```
    food.search_adverse_events_by_product(product_name="Cheerios")
    ```

*   **Get a summary of symptoms reported for "Lucky Charms"**
    ```
    food.get_symptom_summary_for_product(product_name="Lucky Charms")
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
```

## 📊 API Endpoints Used

### Food Safety
- **Enforcement API**: `https://api.fda.gov/food/enforcement.json`
- **Adverse Events API**: `https://api.fda.gov/food/event.json`

---

**SafetySearch** - Making FDA safety data accessible to everyone through the power of MCP.