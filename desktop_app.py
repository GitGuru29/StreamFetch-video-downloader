import webview
import threading
import time
import sys
import os
from app import app  # Import your Flask app

def start_server():
    # Run Flask on a different port if needed, or stick to 5000
    app.run(port=5000, debug=False)

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Wait for the server to start (simple 1 second wait)
    time.sleep(1)

    # Create a full-screen or sizable window
    webview.create_window(
        'StreamFetch | Video Downloader',
        'http://127.0.0.1:5000',
        width=1000,
        height=700,
        resizable=True
    )
    
    # Start the PyWebView main loop
    webview.start()
