#!/usr/bin/env python3
"""
logcat.py -- Live Android logcat filter with colors
Usage: python3 logcat.py [--tag TAG] [--level LEVEL] [--app package]
       python3 logcat.py --tag MyApp --level ERROR
"""
import subprocess, sys, re, argparse
from datetime import datetime

COLORS = {
    'V': '\033[36m',  # cyan
    'D': '\033[34m',  # blue
    'I': '\033[32m',  # green
    'W': '\033[33m',  # yellow
    'E': '\033[31m',  # red
    'F': '\033[35m',  # magenta
    'RST': '\033[0m',
}

LEVEL_MAP = {'V': 0, 'D': 1, 'I': 2, 'W': 3, 'E': 4, 'F': 5}

def parse_line(line):
    m = re.match(r'(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s+(\d+)\s+(\d+)\s+(\w)\s+(\S+):\s+(.*)', line)
    if m:
        return {
            'time': m.group(1),
            'pid': m.group(2),
            'tid': m.group(3),
            'level': m.group(4),
            'tag': m.group(5),
            'msg': m.group(6),
        }
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', help='Filter by tag')
    parser.add_argument('--level', default='V', choices=['V','D','I','W','E','F'])
    parser.add_argument('--app', help='Filter by package (needs pidof)')
    parser.add_argument('--pid', help='Filter by PID')
    parser.add_argument('--no-color', action='store_true')
    args = parser.parse_args()

    min_level = LEVEL_MAP[args.level]

    proc = subprocess.Popen('adb logcat', shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    print(f"\n📋 Android Logcat — {args.level} and above")
    if args.tag: print(f"  Tag filter: {args.tag}")
    if args.pid: print(f"  PID filter: {args.pid}")
    print("(Ctrl+C to stop)\n")

    try:
        for line in proc.stdout:
            data = parse_line(line)
            if not data: continue

            # Filter by level
            if LEVEL_MAP.get(data['level'], 0) < min_level:
                continue

            # Filter by tag
            if args.tag and args.tag.lower() not in data['tag'].lower():
                continue

            # Filter by PID
            if args.pid and args.pid != data['pid']:
                continue

            # Color
            color = '' if args.no_color else COLORS.get(data['level'], '')
            reset = '' if args.no_color else COLORS['RST']

            print(f"{color}{data['time']} {data['pid']:>5} {data['tid']:>5} {data['level']} {data['tag']:<20} {data['msg']}{reset}")

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        proc.terminate()

if __name__ == "__main__":
    main()
