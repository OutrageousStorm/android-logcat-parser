# 📋 Android Logcat Parser

Parse, filter, and analyze Android logcat output. Extract errors, crashes, and warnings.

## Usage
```bash
# Live logcat with filtering
python3 logcat.py --tag MyApp --level ERROR

# Dump full logcat
adb logcat > logcat.txt
python3 analyze.py logcat.txt --output report.csv

# Find crash stacktraces
python3 find_crashes.py logcat.txt
```
