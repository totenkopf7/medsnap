from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests
import socket

def get_local_ip():
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

app = Flask(__name__)

# Get the local IP address
LOCAL_IP = get_local_ip()
print(f"Local IP address: {LOCAL_IP}")

# Configure CORS with specific origins
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins during development
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"],
        "supports_credentials": True
    }
})

ANTHROPIC_API_KEY = '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'

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'Server is running',
        'message': 'You can now send image analysis requests',
        'server_ip': LOCAL_IP,
        'allowed_origins': [
            f"http://{LOCAL_IP}:8000",
            "http://localhost:8000",
            "http://127.0.0.1:8000"
        ]
    })

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_image():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    try:
        print("Received request headers:", dict(request.headers))
        print("Received request method:", request.method)
        print("Origin:", request.headers.get('Origin'))
        
        data = request.json
        if not data:
            print("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        if 'image' not in data:
            print("No image data in request")
            return jsonify({'error': 'No image data provided'}), 400

        base64_image = data['image']
        print("Received image data, length:", len(base64_image))
        
        # Call Anthropic API
        print("Sending request to Anthropic API...")
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01',
            },
            json={
                'model': 'claude-3-opus-20240229',
                'max_tokens': 1024,
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'image',
                                'source': {
                                    'type': 'base64',
                                    'media_type': 'image/jpeg',
                                    'data': base64_image,
                                }
                            },
                            {
                                'type': 'text',
                                'text': 'Analyze this medicine, give benefits in points and give usage (how and when to take) and at the end give some side effects.'
                            }
                        ],
                    }
                ]
            }
        )

        print("Received response from Anthropic API, status code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('content') and len(result['content']) > 0:
                return jsonify({'description': result['content'][0]['text']})
            else:
                print("No content in response:", result)
                return jsonify({'error': 'No analysis content received'}), 500
        else:
            print("Error response from Anthropic API:", response.text)
            return jsonify({'error': f'API request failed: {response.text}'}), response.status_code

    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Server starting...")
    print(f"Test the server at: http://{LOCAL_IP}:3000/test")
    print("Make sure to run Flutter web app on port 8000")
    app.run(host='0.0.0.0', port=3000, debug=True) 