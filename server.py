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
You are an intelligent visual analysis assistant.

Carefully analyze the uploaded image and first identify what it contains.
Do NOT assume it is a medicine unless it clearly is one.

Follow these rules strictly:

1) If the image shows a MEDICINE (syrup, tablet, injection, supplement, medical product, etc.)  
→ Provide a detailed medical-style explanation using THIS EXACT STRUCTURE:

Title (Product Name or Description)

English Description:
A clear, professional explanation of what the medicine is, what it contains, and what it is used for.

Main Ingredients:
- Ingredient name: Explanation of its role and effect.
(Only list ingredients that are visible or commonly associated if clearly identifiable.)

Uses:
- Main medical uses
- Symptoms it helps relieve
- Additional benefits if applicable

Age Group:
- Specify age suitability if known
- Mention medical supervision clearly

Dosage and Method of Use:
- Children (if applicable)
- Adults
- Method of intake
- Always mention that dosage may vary and medical advice is recommended

Time of Use:
- When it is usually taken
- Duration guidance if known

Side Effects:
- Common side effects
- Rare but serious side effects
- Clear warning to stop use and consult a doctor if needed

⚠️ Always include:
"The product must be used under medical supervision."

---

2) If the image shows MEDICAL TEST RESULTS  
(such as blood tests, vitamins levels, ultrasound, X-ray, MRI, CT scan, lab reports, etc.)  
→ Explain it using THIS FORMAT:

Test Name

Parameter Name:
Result:
Normal Range:
Explanation:
(Simple, clear medical explanation of what the value means)

Repeat this structure for each visible parameter.

At the end, include:

Overall Summary:
- Bullet points summarizing health status
- Mention any abnormal findings if present
- If everything is normal, clearly state that

End with:
✅ Overall impression: (Clear, reassuring medical conclusion)

⚠️ Add a disclaimer that this is informational and not a medical diagnosis.

---

3) If the image is NOT medical  
(for example: a person, object, flower, machine, industrial part, animal, device, etc.)  
→ Describe it accurately based ONLY on what is visible in the image:

- What the object is
- Its purpose or function
- Key visible features
- Possible real-world use cases

Do NOT include medical language unless the image is medical.

---

General Rules:
- Be accurate, clear, and professional
- Do not hallucinate details that are not visible
- If information is unclear, say so honestly
- Match the explanation style strictly to the image type
- Never mix formats

""",

    'ar': """
أنت خبير في تحليل الصور.


قم بتحليل الصورة المرفوعة بعناية، وحدد أولًا ما الذي تحتوي عليه الصورة.
لا تفترض أنها دواء إلا إذا كان ذلك واضحًا بشكل صريح.

التزم بالقواعد التالية بدقة:

1) إذا كانت الصورة تُظهر دواءً  
(شراب، أقراص، حقن، مكملات غذائية، منتج طبي، إلخ)
→ قدّم شرحًا طبيًا مفصلًا باستخدام البنية التالية فقط:

العنوان (اسم المنتج أو وصفه)

الوصف باللغة الإنجليزية:
شرح واضح واحترافي يوضح ما هو الدواء، مكوناته، ولماذا يُستخدم.

المكونات الرئيسية:
- اسم المكوّن: شرح دوره وتأثيره.
(اذكر فقط المكونات الظاهرة أو المعروفة إذا كان من الممكن تحديدها بوضوح)

الاستخدامات:
- الاستخدامات الطبية الرئيسية
- الأعراض التي يساعد في تخفيفها
- الفوائد الإضافية إن وُجدت

الفئة العمرية:
- تحديد الأعمار المناسبة للاستخدام إن كانت معروفة
- التأكيد على ضرورة الإشراف الطبي

الجرعة وطريقة الاستخدام:
- الأطفال (إن وُجد)
- البالغون
- طريقة التناول
- التأكيد دائمًا على أن الجرعة قد تختلف حسب الحالة ويجب استشارة الطبيب

