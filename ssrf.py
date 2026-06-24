# ssrf-toctou-bypass

A proof of concept exploit server that bypasses SSRF protection libraries vulnerable to TOCTOU (Time of Check, Time of Use) - responds safely to the security check and redirects the fetcher to internal resources.

Originally developed for the HackTheBox challenge **Saturn**.

---

## How it works

Some web applications protect against SSRF by validating URLs with a security library before fetching them:

```python
su.execute(url)        # security library CHECKS the URL
r = requests.get(url)  # requests FETCHES the URL separately
```

The flaw is that these are two separate HTTP requests to your server. Your server can respond differently to each one:

- **Request #1** (security check) - return `200 OK` with harmless content - passes validation
- **Request #2** (actual fetch) - return `301 redirect` to internal resource - retrieves the flag

By the time the redirect happens, the security check is already done and has no idea what the fetcher does next.

---

## Requirements

- Python 3
- ngrok (or any public tunnel)

---

## Setup

**Step 1 - Clone the repo**
```bash
git clone https://github.com/yourusername/ssrf-toctou-bypass
cd ssrf-toctou-bypass
```

**Step 2 - Edit the redirect target**

Open `saturn.py` and change the `Location` header to your target internal URL:
```python
self.send_header('Location', 'http://127.0.0.1:1337/secret')
```

**Step 3 - Start the exploit server**
```bash
python3 saturn.py
```

**Step 4 - Expose it publicly with ngrok**
```bash
./ngrok http 8000
```

ngrok will give you a public URL like:
```
https://your-tunnel.ngrok-free.dev
```

**Step 5 - Submit the ngrok URL to the vulnerable application**

The server will:
1. Respond `200 Hello World` to the security check - passes validation
2. Respond `301 redirect` to the fetcher - hits the internal resource

---

## How the counter works

Every form submission on the vulnerable app causes exactly two requests to your server - always in the same order:

```
request #1 - security library checking  - odd  - 200 OK
request #2 - requests library fetching  - even - 301 redirect
```

The `count % 2` logic tracks which request is which:

```python
if count % 2 == 1:   # odd  = security check = send 200
else:                # even = actual fetch   = send 301
```

---

## The vulnerability

This exploit works when an application:

1. Validates a URL with one library
2. Fetches the same URL with a different library separately
3. Does not use the validator's own response for the result

The fix is simple - use the security library's own response instead of fetching separately:

```python
# vulnerable
su.execute(url)
r = requests.get(url)   # second independent request

# secure
r = su.execute(url)     # use safeurl's response directly
```

---

## Tested Against

| Challenge | Platform | Library |
|-----------|----------|---------|
| Saturn | HackTheBox | SafeURL-Python 1.3 |

---

## Disclaimer

This tool is for educational purposes and authorised security testing only. Do not use against systems you do not have permission to test.
