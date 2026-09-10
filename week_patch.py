# -*- coding: utf-8 -*-
with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print(f"Loaded: {len(content)} chars")

# 1. CSS
old_css = '.fg{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:8px}'
new_css = (
    '.wk-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}'
    '.wk-btn{background:var(--card2);border:1px solid var(--bdr);border-radius:20px;padding:5px 14px;font-size:11px;font-weight:600;color:var(--t2);cursor:pointer;font-family:inherit;transition:all .2s;white-space:nowrap}'
    '.wk-btn:hover{border-color:var(--violet);color:var(--violet)}'
    '.wk-btn.active{background:var(--violet);border-color:var(--violet);color:#fff}\n    '
    + old_css
)
if old_css in content:
    content = content.replace(old_css, new_css, 1)
    print("1. CSS OK")
else:
    print("1. CSS - target not found, searching similar...")
    import re
    m = re.search(r'\.fg\{[^}]+\}', content)
    if m: print("  Found:", m.group()[:80])

# 2. HTML week bar
idx = content.find('<div class="fs">')
if idx >= 0:
    fg_idx = content.find('<div class="fg">', idx)
    if fg_idx >= 0:
        content = content[:fg_idx] + '<div class="wk-bar" id="wkBar"></div>\n      <div class="fg">' + content[fg_idx + len('<div class="fg">'):]
        print("2. HTML week bar OK")
    else:
        print("2. fg not found")
else:
    print("2. fs not found")

# 3. Week JS
week_js = r"""// Week Navigator
let CW = '';
function getWeekKey(ds) {
  if (!ds) return null;
  var p = ds.trim().split('/');
  if (p.length < 3) return null;
  var d=parseInt(p[0]),m=parseInt(p[1]),y=parseInt(p[2]);
  if (y<100) y+=2000;
  var dt=new Date(y,m-1,d);
  if (isNaN(dt.getTime())) return null;
  var tmp=new Date(Date.UTC(dt.getFullYear(),dt.getMonth(),dt.getDate()));
  tmp.setUTCDate(tmp.getUTCDate()+4-(tmp.getUTCDay()||7));
  var yr=tmp.getUTCFullYear();
  var wn=Math.ceil(((tmp-Date.UTC(yr,0,1))/86400000+1)/7);
  return yr+'-W'+String(wn).padStart(2,'0');
}
function getWeekLabel(wk) {
  if (!wk) return 'ALL';
  var p=wk.split('-W'),yr=parseInt(p[0]),wn=parseInt(p[1]);
  var d1=new Date(yr,0,1+(wn-1)*7),day=d1.getDay();
  var mon=new Date(d1); mon.setDate(d1.getDate()-day+(day===0?-6:1));
  var sun=new Date(mon); sun.setDate(mon.getDate()+6);
  return 'Week '+wn+' ('+mon.getDate()+'/'+(mon.getMonth()+1)+'-'+sun.getDate()+'/'+(sun.getMonth()+1)+'/'+sun.getFullYear()+')';
}
function buildWeekBar() {
  var bar=document.getElementById('wkBar');
  if (!bar||!AD.length) return;
  var keys=Object.keys(AD[0]),dateField='';
  for(var ki=0;ki<keys.length;ki++){if(keys[ki].indexOf('\u0e27\u0e31\u0e19')>=0||keys[ki].toLowerCase().indexOf('date')>=0){dateField=keys[ki];break;}}
  if(!dateField) dateField=keys[2]||keys[0];
  var wkMap={},wkOrder=[];
  AD.forEach(function(d){var wk=getWeekKey(d[dateField]);if(wk&&!wkMap[wk]){wkMap[wk]=0;wkOrder.push(wk);}if(wk)wkMap[wk]++;});
  wkOrder.sort().reverse();
  var html='<button class="wk-btn '+(CW===''?'active':'')+'" onclick="setWeek(\x27\x27)">\u{1F4CB} \u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14 ('+AD.length+')</button>';
  wkOrder.forEach(function(wk){html+='<button class="wk-btn '+(CW===wk?'active':'')+'" onclick="setWeek(\x27'+wk+'\x27)">'+getWeekLabel(wk)+' <span style="opacity:.65;font-size:10px">('+wkMap[wk]+')</span></button>';});
  bar.innerHTML=html;
}
function setWeek(wk){CW=wk;buildWeekBar();af();}
"""

bfo_idx = content.find('function bFO()')
if bfo_idx >= 0:
    comment_idx = content.rfind('//', 0, bfo_idx)
    insert_idx = comment_idx if (bfo_idx - comment_idx < 80) else bfo_idx
    content = content[:insert_idx] + week_js + '\n' + content[insert_idx:]
    print("3. Week JS OK")
else:
    print("3. bFO() not found!")

# 4. CW filter in af()
for ending in ["    return true;\n  }); CP = 1; rt();", "    return true;\r\n  }); CP = 1; rt();"]:
    if ending in content:
        new_ending = "    if(CW){var dfk=Object.keys(d).find(function(k){return k.indexOf('\u0e27\u0e31\u0e19')>=0||k.toLowerCase().indexOf('date')>=0;})||Object.keys(d)[2];if(getWeekKey(d[dfk])!==CW)return false;}\n    return true;\n  }); CP = 1; rt();"
        content = content.replace(ending, new_ending, 1)
        print("4. af() week filter OK")
        break
else:
    print("4. af() return true not found!")

# 5. buildWeekBar call
old_c = "bFO(); FD = [...AD]; rt();"
new_c = "bFO(); buildWeekBar(); FD = [...AD]; rt();"
if old_c in content:
    content = content.replace(old_c, new_c, 1)
    print("5. buildWeekBar() call OK")
else:
    print("5. bFO call not found, trying alternatives...")
    import re
    m = re.search(r'bFO\(\)[^;]*;', content)
    if m: print("  Found:", m.group())

with open(r'C:\xampp\htdocs\demo\it_support.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"\nSaved! {len(content)} chars")