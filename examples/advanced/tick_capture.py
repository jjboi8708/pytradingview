import asyncio

# Enable uvloop for ultra-low latency
try:
    import uvloop
    uvloop.install()
    print("🚀 uvloop enabled")
except ImportError:
    print("⚠️  uvloop not installed, using default event loop")

from pytradingview import AsyncTVclient


async def main():
    """
    This script uses QuoteSession to capture EVERY individual tick.
    
    ChartSession = Candle aggregations (OHLCV) - may skip intermediate ticks
    QuoteSession = Raw tick data - captures EVERY price update
    """
    client = AsyncTVclient()
    quote = client.quote
    
    # Set up quote session with minimal fields for maximum speed
    quote.set_up_quote({'fields': 'price'})  # Only request last price
    
    # Track last price to show what changed
    last_price = None
    tick_count = 0
    
    async def on_tick(data):
        nonlocal last_price, tick_count
        
        try:
            # Extract last price from quote data
            # Data structure: {'type': 'qsd', 'data': [session_id, {'n': symbol, 'v': {fields}}]}
            if data['type'] == 'qsd':
                values = data['data'][1]['v']
                
                if 'lp' in values:
                    price = values['lp']
                    tick_count += 1
                    
                    # Show every tick with change indicator
                    if last_price is not None:
                        change = price - last_price
                        arrow = "🔺" if change > 0 else "🔻" if change < 0 else "➡️"
                        print(f"{arrow} Tick #{tick_count}: {price:,.2f} (Δ {change:+.2f})")
                    else:
                        print(f"⚡ Initial Price: {price:,.2f}")
                    
                    last_price = price
                    
            elif data['type'] == 'quote_completed':
                symbol = data['data'][1]
                print(f"✅ Quote stream ready for {symbol}")
                
        except (KeyError, IndexError, TypeError) as e:
            print(f"⚠️  Parse error: {e}")
    
    # Add symbol - try multiple formats to find the right one
    symbol = "CRYPTO:SOLUSD"  # Format: EXCHANGE:SYMBOL or CRYPTO:SYMBOL
    
    print(f"📡 Subscribing to {symbol}...")
    quote.add_symbol(symbol, on_tick)
    
    # Optional: Add connection handlers for debugging
    client.on_connected(lambda _: print("🌐 Connected to TradingView"))
    client.on_error(lambda e: print(f"❌ Error: {e}"))
    
    # Start the connection
    print("⏳ Connecting...")
    await client.create_connection()


if __name__ == "__main__":
    asyncio.run(main())
