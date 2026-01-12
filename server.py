# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from anthropic import Anthropic
# from dotenv import load_dotenv
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# print("=" * 60)
# print("🚀 Medical Snap Production Server Starting")
# print("=" * 60)

# # Get API key from environment
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# if not ANTHROPIC_API_KEY:
#     logger.error("❌ ANTHROPIC_API_KEY not set in environment variables!")
#     raise ValueError("ANTHROPIC_API_KEY environment variable is required")

# logger.info(f"✅ API Key loaded (length: {len(ANTHROPIC_API_KEY)})")

# # Initialize Anthropic client
# try:
#     client = Anthropic(api_key=ANTHROPIC_API_KEY)
#     logger.info("✅ Anthropic client initialized")
# except Exception as e:
#     logger.error(f"❌ Failed to initialize Anthropic client: {e}")
#     raise

# app = Flask(__name__)

# # Configure CORS for production
# # Allow your Netlify domain and local development
# ALLOWED_ORIGINS = [
#     "https://medsnap.netlify.app",      # Your Netlify domain
#     "https://medsnap-7gvx.onrender.com", # Your Render domain
#     "http://localhost:8000",            # Local Flutter web
#     "http://localhost:5000",            # Local server
#     "http://127.0.0.1:8000",
#     "http://127.0.0.1:5000",
# ]

