import re
import json
from collections import Counter

patterns = {
    "ts": re.compile(r"\[(.*?)\]"),
    "level": re.compile(r"\b(INFO|WARN|ERROR)\b"),
    "user": re.compile(r"User[:=]\s*([A-Za-z0-9_]+)"),
    "action": re.compile(r"Action[:=]\s*([A-Z_]+)"),
    "file": re.compile(r'File="?([\w\.-]+)"?'),
    "ip": re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b"),
}

clean_logs = []
login_ok_count = 0
pwd_fail_count = 0
downloads = Counter()
error_counts = Counter()
ip_counts = Counter()

with open("server_logs.txt") as f:
    for line in f:
        entry = {
            "timestamp": patterns["ts"].search(line).group(1),
            "level": patterns["level"].search(line).group(1),
            "user": patterns["user"].search(line).group(1),
            "action": patterns["action"].search(line).group(1),
            "file": None,
            "ip": patterns["ip"].search(line).group(1),
        }

        m = patterns["file"].search(line)
        if m:
            entry["file"] = m.group(1)
            downloads[entry["user"]] += 1

        clean_logs.append(entry)

        if entry["action"] == "LOGIN_OK":
            login_ok_count += 1
        if entry["action"] == "PASSWORD_FAIL":
            pwd_fail_count += 1
        if entry["level"] == "ERROR":
            error_counts[entry["user"]] += 1

        ip_counts[entry["ip"]] += 1

# JSONL output
with open("clean_logs.jsonl", "w") as out:
    for row in clean_logs:
        out.write(json.dumps(row) + "\n")

# Summary output
with open("summary.txt", "w") as out:
    out.write(f"Total LOGIN_OK: {login_ok_count}\n")
    out.write(f"Total PASSWORD_FAIL: {pwd_fail_count}\n")
    out.write(f"Most downloads: {downloads.most_common(1)}\n")
    out.write(f"Most frequent IP: {ip_counts.most_common(1)}\n")
    out.write(f"User with most ERROR logs: {error_counts.most_common(1)}\n")
