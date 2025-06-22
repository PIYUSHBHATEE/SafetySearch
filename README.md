<p align="center">
  <img src="./SafetySearch-logo.png" alt="SafetySearch Logo" width="200">
</p>

# SafetySearch

> Search. Scan. Stay Safe.

A Model Context Protocol (MCP) server that provides access to FDA (Food and Drug Administration) data across three major categories: **Food**, **Drug**, and **Cosmetic** safety information.

## 🎯 What This Server Provides

This MCP server offers **22 tools** to access product safety data, helping users:
- Check product recalls and safety alerts
- Search drug information and interactions
- Monitor food safety issues
- Review cosmetic safety reports
- Compare FDA-regulated products
- Analyze safety trends across categories

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
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

### Development Mode (MCP Inspector)
Test and validate the server using the MCP Inspector:
```bash
mcp dev server.py
```

### Direct Execution
Run the server directly:
```bash
python server.py
```

### Install in Claude Desktop
Install the server in Claude Desktop for production use:
```bash
mcp install server.py
```

## 🛠️ Available Tools

### Food Safety Tools (6 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_food_recalls` | Search for food recalls by product name, company, or description | `query: str` |
| `get_recent_food_recalls` | Get food recalls from the last specified number of days | `days: int` (default: 30) |
| `get_food_recall_by_class` | Get food recalls by classification (Class I, II, III) | `classification: str` |
| `check_food_product_recall` | Check if a specific food product has any recalls | `product_name: str` |
| `get_food_safety_alerts` | Get recent food safety alerts and warnings | None |
| `analyze_food_recall_trends` | Analyze food recall patterns and trends | None |

### Drug Safety Tools (7 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_drugs` | Search for drug information by name, active ingredient, or description | `query: str` |
| `get_drug_label` | Get detailed drug labeling information including warnings and dosage | `drug_name: str` |
| `get_drug_approvals` | Get drug approvals for a specific year | `year: int` |
| `check_drug_shortages` | Check current drug shortages and availability | None |
| `search_drug_recalls` | Search for drug recalls by product name or company | `query: str` |
| `get_drug_adverse_events` | Get adverse event reports for a specific drug | `drug_name: str` |
| `check_drug_interactions` | Check potential interactions between two drugs | `drug1: str`, `drug2: str` |

### Cosmetic Safety Tools (6 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_cosmetics` | Search for cosmetic products by name or description | `query: str` |
| `get_cosmetic_product_info` | Get detailed information about a cosmetic product | `product_name: str` |
| `get_cosmetic_ingredients` | Get ingredient information for a cosmetic product | `product_name: str` |
| `search_cosmetic_events` | Search for cosmetic adverse events and safety reports | `query: str` |
| `get_cosmetic_recalls` | Get recent cosmetic recalls and safety alerts | None |
| `check_cosmetic_safety` | Check safety information for a cosmetic product | `product_name: str` |

### Cross-Category Tools (3 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_fda_products` | Search across all FDA categories (food, drug, cosmetic) | `category: str`, `query: str` |
| `get_fda_company_info` | Get information about a company across all FDA categories | `company_name: str` |
| `compare_fda_products` | Compare two FDA-regulated products | `product1: str`, `product2: str` |
| `get_fda_statistics` | Get FDA statistics and data for a specific category | `category: str` |

## 📋 Example Usage

### Food Safety Tools
```
```

### Drug Safety Tools
```
```

### Cometic Safety Tools
```
```

### Cross-Category Tools 
```
```