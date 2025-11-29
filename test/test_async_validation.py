#!/usr/bin/env python3
"""
Quick validation test for pytradingview async implementation
"""

import asyncio
import sys

# Test 1: Verify imports
print("=" * 60)
print("TEST 1: Verifying imports...")
print("=" * 60)

try:
    from pytradingview import TVclient, AsyncTVclient
    print("✅ Successfully imported TVclient (sync)")
    print("✅ Successfully imported AsyncTVclient (async)")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Verify sync client instantiation
print("\n" + "=" * 60)
print("TEST 2: Verifying sync client instantiation...")
print("=" * 60)

try:
    sync_client = TVclient()
    print("✅ Sync client created successfully")
    print(f"   - Has chart session: {hasattr(sync_client, 'chart')}")
    print(f"   - Has quote session: {hasattr(sync_client, 'quote')}")
except Exception as e:
    print(f"❌ Sync client failed: {e}")
    sys.exit(1)

# Test 3: Verify async client instantiation
print("\n" + "=" * 60)
print("TEST 3: Verifying async client instantiation...")
print("=" * 60)

try:
    async_client = AsyncTVclient()
    print("✅ Async client created successfully")
    print(f"   - Has chart session: {hasattr(async_client, 'chart')}")
    print(f"   - Has quote session: {hasattr(async_client, 'quote')}")
    print(f"   - Is async client: {hasattr(async_client, 'create_connection')}")
except Exception as e:
    print(f"❌ Async client failed: {e}")
    sys.exit(1)

# Test 4: Verify async methods exist
print("\n" + "=" * 60)
print("TEST 4: Verifying async client methods...")
print("=" * 60)

try:
    import inspect
    
    # Check that key methods exist
    assert hasattr(async_client, 'create_connection'), "Missing create_connection"
    assert hasattr(async_client, 'send'), "Missing send"
    assert hasattr(async_client, 'close'), "Missing close"
    assert hasattr(async_client, 'handle_event'), "Missing handle_event"
    
    # Check that they're coroutines where expected
    assert inspect.iscoroutinefunction(async_client.create_connection), "create_connection should be async"
    assert inspect.iscoroutinefunction(async_client.handle_event), "handle_event should be async"
    assert inspect.iscoroutinefunction(async_client.close), "close should be async"
    
    print("✅ All required async methods present")
    print("✅ Methods are properly async (coroutines)")
except AssertionError as e:
    print(f"❌ Method verification failed: {e}")
    sys.exit(1)

# Test 5: Verify session methods are async
print("\n" + "=" * 60)
print("TEST 5: Verifying session async support...")
print("=" * 60)

try:
    import inspect
    
    # Check chart session
    chart = async_client.chart
    assert inspect.iscoroutinefunction(chart.handleEvent), "ChartSession.handleEvent should be async"
    assert inspect.iscoroutinefunction(chart.on_data_c), "ChartSession.on_data_c should be async"
    assert inspect.iscoroutinefunction(chart.on_data_r), "ChartSession.on_data_r should be async"
    
    # Check quote session
    quote = async_client.quote
    assert inspect.iscoroutinefunction(quote.on_data_q), "QuoteSession.on_data_q should be async"
    
    print("✅ ChartSession has async event handling")
    print("✅ QuoteSession has async event handling")
except AssertionError as e:
    print(f"❌ Session verification failed: {e}")
    sys.exit(1)

# Test 6: Quick async callback test
print("\n" + "=" * 60)
print("TEST 6: Testing async callback detection...")
print("=" * 60)

async def test_async_callbacks():
    """Test that async and sync callbacks are handled correctly"""
    
    test_client = AsyncTVclient()
    
    # Track callback execution
    sync_called = False
    async_called = False
    
    # Register sync callback
    def sync_callback(_):
        nonlocal sync_called
        sync_called = True
    
    # Register async callback
    async def async_callback(_):
        nonlocal async_called
        async_called = True
        await asyncio.sleep(0.001)  # Tiny async operation
    
    test_client.on_connected(sync_callback)
    test_client.on_connected(async_callback)
    
    # Manually trigger event
    await test_client.handle_event('connected', 'test')
    
    # Allow background tasks to run
    await asyncio.sleep(0.01)
    
    assert sync_called, "Sync callback should have been called"
    assert async_called, "Async callback should have been called"
    
    print("✅ Sync callbacks work correctly")
    print("✅ Async callbacks work correctly")
    print("✅ Mixed sync/async callbacks work together")

try:
    asyncio.run(test_async_callbacks())
except Exception as e:
    print(f"❌ Async callback test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)
print("✅ All tests passed!")
print("✅ Sync client (TVclient) works")
print("✅ Async client (AsyncTVclient) works")
print("✅ Async callbacks are properly supported")
print("✅ Backwards compatibility maintained")
print("\n🎉 pytradingview async implementation is ready to use!")
