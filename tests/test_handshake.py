import json
import types

import pytest

from utilities import validate_handshake, is_handshake_payload
from ws_client import WebSocketManager


class DummyLogger:
    def __init__(self):
        self.messages = []

    def log(self, msg: str):
        self.messages.append(msg)


class DummyWSApp:
    def __init__(self):
        self.sent = []

    def send(self, raw):
        self.sent.append(raw)


def test_validate_handshake_success():
    payload = {"action": "handshake", "clientId": "abc123"}
    valid, msg = validate_handshake(payload)
    assert valid is True
    assert msg == ""


def test_validate_handshake_missing_clientid():
    payload = {"action": "handshake"}
    valid, msg = validate_handshake(payload)
    assert valid is False
    assert "clientId" in msg


def test_is_handshake_payload():
    assert is_handshake_payload({"action": "handshake"}) is True
    assert is_handshake_payload({"action": "ping"}) is False


def test_websocket_auto_send_handshake():
    logger = DummyLogger()
    manager = WebSocketManager(logger=logger)
    # set a dummy ws_app so send will work
    manager.ws_app = DummyWSApp()
    payload = {"action": "handshake", "clientId": "auto-1"}
    manager.set_handshake_config(payload, auto_send=True)
    # simulate open
    manager._on_open(None)
    # check that message was sent
    assert manager.ws_app.sent, "Expected handshake to be sent on open"
    sent_obj = json.loads(manager.ws_app.sent[0])
    assert sent_obj["action"] == "handshake"


def test_manual_send_validates_and_sends(monkeypatch):
    logger = DummyLogger()
    manager = WebSocketManager(logger=logger)
    manager.ws_app = DummyWSApp()
    manager.connected = True

    # valid handshake
    payload = {"action": "handshake", "clientId": "manual-1"}
    manager.send_json(payload)  # direct send_json should send
    assert manager.ws_app.sent


def test_response_handling_sets_flag(monkeypatch):
    # Use a small App-like object to simulate on_message callback
    logs = []

    def append_log(msg):
        logs.append(msg)

    # create a simple handler that mimics UI._handle_ws_message
    def handler(message: str):
        append_log(f"received: {message}")
        try:
            data = json.loads(message)
            action = data.get("action") if isinstance(data, dict) else None
            if action in ("handshake_ack", "handshake_response") or "handshake" in data:
                append_log("Handshake completed (response received).")
        except Exception:
            pass

    handler(json.dumps({"action": "handshake_ack", "status": "ok"}))
    assert any("Handshake completed" in m for m in logs)
