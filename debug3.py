import sys
sys.stdout = open(r'C:\xampp\htdocs\demo\debug_out.txt', 'w', encoding='utf-8')

with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ดู renderOv function
idx = content.find('function renderOv(')
end = content.find('\nfunction ', idx+1)
print("=== renderOv ===")
print(content[idx:end])

# ดู KPI cards - หาที่ใช้ AD.filter สำหรับ done/prog/urg
import re
for i, m in enumerate(re.finditer(r'AD\.(filter|length)', content)):
    print(f"\n[{i}] pos {m.start()}: {content[max(0,m.start()-60):m.start()+100]}")

sys.stdout.close()
