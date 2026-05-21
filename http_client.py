import threading

import requests


class HttpClient:
    def __init__(self, logger) -> None:
        self.logger = logger

    def send_request(self, base_url: str, request_data: dict) -> None:
        if not base_url:
            self.logger.log("HTTP Base URL is empty.")
            return

        method = str(request_data.get("method", "POST")).upper()
        path = str(request_data.get("path", "/"))
        headers = request_data.get("headers", {})
        body = request_data.get("body", None)
        timeout = request_data.get("timeout", 10)

        url = f"{base_url.rstrip('/')}{path if path.startswith('/') else '/' + path}"
        self.logger.log(f"Sending HTTP request: {method} {url}")

        def do_request() -> None:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body,
                    timeout=timeout,
                )
                preview = response.text[:2000]
                self.logger.log(
                    f"HTTP response: status={response.status_code}, "
                    f"reason={response.reason}, body={preview}"
                )
            except Exception as exc:
                self.logger.log(f"HTTP request error: {exc}")

        threading.Thread(target=do_request, daemon=True).start()