# CORS(app, resources={
#     r"/*": {
#         "origins": ALLOWED_ORIGINS,
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Accept", "Authorization"],
#         "expose_headers": ["Content-Type"],
#         "supports_credentials": False,
#         "max_age": 600,
#     }
# })

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint for Render.com"""
#     return jsonify({
#         'status': 'healthy',
#         'service': 'medical-snap-api',
#         'version': '1.0.0',
#         'api_ready': True
#     })

# @app.route('/test', methods=['GET'])
# def test():
#     """Test endpoint"""
#     return jsonify({
#         'status': 'Server is running',
#         'service': 'Medical Snap API',
#         'environment': 'production',
#         'cors_allowed_origins': ALLOWED_ORIGINS,
#         'api_key_configured': True
#     })

# @app.route('/analyze', methods=['POST', 'OPTIONS'])
# def analyze_image():
#     """Main analysis endpoint"""
#     # Handle preflight requests
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'ok'})
#         response.headers.add('Access-Control-Allow-Origin', 
#                            request.headers.get('Origin', '*'))
#         return response
    
#     # Log request
#     origin = request.headers.get('Origin', 'unknown')
#     logger.info(f"📨 Request from origin: {origin}")
    
#     try:
#         data = request.json
#         if not data:
#             logger.warning("No JSON data received")
#             return jsonify({'error': 'No data provided'}), 400
            
#         if 'image' not in data:
#             logger.warning("No image data in request")
#             return jsonify({'error': 'No image data provided'}), 400

#         base64_image = data['image']
#         logger.info(f"📷 Processing image, size: {len(base64_image)} chars")
        
#         # Call Anthropic API
#         logger.info("🚀 Sending to Claude API...")
        
#         message = client.messages.create(
#             model="claude-3-haiku-20240307",
#             max_tokens=1024,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "image",
#                             "source": {
#                                 "type": "base64",
#                                 "media_type": "image/jpeg",
#                                 "data": base64_image,
#                             }
#                         },
# {
#   "type": "text",
#   "text": "تۆ پێویستە تەنها و تەنها بە زمانی کوردی (سۆرانی) وەڵام بدەیت. هیچ زمانێکی تر قبوڵ نییە، هیچ وشەیەک بە عەرەبی، ئینگلیزی یان زمانێکی تر بەکارمەهێنە. وێنەی پێوەکراو بە زۆر وردی و بیرکردنەوەی قووڵ شیکردنەوە بکە.\n\nیاسای گشتی:\n- هەموو شیکردنەوەکان و ڕوونکردنەوەکان وەک پزیشکێکی زۆر بەئەزموون بنووسە، وەک ئەوەی نەخۆش ڕاستەوخۆ سەردانی پزیشک کردووە.\n- قسەکان بە شێوەیەکی ئارام، دڵنیاکەرەوە و تێگەیشتوو بنووسە.\n- ئەگەر دڵنیا نیت، ڕوون بڵێ کە پێویستە پشکنینی زیاتر بکرێت.\n\nئەگەر وێنەکە پەیوەندیدار بوو بە دەرمان:\n١- ناوی دەرمانەکە دیاری بکە (ئەگەر بتوانرێت ناوی گشتی).\n٢- ماددەی چالاک و کاریگەرییەکانی لە جەستەدا ڕوون بکە.\n٣- باس بکە بۆ چی بەکاردێت و بۆ چی بەکارناهێنرێت.\n٤- شێوازی بەکارهێنان ڕوون بکە (بڕ، کات، پێش یان دوای خواردن).\n٥- ئاگادارییە گرنگەکان باس بکە (منداڵان، ژنانی دووگیان، نەخۆشییە درێژخایەنەکان).\n٦- تێکچوونی نەرێنی لەگەڵ دەرمانەکانی تر بە وردی باس بکە، بەتایبەتی ئەو دۆخانەی کە هەردوو دەرمانەکە پێکەوە کاریگەری خراپ دروست دەکەن.\n٧- کاریگەری لاوەکیی باوەکان و کاریگەرییە کەمتر باوەکان بنووسە.\n٨- ئامۆژگاری بکە کە کەی پێویستە دەرمان بوەستێنرێت و پزیشک ببینرێت.\n\nئەگەر وێنەکە ئەنجامی تاقیکردنەوەی پزیشکی بوو (خوێن، ڤیتامین، هۆرمۆن، چەوری خوێن، هێلکەی جەستە):\n١- جۆری تاقیکردنەوەکان دیاری بکە.\n٢- هەر ئەنجامێک چییە و چی لە جەستەدا دەکات بە زمانی سادە ڕوون بکە.\n٣- ڕوون بکە ئاستەکان ئاسایی‌ن یان نائاسایی.\n٤- هۆکارە پزیشکییە گونجاوەکان بۆ نائاساییەکان باس بکە.\n٥- ئایا ئەم دۆخە پێویستی بە سەرنجی پزیشکی هەیە یان نا.\n٦- ڕێنمایی چارەسەری ماڵەوە بدە (خواردن، ڕاهێنان، گۆڕینی شێوازی ژیان).\n٧- ئەگەر پێویست بوو، باس بکە کە چ جۆر دەرمانێک (بە ناوی گشتی) بەکاردهێنرێت.\n٨- ڕوون بکە کە کەی پێویستە تاقیکردنەوە دووبارە بکرێت.\n\nئەگەر وێنەکە سۆنار (ئولتراسۆند) بوو:\n١- هەموو وشە و ڕستەکانی لە وێنەکەدا بخوێنەوە و ڕوون بکە.\n٢- ئەنجامەکان وەک پزیشکی پسپۆڕ شیکردنەوە بکە.\n٣- ئایا ئەنجامەکان ئاسایی‌ن یان نائاسایی.\n٤- کاریگەرییەکان لەسەر تەندروستی باس بکە.\n٥- پێشنیاری پزیشکی و هەنگاوە داهاتووەکان بنووسە.\n\nئەگەر وێنەکە تێیدا مرۆڤ بوو:\n- لە پێناو ڕووبەر، جل و ئامرازەکان، هەوڵ بدە پیشە یان چالاکیی ڕۆژانەی بکەیتەوە.\n- هەر تێبینییەکی گشتی و ژیرانە باس بکە.\n\nئەگەر وێنەکە ئامێری ئەلیکترۆنی یان پارچەی پیشەسازی بوو:\n- جۆری ئامێرەکە دیاری بکە.\n- ئەرک و بەکارهێنانی باس بکە.\n- قەبارە و تایبەتمەندییە دیارەکان ڕوون بکە.\n- لە کوێ و بۆ چی بەکاردێت باس بکە.\n\nلە کۆتای هەموو شیکردنەوەیەکی پزیشکیدا:\n- بە ڕوونی بڵێ ئەم شیکردنەوەیە جێگرەوەی سەردانی پزیشکی نییە و تەنها ڕێنماییی گشتییە.\n\nئامانج: ئەپەکە ببێت زیرەکترین و سودمەندترین یارمەتیدەری شیکردنەوەی وێنە لە جیهاندا."
# }


#                     ]
#                 }
#             ]
#         )
        
#         logger.info("✅ Received response from Claude API")
        
#         if message.content and len(message.content) > 0:
#             response_text = message.content[0].text
#             logger.info(f"📄 Response generated: {len(response_text)} chars")
#             return jsonify({'description': response_text})
#         else:
#             logger.error("No content in Claude response")
#             return jsonify({'error': 'No analysis content received'}), 500

#     except Exception as e:
#         logger.error(f"💥 Error in analyze_image: {str(e)}")
#         return jsonify({
#             'error': 'Internal server error',
#             'message': str(e)
#         }), 500

# # Error handlers
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({'error': 'Not found'}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({'error': 'Internal server error'}), 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     logger.info(f"🌐 Starting server on port {port}")
#     logger.info(f"🔧 Health check: http://localhost:{port}/health")
#     logger.info(f"🔧 Test endpoint: http://localhost:{port}/test")
#     app.run(host='0.0.0.0', port=port, debug=False)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from anthropic import Anthropic

print("Medical Snap Server with Multi-Language Support")

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

def get_prompt_for_language(language_code):
    """Get appropriate prompt based on language"""
    
    prompts = {
    'en': """
