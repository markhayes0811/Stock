import websocket
import json
import threading

# Polygon API Key
API_KEY = "H3nRWzRqnMqojU9y1gkbo1UqTbl2peqf"

# Stock tickers to monitor
tickers = ["AAPL", "TSLA", "MSFT"]

# Surge detection threshold (percentage)
THRESHOLD = 1.0

# Dictionary to track the last prices
last_prices = {}

# WebSocket URL for Polygon.io
WS_URL = "wss://socket.polygon.io/stocks"

def on_message(ws, message):
    global last_prices
    data = json.loads(message)

    if "ev" in data and data["ev"] == "T":  # Trade event
        ticker = data["sym"]
        current_price = data["p"]

        # Check for surge
        if ticker in last_prices:
            change = ((current_price - last_prices[ticker]) / last_prices[ticker]) * 100
            if abs(change) >= THRESHOLD:
                print(f"ALERT: {ticker} surged by {change:.2f}% to ${current_price:.2f}")

        # Update the last price
        last_prices[ticker] = current_price

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed.")

def on_open(ws):
    # Authenticate with Polygon.io
    auth_message = {"action": "auth", "params": API_KEY}
    ws.send(json.dumps(auth_message))

    # Subscribe to the tickers
    for ticker in tickers:
        subscribe_message = {"action": "subscribe", "params": f"T.{ticker}"}
        ws.send(json.dumps(subscribe_message))
    print(f"Subscribed to: {', '.join(tickers)}")

# Start the WebSocket
def start_websocket():
    ws = websocket.WebSocketApp(
        WS_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()

# Run the WebSocket in a separate thread
websocket_thread = threading.Thread(target=start_websocket)
websocket_thread.start()
