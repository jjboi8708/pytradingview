"""
TradingView WebSocket Protocol Utilities
========================================

This module provides utility functions for encoding, decoding, compressing, and
parsing WebSocket messages used by TradingView's real-time data feed.

Functions included:
- `parse_ws_packet`: Parses a raw WebSocket message into JSON objects.
- `format_ws_packet`: Encodes a packet (as a dict or string) into the TradingView-specific WebSocket message format.
- `parse_compressed`: Decodes and decompresses a base64-encoded, zlib-compressed JSON string.

Constants:
- `CLEANER_RGX`: Regex pattern to remove heartbeat tokens.
- `SPLITTER_RGX`: Regex pattern to split raw WebSocket messages into individual packets.

These functions are essential for interpreting and composing the custom protocol used
by TradingView's socket.io-based WebSocket API.
"""

import re
import json
import zlib
import base64

try:
    import orjson
    json_loads = orjson.loads
except ImportError:
    json_loads = json.loads


CLEANER_RGX = '~h~'
SPLITTER_RGX = '~m~[0-9]{1,}~m~'

def parse_ws_packet(string):
    """
    Parses a WebSocket packet string into a list of JSON objects.
    
    Optimized implementation using manual string scanning and optional orjson support.
    """
    # Remove heartbeat if present (fast check)
    if '~h~' in string:
        string = string.replace('~h~', '')
        
    packets = []
    idx = 0
    length = len(string)
    
    while idx < length:
        # Expecting ~m~<len>~m~
        if not string.startswith('~m~', idx):
            break
            
        # Skip first ~m~
        idx += 3
        
        # Find next ~m~
        next_m = string.find('~m~', idx)
        if next_m == -1:
            break
            
        # Extract length
        try:
            packet_len = int(string[idx:next_m])
        except ValueError:
            break
            
        # Move past second ~m~
        idx = next_m + 3
        
        # Extract packet data
        data_end = idx + packet_len
        data = string[idx:data_end]
        
        if data:
            try:
                packets.append(json_loads(data))
            except Exception:
                pass
                
        idx = data_end
        
    return packets

def format_ws_packet(packet):
    """
    Formats a WebSocket packet to the required TradingView format.

    This function converts a dictionary packet into a compact JSON string,
    replacing any `null` values with empty strings, and prepends the message 
    with a length header in the format `~m~<length>~m~`.

    Args:
        packet (dict or str): The packet to format. If it's a dictionary, 
                              it will be converted to a JSON string.

    Returns:
        str: The formatted WebSocket packet as a string.
    """
    if isinstance(packet, dict):
        if 'orjson' in globals():
            # orjson.dumps returns bytes, decode to str
            # orjson doesn't support separators arg but is default compact
            packet = orjson.dumps(packet).decode('utf-8').replace('null', '""')
        else:
            packet = json.dumps(packet, separators=(',', ':')).replace('null', '""')
    return f'~m~{len(packet)}~m~{packet}'

def parse_compressed(data):
    """
    Decompresses and decodes a base64-encoded, zlib-compressed JSON string.

    This function is used to handle compressed WebSocket data received 
    from the server, typically for efficiency in data transmission.

    Args:
        data (str): The compressed and base64-encoded string.

    Returns:
        object: The decompressed and parsed JSON content as a Python object 
                (typically a dict or list).
    """
    return json.load(zlib.decompress(base64.b64decode(data)))
