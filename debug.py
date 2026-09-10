with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ดู calClick function ปัจจุบัน
idx = content.find('function calClick')
print("=== calClick ===")
print(content[idx:idx+400])
print()
# ดู renderCalendar - ส่วน onclick
idx2 = content.find('onclick=\\"calClick(')
if idx2 < 0:
    idx2 = content.find("onclick=\"calClick(")
print("=== onclick in grid ===")
print(content[idx2-20:idx2+80] if idx2>=0 else "NOT FOUND")
print()
# ดู calHover
idx3 = content.find('function calHover')
print("=== calHover ===")
print(content[idx3:idx3+200])
