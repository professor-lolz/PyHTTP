# PyHTTP Sniffer

**Tool for intercepting HTTP/HTTPS requests from Python applications** 

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

![example work](https://github.com/professor-lolz/PyHTTP/blob/main/example.png)

## 🔍 Description

This tool injects itself into a Python process and intercepts all outgoing HTTP/HTTPS requests, including:
- Standard requests via `requests`
- Asynchronous requests via `aiohttp`
- Low-level TCP connections via `socket`
- Requests via `http.client`

All intercepted data is saved to a timestamped `logging.txt` file.

## ⚙️ Installing

1. Clone the repository:
```bash
git clone https://github.com/professor-lolz/PyHTTP.git
cd PyHTTP
```
2. Make sure you have Python 3.7+ installed

## 🚀 Using

To inject code into a running Python process, use [PyInjector](https://github.com/call-042PE/PyInjector):

## 📊 Example output

```[2025-03-30 14:30:45] [!] HTTP request detected:
 Method: POST
 URL: https://api.example.com/login
 Headers:
 Content-Type: application/json
 User-Agent: python-requests/2.28.1
 Body: {"username": "test", "password": "qwerty"}

[!] Server response:
 Status: 200
 Size: 125 bytes
 Response headers:
 Content-Type: application/json
 Server: nginx
 Full response body:
 {"status": "success", "token": "abc123"}
````

## ⚠️ Warning

This tool is intended only for:
1. Testing the security of your own applications
2. Debugging network communications
3. Educational purposes
