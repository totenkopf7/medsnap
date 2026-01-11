from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

print("=" * 60)
print("🚀 Medical Snap Production Server Starting")
print("=" * 60)

# Get API key from environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    logger.error("❌ ANTHROPIC_API_KEY not set in environment variables!")
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

logger.info(f"✅ API Key loaded (length: {len(ANTHROPIC_API_KEY)})")

# Initialize Anthropic client
try:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    logger.info("✅ Anthropic client initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Anthropic client: {e}")
    raise

app = Flask(__name__)

# Configure CORS for production
# Allow your Netlify domain and local development
ALLOWED_ORIGINS = [
    "https://medsnap.netlify.app",      # Your Netlify domain
    "https://medsnap-7gvx.onrender.com", # Your Render domain
    "http://localhost:8000",            # Local Flutter web
    "http://localhost:5000",            # Local server
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5000",
]

CORS(app, resources={
    r"/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False,
        "max_age": 600,
    }
})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render.com"""
    return jsonify({
        'status': 'healthy',
        'service': 'medical-snap-api',
        'version': '1.0.0',
        'api_ready': True
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'Server is running',
        'service': 'Medical Snap API',
        'environment': 'production',
        'cors_allowed_origins': ALLOWED_ORIGINS,
        'api_key_configured': True
    })

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_image():
    """Main analysis endpoint"""
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 
                           request.headers.get('Origin', '*'))
        return response
    
    # Log request
    origin = request.headers.get('Origin', 'unknown')
    logger.info(f"📨 Request from origin: {origin}")
    
    try:
        data = request.json
        if not data:
            logger.warning("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        if 'image' not in data:
            logger.warning("No image data in request")
            return jsonify({'error': 'No image data provided'}), 400

        base64_image = data['image']
        logger.info(f"📷 Processing image, size: {len(base64_image)} chars")
        
        # Call Anthropic API
        logger.info("🚀 Sending to Claude API...")
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image,
                            }
                        },
                        {
                            "type": "text",
                            "text": "Analyze this medicine, give benefits in points and give usage (how and when to take) and at the end give some side effects, IMPORTANT: ALL IN ARABIC."
                        }
                    ]
                }
            ]
        )
        
        logger.info("✅ Received response from Claude API")
        
        if message.content and len(message.content) > 0:
            response_text = message.content[0].text
            logger.info(f"📄 Response generated: {len(response_text)} chars")
            return jsonify({'description': response_text})
        else:
            logger.error("No content in Claude response")
            return jsonify({'error': 'No analysis content received'}), 500

    except Exception as e:
        logger.error(f"💥 Error in analyze_image: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🌐 Starting server on port {port}")
    logger.info(f"🔧 Health check: http://localhost:{port}/health")
    logger.info(f"🔧 Test endpoint: http://localhost:{port}/test")
    app.run(host='0.0.0.0', port=port, debug=False)