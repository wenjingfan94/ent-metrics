#!/usr/bin/env python3
"""从 HTML 文件中提取 DEFAULT_DATA 生成 metrics.json"""

import re, json, glob, sys

# 自动找到 HTML 文件
html_files = glob.glob('*.html')
if not html_files:
    print("未找到 HTML 文件")
    sys.exit(1)

# 取最新的 html 文件
html_file = sorted(html_files, key=lambda f: len(f))[-1]
print(f"读取: {html_file}")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 定位 DEFAULT_DATA
start = content.index('const DEFAULT_DATA = [')
bracket_start = content.index('[', start)
depth = 0
for j in range(bracket_start, len(content)):
    if content[j] == '[': depth += 1
    elif content[j] == ']': depth -= 1
    if depth == 0:
        end = j + 1
        break

data_str = content[bracket_start:end]

# 提取每条口径
pattern = r'\{\s*id:\s*"([^"]+)",\s*name:\s*`([^`]*)`\s*,\s*category:\s*"([^"]*)".*?notes:\s*`([^`]*)`\s*,\s*sql:\s*`([^`]*)`'
matches = re.findall(pattern, data_str, re.DOTALL)

items = []
for m in matches:
    items.append({
        'id': m[0],
        'name': m[1].strip(),
        'category': m[2].strip(),
        'notes': m[3].strip(),
        'sql': m[4].strip()
    })

with open('metrics.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"已生成 metrics.json: {len(items)} 条口径")
