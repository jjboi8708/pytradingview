#!/usr/bin/env python3
"""
Async Example for pytradingview

This example demonstrates how to use the AsyncTVclient for high-performance,
low-latency real-time data streaming from TradingView.

Features:
- Asyncio-based WebSocket connection
- Async callback handlers
- Proper async context management
- Zero artificial delays
- High-frequency data handling
"""

import asyncio
from pytradingview import AsyncTVclient

# Optional: Use uvloop for ultra-low latency
try:
    import uvloop
    uvloop.install()
    print("🚀 uvloop enabled for ultra-low latency")
except ImportError:
    print("ℹ️ uvloop not found, using default asyncio loop")


async def main():
    """Main async function demonstrating AsyncTVclient usage."""
    
    # Create the async client and chart
    client = AsyncTVclient()
    chart = client.chart
    
    # Set up the chart
    chart.set_up_chart()
    
    # Set the market
    chart.set_market("BINANCE:BTCUSD", {
        "timeframe": "1",  # 1-minute chart
        "currency": "USD",
    })
    
    # Event: When the symbol data is loaded
    async def on_symbol_loaded(_):
        print("✅ Market loaded:", chart.get_infos['description'])
    
    chart.on_symbol_loaded(on_symbol_loaded)
    
    # Event: When price data is updated
    # Note: This callback is also async!
    async def handle_update(_):
        if chart.get_periods:
            print(f"🟢 New Price: {chart.get_periods['close']}")
    
    chart.on_update(handle_update)
    
    # Optional: Connection event handlers
    client.on_connected(lambda _: print("🔌 Connected to TradingView"))
    client.on_disconnected(lambda _: print("🔌 Disconnected from TradingView"))
    
    # Start the WebSocket connection
    # This will run until the connection is closed
    await client.create_connection()


# Alternative usage with async context manager
async def main_with_context():
    """
    Alternative example using async context manager for automatic cleanup.
    """
    async with AsyncTVclient() as client:
        chart = client.chart
        
        chart.set_up_chart()
        chart.set_market("NASDAQ:AAPL", {"timeframe": "5"})
        
        async def on_update(_):
            if chart.get_periods:
                print(f"📈 AAPL: {chart.get_periods['close']}")
        
        chart.on_update(on_update)
        
        # Run for a limited time (optional)
        connection_task = asyncio.create_task(client.create_connection())
        
        # Wait for 30 seconds then close
        await asyncio.sleep(30)
        await client.close()
        
        # Wait for connection task to complete
        try:
            await connection_task
        except asyncio.CancelledError:
            pass


# Running multiple symbols concurrently
async def multi_symbol_example():
    """
    Advanced example: Monitor multiple symbols concurrently
    using separate clients.
    """
    async def monitor_symbol(symbol, timeframe="1"):
        client = AsyncTVclient()
        chart = client.chart
        
        chart.set_up_chart()
        chart.set_market(symbol, {"timeframe": timeframe})
        
        async def on_update(_):
            if chart.get_periods:
                print(f"[{symbol}] Price: {chart.get_periods['close']}")
        
        chart.on_update(on_update)
        
        await client.create_connection()
    
    # Monitor BTC and ETH simultaneously
    await asyncio.gather(
        monitor_symbol("BINANCE:BTCUSD"),
        monitor_symbol("BINANCE:ETHUSD"),
    )


if __name__ == "__main__":
    # Run the basic example
    # You can also try: asyncio.run(main_with_context())
    # or: asyncio.run(multi_symbol_example())
    asyncio.run(main())
