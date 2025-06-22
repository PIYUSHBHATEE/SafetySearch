#!/usr/bin/env python3
"""
Test script for SafetySearch drug tools using real FDA API endpoints.
This script tests all drug tools to ensure they work correctly.
"""

import asyncio
import sys
import os

# Add the project root to the path so we can import safetyscore
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from safetyscore.tools.drug import register_drug_tools
from mcp.server.fastmcp import FastMCP

# Create a mock MCP server for testing
test_mcp = FastMCP("TestSafetySearch")
register_drug_tools(test_mcp)

# Get the registered tools from the server
def get_tool_functions():
    """Extract tool functions from the FastMCP server's ToolManager."""
    tools = {}
    if hasattr(test_mcp, '_tool_manager') and hasattr(test_mcp._tool_manager, '_tools'):
        for tool_name, tool_obj in test_mcp._tool_manager._tools.items():
            tools[tool_name] = tool_obj.fn
    return tools

async def test_drug_tools():
    """Test all drug tools with real FDA API examples."""
    
    print("💊 Testing SafetySearch Drug Tools")
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
    
    # Test 1: Search for drugs containing "aspirin"
    print("\n💊 Testing aspirin search...")
    await run_test(
        "Search drugs - aspirin",
        tools["search_drugs"],
        query="aspirin"
    )
    
    # Test 2: Get drug label for "acetaminophen"
    print("\n💊 Testing drug label retrieval...")
    await run_test(
        "Get drug label - acetaminophen",
        tools["get_drug_label"],
        drug_name="acetaminophen"
    )
    
    # Test 3: Get drug approvals for current year
    print("\n💊 Testing drug approvals...")
    await run_test(
        "Get drug approvals - 2024",
        tools["get_drug_approvals"],
        year=2024
    )
    
    # Test 4: Check current drug shortages
    print("\n💊 Testing drug shortages...")
    await run_test(
        "Check drug shortages",
        tools["check_drug_shortages"]
    )
    
    # Test 5: Search for drug recalls
    print("\n💊 Testing drug recall search...")
    await run_test(
        "Search drug recalls - generic",
        tools["search_drug_recalls"],
        query="generic"
    )
    
    # Test 6: Get adverse events for a common drug
    print("\n💊 Testing adverse events...")
    await run_test(
        "Get adverse events - ibuprofen",
        tools["get_drug_adverse_events"],
        drug_name="ibuprofen"
    )
    
    # Test 7: Check drug interactions
    print("\n💊 Testing drug interactions...")
    await run_test(
        "Check drug interactions - aspirin and ibuprofen",
        tools["check_drug_interactions"],
        drug1="aspirin",
        drug2="ibuprofen"
    )
    
    # Additional edge case tests
    print("\n🔍 Testing edge cases...")
    
    # Test 8: Search with empty query
    await run_test(
        "Search with empty query",
        tools["search_drugs"],
        query=""
    )
    
    # Test 9: Search with non-existent drug
    await run_test(
        "Search with non-existent drug",
        tools["get_drug_label"],
        drug_name="NONEXISTENTDRUG123"
    )
    
    # Test 10: Check interactions with non-existent drugs
    await run_test(
        "Check interactions with non-existent drugs",
        tools["check_drug_interactions"],
        drug1="NONEXISTENT1",
        drug2="NONEXISTENT2"
    )
    
    # Print test summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {total_tests - passed_tests}")
    print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Drug tools are working correctly.")
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
    success = asyncio.run(test_drug_tools())
    
    if success:
        print("\n🎉 Drug tools test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Drug tools test suite had failures.")
        sys.exit(1) 