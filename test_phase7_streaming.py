#!/usr/bin/env python
"""Test Phase 7: Real Groq Streaming"""
import os
import sys
import time
import httpx
import threading

os.environ['LLM_API_KEY'] = 'test-key-for-groq'
os.environ['LLM_MODEL'] = 'llama-3.3-70b-versatile'

# Add backend to path
sys.path.insert(0, 'backend')

from app.main import app
import uvicorn


def run_server():
    """Start FastAPI server in background"""
    uvicorn.run(app, host='127.0.0.1', port=8002, log_level='critical')


def main():
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)

    # Make streaming request
    try:
        with httpx.Client(timeout=30.0) as client:
            payload = {
                'messages': [
                    {'role': 'user', 'content': 'Tell me a short story in one sentence'}
                ]
            }
            print('=== Streaming Response ===')
            with client.stream('POST', 'http://127.0.0.1:8002/api/chat/stream', json=payload) as resp:
                print(f'Status: {resp.status_code}')
                print(f'Content-Type: {resp.headers.get("content-type")}')
                print(f'Cache-Control: {resp.headers.get("cache-control")}')
                print(f'Connection: {resp.headers.get("connection")}')
                print()
                print('Events (first 15):')
                count = 0
                for line in resp.iter_lines():
                    if line:
                        print(line)
                        count += 1
                        if count >= 15:
                            print('... (truncated - more events follow)')
                            break
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
