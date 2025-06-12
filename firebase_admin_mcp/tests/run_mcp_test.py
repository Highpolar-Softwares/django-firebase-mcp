#!/usr/bin/env python3
"""
Start Django server and test the Firebase MCP endpoint
"""
import subprocess
import time
import sys
import os
import requests


def check_server_running(url, max_attempts=10):
    """Check if the server is running"""
    for i in range(max_attempts):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False


def main():
    print("=== Firebase MCP Server Test Runner ===\n")

    # Check if server is already running
    server_url = 'http://127.0.0.1:8001/mcp/'
    if check_server_running(server_url, max_attempts=1):
        print("✓ Django server already running at http://127.0.0.1:8001/")
        print("Running tests...\n")

        # Run the test
        os.system("python test_mcp_complete.py")
        return

    print("Starting Django server...")

    # Start Django server in background
    try:
        # Change to project directory
        os.chdir("d:\\Dev\\Projects\\django_firebase_mcp")

        # Start server
        server_process = subprocess.Popen([
            "python", "manage.py", "runserver", "8001"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Waiting for server to start...")

        # Wait for server to be ready
        if check_server_running(server_url):
            print("✓ Django server started successfully!")
            print("Running tests...\n")

            # Run the test
            os.system("python test_mcp_complete.py")

        else:
            print("✗ Server failed to start within 10 seconds")

    except Exception as e:
        print(f"✗ Error starting server: {e}")
    finally:
        # Clean up server process
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            try:
                server_process.kill()
            except:
                pass


if __name__ == "__main__":
    main()
