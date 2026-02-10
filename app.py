from flask import Flask, render_template, request, Response, jsonify, stream_with_context
import yt_dlp
import os
import time
import json

app = Flask(__name__)

# Global dictionary to store progress (simple in-memory storage for demo)
# Key: video_id (or some unique identifier), Value: progress dict
download_progress = {}

def progress_hook(d):
    video_id = d.get('info_dict', {}).get('id', 'unknown')
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%', '')
        try:
            download_progress[video_id] = {
                'status': 'downloading',
                'percentage': float(p),
                'speed': d.get('_speed_str', 'N/A'),
                'eta': d.get('_eta_str', 'N/A'),
                'filename': d.get('filename', 'downloading...')
            }
        except ValueError:
             pass
    elif d['status'] == 'finished':
        download_progress[video_id] = {
            'status': 'finished',
            'percentage': 100,
            'filename': d.get('filename', 'completed')
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality', 'best')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Configure yt-dlp options
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]' if quality != 'audio' else 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'noplaylist': True,
    }

    if quality == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        # Merge video and audio
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id', 'unknown')
            
            # Start download in a separate thread or process in a real app
            # For this simple synchronous example, we'll download directly
            # Note: This will block the request until download completes
            # A better approach for a web app is to use Celery or a background thread
            
            # To allow progress updates, we need a way to return immediately and poll
            # For simplicity in this 'single-turn' generation, I'll use a generator checking progress
            # But standard Flask structure suggests AJAX polling.
            
            # Let's start a background thread for the download
            import threading
            def run_download():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_inner:
                    ydl_inner.download([url])
            
            thread = threading.Thread(target=run_download)
            thread.start()
            
            return jsonify({'status': 'started', 'video_id': video_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<video_id>')
def progress(video_id):
    return jsonify(download_progress.get(video_id, {'status': 'unknown'}))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
