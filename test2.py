import asyncio
from pytradingview import AsyncTVclient
async def main():
    client = AsyncTVclient()
    chart = client.chart
    
    # Setup remains identical to sync version
    chart.set_up_chart()
    chart.set_market("CRYPTO:SOLUSD", {"timeframe": "1"})
    
    # Callbacks can be async
    async def on_update(_):
        print(f"Price: {chart.get_periods['close']}")
    
    chart.on_update(on_update)
    
    # Run the connection
    await client.create_connection()
asyncio.run(main())