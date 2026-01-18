from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic
import requests  # Add this import for translation

print("AnyScan Server with Multi-Category & Multi-Language Support")

# Get API key
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not set!")
else:
    print(f"API Key loaded")

# Initialize Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)

app = Flask(__name__)
CORS(app)

def translate_text(text, target_language):
    """Translate text using Google Translate API"""
    try:
        # Google Translate API endpoint
        url = "https://translate.googleapis.com/translate_a/single"
        
        # Map language codes for translation
        language_map = {
            'ar': 'ar',  # Arabic
            'ku': 'ku',  # Kurdish (Sorani/Kurmanji)
            'en': 'en'   # English
        }
        
        target_lang_code = language_map.get(target_language, 'en')
        
        params = {
            'client': 'gtx',
            'sl': 'en',  # source language (always English)
            'tl': target_lang_code,  # target language
            'dt': 't',
            'q': text
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # Extract translated text from response
            translated_parts = []
            for sentence in data[0]:
                if sentence and len(sentence) > 0:
                    translated_text = sentence[0] if sentence[0] else ''
                    if translated_text:
                        translated_parts.append(translated_text)
            
            if translated_parts:
                translated_text = ' '.join(translated_parts)
                print(f"Translation successful: {len(translated_text)} chars to {target_language}")
                return translated_text
            else:
                print("Translation returned empty result")
                return None
        else:
            print(f"Translation API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def get_prompt_for_category(category):
    """Get appropriate prompt based on category"""
    
    # Base prompt template
    base_prompt = """You are a professional analysis assistant operating in {CATEGORY} mode.

GENERAL BEHAVIOR (applies to all modes):
- Give concise, accurate, and actionable explanations.
- Use clear structure and bullet points when helpful.
- Avoid unnecessary verbosity.
- If information is uncertain, explicitly state uncertainty.
- Never fabricate details.
- Adjust technical depth based on the category.
- When appropriate, include safety warnings.
- Do not assume intent beyond what is provided.

OUTPUT STYLE:
- Be factual and professional.
- No roleplay.
- No moral judgment.
- No emojis.
- No unnecessary disclaimers.
"""
    
    # Category-specific rules
    category_rules = {
        'medicine': """CATEGORY-SPECIFIC RULES:

MEDICINE:
- Act as a medical information assistant, not a doctor.
- Identify medicines, medical components, or health-related items.
- Provide educational information only.
- Never diagnose, prescribe, or recommend personal treatment.
- Always include safety notes and advise consulting a licensed professional.""",
        
        'industrial': """CATEGORY-SPECIFIC RULES:

INDUSTRIAL:
- Act as an industrial systems and maintenance specialist.
- Identify equipment, components, and processes.
- Explain function, common issues, and operational context.
- Emphasize safety, standards, and proper procedures.
- Avoid giving unsafe or unauthorized instructions.""",
        
        'person': """CATEGORY-SPECIFIC RULES:

PERSON:
- Describe visible physical characteristics only.
- Do not identify real individuals.
- Do not guess age, ethnicity, religion, health, or personality.
- Focus on clothing, posture, activity, or observable context.""",
        
        'environment': """CATEGORY-SPECIFIC RULES:

ENVIRONMENT:
- Analyze surroundings, location type, conditions, and visible risks.
- Highlight environmental or situational safety concerns.
- Avoid speculation beyond visible evidence.""",
        
        'safety': """CATEGORY-SPECIFIC RULES:

SAFETY:
- Identify hazards, risks, and unsafe conditions.
- Provide general safety guidance and best practices.
- Do not replace professional safety inspections or certifications.
- Use clear warnings when hazards are present.""",
        
        'objects': """CATEGORY-SPECIFIC RULES:

OBJECTS:
- Identify objects and their typical purpose.
- Explain materials, design, and common uses.
- Avoid speculation if identification is uncertain.""",
        
        'food': """CATEGORY-SPECIFIC RULES:

FOOD:
- Identify food items and ingredients if visible.
- Provide general nutritional or culinary information.
- Avoid medical or dietary prescriptions.
- Mention allergies or food safety concerns when relevant.""",
        
        'general': """CATEGORY-SPECIFIC RULES:

GENERAL:
- Provide neutral, informative descriptions.
- Answer clearly based on available information.
- Avoid assumptions or over-analysis."""
    }
    
    # Get the specific category rules, default to general
    specific_rules = category_rules.get(category, category_rules['general'])
    
    # Combine base prompt with category rules
    full_prompt = base_prompt.replace("{CATEGORY}", category.upper()) + "\n\n" + specific_rules
    
    return full_prompt

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_image():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        base64_image = data['image']
        language = data.get('language', 'en')
        category = data.get('category', 'medicine')
        original_language = data.get('original_language', 'en')
        needs_translation = data.get('needs_translation', False)
        
        print(f"Processing request - Category: {category}, Language: {language}, Needs translation: {needs_translation}, Original language: {original_language}")
        
        # ==== CHANGE START: Always use English for AI analysis ====
        # Get appropriate prompt for the category
        prompt = get_prompt_for_category(category)
        
        # Add image analysis instruction
        prompt += "\n\nAnalyze the uploaded image according to the above rules and provide a professional analysis."
        
        print(f"Using prompt for category: {category}")
        # ==== CHANGE END ====
        
        # Call Anthropic API
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            temperature=0.3,
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
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        
        if message.content and len(message.content) > 0:
            response_text = message.content[0].text
            
            result = {
                'description': response_text,
                'success': True,
                'language': language,
                'category': category,
                'translated_description': None
            }
            
            # ==== CHANGE START: Always translate if needed ====
            if needs_translation and original_language != 'en':
                print(f"Translating from English to {original_language}...")
                translated_text = translate_text(response_text, original_language)
                if translated_text:
                    result['translated_description'] = translated_text
                    print(f"Translation successful, length: {len(translated_text)}")
                else:
                    print("Translation failed, keeping English description")
                    # If translation fails, still return English description
            # ==== CHANGE END ====
            
            return jsonify(result)
        else:
            return jsonify({'error': 'No analysis received from AI'}), 500

    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return jsonify({
            'error': 'Failed to analyze image',
            'details': str(e)
        }), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Endpoint to get supported categories"""
    return jsonify({
        'supported_categories': [
            {'code': 'medicine', 'name': 'Medicine'},
            {'code': 'industrial', 'name': 'Industrial'},
            {'code': 'person', 'name': 'Person'},
            {'code': 'environment', 'name': 'Environment'},
            {'code': 'safety', 'name': 'Safety'},
            {'code': 'objects', 'name': 'Objects'},
            {'code': 'food', 'name': 'Food'},
            {'code': 'general', 'name': 'General'}
        ]
    })

@app.route('/languages', methods=['GET'])
def get_languages():
    """Endpoint to get supported languages"""
    return jsonify({
        'supported_languages': [
            {'code': 'en', 'name': 'English'},
            {'code': 'ar', 'name': 'Arabic'},
            {'code': 'ku', 'name': 'Kurdish'}
        ]
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to check server status"""
    return jsonify({
        'status': 'running',
        'service': 'AnyScan AI Analysis',
        'translation_supported': True,
        'categories': ['medicine', 'industrial', 'person', 'environment', 'safety', 'objects', 'food', 'general'],
        'languages': ['en', 'ar', 'ku']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\nAnyScan Server starting on port {port}")
    print(f"Supported categories: Medicine, Industrial, Person, Environment, Safety, Objects, Food, General")
    print(f"Supported languages: English (AI), with Arabic/Kurdish translation")
    print(f"Server ready to process requests...")
    app.run(host='0.0.0.0', port=port)