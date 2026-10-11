
import json
import asyncio
import websockets
import time
from datetime import datetime



def load_config(filename="config.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

try:
    config = load_config()
except (OSError, json.JSONDecodeError) as error:
    print(f"FAIL: Configuration error: {error}")
    raise SystemExit(1)


url = config["url"]
test_duration = config["test_duration"]
heartbeat_interval = config["heartbeat_interval"]
heartbeat_timeout = config["heartbeat_timeout"]
reconnect_delay = config["reconnect_delay"]
latency_threshold = config["latency_threshold"]




async def connect_websocket():
    message_count = 0
    message_delays = []
    previous_time = None
    start_time = time.monotonic()

    while time.monotonic() - start_time < test_duration:
        try:
            print("\nConnecting to server...")

            async with websockets.connect(url) as websocket:
                print("Connected successfully!")

                while time.monotonic() - start_time < test_duration:
                    # Send an echo message at the heartbeat interval
                    await websocket.send("Hello WebSocket")

                    try:
                        message = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=heartbeat_timeout
                        )
                    except asyncio.TimeoutError:
                        print("WARNING: Heartbeat/echo timeout")
                        break

                    current_time = time.monotonic()
                    message_count += 1

                    timestamp = datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    )

                    print("Message:", message)
                    print("Received at:", timestamp)
                    print("Message count:", message_count)

                    if previous_time is not None:
                        delay = (current_time - previous_time) * 1000
                        message_delays.append(delay)

                        print(
                            "Inter-message delay:",
                            round(delay, 2), "ms"
                        )

                        if delay > latency_threshold:
                            print("WARNING: Latency threshold exceeded!")

                    previous_time = current_time

                    # Wait before sending the next heartbeat
                    await asyncio.sleep(heartbeat_interval)

        except asyncio.CancelledError:
            raise
        except Exception as error:
            print("Connection/disconnection error:", error)

        if time.monotonic() - start_time < test_duration:
            print(f"Reconnecting in {reconnect_delay} seconds...")
            await asyncio.sleep(reconnect_delay)

    print("\nMonitoring completed.")
    print("Total messages:", message_count)

    if message_delays:
        average_delay = sum(message_delays) / len(message_delays)
        print("\n" + "=" * 45)
        print("       WEBSOCKET MONITOR REPORT")
        print("=" * 45)
        print(f"WebSocket URL       : {url}")
        print(f"Test duration       : {test_duration} seconds")
        print(f"Total messages      : {message_count}")
        print(f"Average delay       : {average_delay:.2f} ms")
        print(f"Latency threshold   : {latency_threshold} ms")
        print("=" * 45)
        print("Monitoring completed.")

    else:
        print("No message intervals available to calculate an average.")


asyncio.run(connect_websocket())