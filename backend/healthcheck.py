"""Healthcheck script used by CI or container health checks.

Performs an HTTP GET against the backend health endpoint and exits with 0
on success and non-zero on failure.
"""
import sys
import json
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


HEALTH_URL = "http://localhost:8000/health"


def check_health(timeout: int = 5) -> int:
	req = Request(HEALTH_URL, headers={"Accept": "application/json"})
	try:
		with urlopen(req, timeout=timeout) as resp:
			status = resp.getcode()
			if status != 200:
				print(f"Unhealthy status code: {status}")
				return 2
			body = resp.read().decode("utf-8")
			try:
				data = json.loads(body)
				if data.get("status") == "healthy":
					print("OK: healthy")
					return 0
				else:
					print(f"Unexpected health payload: {data}")
					return 3
			except json.JSONDecodeError:
				print("Invalid JSON response from health endpoint")
				return 4
	except (URLError, HTTPError) as exc:
		print(f"Health check request failed: {exc}")
		return 5


if __name__ == "__main__":
	# Simple retry loop to allow server startup
	timeout_seconds = 30
	interval = 1
	deadline = time.time() + timeout_seconds
	while time.time() < deadline:
		rc = check_health()
		if rc == 0:
			sys.exit(0)
		time.sleep(interval)
	print("Healthcheck timed out")
	sys.exit(1)
