# pytradingview

A high-performance Python library for connecting to TradingView's WebSocket API with both synchronous and asynchronous support.

## ✨ Features

- **Dual-Mode Support**: Synchronous (`TVclient`) and Asynchronous (`AsyncTVclient`)
- **Ultra-Low Latency**: Optimized protocol parsing with `orjson` and `uvloop` support
- **Real-Time Data Streaming**: Chart (OHLCV) and Quote (tick-by-tick) sessions
- **Multiple Timeframes**: 1min, 5min, 15min, 1hour, daily, and more
- **Backward Compatible**: Existing code continues to work unchanged

## 📦 Installation

```bash
pip install pytradingview
```

### Optional Performance Enhancements

```bash
pip install orjson uvloop  # 2-4x faster with ultra-low latency
```

## 🚀 Quick Start

### Synchronous Client (Original)

```python
from pytradingview import TVclient

client = TVclient()
chart = client.chart

chart.set_up_chart()
chart.set_market("BINANCE:BTCUSD", {"timeframe": "1"})

def on_update(_):
    if chart.get_periods:
        print(f"Price: {chart.get_periods['close']}")

chart.on_update(on_update)
client.create_connection()
```

### Asynchronous Client (High Performance)

```python
import asyncio
from pytradingview import AsyncTVclient

async def main():
    client = AsyncTVclient()
    chart = client.chart
    
    chart.set_up_chart()
    chart.set_market("BINANCE:BTCUSD", {"timeframe": "1"})
    
    async def on_update(_):
        if chart.get_periods:
            print(f"⚡ Price: {chart.get_periods['close']}")
    
    chart.on_update(on_update)
    await client.create_connection()

asyncio.run(main())
```

**For maximum speed**, enable `uvloop`:

```python
import uvloop
uvloop.install()
```

## 📊 Data Sessions

### ChartSession - OHLCV Candlestick Data

Perfect for charting applications and technical analysis:

```python
chart = client.chart
chart.set_up_chart()
chart.set_market("BINANCE:BTCUSD", {"timeframe": "5"})  # 5-minute candles
chart.on_update(handle_candle_update)
```

**Use cases:**

- Candlestick charts
- Technical indicators (RSI, MACD, MA)
- Historical data analysis
- Multiple timeframe analysis

### QuoteSession - Tick-by-Tick Data

For real-time price feeds and trade execution:

```python
quote = client.quote
quote.set_up_quote({'fields': 'price'})
quote.add_symbol("BINANCE:BTCUSD", handle_tick)
```

**Use cases:**

- Real-time price tickers
- Time & sales panels
- Scalping strategies
- Order book displays

## 📁 Examples

See the `/examples` directory for complete working examples:

### Basic Examples

- **`example_app.py`** - Simple synchronous chart example
- **`async_example.py`** - Async client with multiple symbols
- **`quickstart_chart.py`** - Minimal async chart setup

### Advanced Examples (`/examples/advanced`)

- **`tick_capture.py`** - Capture every tick with detailed change tracking
- **`debug_raw_stream.py`** - Debug WebSocket messages

### Benchmarks (`/examples/benchmarks`)

- **`benchmark_quote_vs_chart.py`** - Compare update frequencies
- **`analyze_quote_data.py`** - Analyze tick data patterns

## 🎯 Performance

With optimizations enabled (`orjson` + `uvloop`):

- **Protocol parsing**: ~56% faster than regex-based parsing
- **JSON processing**: 2-4x faster with `orjson`
- **Event loop**: 2-4x faster with `uvloop`
- **Message dispatch**: < 3ms latency

## 🔧 Command Line Interface

```bash
# Download historical data
python -m pytradingview -d -s '2025-04-24 00:00' -e '2025-04-25 00:00' -p 'FX:EURUSD'

# Search for symbols
python -m pytradingview --search BTCUSD --max 50
```

## 🛠️ Advanced Configuration

### Multiple Symbols

```python
symbols = ["BINANCE:BTCUSD", "BINANCE:ETHUSD", "BINANCE:SOLUSD"]

for symbol in symbols:
    quote.add_symbol(symbol, lambda data: print(f"{symbol}: {data}"))
```

### Custom Fields

```python
quote.set_up_quote({
    'customFields': ['lp', 'volume', 'bid', 'ask', 'high_price', 'low_price']
})
```

### Async Context Manager

```python
async with AsyncTVclient() as client:
    chart = client.chart
    # ... setup and use
    # Connection automatically closed on exit
```

## 📚 API Reference

### TVclient (Sync) / AsyncTVclient (Async)

**Methods:**

- `chart` - Access ChartSession
- `quote` - Access QuoteSession
- `create_connection()` - Start WebSocket connection
- `on_connected(callback)` - Connection established
- `on_error(callback)` - Error handler
- `on_disconnected(callback)` - Connection closed

### ChartSession

**Methods:**

- `set_up_chart()` - Initialize chart
- `set_market(symbol, options)` - Set symbol and timeframe
- `on_update(callback)` - Price update events
- `on_symbol_loaded(callback)` - Symbol metadata loaded
- `get_periods` - Current OHLCV data
- `get_infos` - Symbol metadata

### QuoteSession

**Methods:**

- `set_up_quote(options)` - Initialize with fields
- `add_symbol(symbol, callback)` - Subscribe to symbol
- `delete()` - Close session

## 🤝 Contributing

Contributions welcome! Please open issues or PRs.

## 📄 License

See [LICENSE](LICENSE) file.

## 🙏 Credits

Built on the TradingView WebSocket API.
Async implementation and performance optimizations added in v0.4.0.
