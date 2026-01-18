// --------------------------------------------------
import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'claude_service.dart';
import 'theme/app_colors.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  dynamic _image;
  String? _description;
  bool _isLoading = false;
  String _selectedCategory = 'Medicine';
  final _picker = ImagePicker();
  String _selectedLanguage = 'Kurdish';
  // ==== CHANGE START: Add variables for text animation and scrolling ====
  String _displayedText = '';
  bool _isAnimatingText = false;
  int _textAnimationIndex = 0;
  final ScrollController _scrollController = ScrollController();
  final GlobalKey _resultsKey = GlobalKey();
  // ==== CHANGE END ====

  final List<String> _languages = ['English', 'Arabic', 'Kurdish'];
  final List<String> _categories = [
    'Medicine',
    'Industrial',
    'Person',
    'Environment',
    'Safety',
    'Objects',
    'Food',
    'General'
  ];

  @override
  void dispose() {
    // ==== CHANGE START: Dispose scroll controller ====
    _scrollController.dispose();
    // ==== CHANGE END ====
    super.dispose();
  }

  void refresh() {
    setState(() {
      _image = null;
      _description = null;
      _isLoading = false;
      _selectedCategory = 'Medicine';
      _selectedLanguage = 'Kurdish';
      // ==== CHANGE START: Reset animation variables ====
      _displayedText = '';
      _isAnimatingText = false;
      _textAnimationIndex = 0;
      // ==== CHANGE END ====
    });
  }

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
          // ==== CHANGE START: Reset animation variables ====
          _displayedText = '';
          _isAnimatingText = false;
          _textAnimationIndex = 0;
          // ==== CHANGE END ====
        });
        await _analyzeImage();
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  Future<void> _analyzeImage() async {
    try {
      final description = await ClaudeService().analyzeImage(
        _image,
        language: _selectedLanguage,
        category: _selectedCategory,
      );
      setState(() {
        _description = description;
        _isLoading = false;
        // ==== CHANGE START: Start text animation ====
        _displayedText = '';
        _isAnimatingText = true;
        _textAnimationIndex = 0;
        _startTextAnimation(description);
        // ==== CHANGE END ====
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  // ==== CHANGE START: Updated text animation method with auto-scroll ====
  void _startTextAnimation(String fullText) {
    if (fullText.isEmpty) {
      _isAnimatingText = false;
      return;
    }

    _textAnimationIndex = 0;
    _displayedText = '';

    Future.doWhile(() async {
      if (_textAnimationIndex < fullText.length && _isAnimatingText) {
        await Future.delayed(
            const Duration(milliseconds: 10)); // Adjust speed here

        setState(() {
          _displayedText = fullText.substring(0, _textAnimationIndex + 1);
          _textAnimationIndex++;
        });

        // Auto-scroll to bottom as text grows - with a small delay to ensure layout
        await Future.delayed(const Duration(milliseconds: 20));

        if (_scrollController.hasClients) {
          _scrollController.animateTo(
            _scrollController.position.maxScrollExtent,
            duration: const Duration(milliseconds: 50),
            curve: Curves.easeOut,
          );
        }

        return true;
      } else {
        _isAnimatingText = false;
        return false;
      }
    });
  }
  // ==== CHANGE END ====

  // ==== CHANGE START: Add method to scroll to results ====
  void _scrollToResults() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_resultsKey.currentContext != null) {
        Scrollable.ensureVisible(
          _resultsKey.currentContext!,
          duration: const Duration(milliseconds: 500),
          curve: Curves.easeInOut,
        );
      }
    });
  }
  // ==== CHANGE END ====

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Any Scan',
          style: TextStyle(
            fontWeight: FontWeight.w600,
            color: Colors.white,
          ),
        ),
        centerTitle: true,
        backgroundColor: AppColors.primaryColor,
        elevation: 0,
        actions: [
          IconButton(
            tooltip: 'Refresh',
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: refresh,
          ),
        ],
      ),
      body: // ==== CHANGE START: Wrap with SingleChildScrollView and controller ====
          SingleChildScrollView(
        controller: _scrollController,
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Row(
                children: [
                  // Category Selection Card
                  Expanded(child: _buildCategoryCard()),

                  SizedBox(width: 16),
                  // Language Selection Card
                  Expanded(child: _buildLanguageCard()),
                ],
              ),
              // Image Preview Card
              Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Container(
                  width: double.infinity,
                  height: 300,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    color: Colors.grey[50],
                  ),
                  child: _image != null
                      ? ClipRRect(
                          borderRadius: BorderRadius.circular(16),
                          child: kIsWeb
                              ? Image.network(_image.path, fit: BoxFit.cover)
                              : Image.file(_image, fit: BoxFit.cover),
                        )
                      : Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.camera_alt,
                                size: 64,
                                color: Colors.grey[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'No image selected',
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.grey[600],
                                ),
                              ),
                            ],
                          ),
                        ),
                ),
              ),

              const SizedBox(height: 24),

              // Action Buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _buildActionButton(
                    icon: Icons.camera_alt,
                    label: 'Camera',
                    onPressed: () => _pickImage(ImageSource.camera),
                  ),
                  const SizedBox(width: 16),
                  _buildActionButton(
                    icon: Icons.photo_library,
                    label: 'Gallery',
                    onPressed: () => _pickImage(ImageSource.gallery),
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // Loading Indicator
              if (_isLoading)
                Column(
                  children: [
                    SizedBox(
                      width: 50,
                      height: 50,
                      child: CircularProgressIndicator(
                        valueColor:
                            AlwaysStoppedAnimation(AppColors.primaryColor),
                        strokeWidth: 3,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Analyzing image...',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.grey[700],
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Category: $_selectedCategory • Language: $_selectedLanguage',
                      style: TextStyle(
                        fontSize: 10,
                        color: Colors.grey[600],
                      ),
                    ),
                    // ==== CHANGE START: Show translation info ====
                    if (_selectedLanguage != 'English')
                      Padding(
                        padding: const EdgeInsets.only(top: 8.0),
                        child: Text(
                          'AI analyzing in English, will translate to $_selectedLanguage',
                          style: TextStyle(
                            fontSize: 10,
                            color: Colors.grey[500],
                            fontStyle: FontStyle.italic,
                          ),
                        ),
                      ),
                    // ==== CHANGE END ====
                  ],
                ),

              // Results Section
              if (_description != null && !_isLoading)
                // ==== CHANGE START: Add key to results section ====
                KeyedSubtree(
                  key: _resultsKey,
                  child: Card(
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Row(
                                children: [
                                  _getCategoryIcon(_selectedCategory),
                                  const SizedBox(width: 8),
                                  Text(
                                    'Analysis Results',
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w600,
                                      color: AppColors.primaryColor,
                                    ),
                                  ),
                                ],
                              ),
                              Container(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 12, vertical: 4),
                                decoration: BoxDecoration(
                                  color:
                                      AppColors.primaryColor.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                child: Column(
                                  children: [
                                    Text(
                                      _selectedCategory,
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: AppColors.primaryColor,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                    Text(
                                      _selectedLanguage,
                                      style: TextStyle(
                                        fontSize: 9,
                                        color: AppColors.primaryColor
                                            .withOpacity(0.8),
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.grey[50],
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(
                                color: Colors.grey[200]!,
                                width: 1,
                              ),
                            ),
                            child: // ==== CHANGE START: Use animated text widget ====
                                _isAnimatingText
                                    ? SelectableText.rich(
                                        TextSpan(
                                          text: _displayedText,
                                          style: TextStyle(
                                            fontSize: 15,
                                            color: Colors.grey[800],
                                            height: 1.5,
                                          ),
                                        ),
                                      )
                                    : SelectableText(
                                        _description!,
                                        style: TextStyle(
                                          fontSize: 15,
                                          color: Colors.grey[800],
                                          height: 1.5,
                                        ),
                                      ),
                            // ==== CHANGE END ====
                          ),
                          // ==== CHANGE START: Show animation status ====
                          if (_isAnimatingText)
                            Padding(
                              padding: const EdgeInsets.only(top: 8.0),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.end,
                                children: [
                                  Icon(
                                    Icons.animation,
                                    size: 12,
                                    color: Colors.grey[500],
                                  ),
                                  SizedBox(width: 4),
                                  Text(
                                    'Animating... ${((_textAnimationIndex / (_description?.length ?? 1)) * 100).toStringAsFixed(0)}%',
                                    style: TextStyle(
                                      fontSize: 10,
                                      color: Colors.grey[500],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          // ==== CHANGE END ====
                        ],
                      ),
                    ),
                  ),
                ),
              // ==== CHANGE END ====

              // Empty State
              if (_description == null && !_isLoading)
                Padding(
                  padding: const EdgeInsets.only(top: 40),
                  child: Column(
                    children: [
                      Icon(
                        Icons.category_outlined,
                        size: 64,
                        color: Colors.grey[300],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'Select category and upload image to get AI analysis',
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.grey[600],
                        ),
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(height: 8),
                      Text(
                        'Current: $_selectedCategory • $_selectedLanguage',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[500],
                        ),
                      ),
                      // ==== CHANGE START: Show translation info ====
                      // if (_selectedLanguage != 'English')
                      //   Padding(
                      //     padding: const EdgeInsets.only(top: 4.0),
                      //     child: Text(
                      //       _selectedLanguage == 'Kurdish'
                      //           ? 'AI will analyze in English and translate to Sorani Kurdish'
                      //           : 'AI will analyze in English for better accuracy',
                      //       style: TextStyle(
                      //         fontSize: 12,
                      //         color: Colors.grey[400],
                      //         fontStyle: FontStyle.italic,
                      //       ),
                      //     ),
                      //   ),
                      // ==== CHANGE END ====
                    ],
                  ),
                ),
              const SizedBox(height: 44),
              const Padding(
                padding: EdgeInsets.all(12.0),
                child: Text(
                  'Developed by Zinar Mizury',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                    fontWeight: FontWeight.w400,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ],
          ),
        ),
      ),
      // ==== CHANGE END ====
    );
  }

  Widget _buildActionButton({
    required IconData icon,
    required String label,
    required VoidCallback onPressed,
  }) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primaryColor,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        elevation: 2,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 20),
          const SizedBox(width: 8),
          Text(
            label,
            style: const TextStyle(
              fontWeight: FontWeight.w500,
              fontSize: 15,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryCard() {
    return // Category Selection Card
        Card(
      color: Colors.white,
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(15.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.category, color: AppColors.primaryColor),
                SizedBox(width: 8),
                Text(
                  'Select Category',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: Colors.grey[800],
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _selectedCategory,
              decoration: InputDecoration(
                contentPadding:
                    EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: AppColors.neutralColor),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: AppColors.neutralColor),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: AppColors.primaryColor),
                ),
              ),
              items: _categories
                  .map((category) => DropdownMenuItem(
                        value: category,
                        child: Text(category),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  _selectedCategory = value ?? 'Medicine';
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLanguageCard() {
    return Card(
      color: Colors.white,
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(15.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.language, color: AppColors.primaryColor),
                SizedBox(width: 8),
                Text(
                  'Select Language',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: Colors.grey[800],
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _selectedLanguage,
              decoration: InputDecoration(
                contentPadding:
                    EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: AppColors.neutralColor),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: AppColors.neutralColor),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: AppColors.primaryColor),
                ),
              ),
              items: _languages
                  .map((language) => DropdownMenuItem(
                        value: language,
                        child: Text(language),
                      ))
                  .toList(),
              onChanged: (value) {
                setState(() {
                  _selectedLanguage = value ?? 'Kurdish';
                });
              },
            ),
            // ==== CHANGE START: Add language info with Sorani Kurdish note ====
            // SizedBox(height: 8),
            // Text(
            //   _selectedLanguage == 'English'
            //       ? 'AI analyzes in English'
            //       : _selectedLanguage == 'Kurdish'
            //           ? 'AI analyzes in English, translates to Sorani Kurdish'
            //           : 'AI analyzes in English, translates to $_selectedLanguage',
            //   style: TextStyle(
            //     fontSize: 10,
            //     color: Colors.grey[600],
            //     fontStyle: FontStyle.italic,
            //   ),
            // ),
            // ==== CHANGE END ====
          ],
        ),
      ),
    );
  }

  Icon _getCategoryIcon(String category) {
    switch (category) {
      case 'Medicine':
        return Icon(Icons.medical_services, color: AppColors.primaryColor);
      case 'Industrial':
        return Icon(Icons.factory, color: AppColors.primaryColor);
      case 'Person':
        return Icon(Icons.person, color: AppColors.primaryColor);
      case 'Environment':
        return Icon(Icons.nature, color: AppColors.primaryColor);
      case 'Safety':
        return Icon(Icons.security, color: AppColors.primaryColor);
      case 'Objects':
        return Icon(Icons.category, color: AppColors.primaryColor);
      case 'Food':
        return Icon(Icons.restaurant, color: AppColors.primaryColor);
      default:
        return Icon(Icons.analytics, color: AppColors.primaryColor);
    }
  }
}
