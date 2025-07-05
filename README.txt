Days Since App for Android
========================

A lightweight Android app to track the days, hours, and years since a special date.

How to Use
----------
1. Open the app. On first launch, enter your special date (YYYY-MM-DD).
2. The app will show days, hours, and years since that date.
3. Tap 'Change Date' to update the date at any time.
4. The app saves your date locally and updates the count every time you open it.

How to Build (.apk)
-------------------
1. Install Python 3, Kivy, and Buildozer (see requirements.txt).
2. On Linux, run:
   pip install -r requirements.txt
   buildozer init
   buildozer -v android debug
3. The APK will be in the bin/ folder. Transfer to your Android device and install.

Security
--------
- No internet access, no background running, no trackers, no malware.
- Only local storage is used for saving your date. 