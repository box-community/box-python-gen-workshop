""" Handles the call back request from Box OAuth2.0
---
This is a simple HTTP server that listens for a request from Box OAuth2.0.
picking up the code and csrf_token from the query string.
"""

import logging
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from box_sdk_gen import BoxOAuth


CSRF_TOKEN_ORIG = ""
AUTH = None


class CallbackServer(BaseHTTPRequestHandler):
    """
    Creates a mini http request handler to handle a single callback request"""

    def do_GET(self):  # pylint: disable=invalid-name
        """
        Gets the redirect call back from Box OAuth2.0
        capturing the code and csrf_token from the query string
        and calls for the completion of the OAuth2.0 process.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        code = " ".join(params.get("code")) if params.get("code") else None
        state = " ".join(params.get("state")) if params.get("state") else None
        error = " ".join(params.get("error")) if params.get("error") else None
        error_description = (
            " ".join(params.get("error_description")) if params.get("error_description") else None
        )

        logging.info("code: %s", code)
        logging.info("state: %s", state)
        logging.info("error: %s", error)
        logging.info("error_description: %s", error_description)

        assert state == CSRF_TOKEN_ORIG

        if code:
            AUTH.get_tokens_authorization_code_grant(code)

        self.wfile.write(
            bytes(
                "<html><head><title>Sample Box SDK oAuth2 Callback</title></head>",  # noqa: E501
                "utf-8",
            )
        )
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h2>oAuth Callback received:</h2>", "utf-8"))
        self.wfile.write(bytes(f"<h5>Code: {code}</h5>", "utf-8"))
        self.wfile.write(bytes(f"<h5>State: {state}</h5>", "utf-8"))
        self.wfile.write(bytes(f"<h5>Error: {error}</h5>", "utf-8"))
        self.wfile.write(bytes(f"<h5>Error Message: {error_description}</h5>", "utf-8"))  # noqa: E501
        self.wfile.write(bytes("<p>You can close this browser window.</p>", "utf-8"))  # noqa: E501
        self.wfile.write(bytes("</body></html>", "utf-8"))


def callback_handle_request(auth: BoxOAuth, hostname, port, csrf_token: str):
    """
    Handles the call back request from Box OAuth2.0
    Creates a simple HTTP server that listens for a request from Box OAuth2.0.
    """
    global CSRF_TOKEN_ORIG  # pylint: disable=global-statement
    CSRF_TOKEN_ORIG = csrf_token
    global AUTH  # pylint: disable=global-statement
    AUTH = auth

    web_server = HTTPServer((hostname, port), CallbackServer)

    logging.info(
        "Server started http://%s:%s",
        hostname,
        port,
    )

    try:
        web_server.handle_request()
    finally:
        web_server.server_close()

    logging.info("Server stopped.")


def open_browser(auth_url: str):
    """
    Opens a browser to the auth_url
    """
    webbrowser.open(auth_url)
