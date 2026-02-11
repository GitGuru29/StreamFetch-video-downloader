# StreamFetch - Video Downloader

StreamFetch is a powerful and lightweight video downloader application built with Python. It supports downloading high-quality videos (up to 1080p) from YouTube, Facebook, and other platforms supported by `yt-dlp`. You can run it as a local web application or as a standalone desktop application.

## 🚀 Features

*   **High-Quality Downloads**: Supports video downloads up to 1080p resolution.
*   **Audio Extraction**: Option to download audio only (MP3).
*   **Platform Support**: Downloads from YouTube, Facebook, and more.
*   **Real-time Progress**: Visual progress bar tracking download status.
*   **Dual Mode**: Run as a web interface or a native desktop application.
*   **Cross-Platform**: Compatible with Windows and Linux.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
*   **FFmpeg**: Required for merging video and audio streams (for 1080p+ downloads) and audio conversion.
    *   **Linux**: `sudo apt install ffmpeg`
    *   **Windows**: [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/StreamFetch.git](https://github.com/yourusername/StreamFetch.git)
    cd StreamFetch
    ```

2.  **Create a virtual environment (Optional but Recommended)**
    ```bash
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    pip install pywebview pyinstaller  # Required for desktop app and building
    ```

## 🖥️ Usage

### Run as Web App
This starts a local web server. You can access the downloader through your browser.
```bash
python app.py
