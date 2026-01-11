import 'dart:io' as io;
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class ClaudeService {
  // Use your Render.com URL for production
  final String _baseUrl = 'https://medsnap-7gvx.onrender.com/analyze';

  Future<String> analyzeImage(dynamic image) async {
    String base64Image;
    try {
      print('Starting image conversion to base64');

      // Convert image to base64 (same for both web and mobile)
      if (kIsWeb) {
        // Handle web image
        final XFile webImage = image;
        final bytes = await webImage.readAsBytes();
        base64Image = base64Encode(bytes);
      } else {
        // Handle mobile image
        final io.File mobileImage = image;
        final bytes = await mobileImage.readAsBytes();
        base64Image = base64Encode(bytes);
      }

      print('Image converted to base64, length: ${base64Image.length}');

      // Send to your Flask server on Render.com
      print('Sending request to server at $_baseUrl');

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
        const Duration(seconds: 60), // Increased timeout for Render.com
        onTimeout: () {
          throw Exception('Request timed out after 60 seconds');
        },
      );

      print('Received response, status code: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['description'] != null) {
          print('Successfully received analysis');
          return data['description'];
        }
        throw Exception('No description in response: ${response.body}');
      } else {
        print('Server error: ${response.statusCode} - ${response.body}');
        throw Exception(
            'Failed to analyze image: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('Error in analyzeImage: $e');
      rethrow;
    }
  }
}
