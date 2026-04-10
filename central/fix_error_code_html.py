#!/usr/bin/env python3
"""补做错误码站的 HTML 页面（之前批量只生成了 md）"""
import subprocess

MISSING_FILE = "/tmp/error_code_missing.txt"
GEN = "/root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py"

with open(MISSING_FILE) as f:
    lines = [l.strip() for l in f if l.strip()]

print(f"补做 {len(lines)} 个 HTML 页面...")
done = 0
errors = 0

for i, line in enumerate(lines):
    parts = line.split("|")
    if len(parts) != 4:
        continue
    brand, cat, code, url = parts
    model = brand + " " + cat

    cmd = (
        f"python3 {GEN} "
        f"--brand {brand} --category {cat} --code {code} "
        f"--model \"{model}\" "
        f"--url \"{url}\" "
        f"--format html 2>&1"
    )
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    if r.returncode == 0 and "Generated:" in r.stdout:
        done += 1
    else:
        errors += 1

    if (i + 1) % 100 == 0:
        print(f"  进度: {i+1}/{len(lines)} | 完成: {done} | 错误: {errors}")

print(f"\n完成: {done}/{len(lines)} HTML 页面, {errors} 错误")
