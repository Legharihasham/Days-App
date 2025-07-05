# PowerShell script to automatically set up WSL and build APK
# Run this in PowerShell as Administrator

Write-Host "🚀 DaysSinceWeMet APK Builder - WSL Automatic Setup" -ForegroundColor Green
Write-Host "=" * 60

# Check if WSL is installed
$wslVersion = wsl --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ WSL is already installed" -ForegroundColor Green
} else {
    Write-Host "❌ WSL not found. Installing WSL..." -ForegroundColor Yellow
    Write-Host "This requires administrator privileges and a restart."
    
    # Enable WSL feature
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -All
    
    # Install Ubuntu from Microsoft Store (requires user interaction)
    Write-Host "Please install Ubuntu from Microsoft Store after restart." -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit
}

# Check if Ubuntu is installed
$ubuntuStatus = wsl -l -v 2>&1
if ($ubuntuStatus -match "Ubuntu") {
    Write-Host "✅ Ubuntu is installed" -ForegroundColor Green
} else {
    Write-Host "❌ Ubuntu not found. Please install Ubuntu from Microsoft Store." -ForegroundColor Red
    Start-Process "ms-windows-store://pdp/?productid=9nblggh4msv6"
    exit
}

# Get current directory
$currentDir = Get-Location
$wslPath = $currentDir.Path -replace '\\', '/' -replace 'C:', '/mnt/c'

Write-Host "📁 Current directory: $currentDir" -ForegroundColor Blue
Write-Host "📁 WSL path: $wslPath" -ForegroundColor Blue

# Create build script for WSL
$buildScript = @"
#!/bin/bash
echo "🔧 Setting up Android build environment..."

# Update system
sudo apt update -y

# Install required packages
sudo apt install -y python3-pip git openjdk-11-jdk unzip wget

# Install Python dependencies
pip3 install --upgrade pip
pip3 install buildozer cython==0.29.33 kivy

# Change to app directory
cd "$wslPath"

echo "📱 Building Android APK..."
echo "This will take 10-15 minutes for the first build..."

# Build APK
buildozer android debug

if [ -f "bin/*.apk" ]; then
    echo "🎉 SUCCESS! APK built successfully!"
    echo "📱 APK location: bin/"
    ls -la bin/*.apk
    
    # Copy APK to Windows desktop for easy access
    cp bin/*.apk /mnt/c/Users/\$USER/Desktop/DaysSinceWeMet.apk 2>/dev/null || echo "Could not copy to desktop"
    
    echo "✅ APK ready for installation on Android device!"
else
    echo "❌ Build failed. Check the error messages above."
fi
"@

$buildScript | Out-File -FilePath "build_apk.sh" -Encoding UTF8

Write-Host "📝 Created build script: build_apk.sh" -ForegroundColor Green

# Execute the build in WSL
Write-Host "🚀 Starting APK build in WSL..." -ForegroundColor Green
Write-Host "This will take 10-15 minutes for the first build..." -ForegroundColor Yellow

wsl bash build_apk.sh

Write-Host "🎯 Build process completed!" -ForegroundColor Green
Write-Host "Check the bin/ folder for your APK file." -ForegroundColor Blue
