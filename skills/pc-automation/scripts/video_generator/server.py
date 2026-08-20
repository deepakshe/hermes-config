import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import generator functions
sys.path.append(os.path.dirname(__file__))
from video_generator import (
    get_repo_data,
    generate_hindi_script,
    generate_voiceover,
    build_60s_video
)

class VideoAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_json({"status": "ok"})

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)
        path = parsed_url.path

        if path == "/health":
            self._send_json({"status": "ok", "message": "1-Minute Hindi GitHub Video API is running!"})
            return

        if path == "/api/script":
            topic = params.get('topic', ['ollama'])[0]
            repo_data = get_repo_data(topic)
            full_script, segments = generate_hindi_script(repo_data)
            self._send_json({
                "repo_name": repo_data["name"],
                "stars": repo_data["stars"],
                "tagline": repo_data["tagline"],
                "script": full_script,
                "segments": segments
            })
            return

        if path == "/api/image-prompt":
            topic = params.get('topic', ['ollama'])[0]
            repo_data = get_repo_data(topic)
            self._send_json({
                "repo_name": repo_data["name"],
                "terminal_command": repo_data["command"],
                "pros": repo_data["pros"],
                "cons": repo_data["cons"]
            })
            return

        if path == "/api/image-url":
            topic = params.get('topic', ['ollama'])[0]
            repo_data = get_repo_data(topic)
            self._send_json({
                "scene_layout": "5-Scene GitHub Showcase (Header, Terminal CLI, Pros, Cons, Outro)",
                "status": "Ready for MoviePy compile"
            })
            return

        if path == "/api/generate-voice":
            text = params.get('text', ['Agar aap ek programmer ya AI enthusiast hain...'])[0]
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            out_file = os.path.join(downloads_dir, 'temp_hindi_voice.mp3')
            generate_voiceover(text, out_file)
            self._send_json({"status": "Hindi voiceover audio ready (Madhur Neural)", "audio_path": out_file})
            return

        if path == "/api/hashtags":
            topic = params.get('topic', ['ollama'])[0]
            tags = f"#github #coding #developer #ai #programming #hindi #tech #opensource #{topic.replace('-', '').lower()}"
            self._send_json({"topic": topic, "hashtags": tags})
            return

        if path == "/api/compile":
            topic = params.get('topic', ['ollama'])[0]
            repo_data = get_repo_data(topic)
            full_script, segments = generate_hindi_script(repo_data)
            
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            temp_audio = os.path.join(downloads_dir, 'temp_hindi_voice.mp3')
            output_mp4 = os.path.join(downloads_dir, 'output_reel.mp4')

            if not os.path.exists(temp_audio):
                generate_voiceover(full_script, temp_audio)

            build_60s_video(repo_data, segments, temp_audio, output_mp4)
            self._send_json({
                "status": "1-Minute Hindi GitHub Video Compiled!",
                "video_path": output_mp4,
                "duration": "~50-60 seconds"
            })
            return

        if path == "/api/publish":
            self._send_json({
                "status": "Instagram processed",
                "note": "Ready for Instagram upload"
            })
            return

        if path == "/api/full-pipeline" or path == "/api/generate-video":
            topic = params.get('topic', ['ollama'])[0]
            repo_data = get_repo_data(topic)
            full_script, segments = generate_hindi_script(repo_data)
            
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            temp_audio = os.path.join(downloads_dir, 'temp_hindi_voice.mp3')
            output_mp4 = os.path.join(downloads_dir, 'output_reel.mp4')

            try:
                generate_voiceover(full_script, temp_audio)
                build_60s_video(repo_data, segments, temp_audio, output_mp4)
                hashtags = f"#github #coding #developer #ai #programming #hindi #tech #opensource #{topic.replace('-', '').lower()}"
                caption = f"Top GitHub Repo: {repo_data['name']} 🚀\n\n{full_script}\n\n{hashtags}"

                self._send_json({
                    "status": "success",
                    "message": "1-Minute Hindi GitHub Video Created!",
                    "repo_name": repo_data["name"],
                    "video_path": output_mp4,
                    "caption": caption,
                    "script": full_script,
                    "hashtags": hashtags
                })
            except Exception as e:
                self._send_json({"status": "error", "error": str(e)}, status=500)
            finally:
                if os.path.exists(temp_audio):
                    try: os.remove(temp_audio)
                    except: pass
            return

        self._send_json({"status": "error", "message": "Route not found"}, status=404)

def run_server(port=5000):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, VideoAPIHandler)
    print(f"Hindi GitHub Video API listening on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
