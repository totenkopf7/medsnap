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
  dynamic _image; // Changed from File? to dynamic to handle both web and mobile
  String? _description;
  bool _isLoading = false;
  final _picker = ImagePicker();

  Future<void> _pickImage(ImageSource source) async {
    try {
      print('Starting image pick from ${source.name}');
      final pickedFile = await _picker.pickImage(
        source: source,
        maxHeight: 1080,
        maxWidth: 1920,
        imageQuality: 85,
        preferredCameraDevice: CameraDevice.rear,
      );
      if (pickedFile != null) {
        print('Image picked successfully: ${pickedFile.path}');
        setState(() {
          _image = kIsWeb ? pickedFile : File(pickedFile.path);
          _isLoading = true;
        });
        await _analyzeImage();
      } else {
        print('No image selected.');
      }
    } catch (e) {
      print('Error picking image: $e');
      setState(() {
        _isLoading = false;
      });
      // Show error to user
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error picking image: $e')),
      );
    }
  }

  Future<void> _analyzeImage() async {
    if (_image == null) return;
    setState(() {
      _isLoading = true;
    });
    try {
      print('Starting image analysis');
      final description = await ClaudeService().analyzeImage(_image);
      print('Analysis completed successfully');
      setState(() {
        _description = description;
        _isLoading = false;
      });
    } catch (e) {
      print('Error analyzing image: $e');
      setState(() {
        _isLoading = false;
      });
      // Show error to user
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error analyzing image: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        title: const Text('Medical Snap'),
        centerTitle: true,
        backgroundColor: const Color.fromARGB(255, 202, 98, 66),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                height: 300,
                width: 300,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: _image != null
                    ? kIsWeb
                        ? Image.network(_image.path)
                        : Image.file(_image)
                    : const Center(
                        child: Text(
                        'Choose an image',
                        style:
                            TextStyle(color: Color.fromARGB(255, 202, 98, 66)),
                      )),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color.fromARGB(255, 202, 98, 66),
                    ),
                    onPressed: () => _pickImage(ImageSource.camera),
                    child: const Text('Take Photo'),
                  ),
                  const SizedBox(width: 10),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color.fromARGB(255, 202, 98, 66),
                    ),
                    onPressed: () => _pickImage(ImageSource.gallery),
                    child: const Text('Pick from Gallery'),
                  ),
                ],
              ),
              const SizedBox(height: 25),
              if (_isLoading)
                const Column(
                  children: [
                    CircularProgressIndicator(),
                    SizedBox(height: 10),
                    Text(
                      'Analyzing image...',
                      style: TextStyle(color: Color.fromARGB(255, 202, 98, 66)),
                    ),
                  ],
                )
              else if (_description != null)
                Container(
                  padding: const EdgeInsets.all(16.0),
                  decoration: BoxDecoration(
                    color: Colors.grey[900],
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    _description!,
                    style: const TextStyle(
                        fontSize: 16,
                        fontFamily: 'Noto',
                        color: Color.fromARGB(255, 202, 98, 66)),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
