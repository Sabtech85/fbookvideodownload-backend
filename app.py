from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'ONLINE'})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json(force=True, silent=True) or {}
    url = data.get('url')
    quality = data.get('quality', 'HD')
    if not url:
        return jsonify({'error': 'Babu link'}), 400
    url = url.strip()
    if quality == 'HD':
        ydl_format = 'best[ext=mp4]/best'
    else:
        ydl_format = 'best[height<=480][ext=mp4]/best[height<=480]'
    ydl_opts = {
        'format': ydl_format,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Facebook Video')
            thumbnail = info.get('thumbnail', '')
            if not video_url:
                return jsonify({'error': 'Ba a samu bidiyon ba'}), 404
            return jsonify({'success': True, 'videoUrl': video_url, 'title': title, 'thumbnail': thumbnail})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
