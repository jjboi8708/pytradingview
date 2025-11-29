# pytradingview Examples

This directory contains working examples demonstrating various features of pytradingview.

## 📁 Directory Structure

```
examples/
├── README.md (this file)
├── example_app.py          # Simple sync client example
├── async_example.py        # Async client with multiple symbols
├── quickstart_chart.py     # Minimal async chart setup
├── advanced/               # Advanced usage patterns
│   ├── tick_capture.py     # Capture individual ticks with change tracking
│   └── debug_raw_stream.py # Debug WebSocket protocol messages
└── benchmarks/             # Performance analysis tools
    ├── benchmark_quote_vs_chart.py  # Compare QuoteSession vs ChartSession
    └── analyze_quote_data.py        # Analyze tick data patterns
```

## 🚀 Getting Started

### 1. Simple Synchronous Example

**File:** `example_app.py`

Basic chart with synchronous callbacks:

```bash
python example_app.py
```

Perfect for learning the basics.

---

### 2. Async Example

**File:** `async_example.py`

Demonstrates:

- Async/await patterns
- Multiple symbol monitoring
- Async context manager
- Mixed sync/async callbacks

```bash
python async_example.py
```

---

### 3. Quick chart Chart

**File:** `quickstart_chart.py`

Minimal async setup with uvloop for maximum performance:

```bash
python quickstart_chart.py
```

---

## 🔬 Advanced Examples

Navigate to `advanced/` for specialized use cases:

### Tick Capture

**File:** `advanced/tick_capture.py`

Captures every individual tick (price change) with:

- Change tracking (Δ calculations)
- Arrow indicators (🔺🔻)
- Tick counter
- Real-time display

```bash
python advanced/tick_capture.py
```

**Use when you need:**

- Tick-by-tick data
- Price change monitoring
- Scalping strategies

---

### Debug Raw Stream

**File:** `advanced/debug_raw_stream.py`

Shows ALL raw WebSocket messages for debugging:

```bash
python advanced/debug_raw_stream.py
```

**Use when you need:**

- Protocol debugging
- Understanding message flow
- Troubleshooting issues

---

## 📊 Benchmarks

Navigate to `benchmarks/` for performance analysis:

### Quote vs Chart Comparison

**File:** `benchmarks/benchmark_quote_vs_chart.py`

Runs both sessions simultaneously for 30 seconds and compares:

- Update frequency
- Average interval
- Unique price percentage
- Which is faster for your symbol

```bash
python benchmarks/benchmark_quote_vs_chart.py
```

---

### Quote Data Analysis

**File:** `benchmarks/analyze_quote_data.py`

Deep analysis of QuoteSession data (60 seconds):

- Field frequency analysis
- Price change rate
- Update statistics
- Interpretation guide

```bash
python benchmarks/analyze_quote_data.py
```

---

## 💡 Tips

### Enable uvloop for Maximum Performance

Add to any example:

```python
import uvloop
uvloop.install()
```

### Using with Your Own Code

All examples can be modified:

1. Change the symbol (e.g., `"BINANCE:BTCUSD"` → `"NASDAQ:TSLA"`)
2. Change timeframe (e.g., `"1"` → `"5"` for 5-minute candles)
3. Add your own callbacks

### Common Patterns

**ChartSession** (OHLCV candles):

```python
chart = client.chart
chart.set_up_chart()
chart.set_market(symbol, {"timeframe": "1"})
chart.on_update(your_callback)
```

**QuoteSession** (tick-by-tick):

```python
quote = client.quote
quote.set_up_quote({'fields': 'price'})
quote.add_symbol(symbol, your_callback)
```

---

## 🎯 Which Example Should I Use?

| Use Case | Example |
|----------|---------|
| Learning the library | `example_app.py` |
| Building an app | `async_example.py` |
| Need max performance | `quickstart_chart.py` |
| Tick-level trading | `advanced/tick_capture.py` |
| Debugging issues | `advanced/debug_raw_stream.py` |
| Performance testing | `benchmarks/*` |

---

## 📝 Notes

- All async examples support both sync and async callbacks
- Examples run indefinitely - press Ctrl+C to stop
- Free WebSocket API has rate limits - be respectful
