#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {command}")
    if isinstance(command, str):
        command = command.split()
    
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command)
    
    return result

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    run_command("pip install python-for-android")
    run_command("pip install cython")

def build_apk():
    """Build APK using python-for-android"""
    print("Building APK...")
    
    # Create a build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Copy main.py to build directory
    shutil.copy("main.py", build_dir)
    
    # Create a simple setup
    p4a_command = [
        "python", "-m", "pythonforandroid.toolchain",
        "apk",
        "--name", "DaysSinceWeMet",
        "--package", "org.example.dayssincewemet",
        "--version", "1.0",
        "--bootstrap", "sdl2",
        "--requirements", "python3,kivy",
        "--private", str(build_dir),
        "--orientation", "portrait",
        "--permission", "WRITE_EXTERNAL_STORAGE",
        "--arch", "armeabi-v7a",
        "--release"
    ]
    
    try:
        run_command(p4a_command)
        print("APK built successfully!")
        
        # Find the APK file
        apk_path = None
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = os.path.join(root, file)
                    break
            if apk_path:
                break
        
        if apk_path:
            print(f"APK location: {apk_path}")
            # Copy to current directory
            shutil.copy(apk_path, "DaysSinceWeMet.apk")
            print("APK copied to current directory as DaysSinceWeMet.apk")
        else:
            print("APK file not found!")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False
    
    return True

def main():
    """Main build function"""
    print("Building Android APK on Windows...")
    
    try:
        install_requirements()
        success = build_apk()
        
        if success:
            print("\nBuild completed successfully!")
            print("You can find the APK file as 'DaysSinceWeMet.apk' in the current directory.")
        else:
            print("\nBuild failed!")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
