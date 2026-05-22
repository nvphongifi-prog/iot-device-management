import json
from unittest.mock import Mock

import pytest

import ui
import ws_client
from utilities import validate_handshake, is_handshake_payload


class DummyLogger:
    def __init__(self):
        self.messages = []

    def log(self, msg: str):
        self.messages.append(msg)


class DummyApp:
    def __init__(self, raw_text: str | None = None):
        self._raw_text = raw_text
        self.logger = DummyLogger()
        self.ws_manager = Mock()
        self.handshake_completed = False

    def _get_request_text(self):
        return self._raw_text

    def _parse_request_json(self):
        raw_text = self._get_request_text()
        if not raw_text:
            self.logger.log("Request textbox is empty.")
            return None
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            self.logger.log(f"Invalid JSON: {exc}")
            return None


def test_parse_request_json_valid_and_invalid():
    valid = DummyApp(raw_text=json.dumps({"action": "ping"}))
    result = ui.AppUI._parse_request_json(valid)
    assert result == {"action": "ping"}

    invalid = DummyApp(raw_text="not-json")
    result2 = ui.AppUI._parse_request_json(invalid)
    assert result2 is None
    assert any("Invalid JSON" in m for m in invalid.logger.messages)


def test_send_websocket_manual_validation_calls_send_json_only_when_valid():
    app = DummyApp()
    app._raw_text = None
    ui.AppUI.send_websocket(app)
    assert not app.ws_manager.send_json.called

    payload = {"action": "echo", "message": "hello"}
    app._raw_text = json.dumps(payload)
    ui.AppUI.send_websocket(app)
    app.ws_manager.send_json.assert_called_with(payload)


def test_ws_on_open_invalid_handshake_does_not_send():
    logger = DummyLogger()
    manager = ws_client.WebSocketManager(logger=logger)
    manager.ws_app = Mock()
    manager.handshake_payload = {"action": "handshake", "nonce": "abc123"}
    manager.auto_send_handshake = True

    sent = {}

    def fake_send(payload):
        sent["payload"] = payload

    manager.send_json = fake_send
    manager._on_open(None)

    assert manager.connected is True
    assert sent.get("payload") is None
    assert any("Handshake validation failed" in m for m in logger.messages)


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


class DummyWSApp:
    def __init__(self):
        self.sent = []

    def send(self, raw):
        self.sent.append(raw)


def test_websocket_auto_send_handshake():
    logger = DummyLogger()
    manager = ws_client.WebSocketManager(logger=logger)
    manager.ws_app = DummyWSApp()
    payload = {"action": "handshake", "clientId": "auto-1"}
    manager.set_handshake_config(payload, auto_send=True)
    manager._on_open(None)
    assert manager.ws_app.sent
    sent_obj = json.loads(manager.ws_app.sent[0])
    assert sent_obj["action"] == "handshake"


def test_manual_send_validates_and_sends():
    logger = DummyLogger()
    manager = ws_client.WebSocketManager(logger=logger)
    manager.ws_app = DummyWSApp()
    manager.connected = True

    payload = {"action": "handshake", "clientId": "manual-1"}
    manager.send_json(payload)
    assert manager.ws_app.sent


def test_handle_ws_message_sets_handshake_completed_flag():
    app = DummyApp()
    ui.AppUI._handle_ws_message(app, json.dumps({"action": "handshake_ack", "status": "ok"}))
    assert app.handshake_completed is True
    assert any("Handshake completed" in m for m in app.logger.messages)