You are an expert image analyzer.

When given an image, analyze it thoroughly and provide structured, useful information. Consider the type of image:

- **Medicine**: Identify drug name(s), class, form, primary indications, dosage, usage instructions, side effects, interactions with other medicines, and guidance for patients.
- **Medical test results (blood, vitamins, hormones, ultrasound, etc.)**: Explain what each result measures, its effect on the body, whether attention is needed, and recommend ways to improve with diet, lifestyle, or exercise. Act as an experienced doctor.
- **Person**: Describe the person’s appearance, possible profession based on clothing, posture, or accessories, and any notable features.
- **Electronics or industrial components**: Identify type, size if possible, usage, and key features.
- **Other objects or scenes**: Describe what is visible, its function, purpose, and potential uses.

Use structured sections, make explanations clear and detailed, and give actionable information when appropriate. 

Respond in English.
""",

    'ar': """
أنت خبير في تحليل الصور.

عند إعطاء صورة، قم بتحليلها بدقة وقدم معلومات منظمة ومفيدة. اعتبر نوع الصورة:

- **الدواء**: تحديد اسم الدواء، فئته، شكله، الاستخدامات الرئيسية، الجرعة وطريقة الاستخدام، الآثار الجانبية، التفاعلات مع أدوية أخرى، وإرشادات للمريض.
- **نتائج الفحوصات الطبية (الدم، الفيتامينات، الهرمونات، الأشعة، إلخ)**: شرح ما يقيسه كل فحص، تأثيره على الجسم، هل يحتاج لمتابعة طبية، والتوصية بتحسين الحالة عبر الغذاء، النشاط البدني، ونمط الحياة. تصرف كطبيب خبير.
- **الشخص**: وصف مظهر الشخص، المهنة المحتملة بناءً على الملابس أو الوضع أو الإكسسوارات، وأي ميزات مميزة.
- **الأجهزة الإلكترونية أو المكونات الصناعية**: تحديد النوع، الحجم إذا أمكن، الاستخدام، والخصائص الأساسية.
- **أشياء أو مشاهد أخرى**: وصف ما هو ظاهر، وظيفته، الغرض منه، والاستخدامات المحتملة.

