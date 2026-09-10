with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# หา toggleCal และแสดงโค้ดปัจจุบัน
idx = content.find('function toggleCal(')
print(content[idx:idx+600])