وقت الاستخدام:
- متى يُستخدم عادة
- مدة الاستخدام إن كانت معروفة

الآثار الجانبية:
- الآثار الجانبية الشائعة
- الآثار النادرة ولكن الخطيرة
- تحذير واضح بضرورة إيقاف الاستخدام واستشارة الطبيب عند الحاجة

⚠️ يجب دائمًا تضمين العبارة التالية:
"يجب استخدام المنتج تحت إشراف طبي."

---

2) إذا كانت الصورة تُظهر نتائج فحوصات طبية  
(مثل تحاليل الدم، مستويات الفيتامينات، الأشعة فوق الصوتية، الأشعة السينية، الرنين المغناطيسي، الأشعة المقطعية، تقارير المختبر، إلخ)
→ يجب شرحها باستخدام الصيغة التالية:

اسم الفحص

اسم المؤشر:
النتيجة:
النطاق الطبيعي:
الشرح:
(تفسير طبي بسيط وواضح لمعنى النتيجة)

يتم تكرار هذه الصيغة لكل مؤشر ظاهر في التقرير.

وفي النهاية، أضف:

الملخص العام:
- نقاط مختصرة تلخص الحالة الصحية
- الإشارة إلى أي نتائج غير طبيعية إن وُجدت
- في حال كانت جميع النتائج طبيعية، يجب توضيح ذلك بوضوح

واختم بـ:
✅ الانطباع العام: (خلاصة طبية مطمئنة وواضحة)

⚠️ أضف تنبيهًا بأن هذا الشرح لغرض المعلومات فقط ولا يُعد تشخيصًا طبيًا.

---

3) إذا لم تكن الصورة طبية  
(مثل شخص، غرض، زهرة، آلة، جزء صناعي، حيوان، جهاز، إلخ)
→ قم بوصفها بدقة اعتمادًا فقط على ما هو ظاهر في الصورة:

- ما هو الشيء
- وظيفته أو الغرض منه
- الخصائص الظاهرة
- الاستخدامات المحتملة في الواقع

لا تستخدم أي مصطلحات طبية إلا إذا كانت الصورة طبية بالفعل.

---

قواعد عامة:
- كن دقيقًا وواضحًا واحترافيًا
- لا تختلق معلومات غير ظاهرة في الصورة
- إذا كانت بعض المعلومات غير واضحة، اذكر ذلك بصراحة
- التزم بأسلوب الشرح المناسب لنوع الصورة فقط
- لا تخلط بين الصيغ المختلفة

""",

    'ku': """
تۆ یارمەتیدەری زیرەکی شیکردنەوەی وێنەی.

وێنەی بارکراو بە وردی شیکردنەوە بکە و سەرەتا دیاری بکە وێنەکە چی پیشان دەدات.
هیچ شتێک وەک دەرمان مەفڕێنەوە، مەگەر ئەگەر بە ڕوونی دەرمان بوو.

ئەم یاسایانە بە تەواوی جێبەجێ بکە:

1) ئەگەر وێنەکە دەرمان پیشان بدات  
(شەربەت، حەب، دەرزی، پێکهاتەی خۆراکی، یان هەر بەرهەمێکی پزیشکی)
→ پێویستە شیکردنەوەیەکی پزیشکی و ورد پێشکەش بکە بە ئەم ڕێکخستنەی خوارەوە تەنها:

ناونیشان (ناوی بەرهەم یان وەسفی)

وەسف بە زمانی ئینگلیزی:
ڕوونکردنەوەیەکی پیشه‌کی و ئاشکرا لەسەر ئەوەی دەرمانەکە چییە، چی پێکهاتەیەکی هەیە و بۆ چی بەکاردێت.

پێکهاتە سەرەکییەکان:
- ناوی پێکهاتە: ڕوونکردنەوەی کاریگەری و ئەرکەکەی.
(تەنها ئەو پێکهاتانە بنووسە کە دیارە یان بە ئاسانی ناسراون)

