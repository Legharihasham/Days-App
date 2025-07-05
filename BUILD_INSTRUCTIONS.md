
# Building DaysSinceWeMet Android APK

## Method 1: Using WSL (Windows Subsystem for Linux) - Recommended

1. Install WSL2 from Microsoft Store
2. Open WSL terminal and run:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip git
   pip3 install buildozer
   git clone <your-repo> # or copy your files
   cd AndroidApp
   buildozer android debug
   ```

## Method 2: Using GitHub Actions (Online Build)

1. Push this code to GitHub
2. Go to Actions tab
3. Click "Run workflow" on the "Build Android APK" workflow
4. Download the built APK from the artifacts

## Method 3: Using Online Build Services

1. Visit: https://buildozer.readthedocs.io/en/latest/
2. Or use: https://kivy.org/doc/stable/guide/packaging-android.html

## Method 4: Using Docker (if available)

1. Install Docker Desktop for Windows
2. Run: `python build_with_docker.py`

## Current Status
The app is ready to build but requires a Linux environment.
The Python app runs successfully on Windows for testing.
