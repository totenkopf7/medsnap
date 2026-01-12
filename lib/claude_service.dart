// import 'dart:io' as io;
// import 'dart:convert';
// import 'package:flutter/foundation.dart' show kIsWeb;
// import 'package:http/http.dart' as http;
// import 'package:image_picker/image_picker.dart';

// class ClaudeService {
//   // Production URL - your Render.com backend
//   static const String _productionUrl =
//       'https://medsnap-7gvx.onrender.com/analyze';

//   // Local development URL
//   static const String _localUrl = 'http://localhost:5000/analyze';

//   String get _baseUrl {
//     // For production builds, always use production URL
//     if (const bool.fromEnvironment('dart.vm.product')) {
//       return _productionUrl;
//     }

//     // For development, use localhost on web
//     if (kIsWeb) {
//       // Check if we're on localhost for development
//       final host = Uri.base.host;
//       if (host == 'localhost' || host == '127.0.0.1') {
//         return _localUrl;
//       }
//       // If not localhost, use production
//       return _productionUrl;
//     } else {
//       // For mobile apps, you might want different logic
//       // For now, use production
//       return _productionUrl;
//     }
//   }

//   Future<String> analyzeImage(dynamic image) async {
//     String base64Image;
//     try {
//       print('Starting image conversion to base64');

//       // Convert image to base64
//       if (kIsWeb) {
//         final XFile webImage = image;
//         final bytes = await webImage.readAsBytes();
//         base64Image = base64Encode(bytes);
//       } else {
//         final io.File mobileImage = image;
//         final bytes = await mobileImage.readAsBytes();
//         base64Image = base64Encode(bytes);
//       }

//       print('Image converted to base64, length: ${base64Image.length}');
//       print('Sending request to: $_baseUrl');

//       final response = await http
//           .post(
//         Uri.parse(_baseUrl),
//         headers: {
//           'Content-Type': 'application/json',
//           'Accept': 'application/json',
//         },
//         body: jsonEncode({'image': base64Image}),
//       )
//           .timeout(
//         const Duration(seconds: 60),
//         onTimeout: () {
//           throw Exception('Request timed out after 60 seconds');
//         },
//       );

//       print('Received response, status code: ${response.statusCode}');

//       if (response.statusCode == 200) {
//         final data = jsonDecode(response.body);
//         if (data['description'] != null) {
//           print('Successfully received analysis');
//           return data['description'];
//         }
//         throw Exception('No description in response: ${response.body}');
//       } else {
//         print('Server error: ${response.statusCode} - ${response.body}');
//         throw Exception(
//             'Failed to analyze image: ${response.statusCode} - ${response.body}');
//       }
//     } catch (e) {
//       print('Error in analyzeImage: $e');
//       rethrow;
//     }
//   }
// }

import 'dart:io' as io;
import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class ClaudeService {
  // Production URL
  static const String _productionUrl =
      'https://medsnap-7gvx.onrender.com/analyze';
  static const String _localUrl = 'http://localhost:5000/analyze';

  String get _baseUrl {
    if (const bool.fromEnvironment('dart.vm.product')) {
      return _productionUrl;
    }

    if (kIsWeb) {
      final host = Uri.base.host;
      if (host == 'localhost' || host == '127.0.0.1') {
        return _localUrl;
      }
      return _productionUrl;
    } else {
      return _productionUrl;
    }
  }

  // Language mapping
  static const Map<String, String> _languageCodes = {
    'English': 'en',
    'Arabic': 'ar',
    'Kurdish': 'ku',
  };

  Future<String> analyzeImage(dynamic image,
      {String language = 'English'}) async {
    String base64Image;
    try {
      print('Starting image conversion to base64');

      // Convert image to base64
      if (kIsWeb) {
        final XFile webImage = image;
        final bytes = await webImage.readAsBytes();
        base64Image = base64Encode(bytes);
      } else {
        final io.File mobileImage = image;
        final bytes = await mobileImage.readAsBytes();
        base64Image = base64Encode(bytes);
      }

      print('Image converted to base64, length: ${base64Image.length}');
      print('Selected language: $language');
      print('Sending request to: $_baseUrl');

      final response = await http
          .post(
        Uri.parse(_baseUrl),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'image': base64Image,
          'language': _languageCodes[language] ?? 'en', // Send language code
        }),
      )
          .timeout(
        const Duration(seconds: 60),
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
