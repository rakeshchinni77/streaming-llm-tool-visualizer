import requests

url = "http://127.0.0.1:8000/api/chat/stream"
payload = {"messages": [{"role": "user", "content": "What time is it in UTC?"}]}

with requests.post(url, json=payload, stream=True) as r:
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if line:
            print(line)
