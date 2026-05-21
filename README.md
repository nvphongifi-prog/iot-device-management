# 🚀 Tkinter WebSocket + HTTP Client

A lightweight Python 3 desktop client built with `tkinter` for testing
and interacting with servers via **WebSocket** and **HTTP**.

This tool is designed for developers who need a simple UI to send
JSON-based commands, debug APIs, and monitor responses in real time.

------------------------------------------------------------------------

## ✨ Features

-   🧩 **User-friendly GUI (Tkinter)**
-   ⚡ **WebSocket support**
    -   Connect / Disconnect
    -   Send JSON messages
    -   Real-time response logging
-   🌐 **HTTP client**
    -   Send customizable HTTP requests (method, headers, body)
-   📋 **Command input**
    -   Paste or edit JSON commands easily
-   🎯 **Quick presets**
    -   5 selectable default commands for fast testing
-   🪵 **Live logging panel**
    -   Displays connection status, requests, responses, and errors
-   🧵 **Non-blocking UI**
    -   WebSocket and HTTP run in background threads
-   ✅ **JSON validation before sending**

------------------------------------------------------------------------

## 🗂 Project Structure

	tk_ws_http_client_refactored/
	├── main.py
	├── ui.py
	├── ws_client.py
	├── http_client.py
	├── utilities.py
	├── requirements.txt
	└── README.md

------------------------------------------------------------------------

## ⚙️ Requirements

-   Python **3.10+**
-   tkinter (included with Python, Linux may need python3-tk)

------------------------------------------------------------------------

## 📦 Installation

``` bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Run

``` bash
python main.py
```

------------------------------------------------------------------------

## 🧪 Usage

### WebSocket

-   Enter URL: ws://localhost:8765/ws
-   Click Connect → Send → Disconnect

Example:

``` json
{
  "action": "ping",
  "timestamp": "2026-03-27T12:00:00Z"
}
```

### HTTP

``` json
{
  "method": "POST",
  "path": "/api/commands",
  "headers": {"Content-Type": "application/json"},
  "body": {"action": "status"},
  "timeout": 10
}
```

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Python
-   Tkinter
-   requests
-   websocket-client

------------------------------------------------------------------------

## 📄 License

Free to use and modify.
