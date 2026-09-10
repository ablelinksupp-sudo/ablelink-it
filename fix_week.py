with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

week_start = content.find('// Week Navigator')
filter_opts = content.find('function bFO()', week_start)
print(f"week_start={week_start}, filter_opts={filter_opts}")

before = content[:week_start]
after = content[filter_opts:]

week_js = (
    "// Week Navigator\n"
    "let CW = '';\n\n"
    "function getWeekKey(ds) {\n"
    "  if (!ds) return null;\n"
    "  const p = ds.trim().split('/');\n"
    "  if (p.length < 3) return null;\n"
    "  let d = parseInt(p[0]), m = parseInt(p[1]), y = parseInt(p[2]);\n"
    "  if (y < 100) y += 2000;\n"
    "  const dt = new Date(y, m - 1, d);\n"
    "  if (isNaN(dt.getTime())) return null;\n"
    "  const tmp = new Date(Date.UTC(dt.getFullYear(), dt.getMonth(), dt.getDate()));\n"
    "  tmp.setUTCDate(tmp.getUTCDate() + 4 - (tmp.getUTCDay() || 7));\n"
    "  const yr = tmp.getUTCFullYear();\n"
    "  const wn = Math.ceil(((tmp - Date.UTC(yr, 0, 1)) / 86400000 + 1) / 7);\n"
    "  return yr + '-W' + String(wn).padStart(2, '0');\n"
    "}\n\n"
    "function getWeekLabel(wk) {\n"
    "  if (!wk) return '\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14';\n"
    "  const parts = wk.split('-W');\n"
    "  const yr = parseInt(parts[0]), wn = parseInt(parts[1]);\n"
    "  const d1 = new Date(yr, 0, 1 + (wn - 1) * 7);\n"
    "  const day = d1.getDay();\n"
    "  const mon = new Date(d1); mon.setDate(d1.getDate() - day + (day === 0 ? -6 : 1));\n"
    "  const sun = new Date(mon); sun.setDate(mon.getDate() + 6);\n"
    "  return '\u0e2a\u0e31\u0e1b\u0e14\u0e32\u0e2b\u0e4c\u0e17\u0e35\u0e48 ' + wn + ' (' + mon.getDate() + '/' + (mon.getMonth()+1) + '-' + sun.getDate() + '/' + (sun.getMonth()+1) + '/' + sun.getFullYear() + ')';\n"
    "}\n\n"
    "function buildWeekBar() {\n"
    "  const bar = document.getElementById('wkBar');\n"
    "  if (!bar || !AD.length) return;\n"
    "  const dateField = Object.keys(AD[0]).find(function(k){ return k.includes('\u0e27\u0e31\u0e19') || k.toLowerCase().includes('date'); }) || '\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48';\n"
    "  const wkSet = new Set();\n"
    "  AD.forEach(function(d){ const wk = getWeekKey(d[dateField]); if (wk) wkSet.add(wk); });\n"
    "  const weeks = Array.from(wkSet).sort().reverse();\n"
    "  let html = '<button class=\"wk-btn ' + (CW==='' ? 'active' : '') + '\" onclick=\"setWeek(\\'\\')\">\uD83D\uDCCB \u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14 (' + AD.length + ')</button>';\n"
    "  weeks.forEach(function(wk) {\n"
    "    const count = AD.filter(function(d){ return getWeekKey(d[dateField]) === wk; }).length;\n"
    "    html += '<button class=\"wk-btn ' + (CW===wk ? 'active' : '') + '\" onclick=\"setWeek(\\'' + wk + '\\'\">' + getWeekLabel(wk) + ' <span style=\"opacity:.6;font-size:10px\">(' + count + ')</span></button>';\n"
    "  });\n"
    "  bar.innerHTML = html;\n"
    "}\n\n"
    "function setWeek(wk) { CW = wk; buildWeekBar(); af(); }\n\n"
)

# Remove surrogate chars from emoji
week_js = week_js.encode('utf-16', 'surrogatepass').decode('utf-16')
new_content = before + week_js + after

with open(r'C:\xampp\htdocs\demo\it_support.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("SUCCESS! File size:", len(new_content))
