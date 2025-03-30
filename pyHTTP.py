import sys
import inspect
import json
from functools import wraps
from datetime import datetime
import os
import subprocess

def enable_console_output():
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.AllocConsole()
    sys.stdout = open('CONOUT$', 'w')
    sys.stderr = open('CONOUT$', 'w')
    sys.stdin = open('CONIN$', 'r')

def log_message(message, add_timestamp=True, add_newline=True):
    with open("logging.txt", "a", encoding="utf-8") as f:
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}")
        else:
            f.write(message)
        if add_newline:
            f.write("\n")

def log_http_request(method, url, headers=None, body=None, response=None):
    log_entry = "\n" + "=" * 80 + "\n"
    log_entry += f"[!] HTTP request detected:\n"
    log_entry += f"    Method: {method}\n"
    log_entry += f"    URL: {url}\n"
    
    if headers:
        log_entry += "    Headers:\n"
        for k, v in headers.items():
            log_entry += f"      {k}: {v}\n"
    
    if body:
        log_entry += f"    Body: {body}\n"
    
    if response:
        log_entry += f"\n[!] Server response:\n"
        log_entry += f"    Status: {response.status_code}\n"
        log_entry += f"    Size: {len(response.text)} bytes\n"
        
        if hasattr(response, 'headers'):
            log_entry += "    Response headers:\n"
            for k, v in response.headers.items():
                log_entry += f"      {k}: {v}\n"
        
        try:
            response_body = response.text if hasattr(response, 'text') else str(response)
            log_entry += f"    Full response body:\n{response_body}\n"
        except Exception as e:
            log_entry += f"    Failed to get response body: {str(e)}\n"
    
    log_entry += "=" * 80 + "\n\n"
    
    print(f"[!] Detected HTTP {method} request. Details in logging.txt")
    log_message(log_entry, add_timestamp=True, add_newline=False)

def patch_requests_library():
    if 'requests' not in sys.modules:
        return

    import requests
    original = requests.Session.request

    @wraps(original)
    def wrapped(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        body = kwargs.get('data', kwargs.get('json', None))
        if body and isinstance(body, (dict, list)):
            body = json.dumps(body)
        
        log_http_request(method, url, headers, body)
        response = original(self, method, url, **kwargs)
        log_http_request(method, url, response=response)
        return response

    requests.Session.request = wrapped
    log_message("[+] requests successfully patched!\n")
    print("[+] requests successfully patched!")

def patch_aiohttp_library():
    if 'aiohttp' not in sys.modules:
        return

    import aiohttp
    original = aiohttp.ClientSession._request

    @wraps(original)
    async def wrapped(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        body = kwargs.get('data', kwargs.get('json', None))
        if body and inspect.isawaitable(body):
            body = await body
        if body and isinstance(body, (dict, list)):
            body = json.dumps(body)
        
        log_http_request(method, str(url), headers, body)
        response = await original(self, method, url, **kwargs)
        response_text = await response.text()
        response._body = response_text
        log_http_request(method, str(url), response=response)
        return response

    aiohttp.ClientSession._request = wrapped
    log_message("[+] aiohttp successfully patched!\n")
    print("[+] aiohttp successfully patched!")

def patch_socket_library():
    import socket
    original = socket.socket

    class WrappedSocket(original):
        def connect(self, address):
            host, port = address
            message = "\n" + "=" * 80 + "\n"
            message += f"[!] Detected direct TCP connection: {host}:{port}\n"
            message += "=" * 80 + "\n\n"
            print(f"[!] Detected direct TCP connection: {host}:{port}")
            log_message(message, add_timestamp=True, add_newline=False)
            return original.connect(self, address)

    socket.socket = WrappedSocket
    log_message("[+] socket successfully patched!\n")
    print("[+] socket successfully patched!")

def patch_http_client():
    import http.client
    original = http.client.HTTPConnection

    class WrappedConnection(original):
        def request(self, method, url, body=None, headers=None, **kwargs):
            if headers is None:
                headers = {}
            log_http_request(method, f"http://{self.host}{url}", headers, body)
            
            original.request(self, method, url, body, headers, **kwargs)
            response = self.getresponse()
            response_body = response.read().decode('utf-8', errors='replace')
            
            class FakeResponse:
                def __init__(self, status, headers, body):
                    self.status_code = status
                    self.headers = headers
                    self.text = body
            
            fake_response = FakeResponse(response.status, dict(response.getheaders()), response_body)
            log_http_request(method, f"http://{self.host}{url}", response=fake_response)
            return response

    http.client.HTTPConnection = WrappedConnection
    log_message("[+] http.client successfully patched!\n")
    print("[+] http.client successfully patched!")

def initialize_monitoring():
    enable_console_output()
    
    with open("logging.txt", "w", encoding="utf-8") as f:
        f.write("made by @professor_contact | lolz.live/moriarty\n")
        f.write("=" * 50 + "\n\n")
    
    print("made by @professor_contact | lolz.live/moriarty\n")

    patch_requests_library()
    patch_aiohttp_library()
    patch_socket_library()
    patch_http_client()
    footer = "\n[+] All HTTP modules intercepted! Waiting for requests...\n\n"
    print(footer)
    log_message(footer, add_timestamp=True, add_newline=False)

if __name__ == "__main__":
    initialize_monitoring()
