import 'dart:io' as io;
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class ClaudeService {
  // Use the local IP address for web development
  final String _baseUrl = kIsWeb
      ? 'https://api.medsnap.help/analyze' //AWS-EC2-IP
      : 'https://api.anthropic.com/v1/messages';

  Future<String> analyzeImage(dynamic image) async {
    String base64Image;
    try {
      print('Starting image conversion to base64');

      if (kIsWeb) {
        // Handle web image
        final XFile webImage = image;
        final bytes = await webImage.readAsBytes();
        base64Image = base64Encode(bytes);
        print('Web image converted to base64, length: ${base64Image.length}');

        // Send to local server
        print('Sending request to local server at $_baseUrl');
        final response = await http
            .post(
          Uri.parse(_baseUrl),
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: jsonEncode({'image': base64Image}),
        )
            .timeout(
          const Duration(seconds: 30),
          onTimeout: () {
            throw Exception('Request timed out');
          },
        );

        print(
            'Received response from server, status code: ${response.statusCode}');
        print('Response body: ${response.body}');

        if (response.statusCode == 200) {
          final data = jsonDecode(response.body);
          if (data['description'] != null) {
            return data['description'];
          }
          throw Exception('No description in response: ${response.body}');
        }
        throw Exception(
            'Failed to analyze image: ${response.statusCode} - ${response.body}');
      } else {
        // Handle mobile image
        final io.File mobileImage = image;
        final bytes = await mobileImage.readAsBytes();
        base64Image = base64Encode(bytes);
        print(
            'Mobile image converted to base64, length: ${base64Image.length}');

        // Send directly to Anthropic API
        print('Sending request to Anthropic API');
        final response = await http.post(
          Uri.parse(_baseUrl),
          headers: {
            'Content-Type': 'application/json',
            'x-api-key':
                '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',
            'anthropic-version': '2023-06-01',
          },
          body: jsonEncode({
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
                      'data': base64Image,
                    }
                  },
                  {
                    'type': 'text',
                    'text': """
You are a highly experienced medical doctor. When a user submits a photo of a medicine, you will:
Identify the medicine and its active ingredients.
Explain its uses, benefits, and dosage clearly.
Warn about common side effects, precautions, and possible interactions with other medications (especially critical ones).
Respond in a friendly, clear, and respectful tone suitable for non-medical users.

When a user submits a test result, you will:
Read and interpret the test as a real physician would.
Explain what the values mean, and if any are abnormal, explain the potential reasons.
Give practical advice based on the results as if talking to a patient: what to do, what to watch for, and when to seek medical attention.
Always make it clear that the analysis is not a substitute for professional medical diagnosis, and encourage the user to consult a real doctor for confirmation and treatment decisions.

Keep the tone warm, supportive, and free of unnecessary medical jargon.
"""
                  }
                ],
              }
            ]
          }),
        );

        if (response.statusCode == 200) {
          final data = jsonDecode(response.body);
          if (data['content'] != null && data['content'].isNotEmpty) {
            return data['content'][0]['text'];
          }
        }
        throw Exception('Failed to analyze image: ${response.statusCode}');
      }
    } catch (e) {
      print('Error in analyzeImage: $e');
      rethrow;
    }
  }
}
