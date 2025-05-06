#!/bin/bash

set -e  # Fail on first error

echo "Cloning Flutter..."
git clone https://github.com/flutter/flutter.git -b stable

echo "Adding Flutter to PATH..."
export PATH="$PWD/flutter/bin:$PATH"

echo "Running flutter doctor..."
flutter doctor

echo "Enabling web support..."
flutter config --enable-web

echo "Pre-caching dependencies..."
flutter precache

echo "Running pub get..."
flutter pub get

echo "Building web app..."
flutter build web
