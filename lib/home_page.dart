// import 'dart:io';
// import 'package:flutter/foundation.dart' show kIsWeb;
// import 'package:flutter/material.dart';
// import 'package:image_picker/image_picker.dart';
// import 'claude_service.dart';

// class HomePage extends StatefulWidget {
//   const HomePage({super.key});

//   @override
//   State<HomePage> createState() => _HomePageState();
// }

// class _HomePageState extends State<HomePage> {
//   dynamic _image;
//   String? _description;
//   bool _isLoading = false;
//   final _picker = ImagePicker();

//   Future<void> _pickImage(ImageSource source) async {
//     try {
//       final pickedFile = await _picker.pickImage(
//         source: source,
//         maxHeight: 1080,
//         maxWidth: 1920,
//         imageQuality: 85,
//         preferredCameraDevice: CameraDevice.rear,
//       );
//       if (pickedFile != null) {
//         setState(() {
//           _image = kIsWeb ? pickedFile : File(pickedFile.path);
//           _isLoading = true;
//         });
//         await _analyzeImage();
//       }
//     } catch (e) {
//       setState(() {
//         _isLoading = false;
//       });
//       ScaffoldMessenger.of(context).showSnackBar(
//         SnackBar(content: Text('Error: $e')),
//       );
//     }
//   }

//   Future<void> _analyzeImage() async {
//     if (_image == null) return;
//     try {
//       final description = await ClaudeService().analyzeImage(_image);
//       setState(() {
//         _description = description;
//         _isLoading = false;
//       });
//     } catch (e) {
//       setState(() {
//         _isLoading = false;
//       });
//       ScaffoldMessenger.of(context).showSnackBar(
//         SnackBar(content: Text('Error: $e')),
//       );
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       backgroundColor: Colors.white,
//       appBar: AppBar(
//         title: const Text(
//           'AnyScan',
//           style: TextStyle(
//             fontWeight: FontWeight.w600,
//             color: Colors.white,
//           ),
//         ),
//         centerTitle: true,
//         backgroundColor: Color(0xFF2E7D32), // Professional medical green
//         elevation: 0,
//       ),
//       body: SingleChildScrollView(
//         child: Padding(
//           padding: const EdgeInsets.all(20.0),
//           child: Column(
//             children: [
//               // Image Preview Card
//               Card(
//                 elevation: 4,
//                 shape: RoundedRectangleBorder(
//                   borderRadius: BorderRadius.circular(16),
//                 ),
//                 child: Container(
//                   width: double.infinity,
//                   height: 300,
//                   decoration: BoxDecoration(
//                     borderRadius: BorderRadius.circular(16),
//                     color: Colors.grey[50],
//                   ),
//                   child: _image != null
//                       ? ClipRRect(
//                           borderRadius: BorderRadius.circular(16),
//                           child: kIsWeb
//                               ? Image.network(_image.path, fit: BoxFit.cover)
//                               : Image.file(_image, fit: BoxFit.cover),
//                         )
//                       : Center(
//                           child: Column(
//                             mainAxisAlignment: MainAxisAlignment.center,
//                             children: [
//                               Icon(
//                                 Icons.camera_alt,
//                                 size: 64,
//                                 color: Colors.grey[400],
//                               ),
//                               const SizedBox(height: 16),
//                               Text(
//                                 'No image selected',
//                                 style: TextStyle(
//                                   fontSize: 18,
//                                   color: Colors.grey[600],
//                                 ),
//                               ),
//                             ],
//                           ),
//                         ),
//                 ),
//               ),

//               const SizedBox(height: 24),

//               // Action Buttons
//               Row(
//                 mainAxisAlignment: MainAxisAlignment.center,
//                 children: [
//                   _buildActionButton(
//                     icon: Icons.camera_alt,
//                     label: 'Camera',
//                     onPressed: () => _pickImage(ImageSource.camera),
//                   ),
//                   const SizedBox(width: 16),
//                   _buildActionButton(
//                     icon: Icons.photo_library,
//                     label: 'Gallery',
//                     onPressed: () => _pickImage(ImageSource.gallery),
//                   ),
//                 ],
//               ),

