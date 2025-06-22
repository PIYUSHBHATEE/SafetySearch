#!/usr/bin/env python3
"""
Test script for SafetySearch common tools using real FDA API endpoints.
This script tests all common tools to ensure they work correctly across categories.
"""

import asyncio
import sys
import os
from datetime import datetime
import pytest

# Add the project root to the path so we can import safetyscore
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from safetyscore.tools.common import register_common_tools
from mcp.server.fastmcp import FastMCP

# Create a mock MCP server for testing
test_mcp = FastMCP("TestSafetySearch")
register_common_tools(test_mcp)

# Get the registered tools from the server
def get_tool_functions():
    """Extract tool functions from the FastMCP server's ToolManager."""
    tools = {}
    if hasattr(test_mcp, '_tool_manager') and hasattr(test_mcp._tool_manager, '_tools'):
        for tool_name, tool_obj in test_mcp._tool_manager._tools.items():
            tools[tool_name] = tool_obj.fn
    return tools

@pytest.mark.asyncio
async def test_common_tools():
    """Test all common tools with real FDA API examples."""
    
    print("🔍 Testing SafetySearch Common Tools (Cross-Category)")
    print("=" * 60)
    
    # Get the tool functions
    tools = get_tool_functions()
    
    if not tools:
        print("❌ No tools found! Check if tools are properly registered.")
        return False
    
    print(f"📋 Found {len(tools)} tools: {list(tools.keys())}")
    
    # Test results tracking
    passed_tests = 0
    total_tests = 0
    
    async def run_test(test_name, tool_func, *args, **kwargs):
        """Helper function to run a test and track results."""
        nonlocal passed_tests, total_tests
        total_tests += 1
        
        print(f"\n📋 Test {total_tests}: {test_name}")
        print("-" * 50)
        
        try:
            # Await the async function
            result = await tool_func(*args, **kwargs)
            
            # Check if the result is valid
            if result and not result.startswith("Error"):
                print(f"✅ PASS: {result[:100]}...")
                passed_tests += 1
                return True
            else:
                print(f"❌ FAIL: {result}")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return False
    
    # Test 1: Search FDA products in food category
    print("\n🍎 Testing food category search...")
    await run_test(
        "Search FDA products - food category",
        tools["search_fda_products"],
        category="food",
        query="ice cream"
    )
    
    # Test 2: Search FDA products in drug category
    print("\n💊 Testing drug category search...")
    await run_test(
        "Search FDA products - drug category",
        tools["search_fda_products"],
        category="drug",
        query="aspirin"
    )
    
    # Test 3: Search FDA products in cosmetic category
    print("\n💄 Testing cosmetic category search...")
    await run_test(
        "Search FDA products - cosmetic category",
        tools["search_fda_products"],
        category="cosmetic",
        query="lotion"
    )
    
    # Test 4: Get FDA company information
    print("\n🏢 Testing company information...")
    await run_test(
        "Get FDA company info - generic company search",
        tools["get_fda_company_info"],
        company_name="generic"
    )
    
    # Test 5: Compare FDA products
    print("\n⚖️ Testing product comparison...")
    await run_test(
        "Compare FDA products - aspirin vs ibuprofen",
        tools["compare_fda_products"],
        product1="aspirin",
        product2="ibuprofen"
    )
    
    # Test 6: Get FDA statistics for food
    print("\n📊 Testing food statistics...")
    await run_test(
        "Get FDA statistics - food category",
        tools["get_fda_statistics"],
        category="food"
    )
    
    # Test 7: Get FDA statistics for drug
    print("\n📊 Testing drug statistics...")
    await run_test(
        "Get FDA statistics - drug category",
        tools["get_fda_statistics"],
        category="drug"
    )
    
    # Test 8: Get FDA statistics for cosmetic
    print("\n📊 Testing cosmetic statistics...")
    await run_test(
        "Get FDA statistics - cosmetic category",
        tools["get_fda_statistics"],
        category="cosmetic"
    )
    
    # Additional edge case tests
    print("\n🔍 Testing edge cases...")
    
    # Test 9: Search with invalid category
    await run_test(
        "Search with invalid category",
        tools["search_fda_products"],
        category="invalid",
        query="test"
    )
    
    # Test 10: Search with empty query
    await run_test(
        "Search with empty query",
        tools["search_fda_products"],
        category="food",
        query=""
    )
    
    # Test 11: Get statistics with invalid category
    await run_test(
        "Get statistics with invalid category",
        tools["get_fda_statistics"],
        category="invalid"
    )
    
    # Test 12: Compare non-existent products
    await run_test(
        "Compare non-existent products",
        tools["compare_fda_products"],
        product1="NONEXISTENT1",
        product2="NONEXISTENT2"
    )
    
    # Test 13: Get company info for non-existent company
    await run_test(
        "Get company info for non-existent company",
        tools["get_fda_company_info"],
        company_name="NONEXISTENTCOMPANY123"
    )
    
    # Test 14: Search with special characters
    print("\n🔤 Testing special characters...")
    await run_test(
        "Search with special characters",
        tools["search_fda_products"],
        category="food",
        query="Ben & Jerry's"
    )
    
    # Test 15: Test case sensitivity
    print("\n🔤 Testing case sensitivity...")
    await run_test(
        "Test case sensitivity - FOOD vs food",
        tools["search_fda_products"],
        category="FOOD",
        query="milk"
    )
    
    # Print test summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary:")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {total_tests - passed_tests}")
    print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Common tools are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed_tests == total_tests

def run_individual_tool(tool_name, *args, **kwargs):
    """Test a specific tool with given parameters."""
    tools = get_tool_functions()
    
    if tool_name not in tools:
        print(f"❌ Tool '{tool_name}' not found!")
        return None
    
    async def run_single_test():
        return await tools[tool_name](*args, **kwargs)
    
    return asyncio.run(run_single_test())

def test_cross_category_functionality():
    """Test specific cross-category scenarios."""
    print("\n🔄 Testing Cross-Category Functionality")
    print("=" * 50)
    
    # Test scenarios that involve multiple categories
    test_scenarios = [
        {
            "name": "Food to Drug Comparison",
            "tool": "compare_fda_products",
            "args": ["ice cream", "aspirin"],
            "description": "Compare a food product with a drug"
        },
        {
            "name": "Drug to Cosmetic Comparison", 
            "tool": "compare_fda_products",
            "args": ["acetaminophen", "lotion"],
            "description": "Compare a drug with a cosmetic"
        },
        {
            "name": "Multi-Category Company Search",
            "tool": "get_fda_company_info",
            "args": ["Johnson"],
            "description": "Search for a company across all categories"
        }
    ]
    
    tools = get_tool_functions()
    passed = 0
    total = len(test_scenarios)
    
    for scenario in test_scenarios:
        print(f"\n📋 {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        
        try:
            result = asyncio.run(tools[scenario['tool']](*scenario['args']))
            if result and not result.startswith("Error"):
                print(f"   ✅ PASS: {result[:80]}...")
                passed += 1
            else:
                print(f"   ❌ FAIL: {result}")
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print(f"\n📊 Cross-Category Test Summary: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    # Run the main test suite
    print("🚀 Starting SafetySearch Common Tools Test Suite")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = asyncio.run(test_common_tools())
    
    # Run cross-category tests
    cross_category_success = test_cross_category_functionality()
    
    if success and cross_category_success:
        print("\n🎉 Common tools test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Common tools test suite had failures.")
        sys.exit(1) 