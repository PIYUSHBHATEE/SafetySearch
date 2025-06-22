#!/usr/bin/env python3
"""
Test script for SafetySearch food tools using examples from README.
This script tests all food tools with real-world examples to ensure they work correctly.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the project root to the path so we can import safetyscore
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
print('DEBUG project_root:', project_root)
sys.path.insert(0, project_root)
print('DEBUG sys.path:', sys.path)

from safetyscore.tools.food import register_food_tools
from mcp.server.fastmcp import FastMCP

# Create a mock MCP server for testing
test_mcp = FastMCP("TestSafetySearch")
register_food_tools(test_mcp)

# Debug: print FastMCP attributes to find where tools are stored
print("DEBUG FastMCP attributes:", dir(test_mcp))
print("DEBUG _tool_manager:", test_mcp._tool_manager)
print("DEBUG _tool_manager dir:", dir(test_mcp._tool_manager))
print("DEBUG _tool_manager _tools:", test_mcp._tool_manager._tools)

# Get the registered tools from the server
def get_tool_functions():
    """Extract tool functions from the FastMCP server's ToolManager."""
    tools = {}
    if hasattr(test_mcp, '_tool_manager') and hasattr(test_mcp._tool_manager, '_tools'):
        for tool_name, tool_obj in test_mcp._tool_manager._tools.items():
            tools[tool_name] = tool_obj.fn
    return tools

async def test_food_tools():
    """Test all food tools with examples from the README."""
    
    print("🧪 Testing SafetySearch Food Tools")
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
    
    # Test 1: Search for recalls of "ice cream"
    print("\n🍦 Testing ice cream recalls...")
    await run_test(
        "Search recalls by product description - ice cream",
        tools["search_recalls_by_product_description"],
        query="ice cream"
    )
    
    # Test 2: Find recalls for "Bakery" products
    print("\n🥖 Testing bakery product recalls...")
    await run_test(
        "Search recalls by product type - Bakery",
        tools["search_recalls_by_product_type"],
        product_type="Bakery"
    )
    
    # Test 3: Check for recalls on "Ben & Jerry's Chocolate Fudge Brownie"
    print("\n🍫 Testing specific product recall check...")
    await run_test(
        "Search recalls by specific product - Ben & Jerry's",
        tools["search_recalls_by_specific_product"],
        product_name="Ben & Jerry's Chocolate Fudge Brownie"
    )
    
    # Test 4: Find recalls with classification "Class I"
    print("\n⚠️ Testing Class I recalls...")
    await run_test(
        "Search recalls by classification - Class I",
        tools["search_recalls_by_classification"],
        classification="Class I"
    )
    
    # Test 5: Search for a recall with code info "222268"
    print("\n🔢 Testing code info search...")
    await run_test(
        "Search recalls by code info - 222268",
        tools["search_recalls_by_code_info"],
        code_info="222268"
    )
    
    # Test 6: Get all recalls from the last 14 days
    print("\n📅 Testing recent recalls (14 days)...")
    await run_test(
        "Search recalls by date - last 14 days",
        tools["search_recalls_by_date"],
        days=14
    )
    
    # Test 7: Get top 5 reasons for recalls in the last 90 days
    print("\n📊 Testing recall trends analysis...")
    await run_test(
        "Get recall trends by reason",
        tools["get_recall_trends_by_reason"]
    )
    
    # Test 8: Find adverse events for "Cheerios"
    print("\n🥣 Testing adverse events for Cheerios...")
    await run_test(
        "Search adverse events by product - Cheerios",
        tools["search_adverse_events_by_product"],
        product_name="Cheerios"
    )
    
    # Test 9: Get a summary of symptoms reported for "Lucky Charms"
    print("\n🍀 Testing symptom summary for Lucky Charms...")
    await run_test(
        "Get symptom summary for product - Lucky Charms",
        tools["get_symptom_summary_for_product"],
        product_name="Lucky Charms"
    )
    
    # Additional edge case tests
    print("\n🔍 Testing edge cases...")
    
    # Test 10: Search with empty query
    await run_test(
        "Search with empty query",
        tools["search_recalls_by_product_description"],
        query=""
    )
    
    # Test 11: Search with very short date range
    await run_test(
        "Search with 1 day range",
        tools["search_recalls_by_date"],
        days=1
    )
    
    # Test 12: Search with non-existent code
    await run_test(
        "Search with non-existent code",
        tools["search_recalls_by_code_info"],
        code_info="NONEXISTENT123"
    )
    
    # Print test summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {total_tests - passed_tests}")
    print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Food tools are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed_tests == total_tests

def test_individual_tool(tool_name, *args, **kwargs):
    """Test a specific tool with given parameters."""
    tools = get_tool_functions()
    
    if tool_name not in tools:
        print(f"❌ Tool '{tool_name}' not found!")
        return None
    
    print(f"\n🧪 Testing {tool_name}...")
    print("-" * 40)
    
    try:
        tool_func = tools[tool_name]
        result = asyncio.run(tool_func(*args, **kwargs))
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 Starting SafetySearch Food Tools Test Suite")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    success = asyncio.run(test_food_tools())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 