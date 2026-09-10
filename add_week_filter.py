with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# ========== 1. CSS ==========
old_css = ".fg{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:8px}"
new_css = (
    ".wk-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}"
    ".wk-btn{background:var(--card2);border:1px solid var(--bdr);border-radius:20px;padding:5px 14px;font-size:11px;font-weight:600;color:var(--t2);cursor:pointer;font-family:inherit;transition:all .2s;white-space:nowrap}"
    ".wk-btn:hover{border-color:var(--violet);color:var(--violet)}"
    ".wk-btn.active{background:var(--violet);border-color:var(--violet);color:#fff}\n    "
    + old_css
)
if old_css in content:
    content = content.replace(old_css, new_css, 1)
    print("CSS added OK")
else:
    print("CSS target not found!")

# ========== 2. HTML - insert week bar before filter grid ==========
old_html = '<div class="fg">'
new_html = '<div class="wk-bar" id="wkBar"></div>\n      <div class="fg">'
# only replace the FIRST occurrence inside the filter section
idx = content.find('<div class="fs">')
if idx >= 0:
    fg_idx = content.find(old_html, idx)
    if fg_idx >= 0:
        content = content[:fg_idx] + new_html + content[fg_idx + len(old_html):]
        print("Week bar HTML added OK")
    else:
        print("fg div not found in fs section!")
else:
    print("fs section not found!")

# ========== 3. JS - Week Navigator functions (insert before bFO) ==========
week_js = '''// Week Navigator
let CW = '';

function getWeekKey(ds) {
  if (!ds) return null;
  var p = ds.trim().split('/');
  if (p.length < 3) return null;
  var d = parseInt(p[0]), m = parseInt(p[1]), y = parseInt(p[2]);
  if (y < 100) y += 2000;
  var dt = new Date(y, m - 1, d);
  if (isNaN(dt.getTime())) return null;
  var tmp = new Date(Date.UTC(dt.getFullYear(), dt.getMonth(), dt.getDate()));
  tmp.setUTCDate(tmp.getUTCDate() + 4 - (tmp.getUTCDay() || 7));
  var yr = tmp.getUTCFullYear();
  var wn = Math.ceil(((tmp - Date.UTC(yr, 0, 1)) / 86400000 + 1) / 7);
  return yr + '-W' + String(wn).padStart(2, '0');
}

function getWeekLabel(wk) {
  if (!wk) return '\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14';
  var parts = wk.split('-W');
  var yr = parseInt(parts[0]), wn = parseInt(parts[1]);
  var d1 = new Date(yr, 0, 1 + (wn - 1) * 7);
  var day = d1.getDay();
  var mon = new Date(d1); mon.setDate(d1.getDate() - day + (day === 0 ? -6 : 1));
  var sun = new Date(mon); sun.setDate(mon.getDate() + 6);
  return '\u0e2a\u0e31\u0e1b\u0e14\u0e32\u0e2b\u0e4c\u0e17\u0e35\u0e48 ' + wn + ' (' + mon.getDate() + '/' + (mon.getMonth()+1) + '-' + sun.getDate() + '/' + (sun.getMonth()+1) + '/' + sun.getFullYear() + ')';
}

function buildWeekBar() {
  var bar = document.getElementById('wkBar');
  if (!bar || !AD.length) return;
  var keys = Object.keys(AD[0]);
  var dateField = '\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48';
  for (var ki = 0; ki < keys.length; ki++) {
    if (keys[ki].indexOf('\u0e27\u0e31\u0e19') >= 0 || keys[ki].toLowerCase().indexOf('date') >= 0) {
      dateField = keys[ki]; break;
    }
  }
  var wkSet = {};
  var wkOrder = [];
  AD.forEach(function(d) {
    var wk = getWeekKey(d[dateField]);
    if (wk && !wkSet[wk]) { wkSet[wk] = 0; wkOrder.push(wk); }
    if (wk) wkSet[wk]++;
  });
  wkOrder.sort().reverse();
  var html = '<button class="wk-btn ' + (CW === '' ? 'active' : '') + '" onclick="setWeek(\x27\x27)">\u{1F4CB} \u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14 (' + AD.length + ')</button>';
  wkOrder.forEach(function(wk) {
    html += '<button class="wk-btn ' + (CW === wk ? 'active' : '') + '" onclick="setWeek(\x27' + wk + '\x27)">' + getWeekLabel(wk) + ' <span style="opacity:.65;font-size:10px">(' + wkSet[wk] + ')</span></button>';
  });
  bar.innerHTML = html;
}

function setWeek(wk) { CW = wk; buildWeekBar(); af(); }

'''

bfo_idx = content.find('function bFO()')
if bfo_idx >= 0:
    # Find comment before bFO
    comment_idx = content.rfind('//', 0, bfo_idx)
    insert_idx = comment_idx if (bfo_idx - comment_idx < 60) else bfo_idx
    content = content[:insert_idx] + week_js + content[insert_idx:]
    print("Week JS functions added OK")
else:
    print("bFO() not found!")

# ========== 4. JS - Add CW filter to af() function ==========
old_filter = "    return true;\n  }); CP = 1; rt();"
new_filter = (
    "    if (CW) {\n"
    "      var dfKey = '\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48';\n"
    "      var ks = Object.keys(d);\n"
    "      for (var ki=0; ki<ks.length; ki++) { if (ks[ki].indexOf('\u0e27\u0e31\u0e19')>=0||ks[ki].toLowerCase().indexOf('date')>=0){dfKey=ks[ki];break;} }\n"
    "      if (getWeekKey(d[dfKey]) !== CW) return false;\n"
    "    }\n"
    "    return true;\n"
    "  }); CP = 1; rt();"
)
if old_filter in content:
    content = content.replace(old_filter, new_filter, 1)
    print("Week filter in af() added OK")
else:
    # try \r\n version
    old_filter2 = "    return true;\r\n  }); CP = 1; rt();"
    if old_filter2 in content:
        content = content.replace(old_filter2, new_filter, 1)
        print("Week filter in af() added OK (CRLF version)")
    else:
        print("af() return true not found!")

# ========== 5. JS - Call buildWeekBar() after bFO() in data load ==========
old_call = "bFO(); FD = [...AD]; rt();"
new_call = "bFO(); buildWeekBar(); FD = [...AD]; rt();"
if old_call in content:
    content = content.replace(old_call, new_call, 1)
    print("buildWeekBar() call added OK")
else:
    print("bFO(); FD call not found!")

with open(r'C:\xampp\htdocs\demo\it_support.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"\nDone! File size: {len(content)} chars")
