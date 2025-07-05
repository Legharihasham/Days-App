#!/bin/bash

# Install buildozer and dependencies
pip install buildozer cython==0.29.33 kivy

# Accept Android licenses
yes | android update sdk --no-ui --all --filter tool,extra-android-m2repository,extra-android-support,extra-google-google_play_services,extra-google-m2repository

# Build APK
buildozer android debug

echo "APK built! Check the bin/ directory"
