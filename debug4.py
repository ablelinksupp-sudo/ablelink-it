with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# เพิ่ม ovDateRange badge ก่อน <div id="co">
old_co_div = '<!-- Overview Tab -->\n  <div id="co">'
new_co_div = (
    '<!-- Overview Tab -->\n'
    '  <div id="ovDateRangeBanner" style="display:none;background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.3);'
    'border-radius:8px;padding:7px 14px;margin-bottom:10px;font-size:11px;color:#a78bfa;display:flex;align-items:center;gap:8px">'
    '<span>\U0001f4c5</span>'
    '<span id="ovDateRange"></span>'
    '<button onclick="calClear()" style="margin-left:auto;background:none;border:1px solid rgba(139,92,246,.3);color:#a78bfa;border-radius:5px;padding:2px 8px;font-size:10px;cursor:pointer;font-family:inherit">'
    '\u25b6 \u0e25\u0e49\u0e32\u0e07\u0e01\u0e32\u0e23\u0e40\u0e25\u0e37\u0e2d\u0e01</button></div>\n'
    '  <div id="co">'
)
if old_co_div in content:
    content = content.replace(old_co_div, new_co_div, 1)
    print("Added ovDateRange banner OK")
else:
    print("old_co_div not found, trying without newline...")
    old2 = '<!-- Overview Tab -->'
    idx = content.find(old2)
    print(f"  Overview Tab comment at: {idx}")
    print(f"  Context: {repr(content[idx:idx+60])}")

# แก้ renderOv ให้ control banner display ด้วย
old_label = (
    "  var drLabel = document.getElementById('ovDateRange');\n"
    "  if (drLabel) {\n"
    "    if (RANGE_START && RANGE_END) {\n"
)
new_label = (
    "  var drBanner = document.getElementById('ovDateRangeBanner');\n"
    "  var drLabel = document.getElementById('ovDateRange');\n"
    "  if (drLabel) {\n"
    "    if (RANGE_START && RANGE_END) {\n"
)
if old_label in content:
    content = content.replace(old_label, new_label, 1)

old_show = "      drLabel.style.display = 'inline-block';\n"
new_show = "      drLabel.style.display = 'inline-block';\n      if(drBanner) drBanner.style.display = 'flex';\n"
if old_show in content:
    content = content.replace(old_show, new_show, 1)

old_hide = "      drLabel.style.display = 'none';\n"
new_hide = "      drLabel.style.display = 'none';\n      if(drBanner) drBanner.style.display = 'none';\n"
if old_hide in content:
    content = content.replace(old_hide, new_hide, 1)

with open(r'C:\xampp\htdocs\demo\it_support.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Done! Final: {len(content)} chars")
