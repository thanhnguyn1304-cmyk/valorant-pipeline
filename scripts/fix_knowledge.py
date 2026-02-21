import os

filepath = r'C:\Users\Yoga\ValorTracker\ValorTracker\backend\services\coaching_knowledge.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any occurrence of `"agent": all,` with `"agent": "all",`
content = content.replace('"agent": all,', '"agent": "all",')
content = content.replace('"map": all,', '"map": "all",')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed unquoted all values in coaching_knowledge.py")
