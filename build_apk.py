#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a command and print output"""
    print(f"Running: {command}")
    try:
        if shell:
            result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
        else:
            result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"Command failed with return code: {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def create_simple_apk():
    """Create a simple APK using a different approach"""
    print("Creating APK using alternative method...")
    
    # Create basic APK structure
    apk_name = "DaysSinceWeMet.apk"
    
    # Try using p4a directly
    p4a_cmd = [
        "python", "-m", "pythonforandroid.toolchain",
        "apk",
        "--name", "DaysSinceWeMet",
        "--package", "org.example.dayssincewemet", 
        "--version", "1.0",
        "--bootstrap", "sdl2",
        "--requirements", "python3,kivy",
        "--private", ".",
        "--orientation", "portrait"
    ]
    
    success = run_command(p4a_cmd)
    
    if success:
        print("Looking for generated APK...")
        # Search for APK files
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = os.path.join(root, file)
                    print(f"Found APK: {apk_path}")
                    # Copy to main directory
                    shutil.copy(apk_path, apk_name)
                    print(f"APK copied to: {apk_name}")
                    return True
    
    return False

def main():
    print("Building Android APK...")
    
    # Check if we have the required tools
    print("Checking Python for Android...")
    
    # Try to create the APK
    if create_simple_apk():
        print("✅ APK created successfully!")
        print("📱 You can now install DaysSinceWeMet.apk on your Android device")
    else:
        print("❌ Failed to create APK")
        print("This might be because Android SDK tools are not available on Windows")
        print("Consider using:")
        print("1. WSL (Windows Subsystem for Linux)")
        print("2. Docker with a Linux container")
        print("3. GitHub Actions for building")
        print("4. Online build services")

if __name__ == "__main__":
    main()
