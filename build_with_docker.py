#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
        return False

def create_dockerfile():
    """Create a Dockerfile for building the APK"""
    dockerfile_content = """FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    python3 python3-pip python3-venv \\
    git zip unzip openjdk-11-jdk \\
    autoconf libtool pkg-config \\
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake \\
    libffi-dev libssl-dev \\
    build-essential ccache \\
    libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 \\
    libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 \\
    python3-distutils \\
    && rm -rf /var/lib/apt/lists/*

# Set up Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools

# Install Android SDK
RUN mkdir -p $ANDROID_HOME && \\
    cd $ANDROID_HOME && \\
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \\
    unzip commandlinetools-linux-9477386_latest.zip && \\
    rm commandlinetools-linux-9477386_latest.zip && \\
    yes | cmdline-tools/bin/sdkmanager --sdk_root=$ANDROID_HOME --licenses && \\
    cmdline-tools/bin/sdkmanager --sdk_root=$ANDROID_HOME "platform-tools" "build-tools;30.0.3" "platforms;android-30" "ndk;21.4.7075529"

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install buildozer cython==0.29.33 kivy

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Build the APK
RUN buildozer android debug

# Copy APK to output
RUN mkdir -p /output && cp bin/*.apk /output/

VOLUME ["/output"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Dockerfile created")

def build_with_docker():
    """Build APK using Docker"""
    try:
        print("Building Docker image...")
        result = subprocess.run([
            'docker', 'build', '-t', 'kivy-android-builder', '.'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Docker build failed:")
            print(result.stderr)
            return False
        
        print("✅ Docker image built successfully")
        
        print("Building APK in Docker container...")
        result = subprocess.run([
            'docker', 'run', '--rm', 
            '-v', f"{os.getcwd()}:/output",
            'kivy-android-builder'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ APK build failed:")
            print(result.stderr)
            return False
        
        print("✅ APK built successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error building with Docker: {e}")
        return False

def create_simple_build_instructions():
    """Create simple build instructions for the user"""
    instructions = """
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
"""
    
    with open("BUILD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("✅ Build instructions created: BUILD_INSTRUCTIONS.md")

def main():
    """Main function to try building the APK"""
    print("🚀 Building Android APK for DaysSinceWeMet")
    print("=" * 50)
    
    if check_docker():
        print("Attempting to build with Docker...")
        create_dockerfile()
        if build_with_docker():
            print("🎉 Success! APK should be available in the current directory")
            return
        else:
            print("Docker build failed, creating alternative instructions...")
    else:
        print("Docker not available, creating build instructions...")
    
    create_simple_build_instructions()
    
    print("\n🔧 Alternative Build Methods:")
    print("1. Use WSL (Windows Subsystem for Linux)")
    print("2. Use GitHub Actions (upload code to GitHub)")
    print("3. Use Docker (install Docker Desktop)")
    print("4. Use online build services")
    print("\nSee BUILD_INSTRUCTIONS.md for detailed steps.")

if __name__ == "__main__":
    main()
