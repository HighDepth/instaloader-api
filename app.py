from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL missing'}), 400

    filename = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join("downloads", filename)
    os.makedirs("downloads", exist_ok=True)

    try:
        cmd = f"instaloader --dirname-pattern=downloads --no-metadata-json --no-captions --no-profile-pic --no-compress-json '{url}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        return jsonify({'message': 'Download completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
