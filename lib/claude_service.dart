import 'dart:io' as io;
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class ClaudeService {
  // Use AWS instance IP for web development
  final String _baseUrl = kIsWeb
      ? 'http://16.16.212.44:3000/analyze' //'https://api.medsnap.help/analyze'
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
                    'text':
                        'Analyze this medicine, give benefits in points and give usage (how and when to take) and at the end give some side effects.'
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
