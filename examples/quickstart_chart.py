import asyncio
import os

# Try to enable uvloop for ultra-low latency
try:
    import uvloop
    uvloop.install()
    print("🚀 uvloop enabled")
except ImportError:
    print("⚠️ uvloop not installed")

from pytradingview import AsyncTVclient

async def main():
    client = AsyncTVclient()

    # Setup ChartSession
    chart = client.chart
    chart.set_up_chart()
    chart.set_market("CRYPTO:SOLUSD", {"timeframe": "1"})
    
    async def on_update(changes):
        # Only print if price changed to avoid clutter
        # But for "blink of an eye" feel, printing every update shows the speed
        if chart.get_periods:
            print(f"⚡ Price: {chart.get_periods['close']}")
    
    chart.on_update(on_update)
    
    # Run the connection
    await client.create_connection()

asyncio.run(main())