بەکارهێنانەکان:
- بەکارهێنانی پزیشکی سەرەکی
- ئەو نیشانانەی کە سووک دەکات
- سوودە زیادەکان ئەگەر هەبوو

گرووپی تەمەن:
- دیاریکردنی تەمەنە گونجاوەکان ئەگەر زانیاری هەبوو
- جەختکردنەوە لەسەر پێویستی چاودێری پزیشک

دوز و شێوازی بەکارهێنان:
- منداڵان (ئەگەر هەبوو)
- گەورەکان
- شێوازی خواردن یان بەکارهێنان
- هەمیشە جەخت بکەوە کە دوز لە کەسێک بۆ کەسێکی تر جیاواز دەبێت و پێویستە پزیشک ڕاوێژ بکرێت

کاتی بەکارهێنان:
- کاتێک بە زۆری بەکاردێت
- ماوەی بەکارهێنان ئەگەر دیاربوو

کاریگەرییە لاوەکییەکان:
- کاریگەرییە باوەکان
- کاریگەرییە دەگمەن و توندەکان
- ئاگاداری ڕوون بۆ وەستاندنی بەکارهێنان و پەیوەندی کردن بە پزیشک

⚠️ هەمیشە ئەم دەستەواژەیە بنووسە:
"پێویستە ئەم بەرهەمە لەژێر چاودێری پزیشکدا بەکاربهێنرێت."

---

2) ئەگەر وێنەکە ئەنجامی تاقیکردنەوەی پزیشکی پیشان بدات  
(وەک تاقیکردنەوەی خوێن، ئاستی ڤیتامینەکان، ئەلتراسەوند، تیشکی X، MRI، CT Scan، ڕاپۆرتی تاقیگە، هتد)
→ شیکردنەوەکە بە ئەم شێوازە بکە:

ناوی تاقیکردنەوە

ناوی پێوانە:
ئەنجام:
ئاستی ئاسایی:
ڕوونکردنەوە:
(تێگەیشتنێکی پزیشکی سادە و ڕوون بۆ واتای ئەنجامەکە)

ئەم ڕێکخستنە بۆ هەر پێوانەیەکی دیارکراو دووبارە بکە.

لە کۆتایی، ئەمانە زیاد بکە:

پوختەی گشتی:
- خاڵەکان بۆ کورتەکردنەوەی دۆخی تەندروستی
- ئاماژە بە ئەنجامە نائاساییەکان ئەگەر هەبوو
- ئەگەر هەموو ئەنجامەکان ئاسایی بوون، بە ڕوونی باس بکە

کۆتایی بکە بە:
✅ تێبینی گشتی: (پوختەیەکی پزیشکی ئارامبەخش و ڕوون)

⚠️ ئاگاداری زیاد بکە کە ئەم زانیارییانە تەنها بۆ ئاشنابوونن و تشخیص نییە.

---

3) ئەگەر وێنەکە پزیشکی نەبوو  
(وەک کەسێک، شتێک، گوڵ، ئامێر، پارچەی پیشەسازی، ئاژەڵ، ئامێرێک، هتد)
→ وەسفی بە وردی بکە تەنها بە پێی ئەوەی لە وێنەکەدا دیارە:

- ئەو شتە چییە
- ئامانج یان کارکردنی
- تایبەتمەندییە دیارەکان
- بەکارهێنانی ئەگادار لە ژیاندا

هیچ زمانێکی پزیشکی بەکار مەهێنە، مەگەر ئەگەر وێنەکە پزیشکی بوو.

---

یاسا گشتییەکان:
- ورد، ڕوون و پیشه‌کی بە
- زانیاری نادیار دروست مەکە
- ئەگەر شتێک ڕوون نەبوو، بە ڕاستی باس بکە
- تەنها شێوازی گونجاو بە جۆری وێنەکە بەکاربهێنە
- ڕێکخستنەکان تێکەڵ مەکە

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