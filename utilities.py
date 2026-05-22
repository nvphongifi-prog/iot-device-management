from datetime import datetime


DEFAULT_COMMANDS = [
    {
        "name": "Ping",
        "payload": {
            "action": "ping",
            "timestamp": "2026-03-27T12:00:00Z",
        },
    },
    {
        "name": "Login",
        "payload": {
            "action": "login",
            "username": "demo_user",
            "token": "replace-me",
        },
    },
    {
        "name": "Subscribe",
        "payload": {
            "action": "subscribe",
            "channel": "events",
        },
    },
    {
        "name": "Echo",
        "payload": {
            "action": "echo",
            "message": "hello from tkinter client",
        },
    },
    {
        "name": "Handshake",
        "payload": {
            "action": "handshake",
            "clientId": "client-123",
            "token": "optional-token",
            "capabilities": {"version": "1.0"},
        },
    },
    {
        "name": "HTTP POST sample",
        "payload": {
            "method": "POST",
            "path": "/api/commands",
            "headers": {
                "Content-Type": "application/json",
            },
            "body": {
                "action": "status",
            },
            "timeout": 10,
        },
    },
]


class AppLogger:
    def __init__(self, callback) -> None:
        self.callback = callback

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.callback(f"[{timestamp}] {message}\n")


def is_handshake_payload(payload: dict) -> bool:
    """Return True if payload looks like a handshake payload."""
    if not isinstance(payload, dict):
        return False
    return payload.get("action") == "handshake"


def validate_handshake(payload: dict) -> (bool, str):
    """Validate minimal handshake schema.

    Requirements:
    - payload is a dict
    - action == 'handshake'
    - clientId is a non-empty string

    Returns (True, '') on success or (False, error_message) on failure.
    """
    if not isinstance(payload, dict):
        return False, "Handshake payload must be a JSON object."
    if payload.get("action") != "handshake":
        return False, "Handshake payload must have action=='handshake'."
    client_id = payload.get("clientId")
    if not client_id or not isinstance(client_id, str):
        return False, "Handshake payload missing required 'clientId' string."
    return True, ""
