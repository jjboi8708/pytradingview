import asyncio
import time
from collections import defaultdict

# Enable uvloop for consistent performance
try:
    import uvloop
    uvloop.install()
    print("🚀 uvloop enabled\n")
except ImportError:
    print("⚠️  uvloop not installed\n")

from pytradingview import AsyncTVclient


async def main():
    """
    Benchmark: QuoteSession vs ChartSession
    
    This will show which receives updates faster and more frequently.
    """
    client = AsyncTVclient()
    symbol = "CRYPTO:SOLUSD"
    
    # Statistics tracking
    quote_updates = []
    chart_updates = []
    quote_prices = []
    chart_prices = []
    
    start_time = None
    
    # === QUOTE SESSION (Tick Data) ===
    quote = client.quote
    quote.set_up_quote({'fields': 'price'})
    
    async def on_quote(data):
        nonlocal start_time
        if start_time is None:
            start_time = time.time()
        
        try:
            if data['type'] == 'qsd':
                values = data['data'][1]['v']
                if 'lp' in values:
                    timestamp = time.time()
                    price = values['lp']
                    quote_updates.append(timestamp)
                    quote_prices.append(price)
                    
                    if len(quote_updates) == 1:
                        print(f"📊 QUOTE:  First update at t=0.000s - Price: {price}")
                    elif len(quote_updates) <= 5:
                        elapsed = timestamp - start_time
                        print(f"📊 QUOTE:  Update #{len(quote_updates)} at t={elapsed:.3f}s - Price: {price}")
        except (KeyError, IndexError):
            pass
    
    quote.add_symbol(symbol, on_quote)
    
    # === CHART SESSION (Candle Data) ===
    chart = client.chart
    chart.set_up_chart()
    chart.set_market(symbol, {"timeframe": "1"})
    
    async def on_chart(changes):
        nonlocal start_time
        if start_time is None:
            start_time = time.time()
        
        if chart.get_periods:
            timestamp = time.time()
            price = chart.get_periods['close']
            chart_updates.append(timestamp)
            chart_prices.append(price)
            
            if len(chart_updates) == 1:
                print(f"📈 CHART:  First update at t=0.000s - Price: {price}")
            elif len(chart_updates) <= 5:
                elapsed = timestamp - start_time
                print(f"📈 CHART:  Update #{len(chart_updates)} at t={elapsed:.3f}s - Price: {price}")
    
    chart.on_update(on_chart)
    
    # Run for 30 seconds
    print(f"⏱️  Starting 30-second benchmark for {symbol}...")
    print("=" * 60)
    
    # Start connection in background
    connection_task = asyncio.create_task(client.create_connection())
    
    # Wait 30 seconds
    try:
        await asyncio.sleep(30)
    except KeyboardInterrupt:
        pass
    
    # Results
    print("\n" + "=" * 60)
    print("📊 BENCHMARK RESULTS (30 seconds)")
    print("=" * 60)
    
    print(f"\n🏆 QUOTE SESSION (Tick Data):")
    print(f"   • Total Updates: {len(quote_updates)}")
    if len(quote_updates) > 1:
        avg_interval = (quote_updates[-1] - quote_updates[0]) / (len(quote_updates) - 1) * 1000
        print(f"   • Avg Interval: {avg_interval:.1f}ms between updates")
        print(f"   • Update Rate: {len(quote_updates) / 30:.1f} updates/second")
        unique_prices = len(set(quote_prices))
        print(f"   • Unique Prices: {unique_prices} ({unique_prices / len(quote_updates) * 100:.1f}% unique)")
    
    print(f"\n📈 CHART SESSION (Candle Data):")
    print(f"   • Total Updates: {len(chart_updates)}")
    if len(chart_updates) > 1:
        avg_interval = (chart_updates[-1] - chart_updates[0]) / (len(chart_updates) - 1) * 1000
        print(f"   • Avg Interval: {avg_interval:.1f}ms between updates")
        print(f"   • Update Rate: {len(chart_updates) / 30:.1f} updates/second")
        unique_prices = len(set(chart_prices))
        print(f"   • Unique Prices: {unique_prices} ({unique_prices / len(chart_updates) * 100:.1f}% unique)")
    
    # Winner
    print("\n" + "=" * 60)
    if len(quote_updates) > len(chart_updates):
        diff = len(quote_updates) - len(chart_updates)
        pct = (diff / len(chart_updates)) * 100 if chart_updates else 0
        print(f"✅ QUOTE SESSION is FASTER")
        print(f"   → {diff} more updates (+{pct:.0f}%)")
        print(f"   → Better for: tick-level trading, scalping, precise entry/exit")
    elif len(chart_updates) > len(quote_updates):
        diff = len(chart_updates) - len(quote_updates)
        pct = (diff / len(quote_updates)) * 100 if quote_updates else 0
        print(f"✅ CHART SESSION is FASTER")
        print(f"   → {diff} more updates (+{pct:.0f}%)")
    else:
        print(f"🤝 TIE - Both received {len(quote_updates)} updates")
    
    print("=" * 60)
    
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
        print("\n\n⚠️  Benchmark interrupted by user")
