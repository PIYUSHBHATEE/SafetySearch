#!/usr/bin/env python3
"""
Test script for SafetySearch cosmetic tools using real FDA API endpoints.
This script tests all cosmetic tools to ensure they work correctly.
"""

import asyncio
import sys
import os

# Add the project root to the path so we can import safetyscore
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from safetyscore.tools.cosmetic import register_cosmetic_tools
from mcp.server.fastmcp import FastMCP

# Create a mock MCP server for testing
test_mcp = FastMCP("TestSafetySearch")
register_cosmetic_tools(test_mcp)

# Get the registered tools from the server
def get_tool_functions():
    """Extract tool functions from the FastMCP server's ToolManager."""
    tools = {}
    if hasattr(test_mcp, '_tool_manager') and hasattr(test_mcp._tool_manager, '_tools'):
        for tool_name, tool_obj in test_mcp._tool_manager._tools.items():
            tools[tool_name] = tool_obj.fn
    return tools

async def test_cosmetic_tools():
    """Test all cosmetic tools with real FDA API examples."""
    
    print("💄 Testing SafetySearch Cosmetic Tools")
    print("=" * 50)
    
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
        print("-" * 40)
        
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
    
    # Test 1: Search for cosmetic products
    print("\n💄 Testing cosmetic search...")
    await run_test(
        "Search cosmetics - lotion",
        tools["search_cosmetics"],
        query="lotion"
    )
    
    # Test 2: Get cosmetic product information
    print("\n💄 Testing product info retrieval...")
    await run_test(
        "Get cosmetic product info - generic search",
        tools["get_cosmetic_product_info"],
        product_name="lotion"
    )
    
    # Test 3: Get cosmetic ingredients
    print("\n💄 Testing ingredient retrieval...")
    await run_test(
        "Get cosmetic ingredients - generic search",
        tools["get_cosmetic_ingredients"],
        product_name="cream"
    )
    
    # Test 4: Search for cosmetic events
    print("\n💄 Testing cosmetic events...")
    await run_test(
        "Search cosmetic events - skin",
        tools["search_cosmetic_events"],
        query="skin"
    )
    
    # Test 5: Get cosmetic recalls
    print("\n💄 Testing cosmetic recalls...")
    await run_test(
        "Get cosmetic recalls",
        tools["get_cosmetic_recalls"]
    )
    
    # Test 6: Check cosmetic safety
    print("\n💄 Testing cosmetic safety check...")
    await run_test(
        "Check cosmetic safety - generic search",
        tools["check_cosmetic_safety"],
        product_name="shampoo"
    )
    
    # Additional edge case tests
    print("\n🔍 Testing edge cases...")
    
    # Test 7: Search with empty query
    await run_test(
        "Search with empty query",
        tools["search_cosmetics"],
        query=""
    )
    
    # Test 8: Search with non-existent product
    await run_test(
        "Search with non-existent product",
        tools["get_cosmetic_product_info"],
        product_name="NONEXISTENTCOSMETIC123"
    )
    
    # Test 9: Get ingredients for non-existent product
    await run_test(
        "Get ingredients for non-existent product",
        tools["get_cosmetic_ingredients"],
        product_name="NONEXISTENTCOSMETIC123"
    )
    
    # Test 10: Check safety for non-existent product
    await run_test(
        "Check safety for non-existent product",
        tools["check_cosmetic_safety"],
        product_name="NONEXISTENTCOSMETIC123"
    )
    
    # Print test summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {total_tests - passed_tests}")
    print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Cosmetic tools are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed_tests == total_tests

def test_individual_tool(tool_name, *args, **kwargs):
    """Test a specific tool with given parameters."""
    tools = get_tool_functions()
    
    if tool_name not in tools:
        print(f"❌ Tool '{tool_name}' not found!")
        return None
    
    async def run_single_test():
        return await tools[tool_name](*args, **kwargs)
    
    return asyncio.run(run_single_test())

if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(test_cosmetic_tools())
    
    if success:
        print("\n🎉 Cosmetic tools test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Cosmetic tools test suite had failures.")
        sys.exit(1) 