استخدم أقسام منظمة، واجعل الشرح واضحاً ومفصلاً، وقدم معلومات قابلة للتطبيق عند الاقتضاء.

رد باللغة العربية.
""",

    'ku': """
تۆ پزیشکی و ئامێرێکی زیرەکی شیکردنەوەی وێنەیت.

کاتێک وێنەیەک پێشکەش کرا، بە وردی شیکردنەوە بکە و زانیارییەکی ڕێکخراو و سودمەند بدە. بە شێوەی گشتی، ئەم جۆرانە دابنێ:

- **دەرمان**: ناوی دەرمان، جۆر، شێوە، بەکارهێنانە سەرەکییەکان، دەستوری خواردنەوە، کاریگەریە لاوەکییەکان، تێکچوونی نەرێنی لەگەڵ دەرمانە تر، و ڕێنمایی بۆ نەخۆش.
- **ئەنجامەکانی تاقیکردنەوەی پزیشکی (خوێن، ڤیتامین، هۆرمۆن، سۆنار و ئولتراسۆند، و هتد)**: چی دیاری دەکات، کاریگەرییەکانی لە جەستە، ئایا پێویستی بە سەرنجی پزیشکی هەیە، و پێشنیاری گۆڕینی ژیان، خواردن، ڕاهێنان، و چالاکی بدە. وەک پزیشکی تەجرووبەدار فێر بکە.
- **مرۆڤ**: پێناسەکردنی شیکاری، ڕووبەر و جل، پێویستی بۆ شێوەی کارەکە یان چالاکی ڕۆژانە بە سەیری جل و کەلە، و تایبەتمەندییەکانی.
- **پارچەکان یان ئامێرەکانی ئەلیکترۆنی/پیشەسازی**: جۆر، قەبارە (ئەگەر بتوانرێت)، بەکارهێنان، و تایبەتمەندییە گرنگەکان.
- **هەر شتێکی تر**: چی دیاری دەکات، ئەرک و بەکارهێنان، کارایەتی، و بەکارهێنانی پێویست.

هەموو شیکردنەوەکان ڕوون، تەفصیلی، و ڕێنمایییەکی پێویست بدە، و ڕێنمایی بکە ئەگەر توانای ئەنجام دان بێت.

وەڵامەکان تەنها بە کوردی سۆرانی بنووسە، بە شێوازی نێیتڤ و خۆری، هیچ وشەیەک بە عەرەبی، ئینگلیزی یان زمانێکی تر بەکارمەهێنە.
"""
}

    
    return prompts.get(language_code, prompts['en'])

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_image():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        base64_image = data['image']
        language = data.get('language', 'en')  # Get language from request, default to English
        
        print(f"Processing request with language: {language}")
        
        # Get appropriate prompt for the language
        prompt = get_prompt_for_language(language)
        
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
            
            # Add disclaimer in appropriate language
            disclaimers = {
                'en': "\n\n⚠️ **Important**: This is AI-generated information. Always verify with a healthcare professional.",
                'ar': "\n\n⚠️ **مهم**: هذه معلومات تم إنشاؤها بواسطة الذكاء الاصطناعي. تحقق دائمًا مع أخصائي رعاية صحية.",
                'ku': "\n\n⚠️ **گرنگ**: ئەمە زانیارییەکی دروستکراوی AI-ە. هەمیشە لەگەڵ پسپۆڕێکی تەندروستیدا پشتڕاست بکەرەوە."
            }
            
            response_text += disclaimers.get(language, disclaimers['en'])
            
            return jsonify({
                'description': response_text,
                'success': True,
                'language': language
            })
        else:
            return jsonify({'error': 'No analysis received from AI'}), 500

    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return jsonify({
            'error': 'Failed to analyze image',
            'details': str(e)
        }), 500

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\nServer starting on port {port}")
    print(f"Supported languages: English, Arabic, Kurdish")
    app.run(host='0.0.0.0', port=port)