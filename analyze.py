#!/usr/bin/env python3
"""
analyze.py -- Analyze Android logcat file
Extract stats, find errors, crashes, warnings. Export to CSV.
Usage: python3 analyze.py logcat.txt [--output report.csv] [--errors-only]
"""
import sys, re, csv, argparse
from collections import defaultdict

def parse_logcat_file(path):
    logs = []
    with open(path, 'r') as f:
        for line in f:
            m = re.match(r'(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s+(\d+)\s+(\d+)\s+(\w)\s+(\S+):\s+(.*)', line.strip())
            if m:
                logs.append({
                    'time': m.group(1),
                    'pid': m.group(2),
                    'tid': m.group(3),
                    'level': m.group(4),
                    'tag': m.group(5),
                    'msg': m.group(6),
                })
    return logs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('logcat_file')
    parser.add_argument('--output', help='CSV output file')
    parser.add_argument('--errors-only', action='store_true')
    parser.add_argument('--top-tags', type=int, default=10)
    args = parser.parse_args()

    print(f"Parsing {args.logcat_file}...")
    logs = parse_logcat_file(args.logcat_file)
    print(f"Total lines: {len(logs)}\n")

    # Stats
    by_level = defaultdict(int)
    by_tag = defaultdict(int)
    errors = []

    for log in logs:
        by_level[log['level']] += 1
        by_tag[log['tag']] += 1
        if log['level'] in ['E', 'W', 'F']:
            errors.append(log)

    print("Levels:")
    for level in 'VDIWEF':
        count = by_level[level]
        if count > 0:
            print(f"  {level}: {count}")

    print(f"\nTop {args.top_tags} tags:")
    top = sorted(by_tag.items(), key=lambda x: x[1], reverse=True)[:args.top_tags]
    for tag, count in top:
        print(f"  {tag:<30} {count:>6}")

    if errors:
        print(f"\nErrors & Warnings: {len(errors)}")
        for log in errors[:20]:
            print(f"  [{log['level']}] {log['tag']}: {log['msg'][:70]}")
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more")

    if args.output:
        with open(args.output, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['time', 'level', 'tag', 'pid', 'msg'])
            for log in (errors if args.errors_only else logs):
                w.writerow([log['time'], log['level'], log['tag'], log['pid'], log['msg'][:200]])
        print(f"\n✅ Exported to {args.output}")

if __name__ == "__main__":
    main()
