import asyncio
import time

try:
    import uvloop
    uvloop.install()
    print("🚀 uvloop enabled\n")
except ImportError:
    pass

from pytradingview import AsyncTVclient


async def main():
    """
    Debug script to capture ALL data from QuoteSession with ALL fields.
    This will help us see if TradingView is sending every tick or throttling.
    """
    client = AsyncTVclient()
    symbol = "CRYPTO:SOLUSD"
    
    # Track all updates with timestamps
    updates = []
    last_price = None
    
    print(f"📡 Monitoring {symbol} with ALL quote fields enabled")
    print("=" * 70)
    
    # Use ALL available fields (not just price)
    all_fields = [
        'lp',           # Last Price (most important)
        'lp_time',      # Last Price Time
        'ch',           # Change
        'chp',          # Change Percent
        'volume',       # Volume
        'ask',          # Ask Price
        'bid',          # Bid Price
        'high_price',   # High
        'low_price',    # Low
        'open_price',   # Open
        'prev_close_price',  # Previous Close
    ]
    
    quote = client.quote
    quote.set_up_quote({'customFields': all_fields})
    
    async def on_quote(data):
        nonlocal last_price
        
        try:
            if data['type'] == 'qsd':
                timestamp = time.time()
                values = data['data'][1]['v']
                
                # Log the update
                updates.append({
                    'time': timestamp,
                    'data': values.copy()
                })
                
                # Print detailed info for first 20 updates
                if len(updates) <= 20:
                    print(f"\n📊 Update #{len(updates)} at {time.strftime('%H:%M:%S', time.localtime(timestamp))}")
                    
                    # Show what fields changed
                    if 'lp' in values:
                        price = values['lp']
                        if last_price is not None and price != last_price:
                            delta = price - last_price
                            print(f"   💲 PRICE: {last_price} → {price} (Δ {delta:+.2f})")
                        else:
                            print(f"   💲 PRICE: {price}")
                        last_price = price
                    
                    # Show other field changes
                    if 'volume' in values:
                        print(f"   📊 VOLUME: {values['volume']}")
                    if 'bid' in values and 'ask' in values:
                        spread = values['ask'] - values['bid']
                        print(f"   📈 BID/ASK: {values['bid']}/{values['ask']} (spread: {spread:.2f})")
                    
                    # Show ALL fields received
                    print(f"   🔍 Fields in this update: {list(values.keys())}")
                
                elif len(updates) == 21:
                    print(f"\n... (showing first 20 updates, continuing to collect data) ...\n")
                    
            elif data['type'] == 'quote_completed':
                print(f"✅ Quote stream ready for {data['data'][1]}\n")
                
        except (KeyError, IndexError, TypeError) as e:
            print(f"⚠️  Parse error: {e}")
    
    quote.add_symbol(symbol, on_quote)
    
    # Run for 60 seconds
    print(f"⏱️  Collecting data for 60 seconds...\n")
    
    connection_task = asyncio.create_task(client.create_connection())
    
    try:
        await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    
    # Analysis
    print("\n" + "=" * 70)
    print("📊 ANALYSIS")
    print("=" * 70)
    
    if len(updates) > 1:
        # Calculate update frequency
        duration = updates[-1]['time'] - updates[0]['time']
        avg_interval = duration / (len(updates) - 1) * 1000
        
        print(f"\n📈 Update Statistics:")
        print(f"   • Total Updates: {len(updates)}")
        print(f"   • Duration: {duration:.1f}s")
        print(f"   • Avg Interval: {avg_interval:.1f}ms")
        print(f"   • Update Rate: {len(updates) / duration:.2f} updates/second")
        
        # Check for price changes
        price_updates = [u for u in updates if 'lp' in u['data']]
        prices = [u['data']['lp'] for u in price_updates]
        unique_prices = len(set(prices))
        
        print(f"\n💲 Price Changes:")
        print(f"   • Updates with price: {len(price_updates)}")
        print(f"   • Unique prices: {unique_prices}")
        print(f"   • Price change rate: {unique_prices / len(price_updates) * 100:.1f}%")
        
        if unique_prices > 1:
            print(f"\n   Price range: {min(prices):.2f} → {max(prices):.2f}")
        
        # Field frequency analysis
        print(f"\n🔍 Field Frequency:")
        field_counts = {}
        for update in updates:
            for field in update['data'].keys():
                field_counts[field] = field_counts.get(field, 0) + 1
        
        for field, count in sorted(field_counts.items(), key=lambda x: -x[1]):
            pct = count / len(updates) * 100
            print(f"   • {field}: {count}/{len(updates)} ({pct:.0f}%)")
    
    print("\n" + "=" * 70)
    print("💡 INTERPRETATION:")
    print("=" * 70)
    
    if len(updates) > 0:
        price_updates = [u for u in updates if 'lp' in u['data']]
        if price_updates:
            prices = [u['data']['lp'] for u in price_updates]
            unique = len(set(prices))
            
            if unique == len(prices):
                print("✅ Every update had a UNIQUE price - getting all ticks!")
            elif unique < len(prices) * 0.5:
                print("⚠️  Many duplicate prices - updates triggered by other fields")
                print("   → QuoteSession updates on volume/bid/ask too, not just price")
            else:
                print(f"📊 {unique / len(prices) * 100:.0f}% of updates had price changes")
        
        print("\n🤔 If you're still missing ticks compared to TradingView:")
        print("   1. TradingView's web UI may use a different (internal) data feed")
        print("   2. WebSocket APIs typically provide sampled data, not every tick")
        print("   3. Consider upgrading to TradingView's official data feed API")
    
    # Cleanup
    connection_task.cancel()
    try:
        await connection_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
