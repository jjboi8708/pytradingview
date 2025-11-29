import asyncio
import uvloop
uvloop.install()

from pytradingview import AsyncTVclient


async def main():
    """Debug script to see ALL raw WebSocket messages"""
    client = AsyncTVclient()
    
    # Hook into data event to see ALL messages
    async def on_data(packet):
        print(f"📦 RAW DATA: {packet}")
    
    async def on_error(err):
        print(f"❌ ERROR: {err}")
    
    client.on_data(on_data)
    client.on_error(on_error)
    client.on_connected(lambda _: print("✅ Connected\n"))
    
    # Set up BOTH chart and quote to compare
    print("Setting up ChartSession...")
    chart = client.chart
    chart.set_up_chart()
    chart.set_market("CRYPTO:SOLUSD", {"timeframe": "1"})
    
    print("Setting up QuoteSession...")
    quote = client.quote
    quote.set_up_quote({'customFields': ['lp', 'ch', 'chp']})
    quote.add_symbol("CRYPTO:SOLUSD", lambda d: print(f"📊 QUOTE: {d}"))
    
    print("\n⏳ Connecting...\n")
    await client.create_connection()


if __name__ == "__main__":
    asyncio.run(main())
