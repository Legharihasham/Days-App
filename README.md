# DaysSinceWeMet Android App

A lightweight Android app to track the days, hours, and years since a special date.

## Features
- Track days since a special date
- Real-time updates showing days, hours, and years
- Simple and clean interface
- No internet required, completely private
- Save your date locally

## Building APK

This repository is configured to automatically build APK files using GitHub Actions.

### Automatic Build (Recommended)
1. Push code to GitHub
2. Go to Actions tab
3. Click "Build Android APK" workflow
4. Download APK from artifacts

### Manual Build (Linux/WSL)
```bash
pip install buildozer
buildozer android debug
```

## Installation
1. Download the APK from releases or actions
2. Enable "Install from unknown sources" on your Android device
3. Install the APK

## App Preview
- Enter your special date (YYYY-MM-DD format)
- View real-time countdown
- Change date anytime
- Simple, clean interface

Built with Python + Kivy