//               const SizedBox(height: 32),

//               // Loading Indicator
//               if (_isLoading)
//                 Column(
//                   children: [
//                     SizedBox(
//                       width: 50,
//                       height: 50,
//                       child: CircularProgressIndicator(
//                         valueColor: AlwaysStoppedAnimation(Color(0xFF2E7D32)),
//                         strokeWidth: 3,
//                       ),
//                     ),
//                     const SizedBox(height: 16),
//                     Text(
//                       'Analyzing image...',
//                       style: TextStyle(
//                         fontSize: 16,
//                         color: Colors.grey[700],
//                         fontWeight: FontWeight.w500,
//                       ),
//                     ),
//                   ],
//                 ),

//               // Results Section
//               if (_description != null && !_isLoading)
//                 Card(
//                   elevation: 4,
//                   shape: RoundedRectangleBorder(
//                     borderRadius: BorderRadius.circular(16),
//                   ),
//                   child: Padding(
//                     padding: const EdgeInsets.all(24.0),
//                     child: Column(
//                       crossAxisAlignment: CrossAxisAlignment.start,
//                       children: [
//                         Row(
//                           children: [
//                             Icon(
//                               Icons.medical_services,
//                               color: Color(0xFF2E7D32),
//                               size: 24,
//                             ),
//                             const SizedBox(width: 8),
//                             Text(
//                               'Analysis Results',
//                               style: TextStyle(
//                                 fontSize: 18,
//                                 fontWeight: FontWeight.w600,
//                                 color: Color(0xFF2E7D32),
//                               ),
//                             ),
//                           ],
//                         ),
//                         const SizedBox(height: 16),
//                         Container(
//                           width: double.infinity,
//                           padding: const EdgeInsets.all(16),
//                           decoration: BoxDecoration(
//                             color: Colors.grey[50],
//                             borderRadius: BorderRadius.circular(12),
//                             border: Border.all(
//                               color: Colors.grey[200]!,
//                               width: 1,
//                             ),
//                           ),
//                           child: Text(
//                             _description!,
//                             style: TextStyle(
//                               fontSize: 15,
//                               color: Colors.grey[800],
//                               height: 1.5,
//                             ),
//                           ),
//                         ),
//                       ],
//                     ),
//                   ),
//                 ),

//               // Empty State
//               if (_description == null && !_isLoading)
//                 Padding(
//                   padding: const EdgeInsets.only(top: 40),
//                   child: Column(
//                     children: [
//                       Icon(
//                         Icons.description,
//                         size: 64,
//                         color: Colors.grey[300],
//                       ),
//                       const SizedBox(height: 16),
//                       Text(
//                         'Upload an image to get AI analysis',
//                         style: TextStyle(
//                           fontSize: 16,
//                           color: Colors.grey[600],
//                         ),
//                       ),
//                     ],
//                   ),
//                 ),
//               const SizedBox(height: 40),
//               Text(
//                 'Developed by Zinar Mizury',
//                 style: TextStyle(
//                   fontSize: 12,
//                   color: Colors.grey,
//                   fontWeight: FontWeight.w400,
//                 ),
//                 textAlign: TextAlign.center,
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }

//   Widget _buildActionButton({
//     required IconData icon,
//     required String label,
//     required VoidCallback onPressed,
//   }) {
//     return ElevatedButton(
//       onPressed: onPressed,
//       style: ElevatedButton.styleFrom(
//         backgroundColor: Color(0xFF2E7D32),
//         foregroundColor: Colors.white,
//         padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
//         shape: RoundedRectangleBorder(
//           borderRadius: BorderRadius.circular(12),
//         ),
//         elevation: 2,
//       ),
//       child: Row(
//         mainAxisSize: MainAxisSize.min,
//         children: [
//           Icon(icon, size: 20),
//           const SizedBox(width: 8),
//           Text(
//             label,
//             style: const TextStyle(
//               fontWeight: FontWeight.w500,
//               fontSize: 15,
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }

