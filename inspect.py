with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

wk_css_idx = content.find('.wk-bar')
wk_css_end = content.find('.fg{display:grid', wk_css_idx)
print(f"wk CSS: {wk_css_idx} to {wk_css_end}")

wk_html_idx = content.find('id="wkBar"')
wk_html_end = content.find('<div class="fg">', wk_html_idx)
print(f"wk HTML: {wk_html_idx} to {wk_html_end}")

wk_js_idx = content.find('// Week Navigator')
wk_js_end = content.find('function bFO()', wk_js_idx)
print(f"wk JS: {wk_js_idx} to {wk_js_end}")

cw_filter = content.find('if(CW){')
print(f"CW filter: {cw_filter}")
# context around CW filter
print(content[cw_filter:cw_filter+300])
