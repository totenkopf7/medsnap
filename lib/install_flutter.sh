#!/bin/bash

# Install Flutter SDK
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:$PWD/flutter/bin"

# Enable web support
flutter config --enable-web

# Pre-download dependencies
flutter precache
flutter pub get