import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'claude_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  dynamic _image;
  String? _description;
  bool _isLoading = false;

  final _picker = ImagePicker();
  String _selectedLanguage = 'Kurdish';
  final List<String> _languages = ['English', 'Arabic', 'Kurdish'];

  static const Color primaryColor = Color(0xFF63CFF1);
  static const Color neutralColor = Color(0xFFCDD3D9);

  Future<void> _pickImage(ImageSource source) async {
    try {
      final pickedFile = await _picker.pickImage(
        source: source,
        maxHeight: 1080,
        maxWidth: 1920,
        imageQuality: 85,
        preferredCameraDevice: CameraDevice.rear,
      );

      if (pickedFile != null) {
        setState(() {
          _image = kIsWeb ? pickedFile : File(pickedFile.path);
          _isLoading = true;
          _description = null;
        });
        await _analyzeImage();
      }
    } catch (e) {
      _isLoading = false;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  Future<void> _analyzeImage() async {
    try {
      final description = await ClaudeService()
          .analyzeImage(_image, language: _selectedLanguage);
      setState(() {
        _description = description;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: primaryColor,
        centerTitle: true,
        title: const Text(
          'Any Scan',
          style: TextStyle(fontWeight: FontWeight.w600),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            _languageSelector(),
            const SizedBox(height: 20),
            _imagePreview(),
            const SizedBox(height: 24),
            _actionButtons(),
            const SizedBox(height: 32),
            if (_isLoading) _loadingSection(),
            if (_description != null && !_isLoading) _resultSection(),
            if (_description == null && !_isLoading) _emptyState(),
            const SizedBox(height: 80),
            const Text(
              'Developed by Zinar Mizury',
              style: TextStyle(fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  // ---------------- UI SECTIONS ----------------

  Widget _languageSelector() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: neutralColor),
      ),
      child: Row(
        children: [
          const Icon(Icons.language, color: primaryColor),
          const SizedBox(width: 12),
          const Text(
            'Language',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
          const Spacer(),
          DropdownButton<String>(
            value: _selectedLanguage,
            underline: const SizedBox(),
            icon: const Icon(Icons.keyboard_arrow_down),
            onChanged: (value) {
              setState(() => _selectedLanguage = value!);
            },
            items: _languages
                .map(
                  (lang) => DropdownMenuItem(
                    value: lang,
                    child: Text(lang),
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }

  Widget _imagePreview() {
    return Container(
      height: 280,
      width: double.infinity,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: neutralColor),
      ),
      child: _image != null
          ? ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: kIsWeb
                  ? Image.network(_image.path, fit: BoxFit.cover)
                  : Image.file(_image, fit: BoxFit.cover),
            )
          : Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Icon(Icons.image, size: 60, color: neutralColor),
                SizedBox(height: 12),
                Text('No image selected'),
              ],
            ),
    );
  }

  Widget _actionButtons() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _primaryButton(
          icon: Icons.camera_alt,
          label: 'Camera',
          onPressed: () => _pickImage(ImageSource.camera),
        ),
        const SizedBox(width: 16),
        _primaryButton(
          icon: Icons.photo_library,
          label: 'Gallery',
          onPressed: () => _pickImage(ImageSource.gallery),
        ),
      ],
    );
  }

  Widget _primaryButton({
    required IconData icon,
    required String label,
    required VoidCallback onPressed,
  }) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: primaryColor,
        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
        ),
      ),
      icon: Icon(icon),
      label: Text(label),
    );
  }

  Widget _loadingSection() {
    return Column(
      children: const [
        SizedBox(
          height: 40,
          width: 40,
          child: CircularProgressIndicator(color: primaryColor),
        ),
        SizedBox(height: 16),
        Text('Analyzing image...'),
      ],
    );
  }

  Widget _resultSection() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: neutralColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Analysis Result',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            _description!,
            style: const TextStyle(height: 1.5),
          ),
        ],
      ),
    );
  }

  Widget _emptyState() {
    return Column(
      children: const [
        Icon(Icons.search, size: 56, color: neutralColor),
        SizedBox(height: 12),
        Text('Upload a clear image to start analysis'),
      ],
    );
  }
}
