# Medical Snap

A Flutter application that uses AI to analyze medicines and provide information about their benefits, usage, and side effects.

## Features

- Take photos of medicines or select from gallery
- AI-powered analysis of medicines
- Works on both mobile and web platforms
- Detailed information about benefits, usage, and side effects

## Setup

### Prerequisites

- Flutter SDK
- Python 3.x
- Anthropic API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/med_snap.git
cd med_snap
```

2. Install Flutter dependencies:
```bash
flutter pub get
```

3. Install Python dependencies:
```bash
pip install flask flask-cors python-dotenv requests
```

4. Create a `.env` file in the root directory and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### Running the Application

1. Start the Flask server:
```bash
python backend/server.py
```

2. Run the Flutter app:
- For web:
```bash
flutter run -d chrome --web-port 8000
```
- For mobile:
```bash
flutter run
```

## Project Structure

- `lib/` - Flutter application code
  - `main.dart` - Entry point
  - `home_page.dart` - Main UI
  - `claude_service.dart` - API integration
- `backend/` - Python Flask server
  - `server.py` - Backend server code

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
