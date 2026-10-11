# Assignment 4: Real-Time WebSocket Monitor

## 1. Overview

This project implements a Python WebSocket client that monitors message flow, records received messages and timestamps, calculates inter-message delays, reports latency warnings, detects heartbeat/echo timeouts, and attempts to reconnect after connection failures.

A local WebSocket echo server is included to test the client without depending on an external market-data service.

## 2. Project Structure

```text
Assing4/
├── websocket.py
├── test_server.py
├── config.json
├── sample.txt
└── README.md
```

## 3. Requirements

- Python 3.10 or later
- The `websockets` Python package

Install the dependency:

```bash
pip install websockets
```

## 4. Configuration

The settings are stored in `config.json`:

```json
{
    "url": "ws://localhost:8765",
    "test_duration": 60,
    "heartbeat_interval": 5,
    "heartbeat_timeout": 10,
    "reconnect_delay": 2,
    "latency_threshold": 1000
}
```

- `url`: WebSocket endpoint used by the monitor.
- `test_duration`: Monitoring duration in seconds.
- `heartbeat_interval`: Interval between echo-test messages.
- `heartbeat_timeout`: Maximum time to wait for a response.
- `reconnect_delay`: Time to wait before attempting reconnection.
- `latency_threshold`: Inter-message delay threshold in milliseconds that triggers a warning.

Change these values in `config.json` to adjust the test. The Python code must read and use the corresponding settings for the changes to take effect.

## 5. How to Run

Use two terminals opened in this project directory.

### Terminal 1: Start the local test server

```bash
python test_server.py
```

Expected startup message:

```text
Test WebSocket server running on port 8765
```

### Terminal 2: Start the monitor

```bash
python websocket.py
```

The client connects to `ws://localhost:8765`, sends `Hello WebSocket`, receives the echoed response, and displays message timestamps, message counts, inter-message delays, and latency warnings when applicable.

## 6. Testing Connection Failure and Reconnection

1. Start `test_server.py`.
2. Start `websocket.py` in a second terminal.
3. While the monitor is running, stop the server with `Ctrl+C`.
4. Observe the connection error and reconnection messages in the monitor terminal.
5. Restart `test_server.py` while the monitor is still running.
6. Confirm that the monitor reconnects when the server becomes available.

## 7. Testing Heartbeat/Echo Timeout

The local server normally echoes every received message. To test a timeout, temporarily disable the response line in `test_server.py`:

```python
await websocket.send(message)
```

Run the server and monitor again. If the client waits for an echo using `asyncio.wait_for(..., timeout=heartbeat_timeout)`, it should report a timeout when no response arrives. Restore the echo line after testing.

A timeout will only lead to reconnection if the client exits the active connection loop and reaches its reconnection logic.

## 8. Sample Output

Example output from a successful monitoring run:

```text
Connecting to server...
Connected successfully!
Message: Hello WebSocket
Received at: 2026-10-10T18:04:03+05:30
Message count: 1
Message: Hello WebSocket
Received at: 2026-10-10T18:04:08+05:30
Message count: 2
Inter-message delay: 5000.0 ms
WARNING: Latency threshold exceeded!
```

Example connection failure and retry messages:

```text
Connection/disconnection error: no close frame received or sent
Reconnecting in 2 seconds...
Connecting to server...
Connection/disconnection error: [WinError 1225] The remote computer refused the network connection
Reconnecting in 2 seconds...
Connecting to server...
Connected successfully!
```

These are examples based on testing; actual timestamps, counts, errors, and delays may differ. Keep `sample.txt` updated with the actual console output from your own test.

## 9. Monitoring Metrics

- **Message count:** Number of messages received by the client.
- **Inter-message delay:** Time between consecutive received messages, in milliseconds.
- **Latency warning:** Appears when the measured inter-message delay exceeds `latency_threshold`.
- **Heartbeat/echo timeout:** Indicates that an expected echo response was not received within the configured timeout.
- **Reconnection:** The client waits for `reconnect_delay` and then attempts to connect again.

Inter-message delay is not the same as network round-trip latency. Since the client sends messages at the configured heartbeat interval, that interval can dominate the measured delay.

## 10. Assumptions and Limitations

- The local server sends synthetic echo responses; it does not provide financial-market data.
- The local endpoint `ws://localhost:8765` works only while the test server is running on the same machine.
- This echo-based heartbeat is suitable for the test server. A production market-data WebSocket may require a subscription message and a server-specific heartbeat or ping/pong protocol.
- Timeout and reconnection behavior should be demonstrated using actual test output rather than a manually written log presented as a real run.
